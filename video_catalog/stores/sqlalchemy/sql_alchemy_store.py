from typing import List

import colorlog
from sqlalchemy.orm import Session

from video_catalog.entities.video import Video
from video_catalog.stores.sqlalchemy.models import VideoModel
from video_catalog.stores.video_store import VideoStore
from video_catalog.stores.sqlalchemy import mapper
from video_catalog.stores.sqlalchemy.data_access_layer import DataAccessLayer

logger = colorlog.getLogger('SQLAlchemyVideoStore')


class SQLAlchemyVideoStore(VideoStore):
    dal = None

    def __new__(cls, conn_string):
        cls.dal = DataAccessLayer(conn_string)
        cls.dal.connect()
        cls.dal.session = cls.dal.Session()

        return super().__new__(cls)

    def add(self, video_id, g_path, public_url, analysis_url, file_public, file_status, user_id, place_id, title,
            description, username, latitude, longitude, positive_votes, negative_votes, reports) -> Video:
        logger.debug("User_id: {} place_id {}".format(user_id, place_id))

        session = SQLAlchemyVideoStore.get_session()
        video_model = VideoModel(
            id=video_id,
            g_path=g_path,
            public_url=public_url,
            analysis_url=analysis_url,
            file_public=file_public,
            file_status=file_status,
            user_id=user_id,
            place_id=place_id,
            title=title,
            description=description,
            username=username,
            latitude=latitude,
            longitude=longitude,
            positive_votes=positive_votes,
            negative_votes=negative_votes,
            reports=reports
        )

        session.add(video_model)
        session.commit()
        session.refresh(video_model)

        logger.debug("Added: {}".format(video_model))
        video = mapper.video_model_to_entity(video_model)

        return video

    def get_video_by_id(self, video_id) -> Video:
        session = SQLAlchemyVideoStore.get_session()
        video = session.query(VideoModel).get(video_id)

        logger.debug("Collected: {}".format(video))

        return Video.NULL if video is None else mapper.video_model_to_entity(video)

    def get_all(self) -> List[Video]:
        session = SQLAlchemyVideoStore.get_session()
        videos = session.query(VideoModel)

        logger.debug("Collected all videos")

        return mapper.query_video_model_to_entity_list(videos)

    def get_videos_by_public(self, file_public) -> List[Video]:
        session = SQLAlchemyVideoStore.get_session()
        videos = session.query(VideoModel).filter_by(file_public=file_public)

        logger.debug("Collected: {}".format("videos where file_public: " + str(file_public)))

        return mapper.query_video_model_to_entity_list(videos)

    def get_videos_by_user(self, user_id) -> List[Video]:
        session = SQLAlchemyVideoStore.get_session()
        videos = session.query(VideoModel).filter_by(user_id=user_id)

        logger.debug("Collected: {}".format("videos where user_id: " + user_id))

        return mapper.query_video_model_to_entity_list(videos)

    def get_videos_by_place(self, place_id) -> List[Video]:
        session = SQLAlchemyVideoStore.get_session()
        videos = session.query(VideoModel).filter_by(place_id=place_id)  # , file_public=True)

        logger.debug("Collected: {}".format("videos where place_id: " + place_id))

        return mapper.query_video_model_to_entity_list(videos)

    def get_videos_by_status(self, file_status) -> List[Video]:
        session = SQLAlchemyVideoStore.get_session()
        videos = session.query(VideoModel).filter_by(file_status=file_status.value)

        logger.debug("Collected: {}".format("videos where file_status: " + str(file_status)))

        return mapper.query_video_model_to_entity_list(videos)

    def get_video_by_gpath(self, gpath) -> Video:
        session = SQLAlchemyVideoStore.get_session()
        videos = session.query(VideoModel).filter_by(g_path=gpath)
        logger.debug("Collected: {}".format("videos where gpath: " + gpath))
        if videos is None:
            return Video.NULL
        video_info = mapper.first_query_video_model_to_entity_list(videos)
        if video_info is None:
            return Video.NULL
        else:
            return video_info

    def update(self, video_id, g_path, public_url, analysis_url, file_public, file_status, user_id, place_id, title,
               description, username, latitude, longitude, positive_votes, negative_votes, reports) -> Video:
        session = SQLAlchemyVideoStore.get_session()
        video_model = session.query(VideoModel).get(video_id)
        if video_model is None:
            return Video.NULL

        video_model.g_path = g_path
        video_model.public_url = public_url
        video_model.file_public = file_public
        video_model.analysis_url = analysis_url
        video_model.file_status = file_status.value
        video_model.user_id = user_id
        video_model.place_id = place_id
        video_model.title = title
        video_model.description = description
        video_model.username = username
        video_model.latitude = latitude
        video_model.longitude = longitude
        video_model.positive_votes = positive_votes
        video_model.negative_votes = negative_votes
        video_model.reports = reports

        session.merge(video_model)
        session.commit()
        session.refresh(video_model)

        logger.debug("Updated: {}".format(video_model))
        video = mapper.video_model_to_entity(video_model)
        return video

    def delete(self, video_id) -> Video:
        session = SQLAlchemyVideoStore.get_session()

        video = session.query(VideoModel).get(video_id)
        if video:
            session.delete(video)
            session.commit()

            logger.debug("Deleted: {}".format(video))
            return mapper.video_model_to_entity(video)

        return Video.NULL

    @staticmethod
    def get_session() -> Session:
        return SQLAlchemyVideoStore.dal.Session()
