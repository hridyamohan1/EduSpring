from django.db import models
from django.utils import timezone

# Create your models here.
class login(models.Model):
    uname = models.CharField(max_length=50)
    pswd = models.CharField(max_length=50)
    usertype = models.IntegerField()
    def __str__(self):
        return self.uname

class tutor(models.Model):
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.IntegerField()
    age = models.IntegerField()
    address = models.CharField(max_length=50)
    img = models.FileField()
    qualification = models.CharField(max_length=50)
    # lang = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    cv = models.FileField()
    uname = models.CharField(max_length=50)
    pswd = models.CharField(max_length=20)
    action = models.CharField(max_length=50)
    def __str__(self):
        return self.uname

class user(models.Model):
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.IntegerField()
    age = models.IntegerField()
    img = models.FileField()
    uname = models.CharField(max_length=50)
    pswd = models.CharField(max_length=20)
    def __str__(self):
        return self.uname


class adcourse(models.Model):
    cname = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    amount = models.IntegerField()
    date = models.DateField(default=timezone.now)
    def __str__(self):
        return self.cname

class courseregister(models.Model):
    cname = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    amount = models.IntegerField()
    ad_amount = models.IntegerField()
    payment_status = models.BooleanField(default=False)
    uname = models.CharField(max_length=50)
    date = models.DateField(default=timezone.now)
    def __str__(self):
        return self.cname


class gethelp(models.Model):
    uname = models.CharField(max_length=50)
    msg = models.CharField(max_length=200)
    action = models.CharField(max_length=50)

class payment(models.Model):
    uname = models.CharField(max_length=50)
    course_details=models.ForeignKey(courseregister,on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10)
    def __str__(self):
        return self.uname

class session(models.Model):
    uname = models.CharField(max_length=50)
    topic = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    notes = models.FileField()
    course = models.CharField(max_length=50)
    def __str__(self):
        return self.topic

class PasswordReset(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    token=models.CharField(max_length=4)

