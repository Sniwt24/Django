from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (get_cookie_view,
                    set_cookie_view,
                    get_session_view,
                    set_session_view,
                    MyLogoutView,
                    MyProfileView,
                    RegisterView,
                    AccountsListView,
                    UpdateUserProfileView,
                    UserDetailsView,
                    UpdateAvatarView,
                    )

app_name = "myauth"
urlpatterns = [
    path("login/",
         LoginView.as_view(
             template_name="myauth/login.html",
             redirect_authenticated_user=True,
         ),
         name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),

    path("", AccountsListView.as_view(), name="accounts_list"),
    path("my_profile/", MyProfileView.as_view(), name="profile"),
    path("my_profile/details/<int:pk>/", UserDetailsView.as_view(), name="details_profile"),
    path("my_profile/update/<int:pk>/", UpdateUserProfileView.as_view(), name="update_profile"),
    path("my_profile/update_avatar/<int:pk>/", UpdateAvatarView.as_view(), name="update_avatar"),
    path("cookie/get/", get_cookie_view, name="get_cookie"),
    path("cookie/set/", set_cookie_view, name="set_cookie"),
    path("session/get/", get_session_view, name="get_session"),
    path("session/set/", set_session_view, name="set_session"),
]
