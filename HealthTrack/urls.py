from django.contrib import admin
from Doctor.api.viewsets import LoginDoctorViewSet, LogoutDoctorViewSet, LogoutAllDoctorViewSet
from django.urls import path, include
from Doctor.urls import doctorpath


urlpatterns = [
    path('login/', LoginDoctorViewSet.as_view(), name='login'),
    path('logout/', LogoutDoctorViewSet.as_view(), name='logout'),
    path('all_logout/', LogoutAllDoctorViewSet.as_view(), name='all_logout'),
    path('admin/', admin.site.urls),
    path('doctor/', include(doctorpath.urls)),
]