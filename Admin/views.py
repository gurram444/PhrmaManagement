from django.shortcuts import render
from . import models
from Student.models import Student
from django.http import HttpResponse,JsonResponse
import requests
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
# Create your views here.


def Adminlogin(request):
    return render(request, "adminlogin.html")


def Adminpage(request):
    recs = Student.objects.filter(Status='False').count()
    regs = Student.objects.filter(Status='True').count()
    return render(request, "MainAdminPage.html",{'rec':recs,'reg':regs})


def AddStock(request):
    if request.method == 'POST':
        InvoiceNumber = request.POST['invoice_number']
        InvoiceDate = request.POST['invoice_date']
        StockEntryDate = request.POST['entry_date']
        RecievedFrom = request.POST['recieved_from']
        TotalCost = int(request.POST['total_bal'])
        insert1 = models.Invoice(Invoice_number=InvoiceNumber, InvoiceDate=InvoiceDate, StockEntryDate=StockEntryDate,
                                 RecievedFrom=RecievedFrom, TotalCost=TotalCost)
        insert1.save()
        count = int(request.POST['czContainer_czMore_txtCount'])
        i = 1
        while i <= count:
            TabletName = request.POST['tab_' + str(i) + '_name']
            TotalTabsRecieved = int(request.POST['tab_' + str(i) + '_qty'])
            RatePerUnit = int(request.POST['tab_' + str(i) + '_rate'])
            insert = models.TabDetails(Invoice_id=insert1, TabletName=TabletName, TotalTabsRecieved=TotalTabsRecieved,
                                      RatePerUnit=RatePerUnit)
            insert.save()
            try:
                x = models.AvailableStock.objects.get(TabletName=TabletName)
                ExistingTabs = int(x.TotalTabs)
                UpdatedTabs = ExistingTabs + TotalTabsRecieved
                x.TotalTabs = UpdatedTabs
                x.save()

            except:
                records = models.AvailableStock(TabletName=TabletName, TotalTabs=TotalTabsRecieved,RatePerUnit=RatePerUnit)
                records.save()


            i += 1

        invoice = models.TabDetails.objects.all()
        return render(request, 'invoices.html', {'invoices': invoice})
    else:
        return render(request, 'MainStockEntyForm.html')



def PhramcyStockIssue(request):
    if request.method == 'POST':
        StockIssueDate = request.POST['issue_date']
        TotalCost = int(request.POST['total_bal'])
        count = int(request.POST['czContainer_czMore_txtCount'])
        i = 1
        while i <= count:
            TabletName = request.POST['tab_' + str(i) + '_name']
            TotalTabsIssued = int(request.POST['tab_' + str(i) + '_qty'])
            RatePerUnit = int(request.POST['tab_' + str(i) + '_rate'])
            insert = models.PharmacyIssuedStock(StockEntryDate=StockIssueDate,TabletName=TabletName,
                                                TotalTabsIssued=TotalTabsIssued, RatePerUnit=RatePerUnit,TotalCost=TotalCost)

            try:
                x = models.AvailableStock.objects.get(TabletName=TabletName)
                ExistingTabs = int(x.TotalTabs)
                if ExistingTabs >= TotalTabsIssued:
                    UpdatedTabs = ExistingTabs - TotalTabsIssued
                    x.TotalTabs = UpdatedTabs
                    x.save()
                else:
                    return HttpResponse('Issued Quantiy Of ' + TabletName + ' Are Not Available in Stock.')
            except:
                pass

            try:
                x = models.PharmacyAvailableStock.objects.get(TabletName=TabletName)
                ExistingTabs = int(x.TotalTabs)
                UpdatedTabs = ExistingTabs + TotalTabsIssued
                x.TotalTabs = UpdatedTabs
                x.save()

            except:
                records = models.PharmacyAvailableStock(TabletName=TabletName, TotalTabs=TotalTabsIssued, RatePerUnit=RatePerUnit)
                records.save()

            insert.save()

            i += 1
        #Issued = True
        #json_data={"Issued":Issued}
        PharmaIssues = models.PharmacyIssuedStock.objects.all()
        #return JsonResponse(json_data)
        #return render(request,'Pharmaissues.html',{'PharmaIssues':PharmaIssues})
        messages.add_message(request, messages.INFO, 'Stock Issued Successfully')
        return render(request, 'PharmacyStockIssue.html')


    TotalTabs = models.AvailableStock.objects.all()
    return render(request, 'PharmacyStockIssue.html', {'TotalTabs': TotalTabs})





