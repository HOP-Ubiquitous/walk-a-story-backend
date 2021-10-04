from utils.null_object import Null


class Caminata:
    NULL = Null()

    def __init__(self, caminata_id, title, description, date, image, place_id, address, latitude, longitude, user_id,
                 participants):
        self.caminata_id = caminata_id
        self.title = title
        self.description = description
        self.date = date
        self.image = image
        self.place_id = place_id
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.user_id = user_id
        self.participants = participants
