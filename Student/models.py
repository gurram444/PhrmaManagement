from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    Student_name = models.CharField(max_length=20)
    Admission_number = models.IntegerField()
    Father_name = models.CharField(max_length=20)
    Mother_name = models.CharField(max_length=20)
    doj = models.DateField()
    coursecomplete = models.DateField()
    department = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    relegion = models.CharField(max_length=10)
    caste = models.CharField(max_length=10)
    sub_caste = models.CharField(max_length=10)
    course = models.CharField(max_length=20)
    contact_no = models.IntegerField()
    email = models.CharField(max_length=30)
    aadhar_no = models.IntegerField()
    Age = models.IntegerField()
    bloodgroup = models.CharField(max_length=10)
    address = models.CharField(max_length=40)
    city = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='image/')
    Status = models.CharField(max_length=10)

    def __str__(self):
        return self.Student_name


class UserProfile(models.Model):
    url = models.URLField()
    home_address = models.TextField()
    phone_numer = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='image/')