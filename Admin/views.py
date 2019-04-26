from django.shortcuts import render, redirect
from . import models
from Student.models import Student
from django.http import HttpResponse,JsonResponse
import requests
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
# Create your views here.


def Adminlogin(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        Password = request.POST['Password']
        if Username == 'admin' and Password == 'admin':
            request.session['admin'] = Username
            return redirect('ManageStudent')
        else:
            messages.add_message(request,messages.INFO, 'Wrong Username/Password Combination')
            return render(request, "adminlogin.html")
    return render(request, "adminlogin.html")

def Adminlogout(request):
    if request.session.has_key('admin'):
        request.session.flush()
        return redirect('Adminlogin')


def Adminpage(request):
    recs = Student.objects.filter(Status='False').count()
    regs = Student.objects.filter(Status='True').count()
    return render(request, "MainAdminPage.html",{'rec':recs,'reg':regs})


def ManageStudent(request):
    if request.session.has_key('admin'):
        recs = Student.objects.filter(Status='False').count()
        regs = Student.objects.filter(Status='True').count()
        return render(request, "ManageStudent.html", {'rec': recs, 'reg': regs})
    return redirect('Adminlogin')

def GetStudent(request):
    if request.session.has_key('admin'):
        if request.method == 'POST':
            try:
                Admission_number = request.POST['Admission_number']
                x = Student.objects.get(Admission_number=Admission_number)
                print(x)
                rec = models.OPDetails.objects.filter(AdmissionNumber=Admission_number)
                print(rec)
                visits = rec.count()
                lastvisit = rec.last()
                return render(request, 'studentprofile.html',
                                  {'Admission_number': Admission_number, 'x': x, 'visits': visits, 'last': lastvisit,'rec': rec})
            except:
                messages.add_message(request,messages.INFO,'NO Details Found for the entered admission number.')
                return render(request, 'GetStudentDetails.html')
        return render(request, 'GetStudentDetails.html')
    return redirect('Adminlogin')

def tabdetails(request,OPNumber):
    if request.session.has_key('admin'):
        op_id = models.OPDetails.objects.get(OPNumber=OPNumber)
        tabs= models.StudentMedicineIssue.objects.filter(Op_id=op_id)
        return render(request, 'studenttabdetails.html', {'tabs':tabs})
    return redirect('Adminlogin')


def ManageStaff(request):
    if request.session.has_key('admin'):
        return render(request,'ManageStaff.html')
    return redirect('Adminlogin')


def ManageStock(request):
    if request.session.has_key('admin'):
        return render(request, 'ManageStock.html')
    return redirect('Adminlogin')


def AddStock(request):
    if request.session.has_key('admin'):
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
            messages.add_message(request, messages.INFO, 'Stock Added Successfully')
            return render(request, 'invoices.html', {'invoices': invoice})
        else:
            return render(request, 'MainStockEntyForm.html')
    return redirect('Adminlogin')


def PhramcyStockIssue(request):
    if request.session.has_key('admin'):
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
            messages.add_message(request, messages.INFO, 'Stock Issued Successfully')
            return redirect('DisplayPharmaIssues')


        TotalTabs = models.AvailableStock.objects.all()
        return render(request, 'PharmacyStockIssue.html', {'TotalTabs': TotalTabs})
    return redirect('Adminlogin')


def DisplayRegistrations(request):
    if request.session.has_key('admin'):
        try:
            Status = 'False'
            recs = Student.objects.filter(Status = Status)
            return render(request,'ViewStudentRegistrations.html', {'registrations':recs})
        except:
            return render(request,'ViewStudentRegistrations.html')
    return redirect('Adminlogin')


def RegisteredStudents(request):
    if request.session.has_key('admin'):
        try:
            RegisteredStudents = Student.objects.filter(Status='True')
            return render(request,'ViewRegisteredStudents.html', {'Registerd':RegisteredStudents})
        except:
            return render(request,'ViewRegisteredStudents.html')
    return redirect('Adminlogin')


def AcceptRegistrationRequest(request, Admission_number):
    if request.session.has_key('admin'):
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
        res = requests.post('https://textbelt.com/text', {
            'phone': mobno,
            'message': 'Hello world',
            'key': 'textbelt',
        })
        recs = Student.objects.filter(Status='False')
        messages.add_message(request, messages.INFO, 'Registration request accepted successfully.')
        return render(request, 'ViewStudentRegistrations.html', {'registrations': recs})
    return redirect('Adminlogin')


def RejectRegistrationRequest(request, Admission_number):
    if request.session.has_key('admin'):
        rec = Student.objects.get(Admission_number = Admission_number)
        StudentName = rec.Student_name
        email = rec.email
        subject = 'Sorry!, Your Registration Request is Rejected.'
        email_message = 'Hello ' + StudentName + '!.\n Your request for registration is rejected, \n you can contact concern department for futher details.'
        From_mail = settings.EMAIL_HOST_USER
        to_list = [email]
        send_mail(subject, email_message, From_mail, to_list, fail_silently=False)
        rec.delete()
        recs = Student.objects.filter(Status='False')
        messages.add_message(request, messages.INFO, 'Registration request rejected successfully.')
        return render(request, 'ViewStudentRegistrations.html', {'registrations': recs})
    return redirect('Adminlogin')


def AddStaff(request):
    if request.session.has_key('admin'):
        if request.method=='POST':
            StaffId = request.POST['StaffId']
            StaffName = request.POST['StaffName']
            ContactNumber = request.POST['ContactNumber']
            UserName = request.POST['UserName']
            Password = request.POST['Password']
            pic = request.FILES['StaffImage']
            Staff = models.AddStaff(StaffId = StaffId, StaffName = StaffName, ContactNumber = ContactNumber, UserName = UserName,
                            Password = Password, StaffImage=pic )
            Staff.save()
            messages.add_message(request, messages.INFO, 'Staff Added successfully.')
            return redirect('DisplayAvailableStaff')
    return redirect('Adminlogin')


def RemoveStaff(request,StaffId):
    if request.session.has_key('admin'):
        member = models.AddStaff.objects.get(StaffId = StaffId)
        member.delete()
        staff = models.AddStaff.objects.all()
        messages.add_message(request, messages.INFO, 'Staff Removed successfully.')
        return render(request, 'ViewExistingStaff.html', {'Staff': staff})
    return redirect('Adminlogin')


def DisplayAvailableStaff(request):
    if request.session.has_key('admin'):
        staff = models.AddStaff.objects.all()
        return render(request,'ViewExistingStaff.html',{'Staff':staff})
    return redirect('Adminlogin')


def DisplayAvailableStock(request):
    if request.session.has_key('admin'):
        recs = models.AvailableStock.objects.all()
        return render(request,'DisplayAvailableStock.html',{'records':recs})
    return redirect('Adminlogin')


def DisplayMainStock(request):
    if request.session.has_key('admin'):
        invoice = models.Invoice.objects.all()
        return render(request, 'invoices.html', {'invoices': invoice})
    return redirect('Adminlogin')


def InvoiceDetails(request,InvoiceNumber):
    if request.session.has_key('admin'):
        invoice = models.Invoice.objects.get(Invoice_number=InvoiceNumber)
        invoiceid = models.TabDetails.objects.filter(Invoice_id=invoice)
        return render(request, 'invoicedetails.html', {'invoicedetails':invoiceid})
    return redirect('Adminlogin')


def DisplayPharmaAvailableStock(request):
    if request.session.has_key('admin'):
        PharmaStock = models.PharmacyAvailableStock.objects.all()
        return render(request,'DisplayPharmaStock.html',{'PharmaStock':PharmaStock})
    return redirect('Adminlogin')


def DisplayPharmaIssues(request):
    if request.session.has_key('admin'):
        PharmaIssues = models.PharmacyIssuedStock.objects.all()
        return render(request, 'Pharmaissues.html', {'PharmaIssues': PharmaIssues})
    return redirect('Adminlogin')


def DisplayLowStock(request):
    if request.session.has_key('admin'):
        LowStock = models.AvailableStock.objects.filter(TotalTabs__lte = 50)
        return render(request, 'DisplayLowStock.html', {'LowStock':LowStock})
    return render(request, "adminlogin.html")