import json

import colorlog
from analyzer.IA_service import IAService
from video_catalog.dto import FileStatus

logger = colorlog.getLogger('Video Intelligence')

ROOT_DIRECTORY = 'gs://bememories/'

ALLOWED_LABELS = ['Future', 'History']
NOT_ALLOWED_LABELS = ['Animation']

ALLOWED_LIKELIHOOD = ['VERY_UNLIKELY', 'UNLIKELY']
NOT_ALLOWED_LIKELIHOOD = ['POSSIBLE', 'LIKELY', 'VERY_LIKELY']
# features example: [videointelligence.enums.Feature.LABEL_DETECTION]


class IAAnalyzer(IAService):
    def __init__(self):
        pass

    def analyze_values(self, json_values):
        try:
            result = json.loads(json_values) #TODO 0 no, se debe buscar explicit_annotation
            for frame in result["annotation_results"][0]["explicit_annotation"]["frames"]:
                if frame["pornography_likelihood"] in NOT_ALLOWED_LIKELIHOOD:
                    return FileStatus.HUMAN_REQUIRED
        except Exception as e:
            logger.error("Exception: " + str(e))
            return FileStatus.FORMAT_ERROR

        return FileStatus.VALID


if __name__ == '__main__':
    analyzer = IAAnalyzer()
    print(analyzer.analyze_values("LIKELY"))
