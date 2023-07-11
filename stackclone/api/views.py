from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserSerializers,QuestionSer,AnswerSer
from .models import *
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework import serializers


# Create your views here.
class UserViewSet(viewsets.ViewSet):
    def create(self,request):
        ser=UserSerializers(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"msg":"Created"})
        return Response({"msg":"Failed"})

class QuestionView(viewsets.ModelViewSet):
    serializer_class=QuestionSer
    queryset=Question.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        ser=QuestionSer(data=request.data)
        if ser.is_valid():
            ser.save(user=request.user)
            return Response(data=ser.data)
        return Response(data=ser.errors)
    # def get_queryset(self):
    #     return Question.objects.all().exclude(user=self.request.user)
    
#localhost:/8000/question/2/add_answer/
    @action(methods=["POST"],detail=True)
    def add_answer(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        quest=Question.objects.get(id=id)
        user=request.user
        ser=AnswerSer(data=request.data)
        if ser.is_valid():
            ser.save(user=user,question=quest)
            return Response(data=ser.data)
        return Response(data=ser.errors)
        

class AnswerView(viewsets.ModelViewSet):
    serializer_class=AnswerSer
    queryset=Answer.objects.all()
    #authentication_classes=[authentication.TokenAuthentication]
    authentication_classes=[]
    permission_classes=[permissions.IsAuthenticated]
    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("method not allowed")
    def list(self, request, *args, **kwargs):
        return serializers.ValidationError("method not allowed")
    def destroy(self, request, *args, **kwargs):
        object=self.get_object()
        if request.user == object.user:
            object.delete()
            return Response(data="Deleted")
        else:
            raise serializers.ValidationError("perimission denied for this user")
        
#localhost:8000/answer/1/add_upvote
    @action(methods=["POST"],detail=True)
    def add_upvote(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        ans=Answer.objects.get(id=id)
        ans.upvote.add(request.user)
        return Response(data="Upvoted")