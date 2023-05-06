from django.db import transaction
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView, LogoutAllView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from Doctor.models import Doctor
from .serializers import RegisterDoctorSerializer, DoctorSerializer, PartialUpdateDoctorSerializer


class LoginDoctorViewSet(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginDoctorViewSet, self). post(request, format=None)


class LogoutDoctorViewSet(LogoutView):
    permission_classes = [permissions.IsAuthenticated]


class LogoutAllDoctorViewSet(LogoutAllView):
    permission_classes = [permissions.IsAuthenticated]


class RegisterDoctorViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterDoctorSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        doctor = RegisterDoctorSerializer(data=request.data)
        if doctor.is_valid():
            doctor.save()
            response_data = {
                'message': 'User created!'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'message': 'User dont created!',
                'errors': doctor.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class DoctorViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        crm = request.POST['crm']
        user = Doctor.objects.filter(crm=crm).first()
        if user is None:
            response_data = {
                'message': 'User dont find!'
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        response_data = {
            'message': f'name: {user.name} '
                       f'email: {user.email} '
                       f'crm: {user.crm}'
        }
        return Response(response_data, status=status.HTTP_200_OK)


class PartialUpdateDoctorViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PartialUpdateDoctorSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()
        return User.objects.filter(pk=self.request.user.pk)

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        update = self.get_object()
        doctor = self.get_serializer(update, data=request.data, partial=partial)
        doctor.is_valid(raise_exception=True)
        self.perform_update(doctor)
        return Response(doctor.data)
