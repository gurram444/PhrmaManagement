# Generated by Django 2.1.7 on 2019-03-18 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Student_name', models.CharField(max_length=20)),
                ('Admission_number', models.IntegerField()),
                ('Father_name', models.CharField(max_length=20)),
                ('Mother_name', models.CharField(max_length=20)),
                ('doj', models.DateField()),
                ('coursecomplete', models.DateField()),
                ('department', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.DateField()),
                ('relegion', models.CharField(max_length=10)),
                ('caste', models.CharField(max_length=10)),
                ('sub_caste', models.CharField(max_length=10)),
                ('course', models.CharField(max_length=20)),
                ('contact_no', models.IntegerField()),
                ('phno', models.IntegerField()),
                ('email', models.CharField(max_length=30)),
                ('aadhar_no', models.IntegerField()),
                ('Age', models.IntegerField()),
                ('bloodgroup', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=40)),
                ('city', models.CharField(max_length=20)),
                ('profile_image', models.ImageField(upload_to='image')),
                ('Status', models.BooleanField()),
            ],
        ),
    ]
