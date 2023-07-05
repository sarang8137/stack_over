from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserSerializers

# Create your views here.
class UserViewSet(viewsets.ViewSet):
    def create(self,request):
        ser=UserSerializers(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"msg":"Created"})
        return Response({"msg":"Failed"})
