from django.db import models
import datetime


class Invoice(models.Model):
    Invoice_number = models.BigIntegerField()
    InvoiceDate = models.DateField()
    StockEntryDate = models.DateField()
    RecievedFrom=models.CharField(max_length=40)
    TotalCost=models.IntegerField()

    def __str__(self):
        return self.RecievedFrom

class TabDetails(models.Model):
    Invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    TabletName = models.CharField(max_length=20)
    TotalTabsRecieved = models.IntegerField()
    RatePerUnit = models.IntegerField()


    def __str__(self):
        return self.TabletName


class AvailableStock(models.Model):
    TabletName = models.CharField(max_length=20)
    TotalTabs = models.IntegerField()
    RatePerUnit = models.IntegerField()

    def __str__(self):
        return self.TabletName


class PharmacyIssuedStock(models.Model):
    StockEntryDate = models.DateField()
    TabletName = models.CharField(max_length=20)
    TotalTabsIssued = models.IntegerField()
    RatePerUnit = models.IntegerField()
    TotalCost = models.IntegerField()

    def __str__(self):
        return self.TabletName


class PharmacyAvailableStock(models.Model):
    TabletName = models.CharField(max_length=20)
    TotalTabs = models.IntegerField()
    RatePerUnit = models.IntegerField()

    def __str__(self):
        return self.TabletName



def increment_op_number():
    last_op = OPDetails.objects.all().order_by('id').last()
    if not last_op:
         return 'SVU101'
    op_no = last_op.OPNumber
    op_int = int(op_no.split('SVU')[-1])
    new_op_int = op_int + 1
    new_op_no = 'SVU' + str(new_op_int)
    return new_op_no

class OPDetails(models.Model):
    OPNumber = models.CharField(max_length=500, default=increment_op_number, null=True, blank=True)
    AdmissionNumber = models.BigIntegerField()
    IssueDate = models.DateField(default=datetime.date.today)
    TotalBalance = models.IntegerField(default=0)
    Status = models.CharField(max_length=10, default='False')

class StudentTabDetails(models.Model):
    AdmissionNumber = models.BigIntegerField()
    OPNumber = models.IntegerField()
    IssueDate = models.DateField()
    TotalBalance = models.IntegerField()
    StudentName = models.CharField(max_length=30)

class StudentMedicineIssue(models.Model):
    Op_id = models.ForeignKey(OPDetails,on_delete=models.CASCADE)
    TabletName = models.CharField(max_length=20)
    TotalTabsIssued = models.IntegerField()
    RatePerUnit = models.IntegerField()


class AddStaff(models.Model):
    StaffId = models.CharField(max_length=20)
    StaffName = models.CharField(max_length=30)
    ContactNumber = models.BigIntegerField()
    UserName = models.CharField(max_length=20)
    Password = models.CharField(max_length=20)
    StaffImage = models.ImageField(upload_to='StaffImages/')

    def __str__(self):
        return self.StaffName