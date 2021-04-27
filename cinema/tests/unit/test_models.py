from datetime import date, time
from django.test import TestCase
from cinema.models import Hall, Session, BookedSession
from django.db.utils import IntegrityError
from cinema.exceptions import SessionsCollideException, NoFreePlacesException, IncorrectDataException, BookedSessionExistsException
from customuser.models import MyUser


class TestHall(TestCase):
    def setUp(self) -> None:
        self.hall = Hall.objects.create(name="hall", size=10)
        self.hall2 = Hall.objects.create(name="hall2", size=10)
        user = MyUser.objects.create_user(username="darkin", password="123")
        session = Session.objects.create(start_time=time(hour=12, minute=30),
                                         end_time=time(hour=15),
                                         start_date=date(year=2021, month=10, day=1),
                                         end_date=date(year=2021, month=11, day=3),
                                         hall=self.hall,
                                         price=10)
        booked_session = BookedSession.objects.create(user=user, session=session, date=date(2021, 11, 2), places=1)

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            hall = Hall.objects.create(name="hall", size=10)

    def test_incorrect_size(self):
        with self.assertRaises(ValueError):
            hall = Hall.objects.create(name="hall1", size="fdkmsj")

    def test_object_created(self):
        hall = Hall.objects.get(id=1)
        self.assertEqual("hall", hall.name)

    def test_non_modfiable_hall_with_booked_sessions(self):
        with self.assertRaises(BookedSessionExistsException):
            self.hall.save()


class TestSession(TestCase):

    def create_session(self, start_time, end_time, start_date, end_date, hall, price):
        return Session(start_time=start_time,
                       end_time=end_time,
                       start_date=start_date,
                       end_date=end_date,
                       hall=hall,
                       price=price)

    def setUp(self) -> None:
        self.user = MyUser.objects.create_user(username="darkin", password="1")
        self.hall1 = Hall.objects.create(name="hall1", size=10)
        self.hall2 = Hall.objects.create(name="hall2", size=10)
        self.session1 = self.create_session(time(hour=12, minute=30), time(hour=15), date(year=2021, month=10, day=1),
                                            date(year=2021, month=11, day=3), self.hall1, 10)
        self.session2 = self.create_session(time(hour=12, minute=30), time(hour=15), date(year=2021, month=8, day=1),
                                            date(year=2021, month=9, day=3), self.hall2, 10)
        self.midnight_session = self.create_session(time(hour=23, minute=30), time(hour=4), date(year=2021, month=8, day=1),
                                                   date(year=2021, month=9, day=3), self.hall2, 10)
        self.session1.save()
        self.session2.save()
        self.midnight_session.save()

    def test_incorrect_session_update2(self):
        session = Session.objects.get(id=1)
        with self.assertRaises(SessionsCollideException):
            session.start_date = date(year=2021, month=8, day=6)
            session.end_date = date(year=2021, month=9, day=6)
            session.hall = self.hall2
            session.save()

    def test_session_collision(self):
        with self.assertRaises(SessionsCollideException):
            session = self.create_session(time(hour=12, minute=30), time(hour=15), date(year=2021, month=10, day=1),
                                          date(year=2021, month=11, day=3), self.hall1, 10)
            session.save()

    def test_session_collision1(self):
        with self.assertRaises(SessionsCollideException):
            session = self.create_session(time(hour=12, minute=30), time(hour=15), date(year=2021, month=9, day=4),
                                          date(year=2021, month=10, day=1), self.hall1, 10)
            session.save()

    def test_session_collision2(self):
        with self.assertRaises(SessionsCollideException):
            session = self.create_session(time(hour=12, minute=30), time(hour=15), date(year=2021, month=9, day=4),
                                          date(year=2021, month=10, day=10), self.hall1, 10)
            session.save()

    def test_session_collision3(self):
        with self.assertRaises(SessionsCollideException):
            session = self.create_session(time(hour=11, minute=30), time(hour=15), date(year=2021, month=9, day=4),
                                          date(year=2021, month=10, day=10), self.hall1, 10)
            session.save()

    def test_session_collision4(self):
        with self.assertRaises(SessionsCollideException):
            session = self.create_session(time(hour=14, minute=30), time(hour=16), date(year=2021, month=9, day=4),
                                          date(year=2021, month=10, day=10), self.hall1, 10)
            session.save()

    def test_session_collision5(self):
        with self.assertRaises(SessionsCollideException):
            session = self.create_session(time(hour=15), time(hour=18), date(year=2021, month=9, day=4),
                                          date(year=2021, month=10, day=10), self.hall1, 10)
            session.save()

    def test_session_collision7(self):
        with self.assertRaises(SessionsCollideException):
            session = self.create_session(time(hour=11, minute=30), time(hour=16), date(year=2021, month=10, day=1),
                                            date(year=2021, month=11, day=3), self.hall1, 10)
            session.save()

    def test_session_collision6(self):
        with self.assertRaises(SessionsCollideException):
            session = self.create_session(time(hour=15), time(hour=19), date(year=2021, month=11, day=3),
                                          date(year=2021, month=12, day=10), self.hall1, 10)
            session.save()

    def test_session_collision8(self):
        with self.assertRaises(SessionsCollideException):
            session = self.create_session(time(hour=13), time(hour=14), date(year=2021, month=11, day=3),
                                          date(year=2021, month=12, day=10), self.hall1, 10)
            session.save()

    def test_midnight_collision_data(self):
        with self.assertRaises(SessionsCollideException):
            session = self.create_session(time(hour=22, minute=30), time(hour=5), date(year=2021, month=7, day=1),
                                          date(year=2021, month=8, day=3), self.hall2, 10)
            session.save()

    def test_midnight_collision_data1(self):
        with self.assertRaises(SessionsCollideException):
            session = self.create_session(time(hour=23, minute=45), time(hour=1), date(year=2021, month=9, day=3),
                                          date(year=2021, month=9, day=8), self.hall2, 10)
            session.save()

    def test_collision_data1(self):
        with self.assertRaises(SessionsCollideException):
            session = self.create_session(time(hour=23, minute=30), time(hour=23, minute=45),
                                          date(year=2021, month=8, day=1),
                                          date(year=2021, month=9, day=3), self.hall2, 10)
            session.save()

    def test_midnight_collision(self):
        with self.assertRaises(SessionsCollideException):
            session = self.create_session(time(hour=14, minute=30), time(hour=11), date(year=2021, month=10, day=1),
                                          date(year=2021, month=11, day=3), self.hall1, 10)
            session.save()

    def test_correct_data_hall(self):
        session = self.create_session(time(hour=15, minute=30), time(hour=18), date(year=2021, month=10, day=1),
                                      date(year=2021, month=11, day=3), self.hall2, 10)
        session.save()
        self.assertTrue(session.id)

    def test_correct_midnight_data(self):
        session = self.create_session(time(hour=18, minute=30), time(hour=8), date(year=2021, month=10, day=1),
                                      date(year=2021, month=11, day=3), self.hall1, 10)
        session.save()
        self.assertTrue(session.id)

    def test_incorrect_midnight_data(self):
        with self.assertRaises(SessionsCollideException):
            session = self.create_session(time(hour=18, minute=30), time(hour=13), date(year=2021, month=10, day=1),
                                          date(year=2021, month=11, day=3), self.hall1, 10)
            session.save()

    def test_correct_time_data(self):
        session = self.create_session(time(hour=9), time(hour=12, minute=25), date(year=2021, month=10, day=1),
                                      date(year=2021, month=11, day=3), self.hall1, 10)
        session.save()
        self.assertTrue(session.id)

    def test_update_session(self):
        session = Session.objects.get(id=1)
        session.start_date = date(2021, 10, 10)
        session.end_date = date(2021, 11, 9)
        session.save()

    def test_unmodifiable_booked_session(self):
        BookedSession.objects.create(session=self.session1, date=date(2021, 10, 2), user=self.user, places=1)
        with self.assertRaises(BookedSessionExistsException):
            self.session1.save()


