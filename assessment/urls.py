from django.urls import path
from . import views

urlpatterns = [
    path('', views.assess, name='assess'),
    path('is-this-abuse/', views.decision_tool, name='decision_tool'),
    path('scenario/', views.scenario_simulator, name='scenario_simulator'),
    path('pathway/', views.action_pathway, name='action_pathway'),
     path('bystander/', views.bystander_tool, name='bystander_tool'),
]
