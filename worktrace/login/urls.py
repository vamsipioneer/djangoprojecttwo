from django.urls import path, re_path
from . import views

app_name = 'login'

urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('authenticate/', views.authenticateUser, name='validateuser'),
    path('etoolsdata/', views.jiradata, name='check'),
    path('jenkinsdata/', views.jenkinsdata, name='check'),
    path('logout/', views.logoutView, name='logout'),
    path('jira/', views.jiraView, name='jira'),
    path('jenkisjobs/', views.jiraView, name='jira'),
    #path('pagination/', views.check, name='paginate'),

]


