import os
import colorlog

from places.services.place_service_impl import PlaceServiceImpl
from places.stores.sqlalchemy.sql_alchemy_city_store import SQLAlchemyCityStore
from places.stores.sqlalchemy.sql_alchemy_point_of_interest_store import SQLAlchemyPointOfInterestStore

logger = colorlog.getLogger('MainPlaces')

if __name__ == '__main__':
    db_directory = "../../db-test"
    if not os.path.isdir(db_directory):
        os.mkdir(db_directory)

    current_path = os.path.dirname(os.path.abspath(__file__))

    sqlite_places_db = 'sqlite:///{}/../../db-test/places.db'.format(current_path)
    logger.debug('Path sqlite videos: {}'.format(sqlite_places_db))

    place_service = PlaceServiceImpl(SQLAlchemyCityStore(sqlite_places_db),
                                     SQLAlchemyPointOfInterestStore(sqlite_places_db))

    city_dto_first = place_service.add_city('primera_good', [])
    city_dto_first = place_service.add_city('primera', [])
    # city_dto = place_service.get_city(city_dto_first.id)
    city_dto_deleted = place_service.delete_city('aae8db78-10b1-4d53-a99d-6fb5936de1b9')
    city_dto_points = place_service.get_city('aae8db78-10b1-4d53-a99d-6fb5936de1b9')
    points_of_interest_dto = place_service.get_points_of_interest_by_city_id(city_dto_points.id)
    city_dto = place_service.update_city(city_dto_points.id, 'segunda')
    point_of_interest_created = place_service.add_point_of_interest('poi6', city_dto_points, 'latitude', 'longitude')
    point_of_interest = place_service.get_all_points_of_interest()
    # city_dto = place_service.delete_city(city_dto_first.id)
    city_dto_points = place_service.get_city('73ce5394-6aa4-451e-8161-c4519f261d47')
    point_of_interest = place_service.update_point_of_interest(point_of_interest_created.id,'nnewname',city_dto_points,'latitude2','longitudenew')
    city_dto_points = place_service.get_city('73ce5394-6aa4-451e-8161-c4519f261d47')
    point_of_interest = place_service.delete_point_of_interest(point_of_interest_created.id)
    print("end")
