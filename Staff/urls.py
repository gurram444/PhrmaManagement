from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('Login/', views.stafflogin, name='stafflogin'),
    path('Staffpage/', views.staffhome, name='Staffpage'),
    path('Staffpage/LogOut/', views.stafflogout),
    path('Staffpage/GetStudent/', views.GetStudent),
    path('Staffpage/ops/',views.issueop),
    url(r'^Staffpage/ops/StudentMedicineIssue/(?P<op_number>[A-Z0-9]+)$', views.StudentMedicineissue),
    url(r'^Staffpage/GetStudent/GenerateOP/(?P<Admission_number>\d+)$', views.generateop),
    path('Staffpage/issuedops/', views.issuedops),
    url(r'^Staffpage/ops/ViewDetails/(?P<op_number>[A-Z0-9]+)$', views.StudentMedicineissue),
    url(r'^Staffpage/issuedops/ViewDetails/(?P<op_number>[A-Z0-9]+)$', views.viewopissue),
]