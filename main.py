import json
import os
from http import HTTPStatus

import colorlog
from flask import Flask
from flask_cors import CORS, cross_origin

from locations.api_rest import api_rest_locations
from locations.services.location_service_impl import LocationServiceImpl
from locations.stores.sqlalchemy.sql_alchemy_store import SQLAlchemyLocationStore
from places.api_rest import api_rest_places
from places.services.place_service_impl import PlaceServiceImpl
from places.stores.sqlalchemy.sql_alchemy_city_store import SQLAlchemyCityStore
from places.stores.sqlalchemy.sql_alchemy_point_of_interest_store import SQLAlchemyPointOfInterestStore
from storage.storage_service_gcloud_impl import StorageServiceGCloudImpl
from utils.custom_logger import logger

import config
from public import app

from google.cloud import videointelligence

from storage.storage_analyze import StorageVideoIntelligence
from analyzer.IA_analyzer import IAAnalyzer
from utils.string_2_boolean import str2bool

from video_catalog.services.video_service_impl import VideoServiceImpl
from video_catalog.stores.sqlalchemy.sql_alchemy_store import SQLAlchemyVideoStore

from analyzer import api_rest_handler
from storage import api_rest_storage

from users.services.user_service_impl import UserServiceImpl
from users.stores.sqlalchemy.sql_alchemy_store import SQLAlchemyUserStore
from users.api_rest import api_rest_users
from users.api_rest.api_rest_users import login_manager

from caminatas.stores.sqlalchemy.sql_alchemy_store import SQLAlchemyCaminataStore
from caminatas.services.caminata_service_impl import CaminataServiceImpl
from caminatas.api_rest import api_rest_caminatas

from comments.stores.sqlalchemy.sql_alchemy_store import SQLAlchemyCommentStore
from comments.services.comment_service_impl import CommentServiceImpl
from comments.api_rest import api_rest_comments

from ratings.stores.sqlalchemy.sql_alchemy_store import SQLAlchemyRatingStore
from ratings.services.rating_service_impl import RatingServiceImpl
from ratings.api_rest import api_rest_ratings

# from OpenSSL import SSL

logger = colorlog.getLogger('Main')

application = Flask(__name__)
application.config['SECRET_KEY'] = config.SECRET_KEY
application.url_map.strict_slashes = False

login_manager.init_app(application)
CORS(application)  # TODO


@application.after_request
@cross_origin()
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,access-control-allow-origin,Origin')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@application.route('/version')
def get_version():
    return Flask.response_class(
        response=json.dumps({
            'version': config.VERSION
        }),
        status=HTTPStatus.OK,
        mimetype='application/json'
    )


def setup_app():

    application.register_blueprint(api_rest_storage.storage, url_prefix='/api/v1/')
    application.register_blueprint(api_rest_handler.analyzer, url_prefix='/api/v1/analyzer')
    application.register_blueprint(api_rest_users.users, url_prefix='/api/v1/users')
    application.register_blueprint(api_rest_caminatas.caminatas, url_prefix='/api/v1/caminatas')
    application.register_blueprint(api_rest_comments.comments, url_prefix='/api/v1/comments')
    application.register_blueprint(api_rest_ratings.ratings, url_prefix='/api/v1/ratings')
    application.register_blueprint(api_rest_places.places, url_prefix='/api/v1/places')
    application.register_blueprint(api_rest_locations.locations, url_prefix='/api/v1/locations')

    # websocket_notification = create_connection("ws://" + WB_URL + ":" + SENDER_PORT)

    db_directory = "../db"
    if not os.path.isdir(db_directory):
        os.mkdir(db_directory)

    current_path = os.path.dirname(os.path.abspath(__file__))

    analyzer_controller = StorageVideoIntelligence(
        'gs://' + config.BUCKET_NAME + '/',
        features=[
            videointelligence.enums.Feature.EXPLICIT_CONTENT_DETECTION,
            videointelligence.enums.Feature.LABEL_DETECTION
        ]
    )

    sqlite_videos_db = 'sqlite:///{}/../db/videos.db'.format(current_path)
    logger.debug('Path sqlite videos: {}'.format(sqlite_videos_db))
    video_catalog = VideoServiceImpl(SQLAlchemyVideoStore(sqlite_videos_db))
    storage_controller = StorageServiceGCloudImpl(
        config.BUCKET_NAME,
        config.ALLOWED_CONTENT_TYPES,
        analyzer_controller,
        video_catalog,
        config.DEFAULT_ACCEPTED_IMAGES_CONTENT_TYPE,
        config.BASE_PATH
    )
    api_rest_storage.storage_service = storage_controller
    api_rest_handler.IA_service = IAAnalyzer()
    api_rest_handler.video_catalog = video_catalog

    sqlite_users_db = 'sqlite:///{}/../db/users.db'.format(current_path)
    logger.debug('Path sqlite users: {}'.format(sqlite_users_db))
    users_service = UserServiceImpl(SQLAlchemyUserStore(sqlite_users_db), config.SUPER_ADMIN_USERNAME)
    api_rest_users.user_service = users_service

    sqlite_caminatas_db = 'sqlite:///{}/../db/caminatas.db'.format(current_path)
    logger.debug('Path sqlite caminatas: {}'.format(sqlite_caminatas_db))
    caminata_service = CaminataServiceImpl(SQLAlchemyCaminataStore(sqlite_caminatas_db))
    api_rest_caminatas.caminatas_service = caminata_service
    api_rest_caminatas.user_service = users_service

    sqlite_comments_db = 'sqlite:///{}/../db/comments.db'.format(current_path)
    logger.debug('Path sqlite comments: {}'.format(sqlite_comments_db))
    comment_service = CommentServiceImpl(SQLAlchemyCommentStore(sqlite_comments_db), config.MAX_COMMENTS_BY_USER)
    api_rest_comments.comment_service = comment_service

    sqlite_ratings_db = 'sqlite:///{}/../db/ratings.db'.format(current_path)
    logger.debug('Path sqlite ratings: {}'.format(sqlite_ratings_db))
    rating_service = RatingServiceImpl(
        SQLAlchemyRatingStore(sqlite_ratings_db),
        config.REPORT_VALUE,
        config.MAX_TIMES_RATING_USER
    )
    api_rest_ratings.rating_service = rating_service
    api_rest_ratings.comment_service = comment_service
    api_rest_ratings.storage_service = storage_controller

    sqlite_places_db = 'sqlite:///{}/../db/places.db'.format(current_path)
    logger.debug('Path sqlite places: {}'.format(sqlite_places_db))
    place_service = PlaceServiceImpl(
        SQLAlchemyCityStore(sqlite_places_db),
        SQLAlchemyPointOfInterestStore(sqlite_places_db),
        caminata_service,
        video_catalog
    )
    api_rest_places.place_service = place_service

    sqlite_locations_db = 'sqlite:///{}/../db/locations.db'.format(current_path)
    logger.debug('Path sqlite locations: {}'.format(sqlite_locations_db))
    location_service = LocationServiceImpl(
        SQLAlchemyLocationStore(sqlite_locations_db),
        is_secure_api=str2bool(config.SECURE_API)
    )
    api_rest_locations.location_service = location_service


setup_app()

if __name__ == '__main__':
    application.run(config.REST_URL, config.REST_PORT, threaded=True, debug=False)
