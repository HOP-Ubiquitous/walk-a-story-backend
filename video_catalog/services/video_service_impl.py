from typing import List

from video_catalog import mapper
from video_catalog.dto import VideoDto, FileStatus
from video_catalog.services.video_service import VideoService
from video_catalog.stores.video_store import VideoStore

DEFAULT_RATING_COUNTS = 0


class VideoServiceImpl(VideoService):
    def __init__(self, video_store: VideoStore):
        self.video_store = video_store

    def add(self, video_dto: VideoDto) -> VideoDto:
        video_info = self.video_store.add(video_dto.id,
                                          video_dto.g_path,
                                          video_dto.public_url,
                                          video_dto.analysis_url,
                                          video_dto.file_public,
                                          video_dto.file_status,
                                          video_dto.user_id,
                                          video_dto.place_id,
                                          video_dto.title,
                                          video_dto.description,
                                          video_dto.username,
                                          video_dto.coordinates.latitude,
                                          video_dto.coordinates.longitude,
                                          DEFAULT_RATING_COUNTS,
                                          DEFAULT_RATING_COUNTS,
                                          DEFAULT_RATING_COUNTS)

        return mapper.entity_to_dto(video_info)

    def get_video_by_id(self, video_id) -> VideoDto:
        video_info = self.video_store.get_video_by_id(video_id)

        return mapper.entity_to_dto(video_info)

    def get_all(self) -> List[VideoDto]:
        videos = self.video_store.get_all()

        return [mapper.entity_to_dto(video_info) for video_info in videos]

    def get_videos_by_public(self, file_public) -> List[VideoDto]:
        videos = self.video_store.get_videos_by_public(file_public)

        return [mapper.entity_to_dto(video_info) for video_info in videos]

    def get_videos_by_user(self, user_id) -> List[VideoDto]:
        videos = self.video_store.get_videos_by_user(user_id)

        return [mapper.entity_to_dto(video_info) for video_info in videos]

    def get_videos_by_place(self, place_id) -> List[VideoDto]:
        videos = self.video_store.get_videos_by_place(place_id)

        return [mapper.entity_to_dto(video_info) for video_info in videos]

    def get_videos_by_status(self, file_status) -> List[VideoDto]:
        videos = self.video_store.get_videos_by_status(file_status)

        return [mapper.entity_to_dto(video_info) for video_info in videos]

    def get_video_by_gpath(self, gpath) -> List[VideoDto]:
        video_info = self.video_store.get_video_by_gpath(gpath)

        return mapper.entity_to_dto(video_info)

    def __generic_vote(self, video_id, positive_value, negative_value):

        video_entity = self.video_store.get_video_by_id(video_id)
        video_entity_updated = self.video_store.update(video_entity.id,
                                                       video_entity.g_path,
                                                       video_entity.public_url,
                                                       video_entity.analysis_url,
                                                       video_entity.file_public,
                                                       FileStatus(video_entity.file_status),
                                                       video_entity.user_id,
                                                       video_entity.place_id,
                                                       video_entity.title,
                                                       video_entity.description,
                                                       video_entity.username,
                                                       video_entity.coordinates.latitude,
                                                       video_entity.coordinates.longitude,
                                                       video_entity.positive_votes + positive_value,
                                                       video_entity.negative_votes + negative_value,
                                                       video_entity.reports)
        return mapper.entity_to_dto(video_entity_updated)

    def add_vote(self, video_id) -> VideoDto:
        return self.__generic_vote(video_id, positive_value=1, negative_value=0)

    def delete_vote(self, video_id) -> VideoDto:
        return self.__generic_vote(video_id, positive_value=0, negative_value=1)

    def __generic_report(self, video_id, value):
        video_entity = self.video_store.get_video_by_id(video_id)
        video_entity_updated = self.video_store.update(video_entity.id,
                                                       video_entity.g_path,
                                                       video_entity.public_url,
                                                       video_entity.analysis_url,
                                                       video_entity.file_public,
                                                       FileStatus(video_entity.file_status),
                                                       video_entity.user_id,
                                                       video_entity.place_id,
                                                       video_entity.title,
                                                       video_entity.description,
                                                       video_entity.username,
                                                       video_entity.coordinates.latitude,
                                                       video_entity.coordinates.longitude,
                                                       video_entity.positive_votes,
                                                       video_entity.negative_votes,
                                                       video_entity.reports + value)
        return mapper.entity_to_dto(video_entity_updated)

    def add_report(self, video_id) -> VideoDto:
        return self.__generic_report(video_id, 1)

    def delete_report(self, video_id) -> VideoDto:
        return self.__generic_report(video_id, -1)

    def update(self, video_dto : VideoDto) -> VideoDto:
        video_info = self.video_store.update(video_dto.id,
                                             video_dto.g_path,
                                             video_dto.public_url,
                                             video_dto.analysis_url,
                                             video_dto.file_public,
                                             FileStatus(video_dto.file_status),
                                             video_dto.user_id,
                                             video_dto.place_id,
                                             video_dto.title,
                                             video_dto.description,
                                             video_dto.username,
                                             video_dto.coordinates.latitude,
                                             video_dto.coordinates.longitude,
                                             video_dto.positive_votes,
                                             video_dto.negative_votes,
                                             video_dto.reports)

        return mapper.entity_to_dto(video_info)

    def delete(self, video_id) -> VideoDto:
        video_info = self.video_store.delete(video_id)
        return mapper.entity_to_dto(video_info)
