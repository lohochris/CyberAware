from django.contrib import admin
from django.urls import path, include
from core.views import home, act, about, privacy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('learn/', include('education.urls')),
    path('assess/', include('assessment.urls')),
    path('act/', act, name='act'),
    path('support/', include('support.urls')),
    path('about/', about, name='about'),
    path('privacy/', privacy, name='privacy'),
    

]
