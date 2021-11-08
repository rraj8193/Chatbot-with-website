from django.urls import path

from . import views

app_name = 'Foodie'
urlpatterns = [
    path('',views.HomePageView.as_view(),name='home'),
    path('protect',views.Login.as_view(),name = 'protect'),
    path('member',views.MemberView.as_view(),name='member'),
    path('review',views.ReviewView.as_view(),name='review'),
]
