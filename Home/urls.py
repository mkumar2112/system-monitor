from django.urls import path
from .views import *

urlpatterns = [
    path("api/upload_system_data/", upload_system_data),
]
urlpatterns += [
    path("api/computers/", ComputerListView.as_view(), name="computer-list"),
]


urlpatterns +=[
    path('dashboard', Home.dashboard, name='dashboard')
]