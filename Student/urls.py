from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from . import views

urlpatterns = [
    path('Login/', views.studentlogin, name='studentlogin'),
    path('Register/', views.studentregister),
    path('StudentProfile/', views.StudentLoggedIn, name='LoggedIn'),
    path('UpdateProfile/', views.UpdateProfile ),
    path('Transactions/', views.Transactions),
    url(r'^Transactions/ViewDetails/(?P<OPNumber>[A-Z0-9]+)$', views.TransactionDetails),
    path('Logout/', views.StudentLogOut, name='LogOut')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)