from typing import List

from video_catalog.entities.video import Video


class VideoStore:
    def add(self, video_id, g_path, public_url, analysis_url, file_public, file_status, user_id, place_id, title,
            description, username, latitude, longitude, positive_votes, negative_votes, reports) -> Video:
        raise NotImplementedError('you must implement this method')

    def get_video_by_id(self, video_id) -> Video:
        raise NotImplementedError('you must implement this method')

    def get_all(self) -> List[Video]:
        raise NotImplementedError('you must implement this method')

    def get_videos_by_public(self, public) -> List[Video]:
        raise NotImplementedError('you must implement this method')

    def get_videos_by_user(self, user_id) -> List[Video]:
        raise NotImplementedError('you must implement this method')

    def get_videos_by_place(self, place_id) -> List[Video]:
        raise NotImplementedError('you must implement this method')

    def get_videos_by_status(self, file_status) -> List[Video]:
        raise NotImplementedError('you must implement this method')

    def get_video_by_gpath(self, gpath) -> Video:
        raise NotImplementedError('you must implement this method')

    def update(
            self,
            video_id,
            g_path,
            public_url,
            analysis_url,
            file_public,
            file_status,
            user_id,
            place_id,
            title,
            description,
            username,
            latitude,
            longitude,
            positive_votes,
            negative_votes,
            reports
    ) -> Video:
        raise NotImplementedError('you must implement this method')

    def delete(self, video_id) -> Video:
        raise NotImplementedError('you must implement this method')
