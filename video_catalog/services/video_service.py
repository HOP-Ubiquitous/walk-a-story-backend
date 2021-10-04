from typing import List

from video_catalog.dto import VideoDto


class VideoService:
    def add(self,video_dto) -> VideoDto:
        raise NotImplementedError('you must implement this method')

    def get_video_by_id(self, video_id) -> VideoDto:
        raise NotImplementedError('you must implement this method')

    def get_all(self) -> List[VideoDto]:
        raise NotImplementedError('you must implement this method')

    def get_videos_by_public(self, public) -> List[VideoDto]:
        raise NotImplementedError('you must implement this method')

    def get_videos_by_user(self, user_id) -> List[VideoDto]:
        raise NotImplementedError('you must implement this method')

    def get_videos_by_place(self, place_id) -> List[VideoDto]:
        raise NotImplementedError('you must implement this method')

    def get_videos_by_status(self, file_status) -> List[VideoDto]:
        raise NotImplementedError('you must implement this method')

    def get_video_by_gpath(self, gpath) -> VideoDto:
        raise NotImplementedError('you must implement this method')

    def update(self, video_dto) -> VideoDto:
        raise NotImplementedError('you must implement this method')

    def add_vote(self, video_id) -> VideoDto:
        raise NotImplementedError('you must implement this method')

    def delete_vote(self, video_id) -> VideoDto:
        raise NotImplementedError('you must implement this method')

    def add_report(self, video_id) -> VideoDto:
        raise NotImplementedError('you must implement this method')

    def delete_report(self, video_id) -> VideoDto:
        raise NotImplementedError('you must implement this method')

    def delete(self, video_id) -> VideoDto:
        raise NotImplementedError('you must implement this method')
