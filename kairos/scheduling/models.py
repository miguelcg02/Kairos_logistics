from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rol = models.IntegerField(blank=False)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"
        db_table = "profile"

    def __str__(self):
        return str(self.user.username)
    
class CVS(models.Model):
    name = models.CharField(max_length=20) #largest name 16 characters

    class Meta:
        verbose_name = "cvs"
        verbose_name_plural = "cvs"
        db_table = "cvs"

    def __str__(self):
        return self.name

class Turn(models.Model):
    cvs = models.ForeignKey(CVS,on_delete=models.CASCADE, blank=False) # location of the service
    typeTire = models.IntegerField(blank=False) # numeric convention for the type of tire
    quantity = models.IntegerField(blank=False) # number of tires to change
    rotation = models.BooleanField(blank=False) # aditional service (rotate maximum the same number of tires that you buy)
    quantityRotate = models.IntegerField(blank=True, null=True) # number of tires to rotate
    duration = models.IntegerField(blank=False) # time in minutes of the service
    date = models.DateField(auto_now=False, auto_now_add=False,blank=False) # date when the service is going to be done
    hour = models.TimeField(auto_now=False, auto_now_add=False,blank=False) # hour when the service is going to be done
    bill = models.IntegerField(blank=False) # number of the bill
    idCustomer = models.IntegerField(blank=False) # identification(CC) of the customer
    nameCustomer = models.TextField(max_length=50,blank=False) # name of the customer
    telCustomer = models.TextField(max_length=15,blank=False) # contact number of the customer
    scheduledBy = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=False,related_name="person_who_schedules") # person who scheduled
    dateScheduled = models.DateTimeField(auto_now=False, auto_now_add=True,blank=False) #date when the service was scheduled 
    modifiedBy = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,related_name="person_who_modifies", null=True)  # person who modified the service 
    dateModified = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True) #date when the service was modified 
    done = models.BooleanField(blank=True, null=True) # verification if the service get done
    comment = models.TextField(max_length=300,blank=True, null=True) # comment about the service or the reason to don't provide the service

    class Meta:
        verbose_name = "turn"
        verbose_name_plural = "turns"
        db_table = "turn"

    def __str__(self):
        return str(self.bill) + ' - ' + self.cvs.name

class Block(models.Model):
    cvs = models.ForeignKey(CVS,on_delete=models.CASCADE, blank=False) # location of the block
    duration = models.IntegerField(blank=False) # time in minutes of the block
    startDate = models.DateField(auto_now=False, auto_now_add=False,blank=False) # the beginning of the block
    startHour = models.TimeField(auto_now=False, auto_now_add=False,blank=False) # the beginning of the block
    endDate = models.DateField(auto_now=False, auto_now_add=False,blank=False) # the end of the block
    endHour = models.TimeField(auto_now=False, auto_now_add=False,blank=False) # the end of the block
    scheduledBy = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=False,related_name="person_who_schedules_block") # person who scheduled the block
    comment = models.TextField(max_length=300,blank=True, null=True) # comment about the block

    class Meta:
        verbose_name = "block"
        verbose_name_plural = "blocks"
        db_table = "block"

    def __str__(self):
        return 'Bloqueo del CVS ' + self.cvs.name + ' de las fechas ' + str(self.startDate) + ' - ' + str(self.endDate)