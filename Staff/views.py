from django.shortcuts import render,redirect
from . import models
from Admin.models import AddStaff,PharmacyAvailableStock,StudentTabDetails,StudentMedicineIssue
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
        return render(request, "StaffPage.html", {'StaffId':StaffId})
    else:
        return redirect('stafflogin')

def stafflogout(request):
    if request.session.has_key('StaffId'):
        request.session.flush()
        return redirect('stafflogin')

def GetStudent(request):
    if request.method=='POST':
        admno = int(request.POST.get('the_post'))
        rec = Student.objects.get(Admission_number=admno)
        response_data={}
        response_data['Admission_number']=rec.Admission_number
        response_data['Student_name'] = rec.Student_name
        response_data['gender'] = rec.gender
        response_data['Age'] = rec.Age
        response_data['Contact_no'] = rec.contact_no
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )



def StudentMedicineissue(request):
    if request.method == 'POST':
        issue_date = request.POST['issue_date']
        op_number = request.POST['op_number']
        Admission_number = request.POST['Admission_number']
        Stuent_name = request.POST['Student_name']
        TotalBalance = request.POST['total_bal']
        insert1 = StudentTabDetails(AdmissionNnumber=Admission_number,OPNumber=op_number,IssueDate=issue_date,
                                   TotalBalance=TotalBalance,StudentName=Stuent_name)
        insert1.save()
        count = int(request.POST['czContainer_czMore_txtCount'])
        i = 1
        while i <= count:
            TabletName = request.POST['tab_' + str(i) + '_name']
            TotalTabsIssued = int(request.POST['tab_' + str(i) + '_qty'])
            RatePerUnit = int(request.POST['tab_' + str(i) + '_rate'])
            insert = StudentMedicineIssue(Op_id=insert1, TabletName=TabletName, TotalTabsIssued=TotalTabsIssued,
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
        return render(request, 'StudentMedincineIssue.html', message="sucess")

    else:
        tabs = PharmacyAvailableStock.objects.all()
        return render(request,'StudentMedincineIssue.html',{'tabs':tabs})