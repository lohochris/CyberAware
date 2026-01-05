from django.urls import path
from .views import learn

urlpatterns = [
    path('', learn, name='learn'),
]
