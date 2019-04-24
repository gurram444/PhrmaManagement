from django.shortcuts import render, redirect
from . import models
from Admin.models import AddStaff, PharmacyAvailableStock, StudentTabDetails, StudentMedicineIssue,OPDetails,PharmacyIssuedStock
from Student.models import Student
from django.http import HttpResponse
from django.contrib import messages
import json


# Create your views here.
def stafflogin(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        Password = request.POST['Password']

        try:
            x = AddStaff.objects.get(UserName=Username)
            pwd = x.Password
            if Password == pwd:
                request.session['StaffId'] = x.StaffId
                return redirect('StaffPage')
            else:
                return HttpResponse('Wrong Username/Password Combination')
        except:
            return HttpResponse('User Does Not Exist')

    return render(request, "stafflogin.html")


def stafflogout(request):
    if request.session.has_key('StaffId'):
        request.session.flush()
        return redirect('stafflogin')


def ManageStudents(request):
    if request.session.has_key('StaffId'):
        return render(request, 'students.html')
    return redirect('stafflogin')


def VerifyStudent(request):
    if request.session.has_key('StaffId'):
        if request.method == 'POST':
            try:
                admno = request.POST['Admission_number']
                rec = Student.objects.get(Admission_number=admno)
                return render(request, "StudentDetails.html", {'Details':rec})
            except:
                messages.add_message(request, messages.INFO, 'No Details Found for the Entered Admission Number.')
                return render(request,'GetStdentDetails.html')
        else:
            return render(request, 'GetStdentDetails.html')
    return redirect('stafflogin')


def generateop(request, Admission_number):
    if request.session.has_key('StaffId'):
        Admission_number = Admission_number
        insert = OPDetails(AdmissionNumber=Admission_number)
        insert.save()
        last_op = OPDetails.objects.all().order_by('id').last()
        studentdetails = Student.objects.get(Admission_number=Admission_number)
        return render(request, 'opform.html', {'op_no': last_op,'Details':studentdetails})
    else:
        return redirect('stafflogin')


def issueop(request):
    if request.session.has_key('StaffId'):
        ops = OPDetails.objects.filter(Status='False')
        return render(request,'ops.html',{'ops':ops})
    else:
        return redirect('stafflogin')


def issuedops(request):
    if request.session.has_key('StaffId'):
        ops = OPDetails.objects.filter(Status='True')
        return render(request, 'StudentIssuedMedicines.html', {'ops':ops})
    else:
        return redirect('stafflogin')


def StudentMedicineissue(request,op_number):
    if request.session.has_key('StaffId'):
        if request.method == 'POST':
            op_number = request.POST['op_number']
            op = OPDetails.objects.get(OPNumber=op_number)
            TotalBalance = request.POST['total_bal']
            op.TotalBalance = TotalBalance
            op.Status = 'True'
            op.save()
            count = int(request.POST['czContainer_czMore_txtCount'])
            i = 1
            while i <= count:
                TabletName = request.POST['tab_' + str(i) + '_name']
                TotalTabsIssued = int(request.POST['tab_' + str(i) + '_qty'])
                RatePerUnit = int(request.POST['tab_' + str(i) + '_rate'])
                insert = StudentMedicineIssue(Op_id=op, TabletName=TabletName, TotalTabsIssued=TotalTabsIssued,
                                              RatePerUnit=RatePerUnit)
                try:
                    x = PharmacyAvailableStock.objects.get(TabletName=TabletName)
                    ExistingTabs = int(x.TotalTabs)
                    if ExistingTabs >= TotalTabsIssued:
                        UpdatedTabs = ExistingTabs - TotalTabsIssued
                        x.TotalTabs = UpdatedTabs
                        x.save()
                    else:
                        return HttpResponse('Issued Quantiy Of ' + TabletName + ' Are Not Available in Stock.')
                except:
                    pass

                insert.save()
                i += 1
            messages.add_message(request, messages.INFO, 'Medicine Issued Successfully.')
            return redirect('issuedops')

        else:
            tabs = PharmacyAvailableStock.objects.all()
            op = OPDetails.objects.get(OPNumber=op_number)
            return render(request, 'StudentMedincineIssue.html', {'tabs': tabs, 'op':op})

    else:
        return redirect('stafflogin')


def viewopissue(request, op_number):
    if request.session.has_key('StaffId'):
        op = OPDetails.objects.get(OPNumber=op_number)
        tabs = StudentMedicineIssue.objects.filter(Op_id=op)

        return render(request, 'viewopissue.html',{'tabs':tabs})
    else:
        return redirect('stafflogin')


def PharmaStockRecieved(request):
    if request.session.has_key('StaffId'):
        PharmaIssues = PharmacyIssuedStock.objects.all()
        return render(request, 'PharmaStockRecieved.html', {'PharmaIssues': PharmaIssues})
    return redirect('stafflogin')


def PharmaStockAvailable(request):
    if request.session.has_key('StaffId'):
        PharmaStock = PharmacyAvailableStock.objects.all()
        return render(request,'PharmaStockAvailable.html',{'PharmaStock':PharmaStock})
    return redirect('stafflogin')

def PharmaLowStock(request):
    if request.session.has_key('StaffId'):
        LowStock = PharmacyAvailableStock.objects.filter(TotalTabs__lte = 50)
        return render(request, 'PharmaLowStock.html', {'LowStock':LowStock})
    return redirect('stafflogin')


def ManageFaculty(request):
    if request.session.has_key('StaffId'):
        return render(request, 'Faculty.html')
    return redirect('stafflogin')


def ManageStaff(request):
    if request.session.has_key('StaffId'):
        return render(request, 'Staff.html')
    return redirect('stafflogin')


def ManagStock(request):
    if request.session.has_key('StaffId'):
        return render(request, 'Stock.html')
    return redirect('stafflogin')