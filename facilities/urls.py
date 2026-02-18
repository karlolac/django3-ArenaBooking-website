from django.urls import path
from . import views

app_name = 'facilities'

urlpatterns = [
    path('',views.facilities,name='facilities'),
    path('<int:facility_id>/',views.facilitydetail,name='facility_detail'),
]
