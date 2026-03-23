from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),              # /login/
    path("logout/", views.logout_view, name="logout"),    # /login/logout/
    path("register/", views.register_view, name="register"),# /login/register/
    path("index1/", views.index1, name="index1"),          # /login/index1/
    path("sale/", views.sale, name="sale"),                # /login/sale/
    path("buy/", views.buy, name="buy"),                   # /login/buy/
    path("profile/", views.profile_view, name="profile"),  # /login/profile/
    path("edit-profile/", views.edit_profile_view, name="edit_profile"),  # /login/edit-profile/
    path("property/<int:property_id>/", views.property_detail_view, name="property_detail"),  # /login/property/1/
]
