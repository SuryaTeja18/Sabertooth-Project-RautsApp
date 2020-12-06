from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render,redirect
from django.views import View
from django.urls import resolve
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
import json
from django.utils.html import escape
from django.core.exceptions import *
from rest_framework.response import Response
from .models import *
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User as DjangoUser
# Create your views here.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        user = serializers.IntegerField(write_only=True)
        fields = ('phone','role_id','user')

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        created_by = serializers.IntegerField(write_only=True)
        fields = ('vehicle_name','number_plate','rc_number','vehicle_insurance','manufacture_date','puc','created_by')

class VehicleDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleDocument
        vehicle_id = serializers.IntegerField(write_only=True)
        fields = ('vehicle_id','document','path')

class User_DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Detail
        user_id = serializers.IntegerField(write_only=True)
        fields = ('user_id','adhaar_card_number','license','name')

class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        user_id = serializers.IntegerField(write_only=True)
        fields = ('user_id','organization_name','address')

class DistributorInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributorInsurance
        distributor_id = serializers.IntegerField(write_only=True)
        fields = ('distributor_id','insurance_master_id','expiry_date')

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def users(request,*args,**kwargs):
    if request.method == 'GET':
        if (kwargs):
            try:
                cu = CustomUser.objects.get(**kwargs)
                res = UserSerializer(CustomUser.objects.filter(id=cu.id), many=True)
                result = [DjangoUser.objects.filter(id=cu.user.id).values('username','email').first()]
                return Response({**result[0],**res.data[0]})
            except:
                return Response({'Data':'No user found with given id'},status=status.HTTP_204_NO_CONTENT)
        else:
            res = UserSerializer(CustomUser.objects.all(),many=True)
            objects = CustomUser.objects.prefetch_related('user').all()
            result = []
            print(len(res.data))
            for i in range(len(res.data)):
                r = {**DjangoUser.objects.filter(id = objects[i].user.id).values('username','email').first(),**res.data[i]}
                result.append(r)
            return Response(result)
    if request.method == "POST":
        d = {'username' : request.data['username'],'password': request.data['password'], 'email':request.data['email'],'role_id':request.data['role_id']}
        user = DjangoUser.objects.create_user(username = d['username'], email=d['email'], password=d['password'])
        request.data.pop('username')
        request.data.pop('password')
        request.data.pop('email')
        request.data['user'] = user.id
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(d, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PUT":
        exceptions = 0
        try:
            user = CustomUser.objects.get(**kwargs)
            serializer = UserSerializer(user,data=request.data)
            exceptions = serializer
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(exceptions.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        user = CustomUser.objects.get(**kwargs)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def vehicles(request,*args,**kwargs):
    if request.method == 'GET':
        if (kwargs):
            try:
                vid = Vehicle.objects.get(**kwargs).id
                res = VehicleSerializer(Vehicle.objects.filter(id=vid), many=True)
                return Response(res.data)
            except:
                return Response({'Data':'No Vehicle found with given id'},status=status.HTTP_204_NO_CONTENT)
        else:
            res = VehicleSerializer(Vehicle.objects.all(),many=True)
            return Response(res.data)
    if request.method == "POST":
        ins = DjangoUser.objects.filter(id=request.user.id)
        print(ins[0].id)
        request.data["created_by"]=ins[0].id
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

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def vehicleDocument(request,*args,**kwargs):
    print(request.auth, request.user)
    if request.method == 'GET':
        if (kwargs):
            try:
                vdid = VehicleDocument.objects.get(**kwargs).id
                res = VehicleDocumentSerializer(VehicleDocument.objects.filter(id=vdid), many=True)
                return Response(res.data)
            except:
                return Response({'Data':'No vehicle documents found'},status=status.HTTP_204_NO_CONTENT)
        else:
            res = VehicleDocumentSerializer(VehicleDocument.objects.all(),many=True)
            return Response(res.data)
    if request.method == "POST":
        serializer = VehicleDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PUT":
        exceptions = 0
        try:
            vehicleDoc = VehicleDocument.objects.get(**kwargs)
            serializer = VehicleDocumentSerializer(vehicleDoc,data=request.data)
            exceptions = serializer
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(exceptions.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        vehicleDoc = VehicleDocument.objects.get(**kwargs)
        vehicleDoc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def userDetails(request,*args,**kwargs):
    print(request.auth, request.user)
    if request.method == 'GET':
        if (kwargs):
            try:
                udid = User_Detail.objects.get(**kwargs).id
                res = User_DetailSerializer(User_Detail.objects.filter(id=udid), many=True)
                return Response(res.data)
            except:
                return Response({'Data':'No User details found'},status=status.HTTP_204_NO_CONTENT)
        else:
            res = User_DetailSerializer(User_Detail.objects.all(),many=True)
            return Response(res.data)
    if request.method == "POST":
        serializer = User_DetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PUT":
        exceptions = 0
        try:
            ud = User_Detail.objects.get(**kwargs)
            serializer = User_DetailSerializer(ud,data=request.data)
            exceptions = serializer
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(exceptions.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        ud = User_Detail.objects.get(**kwargs)
        ud.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def distributor(request,*args,**kwargs):
    print(request.auth, request.user)
    if request.method == 'GET':
        if (kwargs):
            try:
                dis = Distributor.objects.get(**kwargs).id
                res = DistributorSerializer(Distributor.objects.filter(id=dis), many=True)
                return Response(res.data)
            except:
                return Response({'Data':'No Distributors present'},status=status.HTTP_204_NO_CONTENT)
        else:
            res = DistributorSerializer(Distributor.objects.all(),many=True)
            return Response(res.data)
    if request.method == "POST":
        serializer = DistributorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PUT":
        exceptions = 0
        try:
            dis = Distributor.objects.get(**kwargs)
            serializer = DistributorSerializer(dis,data=request.data)
            exceptions = serializer
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(exceptions.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        dis = Distributor.objects.get(**kwargs)
        dis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def distributorInsurance(request,*args,**kwargs):
    print(request.auth, request.user)
    if request.method == 'GET':
        if (kwargs):
            try:
                di = DistributorInsurance.objects.get(**kwargs).id
                res = DistributorInsuranceSerializer(DistributorInsurance.objects.filter(id=di), many=True)
                return Response(res.data)
            except:
                return Response({'Data':'No Distributor Insurances found'},status=status.HTTP_204_NO_CONTENT)
        else:
            res = DistributorInsuranceSerializer(DistributorInsurance.objects.all(),many=True)
            return Response(res.data)
    if request.method == "POST":
        serializer = DistributorInsuranceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PUT":
        exceptions = 0
        try:
            di = DistributorInsurance.objects.get(**kwargs)
            serializer = DistributorInsuranceSerializer(di,data=request.data)
            exceptions = serializer
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(exceptions.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        di = DistributorInsurance.objects.get(**kwargs)
        di.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
