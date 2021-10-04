from http import HTTPStatus

import colorlog
import json
from flask import request, Blueprint, Flask

from places.dto import CityDto, PointOfInterestDto
from places.places_error import PlacesError
from places.services.place_service import PlaceService
from users.role_required_decorators import admin_required, login_required

logger = colorlog.getLogger('REST API Places')
places = Blueprint('places', __name__)
place_service: PlaceService


@places.route('/cities', methods=['POST'])
@admin_required
def add_city():
    try:
        data = json.loads(request.data)
        name = data['name']
        city_dto: CityDto = place_service.add_city(name, [])
        if city_dto == CityDto.NULL:
            logger.error("City was not created")
            message = {"error": "city was not created"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = city_dto.to_dict()
            status = HTTPStatus.CREATED
    except PlacesError as places_error:
        message = {"error": str(places_error)}
        status = places_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as e:
        logger.error('Exception adding city: ', e)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@places.route('/cities/<city_id>', methods=['GET'])
@login_required
def get_city(city_id):
    try:
        city_dto: CityDto = place_service.get_city(city_id)
        if city_dto == CityDto.NULL:
            logger.error("City was not found")
            message = {"error": "city was not found"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = city_dto.to_dict()
            status = HTTPStatus.OK
    except PlacesError as places_error:
        message = {"error": str(places_error)}
        status = places_error.status
    except Exception as exception:
        logger.error('Exception getting city : ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@places.route('/cities', methods=['GET'])
@login_required
def get_cities():
    try:
        poi_id = request.args.get('poi_id')
        if poi_id is None:
            cities_dto: [CityDto] = place_service.get_all_cities()
        else:
            cities_dto: [CityDto] = place_service.get_city_by_point_of_interest_id(poi_id)
        if cities_dto == CityDto.NULL:
            logger.error("City was not found")
            message = {"error": "city was not found"}
            status = HTTPStatus.BAD_REQUEST
        else:
            cities_string = []
            for city_dto in cities_dto:
                cities_string.append(city_dto.to_dict())
            message = cities_string
            status = HTTPStatus.OK

    except PlacesError as places_error:
        message = {"error": str(places_error)}
        status = places_error.status
    except Exception as exception:
        logger.error('Exception getting city : ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@places.route('/cities/<city_id>', methods=['PATCH'])
@admin_required
def update_city(city_id):
    try:
        data = json.loads(request.data)
        name = data['name']
        city_dto: CityDto = place_service.update_city(city_id, name)
        if city_dto == CityDto.NULL:
            logger.error("City was not updated")
            message = {"error": "city was not updated"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = city_dto.to_dict()
            status = HTTPStatus.ACCEPTED
    except PlacesError as places_error:
        message = {"error": str(places_error)}
        status = places_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as e:
        logger.error('Exception updating city: ', e)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@places.route('/cities/<city_id>', methods=['DELETE'])
@admin_required
def delete_city(city_id):
    try:
        city_dto: CityDto = place_service.delete_city(city_id)
        if city_dto == CityDto.NULL:
            logger.error("City was not deleted")
            message = {"error": "city was not deleted"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = city_dto.to_dict()
            status = HTTPStatus.OK
    except PlacesError as places_error:
        message = {"error": str(places_error)}
        status = places_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as e:
        logger.error('Exception deleting city: ', e)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@places.route('/cities/<city_id>/pois', methods=['POST'])
@admin_required
def add_poi(city_id):
    try:
        data = json.loads(request.data)
        name = data['name']
        latitude = data['latitude']
        longitude = data['longitude']
        poi_dto: PointOfInterestDto = place_service.add_point_of_interest(name, city_id, latitude, longitude)
        if poi_dto == PointOfInterestDto.NULL:
            logger.error("Poi was not created")
            message = {"error": "poi was not created"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = poi_dto.to_dict()
            status = HTTPStatus.CREATED
    except PlacesError as places_error:
        message = {"error": str(places_error)}
        status = places_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as e:
        logger.error('Exception adding poi: ', e)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@places.route('/cities/pois/<poi_id>', methods=['GET'])
@login_required
def get_poi(poi_id):
    try:
        poi_dto: PointOfInterestDto = place_service.get_point_of_interest_by_id(poi_id)
        if poi_dto == PointOfInterestDto.NULL:
            logger.error("Poi was not found")
            message = {"error": "poi was not found"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = poi_dto.to_dict()
            status = HTTPStatus.OK
    except PlacesError as places_error:
        message = {"error": str(places_error)}
        status = places_error.status
    except Exception as exception:
        logger.error('Exception getting poi : ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@places.route('/cities/<city_id>/pois', methods=['GET'])
@login_required
def get_poi_by_city_id(city_id):
    try:
        pois_dto: [PointOfInterestDto] = place_service.get_points_of_interest_by_city_id(city_id)
        if pois_dto == PointOfInterestDto.NULL:
            logger.error("Pois was not found")
            message = {"error": "pois was not found"}
            status = HTTPStatus.BAD_REQUEST
        else:
            poi_string = []
            for poi_dto in pois_dto:
                poi_string.append(poi_dto.to_dict())
            message = poi_string
            status = HTTPStatus.OK
    except PlacesError as places_error:
        message = {"error": str(places_error)}
        status = places_error.status
    except Exception as exception:
        logger.error('Exception getting poi : ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@places.route('/cities/pois', methods=['GET'])
@login_required
def get_pois():
    try:
        pois_dto: [PointOfInterestDto] = place_service.get_all_points_of_interest()
        if pois_dto == PointOfInterestDto.NULL:
            logger.error("Poi was not found")
            message = {"error": "poi was not found"}
            status = HTTPStatus.BAD_REQUEST
        else:
            pois_string = []
            for poi_dto in pois_dto:
                pois_string.append(poi_dto.to_dict())
            message = pois_string
            status = HTTPStatus.OK

    except PlacesError as places_error:
        message = {"error": str(places_error)}
        status = places_error.status
    except Exception as exception:
        logger.error('Exception getting pois : ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@places.route('/cities/pois/<poi_id>', methods=['PATCH'])
@admin_required
def update_poi(poi_id):
    try:
        data = json.loads(request.data)
        name = data['name']
        city_id = data['city_id']
        latitude = data['latitude']
        longitude = data['longitude']
        poi_dto: PointOfInterestDto = place_service.update_point_of_interest(poi_id, name, city_id, latitude, longitude)
        if poi_dto == PointOfInterestDto.NULL:
            logger.error("Poi was not updated")
            message = {"error": "poi was not updated"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = poi_dto.to_dict()
            status = HTTPStatus.ACCEPTED
    except PlacesError as places_error:
        message = {"error": str(places_error)}
        status = places_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as e:
        logger.error('Exception updating poi: ', e)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@places.route('/cities/pois/<poi_id>', methods=['DELETE'])
@admin_required
def delete_poi(poi_id):
    try:
        poi_dto: PointOfInterestDto = place_service.delete_point_of_interest(poi_id)
        if poi_dto == PointOfInterestDto.NULL:
            logger.error("Poi was not deleted")
            message = {"error": "poi was not deleted"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = poi_dto.to_dict()
            status = HTTPStatus.ACCEPTED
    except PlacesError as places_error:
        message = {"error": str(places_error)}
        status = places_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as e:
        logger.error('Exception deleting poi: ', e)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )
