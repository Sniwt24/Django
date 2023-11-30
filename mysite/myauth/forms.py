from django.contrib.auth.models import User
from django.forms import ModelForm

from myauth.models import Profile


class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = "username", "first_name", "last_name", "email"


class UpdateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = "bio", "agreement_accept", "avatar"
