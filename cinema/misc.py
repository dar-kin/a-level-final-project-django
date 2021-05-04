from django.contrib.auth.mixins import AccessMixin
from datetime import datetime, date, time
from django.db.models import ObjectDoesNotExist
from customuser.models import MyUser
from cinema.models import Session, Hall


class SuperUserRequired(AccessMixin):
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class DateConverter:
    regex = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
    format = '%Y-%m-%d'

    def to_python(self, value: str) -> date:
        return datetime.strptime(value, self.format).date()

    def to_url(self, value: date) -> str:
        return value.strftime(self.format)


class SessionConverter:
    regex = r'[0-9]+'

    def to_python(self, value: str) -> Session:
        try:
            return Session.objects.get(id=value)
        except ObjectDoesNotExist:
            raise ValueError('Session does not exists')

    def to_url(self, value: Session) -> str:
        return str(value.id)


class TimeConverter:
    regex = r'[0-9]{2}:[0-9]{2}'
    format = '%H:%M'

    def to_python(self, value: str) -> time:
        return datetime.strptime(value, self.format).time()

    def to_url(self, value: time) -> str:
        return value.strftime(self.format)


class HallConverter:
    regex = r'[0-9]+'

    def to_python(self, value: str) -> Hall:
        try:
            return Hall.objects.get(id=value)
        except ObjectDoesNotExist:
            raise ValueError('Hall does not exists')

    def to_url(self, value: Hall) -> str:
        return str(value.id)
