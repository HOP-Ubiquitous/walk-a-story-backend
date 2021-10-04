class StorageService:
    def upload_file(self, path, file, user_id):
        raise NotImplementedError('you must implement this method')

    def upload_simple_file(self, path, file):
        raise NotImplementedError('you must implement this method')

    def get_file(self, path):
        raise NotImplementedError('you must implement this method')

    def get_video_id(self, path):
        raise NotImplementedError('you must implement this method')

    def delete_file(self, video_id):
        raise NotImplementedError('you must implement this method')

    def undelete_file(self, video_id):
        raise NotImplementedError('you must implement this method')

    def permanent_delete(self, video_id):
        raise NotImplementedError('you must implement this method')

    def make_file_public(self, path):
        raise NotImplementedError('you must implement this method')

    def make_file_private(self, path):
        raise NotImplementedError('you must implement this method')

    def move_file(self, path, new_path):
        raise NotImplementedError('you must implement this method')

    def make_file_to_rev(self, path):
        raise NotImplementedError('you must implement this method')

    def list_videos(self):
        raise NotImplementedError('you must implement this method')

    def list_videos_by_user(self, user_id):
        raise NotImplementedError('you must implement this method')

    def list_videos_by_place(self, place_id):
        raise NotImplementedError('you must implement this method')

    def list_videos_by_places(self, place_ids):
        raise NotImplementedError('you must implement this method')

    def get_file_id(self, video_id):
        raise NotImplementedError('you must implement this method')

    def get_file_analysis_id(self, video_id):
        raise NotImplementedError('you must implement this method')

    def update_file(self, video_id, user_id, place_id, title, description, username, latitude, longitude):
        raise NotImplementedError('you must implement this method')

    def put_vote_video(self, video_id, value):
        raise NotImplementedError('you must implement this method')

    def put_report_video(self, video_id, value):
        raise NotImplementedError('you must implement this method')
