import colorlog

from video_catalog.dto import VideoDto
from video_catalog.entities.video import Video

logger = colorlog.getLogger("Mapper Video to VideoDto")


def entity_to_dto(video: Video):
    if video is Video.NULL:
        return VideoDto.NULL

    return VideoDto(video.id,
                    video.g_path,
                    video.public_url,
                    video.analysis_url,
                    video.file_public,
                    video.file_status,
                    video.user_id,
                    video.place_id,
                    video.title,
                    video.description,
                    video.username,
                    video.creation_date,
                    video.coordinates,
                    video.positive_votes,
                    video.negative_votes,
                    video.reports)
