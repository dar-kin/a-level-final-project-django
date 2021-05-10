from datetime import date
from rest_framework import viewsets, mixins
from cinema.models import Hall, Session, BookedSession
from customuser.models import MyUser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from api.API.serializers import HallSerializer, SessionSerializer, MyUserSerializer, \
    BookedSessionSerializer, UserInfoBookedSessionsSerializer
from api.misc import IsAdmin
from cinema import exceptions
from api.misc import ExpiringTokenAuthentication


class HallViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):

    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [IsAdmin]
    authentication_classes = [ExpiringTokenAuthentication]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data["success_message"] = "Hall was created"
        return response

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            response.data["success_message"] = "Hall was updated"
            return response
        except exceptions.BookedSessionExistsException:
            return Response(data={"fail_message": "Booked sessions for this hall exist"}, status=400)


class SessionViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):

    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAdmin]
    authentication_classes = [ExpiringTokenAuthentication]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            response.data["success_message"] = "Session was created"
            return response
        except exceptions.SessionsCollideException:
            return Response(data={"fail_message": "Session collides with another one"}, status=400)

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            response.data["success_message"] = "Session was updated"
            return response
        except exceptions.BookedSessionExistsException:
            return Response(data={"fail_message": "Booked sessions for this session exist"}, status=400)
        except exceptions.SessionsCollideException:
            return Response(data={"fail_message": "Session collides with another one"}, status=400)


class ClientSessionView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        url_date = self.kwargs["date"]
        booked_sessions = BookedSession.objects.filter(date=url_date).values("session")
        booked_sessions = queryset.filter(pk__in=booked_sessions). \
            annotate(free_places=F("hall__size") - Coalesce(Sum(F("booked_sessions__places")), 0))
        # print(booked_sessions.values())
        queryset = queryset.filter(start_date__lte=url_date, end_date__gte=url_date).exclude(pk__in=booked_sessions).\
            annotate(free_places=F("hall__size"))
        # print(queryset.values())
        queryset = booked_sessions.union(queryset)
        # print(queryset.values())
        sort_options = ["start_time", "price"]
        sort = self.kwargs.get("sort", None)
        if sort in sort_options:
            queryset = queryset.order_by(sort)
        return queryset

    @action(methods=["get"], detail=False)
    def get_sessions_in_time(self, request, *args, **kwargs):
        hall = self.kwargs.get("hall", None)
        start_range = self.kwargs.get("start_range", None)
        end_range = self.kwargs.get("end_range", None)
        queryset = Session.objects.filter(start_date__lte=date.today(), end_date__gte=date.today())
        if hall:
            queryset = queryset.filter(hall=hall)
        if start_range and end_range:
            queryset = queryset.filter(start_time__gte=start_range, start_time__lte=end_range)
        data = SessionSerializer(queryset, many=True).data
        return Response(data=data, status=200)


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data["success_message"] = "User was registered"
        return response


class BookedSessionViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = BookedSession.objects.all()
    serializer_class = BookedSessionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, session=self.kwargs["s"], date=self.kwargs["date"])

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            response.data["success_message"] = "Session was booked"
            return response
        except exceptions.NoFreePlacesException:
            return Response(status=400, data={"fail_message": "Not enough free places"})
        except exceptions.IncorrectDataException:
            return Response(status=400, data={"fail_message": "Incorrect data"})
        except exceptions.DateExpiredException:
            return Response(status=400, data={"fail_message": "Date expired"})


class BookedSessionListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = BookedSession.objects.all()
    serializer_class = UserInfoBookedSessionsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        self.total_spent = queryset.aggregate(total=Sum(F("session__price") * F("places")))["total"]
        if not self.total_spent:
            self.total_spent = 0
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data["results"].append({"total_spent": self.total_spent})
        return response

