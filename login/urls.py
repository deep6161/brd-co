from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("index1/", views.index1, name="index1"),
    path("sale/", views.sale, name="sale"),
    path("buy/", views.buy, name="buy"),
    path("profile/", views.profile_view, name="profile"),
    path("edit-profile/", views.edit_profile_view, name="edit_profile"),
    path("property/<int:property_id>/", views.property_detail_view, name="property_detail"),
    path("image/<int:image_id>/", views.serve_property_image, name="property_image"),
    path("property/<int:property_id>/delete/", views.delete_property, name="delete_property"),
]
