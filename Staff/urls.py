from django.urls import path
from . import views
urlpatterns = [
    path('Login/', views.stafflogin, name='stafflogin'),
    path('Staffpage/', views.staffhome, name='Staffpage'),
    path('Staffpage/LogOut/', views.stafflogout),
    path('Staffpage/GetStudent/', views.GetStudent),
    path('Staffpage/StudentMedicineIssue/', views.StudentMedicineissue),
]