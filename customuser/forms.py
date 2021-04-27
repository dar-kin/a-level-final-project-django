from django.contrib.auth.forms import UserCreationForm
from .models import MyUser


class MyUserCreationForm(UserCreationForm):
    class Meta:
        fields = ("username", "password1", "password2")
        model = MyUser
