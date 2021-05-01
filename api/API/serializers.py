from rest_framework import serializers
from django.utils.timezone import now
from cinema.models import Hall, Session, BookedSession
from customuser.models import MyUser


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ["name", "size"]


class MyUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ["id", "username", "password"]


class SessionSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        start_date = data['start_date']
        end_date = data['end_date']
        start_time = data['start_time']
        end_time = data['end_time']
        if (start_date > end_date) or ((start_date == end_date) and (start_time >= end_time)) \
                or end_date < now().date():
            raise serializers.ValidationError("Incorrect date")

        return data

    class Meta:
        fields = ["start_date", "end_date", "start_time", "end_time", "hall", "price"]
        model = Session
