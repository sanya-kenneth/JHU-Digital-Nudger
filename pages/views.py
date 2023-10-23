from django.shortcuts import redirect, render
from django.contrib import messages
from rest_framework.response import Response

from pages.forms import TraineeAdminForm, TraineeSignupForm
from pages.serializers import InfoBipContentRequestSerializer, InfoBipContentSerializer
from .models import Content, Trainer
from rest_framework.views import APIView
from rest_framework import status

def home(request):
    return render(request, "pages/home.html", {})

def login(request):
    return render(request, "pages/login.html", {})

def signup(request):
    if request.method == 'GET':
        form = TraineeSignupForm()
        return render(request, "pages/signup.html", {'form': form})
    
    if request.method == 'POST':
        form = TraineeSignupForm(request.POST) 
        if form.is_valid():
            trainee = form.save()
            messages.success(request, 'You have singed up successfully.')
            return redirect('home')
        else:
            return render(request, 'pages/signup.html', {'form': form})



class InfobipContent(APIView):
    
    def get(self, request, bot, screen,*args, **kwargs):
        content = Content.objects.filter(title=screen, bot__name=bot).first()
        serializer = InfoBipContentSerializer(content)
        if content:
            return Response(serializer.data)
        else:
            return Response({}, 404)
        
    def post(self, request, *args, **kwargs):

        serializer = InfoBipContentRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        content_title = request.data.get('title')
        bot = request.data.get('bot_code')
        
        content = Content.objects.filter(title=content_title, bot__bot_code=bot).first()
        
        response_serializer = InfoBipContentSerializer(content)

        if content:
            return Response(response_serializer.data)
        else:
            return Response({}, 404)
