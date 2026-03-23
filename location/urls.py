from django.urls import include,path
from location import views

urlpatterns = [
    path("location/",views.location, name="location"),
    path('location/',include('area.urls'))
]
