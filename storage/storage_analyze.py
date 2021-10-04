import colorlog

from google.cloud import videointelligence

from utils.json_response import json_response
from video_catalog.dto import FileStatus

logger = colorlog.getLogger('Video Intelligence')


# features example: [videointelligence.enums.Feature.LABEL_DETECTION]

class StorageVideoIntelligence:
    def __init__(self, root_path, features):
        self.video_client = videointelligence.VideoIntelligenceServiceClient()
        self.root_path = root_path
        self.features = features

    def analyze_video(self, path, output_uri):
        data = json_response(path=self.root_path + path, output_uri=self.root_path + output_uri)
        logger.info('Processing video, JSON: ' + data)
        # TODO ANALISIS SI NO EXISTE
        self.video_client.annotate_video(self.root_path + path, features=self.features,
                                         output_uri=self.root_path + output_uri)
        return FileStatus.ANALYZING


if __name__ == '__main__':
    analyzer = StorageVideoIntelligence(
        'gs://bememories/',
        features=[videointelligence.enums.Feature.EXPLICIT_CONTENT_DETECTION,
                  videointelligence.enums.Feature.SHOT_CHANGE_DETECTION]
    )
    print(analyzer.analyze_video('ruinas/rev/sample.mp4', 'ruinas/rev/sample.json'))
