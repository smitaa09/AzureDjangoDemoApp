"""SampleProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.conf.urls import include,url
from MyApp import views

urlpatterns = [
    path('login', views.home),
    path('main', views.home),
    path('ticket-insights', views.home),
    path('api/aion/user-authenticate', views.login),
    path('api/aion/customerDetails', views.customer_details),
    path('api/aion/customerSentimentDetails', views.get_sentiment_details),
    path('api/aion/ci-names', views.get_ci_names),
    path('api/aion/ticketInsights', views.sentiment_details),
    path('api/aion/supportengineer', views.get_selected_support_focal_details),
    path('api/aion/recommendation-feedback', views.save_feedback),
    path('api/aion/aion-user-feedback', views.save_aion_feedback),
    path('api/aion/aion-suggestions', views.save_suggestions),
    path('api/aion/aion-content', views.save_content),
    path('api/aion/aion-training', views.save_training),    
    path('api/aion/user-logout', views.logout),
    path('api/aion/user-log_feedback', views.log_feedback),
    path('api/aion/user-register', views.register),    
    path('api/aion/user-customerdetails', views.get_customer_six_month_details),
    path('api/aion/user-supportfocaldetails', views.get_supportfocal_six_month_details),
	
    
]


