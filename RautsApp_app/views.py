from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render,redirect
from django.views import View
from django.urls import resolve
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework import viewsets, status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
import json
from django.core.exceptions import *
from rest_framework.response import Response
from .models import *
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
# Create your views here.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name','email','phone','password','role_id')

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        created_by = serializers.IntegerField(write_only=True)
        fields = ('vehicle_name','number_plate','rc_number','vehicle_insurance','manufacture_date','puc','created_by')


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def users(request,*args,**kwargs):
    if request.method == 'GET':
        if (kwargs):
            try:
                uid = User.objects.get(**kwargs).id
                res = UserSerializer(User.objects.filter(id=uid), many=True)
                return Response(res.data)
            except:
                return Response({'Data':'No user found with given id'},status=status.HTTP_204_NO_CONTENT)
        else:
            auth = request.auth
            print(auth)
            res = UserSerializer(User.objects.all(),many=True)
            return Response(res.data)
    if request.method == "POST":
        auth = request.auth
        print(auth)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PUT":
        auth = request.auth
        exceptions = 0
        try:
            user = User.objects.get(**kwargs)
            serializer = UserSerializer(user,data=request.data)
            exceptions = serializer
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(exceptions.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        auth = request.auth
        user = User.objects.get(**kwargs)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def vehicles(request,*args,**kwargs):
    print(request.user)
    print(request.auth)
    if request.method == 'GET':
        if (kwargs):
            try:
                vid = Vehicle.objects.get(**kwargs).id
                res = VehicleSerializer(User.objects.filter(id=vid), many=True)
                return Response(res.data)
            except:
                return Response({'Data':'No Vehicle found with given id'},status=status.HTTP_204_NO_CONTENT)
        else:
            res = VehicleSerializer(User.objects.all(),many=True)
            return Response(res.data)
    if request.method == "POST":
        request.data["created_by"]=request.user
        print(request.data)
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PUT":
        auth = request.auth
        exceptions = 0
        try:
            vehicle = Vehicle.objects.get(**kwargs)
            serializer = VehicleSerializer(Vehicle,data=request.data)
            exceptions = serializer
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(exceptions.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        vehicle = Vehicle.objects.get(**kwargs)
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)