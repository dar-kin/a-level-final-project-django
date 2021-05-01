from rest_framework import viewsets, mixins
from cinema.models import Hall, Session, BookedSession
from rest_framework.response import Response
from api.API.serializers import HallSerializer, SessionSerializer
from api.misc import IsAdmin
from cinema import exceptions


class HallViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):

    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [IsAdmin]

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
