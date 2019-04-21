from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('Login/', views.stafflogin, name='stafflogin'),
    path('StaffPage/LogOut/', views.stafflogout),
    path('StaffPage/ManageStudents/', views.ManageStudents, name='StaffPage' ),
    path('StaffPage/ManageStudents/VerifyStudent/', views.VerifyStudent),
    url(r'^StaffPage/ManageStudents/VerifyStudent/GenerateOP/(?P<Admission_number>\d+)$', views.generateop),
    path('StaffPage/ManageStudents/ops/', views.issueop),
    url(r'^StaffPage/ManageStudents/ops/StudentMedicineIssue/(?P<op_number>[A-Z0-9]+)$', views.StudentMedicineissue),
    path('StaffPage/ManageStudents/issuedops/', views.issuedops, name='issuedops'),
    url(r'^StaffPage/ManageStudents/issuedops/ViewDetails/(?P<op_number>[A-Z0-9]+)$', views.viewopissue),
    path('StaffPage/ManageFaculty/', views.ManageFaculty),
    path('StaffPage/ManageStaff/', views.ManageStaff),
    path('StaffPage/ManageStock/', views.ManagStock),
    path('StaffPage/ManageStock/PharmaStockRecieved/', views.PharmaStockRecieved),
    path('StaffPage/ManageStock/PharmaStockAvailable/', views.PharmaStockAvailable),
    path('StaffPage/ManageStock/PharmaLowStock/', views.PharmaLowStock),

]