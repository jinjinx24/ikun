from django.urls import path, include
from django.shortcuts import redirect
from accounts import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('', lambda request: redirect('accounts/login/', permanent=False)),
    path('home/', views.home, name='home'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
