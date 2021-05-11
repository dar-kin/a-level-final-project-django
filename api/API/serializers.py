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
        fields = ["id", "username", "password", "password2", "wallet"]


class SessionSerializer(serializers.ModelSerializer):
    free_places = serializers.IntegerField(validators=[MinValueValidator(0)], required=False, read_only=True)
    id = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        start_date = data.get("start_date", None) or self.instance.start_date
        end_date = data.get("end_date", None) or self.instance.end_date
        start_time = data.get("start_time", None) or self.instance.start_time
        end_time = data.get("end_time", None) or self.instance.end_time
        cond1 = start_date > end_date
        cond2 = start_date == end_date
        cond3 = start_time >= end_time
        cond4 = end_date < now().date()
        if cond1 or cond2 and cond3 or cond4:
            raise serializers.ValidationError("Incorrect date")

        return data

    class Meta:
        fields = ["id", "start_date", "end_date", "start_time", "end_time", "hall", "price", "free_places"]
        model = Session


class BookedSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookedSession
        fields = ["places"]


class UserInfoBookedSessionsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["date", "session", "places"]
        model = BookedSession
