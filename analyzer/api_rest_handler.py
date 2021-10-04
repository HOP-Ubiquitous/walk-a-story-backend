import os
import re

import colorlog
import json
import requests
from flask import request, Blueprint, Response

import config
from analyzer.IA_service import IAService
from video_catalog.dto import VideoDto, FileStatus
from video_catalog.services.video_service import VideoService

logger = colorlog.getLogger('API REST Event Handler')
IA_service: IAService = None
video_catalog: VideoService = None

URL_STORAGE = "http://" + config.REST_URL + ":" + config.REST_PORT + "/api/v1/"
# BUCKET_NAME = os.getenv('BUCKET_NAME', 'co-crew')
BUCKET_NAME = os.getenv('BUCKET_NAME', 'bememories')

# SENDER_PORT = "8082"
# WB_URL = "192.168.1.51"

analyzer = Blueprint('analyzer', __name__)


@analyzer.route('/notify', methods=['POST'])
def data():
    logger.info("Notification received: " + json.dumps(request.json))
    notification = request.json
    analysis_file_path = notification['notification']
    file_path = re.sub(r'\.json$', '', notification['notification'])
    file_path = re.sub(r'analysis/', 'rev/', file_path)
    logger.debug("JSON file in: " + analysis_file_path)

    file_dto = video_catalog.get_video_by_gpath('gs://' + BUCKET_NAME + '/' + file_path)
    if file_dto is VideoDto.NULL:
        logger.debug("Not file to rev: " + file_path)
        return Response(response='{"message":"not_file_to_rev","file":"' + file_path + '"}', status=200,
                        mimetype="application/json")

    # analysis_file = requests.get(URL_STORAGE + analysis_file_path)
    analysis_file = requests.get(URL_STORAGE + 'analysis/' + file_dto.id)
    video_status = IA_service.analyze_values(analysis_file.text)
    if video_status is FileStatus.VALID:
        requests.put(URL_STORAGE + 'public/' + file_dto.id)
    else:
        logger.info(str(video_status) + ' of ' + file_path)
        requests.put(URL_STORAGE + 'rev/' + file_dto.id)
        pass
    logger.info('Analysis status ' + file_dto.g_path + ' is: ' + str(video_status))
    return Response(response='{"message":"' + str(video_status) + '"}', status=200, mimetype="application/json")


@analyzer.route('/data', methods=['POST'])
def data_engine():
    print(request.data)
    return Response(response='{"message":"ok"}', status=200, mimetype="application/json")
