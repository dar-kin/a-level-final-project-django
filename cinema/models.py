from django.db import models
from django.db.models import Q, F, Sum
from django.core.validators import MinValueValidator
from . import exceptions
from customuser.models import MyUser


class Hall(models.Model):
    name = models.CharField(max_length=150, unique=True)
    size = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.id:
            if BookedSession.objects.filter(session__hall=self).exists():
                raise exceptions.BookedSessionExistsException
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Session(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="sessions")
    price = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Session. Time: {self.start_time} - {self.end_time}. Date: {self.start_date} - {self.end_date}"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.id:
            if BookedSession.objects.filter(session=self).exists():
                raise exceptions.BookedSessionExistsException

        # Filter sessions with start date earlier or equal than end date of particular instance
        q1 = Q(start_date__lte=self.end_date)

        # Filter sessions with end date later or equal than start date of particular instance
        q2 = Q(end_date__gte=self.start_date)

        # Filter sessions with particular instance's hall
        q3 = Q(hall=self.hall)
        sessions = Session.objects.filter(q1 & q2 & q3)
        if self.start_time > self.end_time:
            condition = (
                    Q(start_time__gt=F('end_time')) |
                    Q(start_time__lte=self.end_time) |
                    Q(end_time__gte=self.start_time)
            )
        else:
            condition = (
                    Q(start_time__gt=F('end_time'), start_time__lte=self.end_time) |
                    Q(start_time__gt=F('end_time'), end_time__gte=self.start_time) |
                    Q(start_time__lte=self.end_time, end_time__gte=self.start_time)
            )
        sessions = sessions.filter(condition)
        if self.id:
            sessions = sessions.exclude(id=self.id)
        if sessions:
            raise exceptions.SessionsCollideException
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class BookedSession(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="booked_sessions")
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="users")
    date = models.DateField()
    places = models.IntegerField(validators=[MinValueValidator(1)])

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.date < self.session.start_date or self.date > self.session.end_date:
            raise exceptions.IncorrectDataException

        booked_sessions = BookedSession.objects.filter(session=self.session, date=self.date).aggregate(Sum("places"))
        places = booked_sessions["places__sum"]
        if not places:
            places = self.places
        else:
            places += self.places
        if places > self.session.hall.size:
            raise exceptions.NoFreePlacesException
        self.user.wallet -= self.session.price * self.places
        self.user.save()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

