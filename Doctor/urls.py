from rest_framework import routers
from .api.viewsets import RegisterDoctorViewSet, DoctorViewSet

doctorpath = routers.DefaultRouter()
doctorpath.register('register', RegisterDoctorViewSet, basename='register')
doctorpath.register('', DoctorViewSet, basename='')

