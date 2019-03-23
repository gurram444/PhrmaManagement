from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('Login/', views.studentlogin, name='studentlogin'),
    path('Register/', views.studentregister),
    path('LoggedIn/', views.StudentLoggedIn, name='LoggedIn'),
    path('LogOut/', views.StudentLogOut, name='LogOut')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)