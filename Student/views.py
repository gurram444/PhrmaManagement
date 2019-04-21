from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import View
from . import models


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
                return HttpResponse('Your Account is Not activated yet, You will get a mail after your account is activated')
            return HttpResponse('Wrong Username/Password Combination')
        except:
            return HttpResponse('User Does Not Exist')

    return render(request, 'Student/studentlogin.html')



def StudentLoggedIn(request):
    if request.session.has_key('Admission_number'):
        Admission_number = request.session['Admission_number']
        x = models.Student.objects.get(Admission_number=Admission_number)
        return render(request,'Student/logged2.html',{'Admission_number':Admission_number, 'x':x})
    return redirect('studentlogin')


def StudentLogOut(request):
    if request.session.has_key('Admission_number'):
        request.session.flush()
        return redirect('studentlogin')
