from utils.null_object import Null


class Rating:
    NULL = Null()

    def __init__(self, rating_id, associated_id, associated_type, user_id, rating_type, date, value):
        self.rating_id = rating_id
        self.associated_id = associated_id
        self.associated_type = associated_type
        self.user_id = user_id
        self.rating_type = rating_type
        self.date = date
        self.value = value
