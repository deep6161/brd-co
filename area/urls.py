from django.urls import path
from area import views

urlpatterns = [
    
    path("area/",views.yourarea, name="area"),
    
]
