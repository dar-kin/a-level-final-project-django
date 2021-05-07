from rest_framework import serializers
from django.core.validators import MinValueValidator
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
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords mismatch")
        return data

    def create(self, validated_data):
        return MyUser.objects.create_user(username=validated_data["username"], password=validated_data["password"])

    class Meta:
        model = MyUser
        fields = ["id", "username", "password", "password2"]


class SessionSerializer(serializers.ModelSerializer):
    free_places = serializers.IntegerField(validators=[MinValueValidator(0)], required=False, read_only=True)

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
        fields = ["start_date", "end_date", "start_time", "end_time", "hall", "price", "free_places"]
        model = Session


class BookedSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookedSession
        fields = ["places"]


class UserInfoBookedSessionsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["date", "session", "places"]
        model = BookedSession
