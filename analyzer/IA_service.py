from video_catalog.dto import FileStatus


class IAService:
    def analyze_values(self, json_values) -> FileStatus:
        raise NotImplementedError('you must implement this method')
