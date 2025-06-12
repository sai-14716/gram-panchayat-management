from django.urls import path,include
from django.contrib import admin
from django.shortcuts import redirect

from . import views
app_name = "login"

urlpatterns = [
    path("", views.index, name="index"),
    path("display", views.display_page, name="display_page"),
    path("auth/<str:data>",views.auth,name="authenticate"),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('<str:citizen>/dashboard/', views.citizen_dashboard, name='citizen_dashboard'),
    path('employee/update/assets/', views.update_assets, name='update_assets'),
    path('employee/update/citizens/', views.update_citizens, name='update_citizens'),
    path('employee/update/cultivation/', views.update_cultivation, name='update_cultivation'),
    path('employee/update/welfare/', views.update_welfare, name='update_welfare'),
    path('employee/update/vaccination/', views.update_vaccination, name='update_vaccination'),
    path('service_request/',views.service_request, name='service_request'),
    path('admin/', admin.site.urls),
    path('update_service_request', views.update_service_request, name='update_service_request'),
    path('gov_citizens', views.gov_citizens, name='gov_citizens'),
    path('gov_assets', views.gov_assets, name='gov_assets'),

]