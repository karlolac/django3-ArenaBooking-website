from django.urls import path
from . import views

app_name='bookings'

urlpatterns = [
    path('', views.bookings,name='bookings'),
    path('court/<int:court_id>/book/',views.bookcourt, name="book_court"),
]