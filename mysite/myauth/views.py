from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DetailView, TemplateView, CreateView, ListView, UpdateView

from .forms import UpdateUserForm, UpdateProfileForm
from .models import Profile
from shopapp.models import Product
# from django.contrib.auth import authenticate, login, logout

# Create your views here.


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]

        user = authenticate(self.request, username=username, password=password)
        login(request=self.request, user=user)

        profile = Profile()
        profile.user = user
        profile.save()

        return response


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("shopapp:index_def")


class MyProfileView(UserPassesTestMixin, TemplateView):
    def test_func(self):
        if Profile.objects.filter(pk=self.request.user.pk):
            pass
        else:
            profile = Profile()
            profile.user = self.request.user
            profile.save()
        return True

    template_name = "myauth/my_profile.html"


class AccountsListView(ListView):
    template_name = "myauth/accounts_list.html"
    queryset = (User.objects.all())


class UserDetailsView(UserPassesTestMixin, DetailView):
    def test_func(self):
        if Profile.objects.filter(pk=self.kwargs["pk"]):
            pass
        else:
            profile = Profile()
            profile.user = User.objects.get(pk=self.kwargs["pk"])
            profile.save()
        return True

    model = User
    template_name = "myauth/user_details.html"


class UpdateAvatarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        # self.object = self.get_object()
        return ((self.kwargs["pk"] == self.request.user.pk)
                or (self.request.user.is_staff))

    model = Profile
    fields = "avatar",
    success_url = reverse_lazy("myauth:accounts_list")
    template_name = "myauth/avatar_update.html"


class UpdateUserProfileView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # self.object = self.get_object()
        return ((self.kwargs["pk"] == self.request.user.pk)
                or (self.request.user.is_staff))

    template_name = "myauth/user_update.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        pk = kwargs["pk"]

        if not Profile.objects.filter(user=User.objects.get(pk=pk)).exists():
            Profile.objects.create(user=User.objects.get(pk=pk))

        form_user = UpdateUserForm(instance=User.objects.get(pk=pk))

        form_profile = UpdateProfileForm(instance=Profile.objects.get(user_id=pk))
        context = {
            "form_user": form_user,
            "form_profile": form_profile,
        }

        return render(request, 'myauth/user_update.html', context=context)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        pk = kwargs["pk"]
        form_user = UpdateUserForm(request.POST, instance=User.objects.get(pk=pk))
        form_profile = UpdateProfileForm(request.POST, request.FILES, instance=Profile.objects.get(user_id=pk))
        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()
            form_profile.save()
        url = reverse("myauth:accounts_list")
        return redirect(url)


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("Ck", "Set", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("Ck", "Not set")
    return HttpResponse(f"Cookie value: {value!r}")


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["session_var"] = "Var was set"
    return HttpResponse("Session var set")


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("session_var", "Session var was not set")
    return HttpResponse(f"Session var value: {value!r}")
