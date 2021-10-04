import os
import colorlog
from storage.storage_service import StorageService

logger = colorlog.getLogger('Smart Storage')
PATH_LOST_FILES = 'lost/'
REVISION_PATH = 'rev/'


def create_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


class StorageServiceLocalImpl(StorageService): # FIXME

    def __init__(self, upload_folder, allowed_extensions, analyzer):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions
        self.analyzer = analyzer

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def is_file(self, directory_path, filename):
        return (os.path.isfile(self.upload_folder + directory_path + filename) or os.path.isfile(
            self.upload_folder + 'lost/' + filename))

    def upload_file(self, path, file, username):
        if self.is_file(path, file.filename):
            info = 'already_exists'
            status = 409
        elif self.allowed_file(file.filename):
            try:
                file.save(os.path.join(self.upload_folder + path, file.filename))
                # os.setxattr(self.upload_folder + path + file.filename, 'user', bytes(username, 'utf-8'))
                # print("attr: " + os.getxattr(self.upload_folder + path + file.filename))  # => b'baz'
                os.chmod(self.upload_folder + path + file.filename, 000)
            except FileNotFoundError:
                file.save(os.path.join(self.upload_folder + 'lost/', file.filename))
            info = 'uploaded'
            status = 200
        else:
            info = 'not_uploaded'
            status = 406
        return info, status

    def get_file(self, path):
        if os.path.isfile(self.upload_folder + path):
            return self.upload_folder + path
        else:
            return None

    def make_file_public(self, path):
        if os.path.isfile(self.upload_folder + path):
            os.chmod(self.upload_folder + path, 755)
            info = 'private to public'
            status = 200
            return info, status
        else:
            return None

    def make_file_private(self, path):
        if os.path.isfile(self.upload_folder + path):
            os.chmod(self.upload_folder + path, 000)
            info = 'private to public'
            status = 200
            return info, status
        else:
            return None

    def delete_file(self, path):
        if os.path.exists(self.upload_folder + path):
            try:
                os.remove(self.upload_folder + path)
                info = 'deleted'
                status = 204
            except:
                logger.error('Error while deleting file ', path)
                info = 'not_deleted'
                status = 500
        else:
            logger.error('Can not delete the file as it doesn\'t exists ' + path)
            info = 'not_deleted'
            status = 404

        return info, status

    def move_file(self, path, new_path):
        if os.path.exists(self.upload_folder + path):
            try:
                os.rename(self.upload_folder + path, self.upload_folder + new_path)
                info = 'moved'
                status = 201
            except:
                logger.error('Error while moving file ', path)
                info = 'not_deleted'
                status = 500
        else:
            logger.error('Can not move the file as it doesn\'t exists ' + path)
            info = 'not_moved'
            status = 404

        return info, status


if __name__ == '__main__':
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/home/hopu/Descargas/test-imagenes/')
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'gif', 'mp4', 'txt']

    local_storage = StorageServiceLocalImpl(UPLOAD_FOLDER, ALLOWED_EXTENSIONS, None)
    # local_storage.move_file('nuevo/hostapd.png', 'nuevo/hostapd2.png')
    local_storage.delete_file('nuevo/hostapd2.png')
