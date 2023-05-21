from django.urls import path
from django.contrib.auth.views import logout_then_login

from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    
    # HOME PAGES
    path('manager/',views.home_manager,name='home_manager'),
    path('admin/',views.home_admin,name='home_admin'),
    path('adviser/',views.home_adviser,name='home_adviser'),
    path('operator/',views.home_operator,name='home_operator'),

    # FUNCIONALITIES
    path('reports/',views.reports,name='reports'),
    path('block_schedule/',views.block_schedule,name='block_schedule'),
    path('create_user/',views.create_user,name='create_user'),
    path('delete_user/',views.delete_user,name='delete_user'),
    path('see_schedules/',views.see_schedules,name='see_schedules'),
    path('asign_turns/',views.asign_turns,name='asign_turns'),
    path('time_turns/',views.time_turns,name='time_turns'),
    path('select_turns/',views.select_turns,name='select_turns'),
    path('confirm_turns/',views.confirm_turns,name='confirm_turns'),
    path('modify_schedules/',views.modify_schedules,name='modify_schedules'),
    path('modify_turn/',views.modify_turn,name='modify_turn'),
    path('confirm_modify/',views.confirm_modify,name='confirm_modify'),
    path('delete_service/',views.delete_service,name='delete_service'),
    path('validate_service_provided/',views.validate_service_provided,name='validate_service_provided'),
    path('excel/', views.createReport, name='excel'),
    path('logout/', logout_then_login, name='logout'),
    path('preview/', views.preview, name='preview'),

]