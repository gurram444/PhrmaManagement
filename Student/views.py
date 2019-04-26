from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from django.views.generic import View
from . import models
from Admin.models import OPDetails,StudentMedicineIssue

def studentregister(request):
    if request.method == 'POST':
        sname = request.POST['Student_name']
        admno = request.POST['Admission_number']
        fname = request.POST['Father_name']
        mname = request.POST['Mother_name']
        doj = request.POST['doj']
        doc = request.POST['coursecomplete']
        dept = request.POST['department']
        pwd = request.POST['password']
        sex = request.POST['gender']
        dob = request.POST['dob']
        rel = request.POST['relegion']
        caste = request.POST['caste']
        s_caste = request.POST['sub_caste']
        course = request.POST['course']
        phno = request.POST['contact_no']
        email = request.POST['email']
        adno = request.POST['aadhar_no']
        age = request.POST['Age']
        bgp = request.POST['bloodgroup']
        addr = request.POST['address']
        city = request.POST['city']
        pic = request.FILES['image']
        Accept = 'False'


        insert = models.Student(Admission_number = admno, Student_name = sname,Father_name = fname, Mother_name = mname,doj = doj, coursecomplete =doc,
                                department = dept, password = pwd, gender = sex, dob = dob, relegion = rel, caste = caste, sub_caste = s_caste,
                                course = course, contact_no = phno, email = email, aadhar_no = adno, Age = age, bloodgroup = bgp, address = addr,
                                city = city, Status = Accept, profile_image = pic)

        insert.save()

        request.session['Admission_number']=admno

        return redirect('LoggedIn')

    return render(request, "Student/studentreg2.html")


def UpdateProfile(request):
    if request.session.has_key('Admission_number'):
        if request.method == 'POST':
            sname = request.POST['Student_name']
            admno = request.POST['Admission_number']
            fname = request.POST['Father_name']
            mname = request.POST['Mother_name']
            doj = request.POST['doj']
            doc = request.POST['coursecomplete']
            dept = request.POST['department']
            pwd = request.POST['password']
            sex = request.POST['gender']
            dob = request.POST['dob']
            rel = request.POST['relegion']
            caste = request.POST['caste']
            s_caste = request.POST['sub_caste']
            course = request.POST['course']
            phno = request.POST['contact_no']
            email = request.POST['email']
            adno = request.POST['aadhar_no']
            age = request.POST['Age']
            bgp = request.POST['bloodgroup']
            addr = request.POST['address']
            city = request.POST['city']

            insert = models.Student(Admission_number=admno, Student_name=sname, Father_name=fname, Mother_name=mname, doj=doj,
                                    coursecomplete=doc,
                                    department=dept, password=pwd, gender=sex, dob=dob, relegion=rel, caste=caste,
                                    sub_caste=s_caste,
                                    course=course, contact_no=phno, email=email, aadhar_no=adno, Age=age, bloodgroup=bgp,
                                    address=addr,
                                    city=city)

            insert.save()
            messages.add_message(request, messages.INFO, 'Registration Successfully completed, You can login to your account once its activated.')
            return redirect('studentlogin')

        return render(request, 'Student/updateprofile.html')
    return redirect('studentlogin')


def Transactions(request):
    if request.session.has_key('Admission_number'):
        Admission_number = request.session['Admission_number']
        rec = OPDetails.objects.filter(AdmissionNumber=Admission_number)
        print(rec.count())
        return render(request, 'Student/Transactions.html', {'rec':rec})
    return redirect('studentlogin')


def TransactionDetails(request,OPNumber):
    if request.session.has_key('Admission_number'):
        op_id = OPDetails.objects.get(OPNumber=OPNumber)
        tabs= StudentMedicineIssue.objects.filter(Op_id=op_id)
        return render(request, 'Student/TransactionDetails.html', {'tabs':tabs})
    return redirect('studentlogin')


def studentlogin(request):
    if request.method == 'POST':
        Admission_number = request.POST['Admission_number']
        Password = request.POST['pass']
        try:
            x = models.Student.objects.get(Admission_number=Admission_number)
            pwd = x.password
            Status = x.Status
            if Password == pwd and Status == 'True':
                request.session['Admission_number'] = x.Admission_number
                return redirect('LoggedIn')
            elif Password == pwd and Status == 'False':
                messages.add_message(request,messages.INFO,'Your Account is Not activated yet, You will get a mail after your account is activated')
                return redirect('studentlogin')
            messages.add_message(request,messages.INFO,'Wrong Username/Password Combination')
            return redirect('studentlogin')
        except:
            messages.add_message(request,messages.INFO,'User Does Not Exist')
            return redirect('studentlogin')

    return render(request, 'Student/studentlogin.html')



def StudentLoggedIn(request):
    if request.session.has_key('Admission_number'):
        Admission_number = request.session['Admission_number']
        x = models.Student.objects.get(Admission_number=Admission_number)
        rec = OPDetails.objects.filter(AdmissionNumber=Admission_number)
        visits = rec.count()
        lastvisit = rec.last()
        return render(request,'Student/studentpage.html',{'Admission_number':Admission_number, 'x':x, 'visits':visits, 'last':lastvisit})
    return redirect('studentlogin')


def StudentLogOut(request):
    if request.session.has_key('Admission_number'):
        request.session.flush()
        return redirect('studentlogin')
