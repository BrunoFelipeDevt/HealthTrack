from django.db import transaction
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from django.contrib.auth.models import User
from Doctor.models import Doctor


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name', 'cpf', 'rg', 'email', 'crm', 'birth_date']
        extra_kwargs = {
            'cpf': {'write_only': True},
            'rg': {'write_only': True},
            'birth_date': {'write_only': True},
        }


class RegisterDoctorSerializer(ModelSerializer):
    doctor = DoctorSerializer(many=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'doctor']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    @transaction.atomic()
    def create(self, validated_data):
        doctor_data = validated_data.pop('doctor')
        password = validated_data.pop('password')
        validated_data['password'] = make_password(''.join(password))
        user = User.objects.create(**validated_data)
        Doctor.objects.create(user=user, **doctor_data)
        return user


class GetDoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name', 'email', 'crm']


class PartialUpdateDoctorSerializer(ModelSerializer):
    doctor = DoctorSerializer(many=False)

    class Meta:
        model = User
        fields = ['username', 'doctor']