def DisplayRegistrations(request):
    try:
        Status = 'False'
        recs = Student.objects.filter(Status = Status)
        print(recs)
        return render(request,'ViewStudentRegistrations.html', {'registrations':recs})
    except:
        return render(request,'ViewStudentRegistrations.html')

def RegisteredStudents(request):
    try:
        RegisteredStudents = Student.objects.filter(Status='True')
        return render(request,'ViewRegisteredStudents.html', {'Registerd':RegisteredStudents})
    except:
        return render(request,'ViewRegisteredStudents.html')

def AcceptRegistrationRequest(request, Admission_number):
    rec = Student.objects.get(Admission_number = Admission_number)
    rec.Status = 'True'
    rec.save()
    StudentName = rec.Student_name
    email = rec.email
    mobno = rec.contact_no
    subject = 'Congratulations!, Your Account Has Activated.'
    email_message = 'Hello '+ StudentName + '!.\n Your Account Has Activated You can Now login with your credentials.'
    From_mail = settings.EMAIL_HOST_USER
    to_list = [email]
    send_mail(subject, email_message, From_mail, to_list, fail_silently=False)
    print('mail sent')
    res = requests.post('https://textbelt.com/text', {
        'phone': mobno,
        'message': 'Hello world',
        'key': 'textbelt',
    })
    print(res.json())
    return HttpResponse('Request Accepted')

def RejectRegistrationRequest(request, Admission_number):
    rec = Student.objects.get(Admission_number = Admission_number)
    StudentName = rec.Student_name
    email = rec.email
    subject = 'Sorry!, Your Registration Request is Rejected.'
    email_message = 'Hello ' + StudentName + '!.\n Your request for registration is rejected, \n you can contact concern department for futher details.'
    From_mail = settings.EMAIL_HOST_USER
    to_list = [email]
    send_mail(subject, email_message, From_mail, to_list, fail_silently=False)
    rec.delete()
    return HttpResponse("Request Rejected")


def AddStaff(request):
    if request.method=='POST':
        StaffId = request.POST['StaffId']
        StaffName = request.POST['StaffName']
        ContactNumber = request.POST['ContactNumber']
        UserName = request.POST['UserName']
        Password = request.POST['Password']
        Staff = models.AddStaff(StaffId = StaffId, StaffName = StaffName, ContactNumber = ContactNumber, UserName = UserName,
                        Password = Password )
        Staff.save()
        return HttpResponse('Staff added Successfully')

def RemoveStaff(request,StaffId):
    member = models.AddStaff.objects.get(StaffId = StaffId)
    member.delete()
    return HttpResponse('Staff Removed Successfully.')

def DisplayAvailableStaff(request):
    staff = models.AddStaff.objects.all()
    return render(request,'ViewExistingStaff.html',{'Staff':staff})


def DisplayAvailableStock(request):
    recs = models.AvailableStock.objects.all()
    return render(request,'DisplayAvailableStock.html',{'records':recs})


def DisplayMainStock(request):
    invoice = models.TabDetails.objects.all()
    return render(request, 'invoices.html', {'invoices': invoice})

def DisplayPharmaAvailableStock(request):
    PharmaStock = models.PharmacyAvailableStock.objects.all()
    return render(request,'DisplayPharmaStock.html',{'PharmaStock':PharmaStock})

def DisplayPharmaIssues(request):
    PharmaIssues = models.PharmacyIssuedStock.objects.all()
    return render(request, 'Pharmaissues.html', {'PharmaIssues': PharmaIssues})

def DisplayLowStock(request):
    LowStock = models.AvailableStock.objects.filter(TotalTabs__lte = 50)
    return render(request, 'DisplayLowStock.html', {'LowStock':LowStock})