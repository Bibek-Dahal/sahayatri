from django.urls import path
from . import views
app_name = 'user'
urlpatterns = [
    path('pay-fare/<uuid:vehicle_id>',views.CalculateAndPayFare.as_view())
]