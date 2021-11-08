from django.shortcuts import render
from django.shortcuts import render
from . import views
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class HomePageView(View):
    def get(self,request):
        return render (request,'Foodie/index.html')

class Login(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'Foodie/index.html')

class MemberView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'Foodie/member.html')


class ReviewView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'Foodie/index.html')
