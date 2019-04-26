from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('Login/', views.Adminlogin, name='Adminlogin'),
    path('Logout/', views.Adminlogout),
    path('AdminPage/ManageStudent/', views.ManageStudent, name='ManageStudent'),
    path('AdminPage/ManageStudent/ViewStudentRegistrations/', views.DisplayRegistrations),
    path('AdminPage/ManageStudent/ViewRegisteredStudents/',views.RegisteredStudents),
    url(r'^AdminPage/ManageStudent/ViewStudentRegistrations/AcceptRegistrationRequest/(?P<Admission_number>\d+)$', views.AcceptRegistrationRequest),
    url(r'^AdminPage/ManageStudent/ViewStudentRegistrations/RejectRegistrationRequest/(?P<Admission_number>\d+)$', views.RejectRegistrationRequest),
    path('AdminPage/ManageStudent/GetStudent/', views.GetStudent),
    url(r'^AdminPage/ManageStudent/GetStudent/ViewDetails/(?P<OPNumber>[A-Z0-9]+)', views.tabdetails),
    path('AdminPage/ManageStaff/', views.ManageStaff),
    path('AdminPage/ManageStaff/AddStaff', views.AddStaff),
    path('AdminPage/ManageStaff/ViewExistingStaff/', views.DisplayAvailableStaff, name='DisplayAvailableStaff'),
    url(r'^AdminPage/ManageStaff/ViewExistingStaff/RemoveStaff/(?P<StaffId>\d+)$', views.RemoveStaff),
    path('AdminPage/ManageStock/', views.ManageStock),
    path('AdminPage/ManageStock/MainStockEntry/', views.AddStock),
    path('AdminPage/ManageStock/DisplayAvailbleStock/', views.DisplayAvailableStock),
    path('AdminPage/ManageStock/DisplayInvoices/',views.DisplayMainStock),
    url(r'^AdminPage/ManageStock/DisplayInvoices/ViewDetails/(?P<InvoiceNumber>\d+)$', views.InvoiceDetails),
    path('AdminPage/ManageStock/PharmacyStockIssue/',views.PhramcyStockIssue),
    path('AdminPage/ManageStock/DisplayPharmaAvailableStock/', views.DisplayPharmaAvailableStock),
    path('AdminPage/ManageStock/DisplayPharmaIssues/', views.DisplayPharmaIssues, name='DisplayPharmaIssues'),
    path('AdminPage/ManageStock/DisplayLowStock/', views.DisplayLowStock),
]