class TestBookedSession(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/sessions.json",
                "fixtures/booked_sessions.json"]

    def setUp(self) -> None:
        self.fully_booked_session = Session.objects.get(id=1)
        self.user = MyUser.objects.get(id=1)

    def test_user_wallet_modified(self):
        BookedSession.objects.create(session=self.fully_booked_session,
                                     user=self.user, date=date(2021, 10, 20), places=2)
        self.assertEqual(9980, self.user.wallet)

    def test_fully_booked_session(self):
        with self.assertRaises(NoFreePlacesException):
            booked_session = BookedSession.objects.create(session=self.fully_booked_session,
                                                          user=self.user, date=date(2021, 10, 4), places=1)

    def test_incorrect_date_booked_session(self):
        with self.assertRaises(IncorrectDataException):
            booked_session = BookedSession.objects.create(session=self.fully_booked_session,
                                                          user=self.user, date=date(2021, 9, 4), places=1)

    def test_incorrect_data_booked_session1(self):
        with self.assertRaises(IncorrectDataException):
            booked_session = BookedSession.objects.create(session=self.fully_booked_session,
                                                          user=self.user, date=date(2021, 11, 4), places=1)

    def test_correct_date_booked_session(self):
        booked_session = BookedSession.objects.create(session=self.fully_booked_session,
                                                      user=self.user, date=date(2021, 10, 5), places=1)
        self.assertTrue(booked_session.id)

    def test_fully_booked_session_date(self):
        BookedSession.objects.create(session=self.fully_booked_session,
                                     user=self.user, date=date(2021, 10, 6), places=1)
        BookedSession.objects.create(session=self.fully_booked_session,
                                     user=self.user, date=date(2021, 10, 6), places=2)
        with self.assertRaises(NoFreePlacesException):
            BookedSession.objects.create(session=self.fully_booked_session,
                                         user=self.user, date=date(2021, 10, 6), places=1)

    def test_too_many_places(self):
        with self.assertRaises(NoFreePlacesException):
            BookedSession.objects.create(session=self.fully_booked_session,
                                         user=self.user, date=date(2021, 10, 7), places=4)

    def test_too_many_places2(self):
        BookedSession.objects.create(session=self.fully_booked_session,
                                     user=self.user, date=date(2021, 10, 7), places=3)
        with self.assertRaises(NoFreePlacesException):
            BookedSession.objects.create(session=self.fully_booked_session,
                                         user=self.user, date=date(2021, 10, 7), places=3)

    def test_too_many_places3(self):
        BookedSession.objects.create(session=self.fully_booked_session,
                                     user=self.user, date=date(2021, 10, 7), places=3)
        with self.assertRaises(NoFreePlacesException):
            BookedSession.objects.create(session=self.fully_booked_session,
                                         user=self.user, date=date(2021, 10, 7), places=1)

