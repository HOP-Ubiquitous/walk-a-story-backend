from utils.null_object import Null


class City:
    NULL = Null()

    def __init__(self, id, name, points_of_interest):
        self.id = id
        self.name = name
        self.points_of_interest = points_of_interest
