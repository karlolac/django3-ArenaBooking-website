from django.urls import path
from . import views

app_name='bookings'

urlpatterns = [
    path('', views.bookings,name='bookings'),
    path('court/<int:court_id>/book/',views.bookcourt, name="bookcourt"),
    path('approve/', views.approve_bookings, name='approve_bookings'),
    path('approve/<int:booking_id>/<str:new_status>/', views.update_booking_status, name='update_booking_status'),
]