import re
import uuid
from typing import List

import colorlog
from google.cloud import storage
from google.cloud.exceptions import ClientError, NotFound
from google.cloud.storage import Blob

import config
from storage.storage_error import StorageError
from storage.storage_service import StorageService
from utils.coordinates import Coordinates
from video_catalog.dto import VideoDto, FileStatus
from video_catalog.services.video_service import VideoService

REVISION_PATH = '/rev/'
DEFAULT_PUBLIC_FILE = False
DEFAULT_RATING_VALUE = config.REPORT_VALUE


class StorageServiceGCloudImpl(StorageService):

    def __init__(self, bucket_name, allowed_content_type, storage_analyzer, video_service,
                 allowed_images_content_type, base_path):
        self.gcloud_storage = storage.Client()
        self.bucket_name = bucket_name
        self.allowed_content_type = allowed_content_type
        self.logger = colorlog.getLogger('GCloudStorage')
        self.storage_analyzer = storage_analyzer
        self.video_catalog_service: VideoService = video_service
        self.allowed_images_content_type = allowed_images_content_type
        self.base_path = base_path
        try:
            self.bucket = self.gcloud_storage.create_bucket(bucket_name)
        except ClientError:
            self.bucket = self.gcloud_storage.get_bucket(bucket_name)
        self.initial_config()

    def initial_config(self):
        # TODO UPDATE DATABASE WITH GOOGLE CLOUD STORAGE
        pass

    def allowed_file(self, content_type):
        return content_type in self.allowed_content_type

    def gcloud_path_to_path(self, g_path):
        return re.sub(r'gs://' + self.bucket_name + '/', '', g_path)

    def path_to_gcloud_path(self, path):
        return 'gs://' + self.bucket_name + '/' + path

    def upload_file(self, place, file, user_id):
        if self.allowed_file(file.content_type):
            self.logger.debug("Allowed file")
            filename = file.filename.replace(" ", "_")
            blob_name_rev = self.base_path + place + REVISION_PATH + filename
            blob_name = self.base_path + place + '/' + filename
            video_dto = self.video_catalog_service.get_video_by_gpath(self.path_to_gcloud_path(blob_name))
            if video_dto is not VideoDto.NULL:
                return video_dto
            file_dto_rev = self.video_catalog_service.get_video_by_gpath(self.path_to_gcloud_path(blob_name_rev))
            if file_dto_rev is not VideoDto.NULL:
                return file_dto_rev

            blob = self.bucket.blob(blob_name_rev)
            try:  # TODO fix
                blob.upload_from_file(file, content_type=file.content_type)
                self.logger.info("File uploaded: " + blob.name)
                video_dto = VideoDto(
                    str(uuid.uuid4()),
                    'gs://' + self.bucket_name + '/' + blob.name,
                    '',
                    '',
                    DEFAULT_PUBLIC_FILE,
                    FileStatus.UPLOADED.value,
                    user_id,
                    place,
                    '',
                    '',
                    '',
                    '',
                    Coordinates('', ''),
                    DEFAULT_RATING_VALUE,
                    DEFAULT_RATING_VALUE,
                    DEFAULT_RATING_VALUE
                )
                video_dto = self.video_catalog_service.add(video_dto)
                self.logger.debug("User_id: {} place_id {}".format(user_id, place))
                if video_dto.file_status is FileStatus.UPLOADED.value:
                    self.storage_analyzer.analyze_video(self.base_path + place + '/rev/' + filename,
                                                        self.base_path + place + '/analysis/' + filename + '.json')
                    video_dto.analysis_url = self.path_to_gcloud_path(
                        self.base_path + place + '/analysis/' + filename + '.json')
                    video_dto.file_status = FileStatus.ANALYZING
                    return self.video_catalog_service.update(video_dto)
                # Thread(target=self.analyze, args=([absolute_path])).start()
            except Exception as e:
                self.logger.error("not uploaded [{}]".format(e))
        else:
            self.logger.error("Type file not accepted: {}".format(file.filename))
            return VideoDto.NULL

    def upload_simple_file(self, path, file):
        if file.content_type in self.allowed_images_content_type:
            filename = file.filename.replace(" ", "_")
            blob_name = self.base_path + path + '/' + filename
            blob = self.bucket.blob(blob_name)
            try:
                blob.upload_from_file(file, content_type=file.content_type)
                self.logger.info("File uploaded: " + blob.name)
            except Exception as e:
                self.logger.error("not uploaded [{}]".format(e))
            try:
                blob.make_public()
                return blob.public_url
            except Exception as e:
                self.logger.error("not uploaded [{}]".format(e))
        else:
            self.logger.error("Type file not accepted: {}".format(file.filename))
            return None

    def get_file(self, path):
        blob = self.bucket.blob(path)
        if not blob.exists():
            return None
        new_path = '/tmp/' + str(uuid.uuid4()) + '.' + path.split(".")[-1]
        self.logger.info('Saving ' + path + ' to ' + new_path)
        file = open(new_path, "wb")
        try:
            blob.download_to_file(file)
            file.close()
        except NotFound as e:
            return e
        return new_path

    def make_file_public(self, video_id):
        self.logger.debug("Setting public: " + video_id)
        video_dto = self.video_catalog_service.get_video_by_id(video_id)
        if video_dto is VideoDto.NULL or video_dto.file_public is True:
            return video_dto
        if video_dto.file_status is not FileStatus.HUMAN_REQUIRED.value and video_dto.file_status is not FileStatus.ANALYZING.value:
            return VideoDto.NULL
        path = self.gcloud_path_to_path(video_dto.g_path)
        new_path = re.sub(r'rev/', '', path)
        if self.move_file(path, new_path):
            self.logger.debug("New path: " + new_path)
            try:
                blob = self.bucket.blob(new_path)
                blob.make_public()
                video_dto.g_path = self.path_to_gcloud_path(blob.name)
                video_dto.public_url = blob.public_url
                video_dto.file_public = True
                video_dto.file_status = FileStatus.VALID
                return self.video_catalog_service.update(video_dto)
            except Exception as e:
                self.logger.error("Problem making public file: {}, {}".format(video_dto.id, e))
        return VideoDto.NULL

    def make_file_private(self, video_id):
        self.logger.debug("Setting private: " + video_id)
        video_dto = self.video_catalog_service.get_video_by_id(video_id)
        if video_dto is VideoDto.NULL or video_dto.file_public is False:
            self.logger.debug("Empty or not public")
            return video_dto
        if video_dto.file_status is not FileStatus.VALID.value:
            return VideoDto.NULL
        path = self.gcloud_path_to_path(video_dto.g_path)
        new_path = re.sub(r'{}{}/'.format(self.base_path, video_dto.place_id),
                          '{}{}/rev/'.format(self.base_path, video_dto.place_id), path)
        if self.move_file(path, new_path):
            self.logger.debug("New path: " + new_path)
            try:
                blob = self.bucket.blob(new_path)
                blob.make_private()
                video_dto.g_path = self.path_to_gcloud_path(blob.name)
                video_dto.public_url = ''
                video_dto.file_public = False
                video_dto.file_status = FileStatus.HUMAN_REQUIRED
                return self.video_catalog_service.update(video_dto)
            except Exception as e:
                self.logger.error("Problem making private file: {}, {}".format(video_dto.id, e))
        return VideoDto.NULL

    def make_file_to_rev(self, video_id):
        self.logger.debug("ANALYZING to HUMAN_REQUIRED video with id: " + video_id)
        video_dto = self.video_catalog_service.get_video_by_id(video_id)
        if video_dto is VideoDto.NULL or video_dto.file_status is not FileStatus.ANALYZING.value:
            return VideoDto.NULL
        if video_dto.file_public:
            return self.make_file_private(video_id)
        elif video_dto.file_status is FileStatus.ANALYZING.value and video_dto is not VideoDto.NULL:
            video_dto.public_url = ''
            video_dto.file_public = False
            video_dto.file_status = FileStatus.HUMAN_REQUIRED
            video_dto = self.video_catalog_service.update(video_dto)
        return video_dto

    def delete_file(self, video_id):
        self.make_file_private(video_id)
        self.logger.debug("Deleting: " + video_id)
        video_dto = self.video_catalog_service.get_video_by_id(video_id)
        if video_dto is VideoDto.NULL or video_dto.file_status is FileStatus.DELETED.value:
            self.logger.debug("Empty")
            return video_dto
        path = self.gcloud_path_to_path(video_dto.g_path)
        new_path = 'deleted/' + path
        if self.move_file(path, new_path):
            self.logger.debug("New path: " + new_path)
            try:
                blob = self.bucket.blob(new_path)
                video_dto.g_path = self.path_to_gcloud_path(blob.name)
                video_dto.file_public = False
                video_dto.file_status = FileStatus.DELETED
                return self.video_catalog_service.update(video_dto)
            except Exception as e:
                self.logger.error("Problem making private file: {}, {}".format(video_dto.id, e))
        return VideoDto.NULL

    def undelete_file(self, video_id):
        self.logger.debug("Undeleting: " + video_id)
        video_dto = self.video_catalog_service.get_video_by_id(video_id)
        if video_dto is VideoDto.NULL or video_dto.file_status is not FileStatus.DELETED.value:
            self.logger.debug("Not deleted")
            return video_dto
        path = self.gcloud_path_to_path(video_dto.g_path)
        new_path = path.replace('deleted/', '')
        if self.move_file(path, new_path):
            self.logger.debug("New path: " + new_path)
            try:
                blob = self.bucket.blob(new_path)
                video_dto.g_path = self.path_to_gcloud_path(blob.name)
                video_dto.public_url = ''
                video_dto.file_public = False
                video_dto.file_status = FileStatus.HUMAN_REQUIRED
                return self.video_catalog_service.update(video_dto)
            except Exception as e:
                self.logger.error("Problem updating file: {}, {}".format(video_dto.id, e))
        return VideoDto.NULL

    def permanent_delete(self, video_id):
        self.make_file_private(video_id)
        self.logger.debug("Permanent Deleting: " + video_id)
        video_dto = self.video_catalog_service.get_video_by_id(video_id)
        if video_dto is not VideoDto.NULL: #and video_dto.file_status is FileStatus.DELETED.value:
            path = self.gcloud_path_to_path(video_dto.g_path)
            analysis_path = self.gcloud_path_to_path(video_dto.analysis_url)
            self.logger.debug("Deleting: " + path)
            try:
                blob = self.bucket.blob(path)
                blob.delete()
                analysis_blob = self.bucket.blob(analysis_path)
                analysis_blob.delete()
                self.logger.info('File removed from Google Cloud Storage: {}'.format(video_dto.g_path))
            except Exception as e:
                self.logger.error("Problem deleting permanently file: {}, {}".format(video_dto.g_path, e))
            try:
                return self.video_catalog_service.delete(video_id)
            except Exception as e:
                self.logger.error("Problem deleting permanently from local db: {}, {}".format(video_dto.id, e))
        return VideoDto.NULL

    def move_file(self, path, new_path):
        try:
            blob = self.bucket.blob(path)
            self.bucket.rename_blob(blob, new_path)
            return True
        except:
            return False

    def list_videos_by_user(self, user_id):
        blob_array = []
        self.logger.debug("List videos with user_id: {}".format(user_id))
        for element in self.video_catalog_service.get_videos_by_user(user_id):
            self.logger.debug(str(element))
            blob_array.append(element.to_dict())

        return_json = {"videos": blob_array}
        self.logger.debug(return_json)
        return return_json

    def list_videos_by_place(self, place_id):
        # TODO if admin
        blob_array = []
        self.logger.debug("List videos with place_id: {}".format(place_id))
        for element in self.video_catalog_service.get_videos_by_place(place_id):
            self.logger.debug(str(element))
            blob_array.append(element.to_dict())

        return_json = {"videos": blob_array}
        self.logger.debug(return_json)
        return return_json

    def list_videos_by_places(self, place_ids):
        # TODO if admin
        blob_array = []
        self.logger.debug(f'List videos with place_ids: {place_ids}')
        for place_id in place_ids:
            for video in self.video_catalog_service.get_videos_by_place(place_id):
                self.logger.debug(str(video))
                blob_array.append(video.to_dict())

        return_json = {"videos": blob_array}
        self.logger.debug(return_json)
        return return_json

    def list_videos(self):
        # TODO if admin
        blob_array = []
        for element in self.video_catalog_service.get_all():
            blob_array.append(element.to_dict())

        return_json = {"videos": blob_array}
        self.logger.debug(return_json)
        return return_json

    def get_file_id(self, video_id):
        file_dto = self.video_catalog_service.get_video_by_id(video_id)
        if file_dto is not VideoDto.NULL:
            blob = self.bucket.blob(self.gcloud_path_to_path(file_dto.g_path))
            if blob.exists():
                new_path = '/tmp/' + str(uuid.uuid4()) + '.' + blob.name.split(".")[-1]
                self.logger.info('Saving ' + file_dto.g_path + ' to ' + new_path)
                file = open(new_path, "wb")
                try:
                    blob.download_to_file(file)
                    file.close()
                except NotFound as e:
                    return e
                return new_path
        return file_dto

    def get_video_id(self, video_id):
        video_dto = self.video_catalog_service.get_video_by_id(video_id)
        return video_dto

    def get_file_analysis_id(self, video_id):
        file_dto = self.video_catalog_service.get_video_by_id(video_id)
        if file_dto is not VideoDto.NULL:
            blob = self.bucket.blob(self.gcloud_path_to_path(file_dto.analysis_url))
            if blob.exists():
                new_path = '/tmp/' + str(uuid.uuid4()) + '.' + blob.name.split(".")[-1]
                self.logger.info('Saving ' + file_dto.g_path + ' to ' + new_path)
                file = open(new_path, "wb")
                try:
                    blob.download_to_file(file)
                    file.close()
                except NotFound as e:
                    return e
                return new_path
        return VideoDto.NULL

    def update_file(self, video_id, user_id, place_id, title, description, username, latitude, longitude):
        video_dto = self.video_catalog_service.get_video_by_id(video_id)
        if video_dto is VideoDto.NULL:
            return video_dto
        video_dto.user_id = user_id
        if video_dto.place_id != place_id:
            video_dto = self.update_place(video_id, place_id)
        video_dto.title = title
        video_dto.description = description
        video_dto.username = username
        video_dto.coordinates = Coordinates(latitude, longitude)
        return self.video_catalog_service.update(video_dto)

    def update_place(self, video_id, place_id):
        video_dto = self.video_catalog_service.get_video_by_id(video_id)
        if video_dto is VideoDto.NULL or video_dto.place_id is place_id:
            return video_dto
        self.logger.debug("Updating place: " + place_id)
        g_path = video_dto.g_path
        path = self.gcloud_path_to_path(g_path)
        new_g_path = re.sub(r'{}/'.format(video_dto.place_id),
                            '{}/'.format(place_id), g_path)
        new_path = self.gcloud_path_to_path(new_g_path)

        analysis_url = video_dto.analysis_url
        analysis_path = self.gcloud_path_to_path(analysis_url)
        new_analysis = re.sub(r'{}/'.format(video_dto.place_id),
                              '{}/'.format(place_id), analysis_url)
        new_analysis_path = self.gcloud_path_to_path(new_analysis)
        public_url = video_dto.public_url
        new_public_url = re.sub(r'{}/'.format(video_dto.place_id), '{}/'.format(place_id), public_url)

        try:
            if self.move_file(path, new_path) and self.move_file(analysis_path, new_analysis_path):
                video_dto.public_url = new_public_url
                video_dto.g_path = new_g_path
                video_dto.analysis_url = new_analysis
                video_dto.place_id = place_id
                return self.video_catalog_service.update(video_dto)
        except Exception:
            return VideoDto.NULL

    def list_videos_gcs(self):
        blobs: List[Blob] = self.bucket.list_blobs()
        blob_array = []
        for blob in blobs:
            print(str(blob))
            # if "/analysis/" not in blob.name and self.video_catalog_service.get_video_by_gpath(
            #         self.path_to_gcloud_path(blob.name)) is VideoDto.NULL:
            #     self.logger.info("New video detected in GCS: {}".format(blob.name))
            #     blob_array.append(str(blob))
            #     path_without_rev = blob.name.replace("/rev/", "/")
            #     analysis_url = 'analysis/' + path_without_rev
            #     place_id = os.path.basename(path_without_rev)
            #     print("{} {} {}".format(self.path_to_gcloud_path(blob.name), analysis_url, place_id))
            # self.video_catalog_service.add(str(uuid.uuid4()), self.path_to_gcloud_path(blob.name), "", analysis_url,
            #                                False, FileStatus.FORMAT_ERROR, "", place_id, "", "", "")
        return {'blobs': blob_array}

    def put_vote_video(self, video_id, value):
        file_dto = self.video_catalog_service.get_video_by_id(video_id)
        if file_dto is VideoDto.NULL:
            raise StorageError('Video file was not found', status=404)

        if value == 1:
            return self.video_catalog_service.add_vote(video_id)
        elif value == -1:
            return self.video_catalog_service.delete_vote(video_id)

    def put_report_video(self, video_id, value):
        file_dto = self.video_catalog_service.get_video_by_id(video_id)
        if file_dto is VideoDto.NULL:
            raise StorageError('Video file was not found', status=404)
        if value == 1:
            return self.video_catalog_service.add_report(video_id)
        elif value == -1:
            return self.video_catalog_service.delete_report(video_id)
