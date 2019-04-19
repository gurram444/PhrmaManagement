from django.shortcuts import render, redirect
from . import models
from Admin.models import AddStaff, PharmacyAvailableStock, StudentTabDetails, StudentMedicineIssue,OPDetails
from Student.models import Student
from django.http import HttpResponse
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
                return redirect('Staffpage')
            else:
                return HttpResponse('Wrong Username/Password Combination')
        except:
            return HttpResponse('User Does Not Exist')

    return render(request, "stafflogin.html")


def staffhome(request):
    if request.session.has_key('StaffId'):
        StaffId = request.session['StaffId']
        return render(request, "StaffPage.html", {'StaffId': StaffId})
    else:
        return redirect('stafflogin')


def stafflogout(request):
    if request.session.has_key('StaffId'):
        request.session.flush()
        return redirect('stafflogin')


def GetStudent(request):
    if request.session.has_key('StaffId'):
        StaffId = request.session['StaffId']
        if request.method == 'POST':
            admno = request.POST['Admission_number']
            rec = Student.objects.get(Admission_number=admno)
            return render(request, "StaffPage.html", {'StaffId': StaffId, 'Details':rec})

    else:
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
            return render(request, 'StudentMedincineIssue.html')

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

