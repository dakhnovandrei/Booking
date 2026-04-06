from models import Booking


class BookingsRepo:
    model = Booking

    def __init__(self, session):
        self.session = session



