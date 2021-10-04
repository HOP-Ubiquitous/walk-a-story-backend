from sqlalchemy.orm import Query

from video_catalog.entities.video import Video
from video_catalog.stores.sqlalchemy.models import VideoModel


def video_model_to_entity(video_model: VideoModel):
    return Video(video_model.id,
                 video_model.g_path,
                 video_model.public_url,
                 video_model.analysis_url,
                 video_model.file_public,
                 video_model.file_status,
                 video_model.user_id,
                 video_model.place_id,
                 video_model.title,
                 video_model.description,
                 video_model.username,
                 video_model.creation_date,
                 video_model.latitude,
                 video_model.longitude,
                 video_model.positive_votes,
                 video_model.negative_votes,
                 video_model.reports)


def query_video_model_to_entity_list(query_video_models: Query):
    return [
        Video(video_model.id,
              video_model.g_path,
              video_model.public_url,
              video_model.analysis_url,
              video_model.file_public,
              video_model.file_status,
              video_model.user_id,
              video_model.place_id,
              video_model.title,
              video_model.description,
              video_model.username,
              video_model.creation_date,
              video_model.latitude,
              video_model.longitude,
              video_model.positive_votes,
              video_model.negative_votes,
              video_model.reports)
        for video_model in query_video_models.all()
    ]


def first_query_video_model_to_entity_list(query_video_models: Query):
    if len(query_video_models.all()) != 1:
        return None
    return video_model_to_entity(query_video_models.first())
