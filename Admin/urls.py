from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('Login/', views.Adminlogin),
    path('Adminpage/', views.Adminpage),
    path('Adminpage/MainStockEntry/', views.AddStock),
    path('Adminpage/DisplayAvailbleStock/', views.DisplayAvailableStock),
    path('Adminpage/DisplayInvoices/',views.DisplayMainStock),
    path('Adminpage/PharmacyStockIssue/',views.PhramcyStockIssue),
    path('Adminpage/DisplayPharmaAvailableStock/', views.DisplayPharmaAvailableStock),
    path('Adminpage/DisplayPharmaIssues/', views.DisplayPharmaIssues),
    path('Adminpage/DisplayLowStock/', views.DisplayLowStock),
    path('Adminpage/ViewStudentRegistrations/', views.DisplayRegistrations),
    path('Adminpage/ViewRegisteredStudents/',views.RegisteredStudents),
    path('Adminpage/AddStaff', views.AddStaff),
    path('Adminpage/ViewExistingStaff/', views.DisplayAvailableStaff),
    url(r'^Adminpage/ViewStudentRegistrations/AcceptRegistrationRequest/(?P<Admission_number>\d+)$', views.AcceptRegistrationRequest),
    url(r'^Adminpage/ViewStudentRegistrations/RejectRegistrationRequest/(?P<Admission_number>\d+)$', views.RejectRegistrationRequest),
    url(r'^Adminpage/ViewExistingStaff/RemoveStaff/(?P<StaffId>\d+)$', views.RemoveStaff),
]

