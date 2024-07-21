from django.utils import timezone
from django.db import models

# Create your models here.
from basemodel.base_user_model import BaseModel
from my_account.custom_user_manager import MyUserManager
import uuid
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin


class User(AbstractBaseUser,PermissionsMixin,BaseModel):
    PASSENGER='Passenger'
    DRIVER='Driver'

    GENDER_CHOICES = (
        ('Male','Male'),
        ('Female','Female')
    )
    
    USER_TYPE_CHOICES = (
        (PASSENGER, PASSENGER),
        (DRIVER, DRIVER),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    username = models.CharField(unique=True,max_length=20)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=200,unique=True,blank=True,null=True)
    phone_number = models.CharField(unique=True,max_length=10,null=True)
    is_staff = models.BooleanField(
     
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        default=True,
    )
    date_joined = models.DateTimeField(default=timezone.now,editable=False)
    

    def __str__(self):
        return self.email
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone_number",]

    objects = MyUserManager()

    def __str__(self):
        return self.username
    
class DriverProfile(BaseModel):
    PROVINCE1 = 'Province 1'
    MADHESPRADESH = 'Madhesh Pradesh'
    BAGMATI = 'Bagmati'
    GANDAKI = 'Gandaki'
    LUMBINI = 'Lumbini'
    KARNALI = 'Karnali'
    SUDURPASCHIM = 'Sudurpaschim'

    PROVINCE_CHOICES = (
        (PROVINCE1,PROVINCE1),
        (MADHESPRADESH,MADHESPRADESH),
        (BAGMATI,BAGMATI),
        (GANDAKI,GANDAKI),
        (LUMBINI,LUMBINI),
        (KARNALI,KARNALI),
        (SUDURPASCHIM,SUDURPASCHIM)
    )

    GENDER_CHOICES = (
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driverprofile')
    province = models.CharField(choices=PROVINCE_CHOICES,max_length=15)
    city= models.CharField(max_length=30)
    date_of_birth = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES,max_length=6)
    citizenship_number = models.CharField(max_length=20,unique=True)
    avatar = models.ImageField(upload_to='profile')
   

    def __str__(self):
        return f"{self.user.username} - Driver"
    
class UserProfile(BaseModel):
    PROVINCE1 = 'Province 1'
    MADHESPRADESH = 'Madhesh Pradesh'
    BAGMATI = 'Bagmati'
    GANDAKI = 'Gandaki'
    LUMBINI = 'Lumbini'
    KARNALI = 'Karnali'
    SUDURPASCHIM = 'Sudurpaschim'

    PROVINCE_CHOICES = (
        (PROVINCE1,PROVINCE1),
        (MADHESPRADESH,MADHESPRADESH),
        (BAGMATI,BAGMATI),
        (GANDAKI,GANDAKI),
        (LUMBINI,LUMBINI),
        (KARNALI,KARNALI),
        (SUDURPASCHIM,SUDURPASCHIM)
    )

    GENDER_CHOICES = (
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    province = models.CharField(choices=PROVINCE_CHOICES,max_length=15,blank=True,null=True)
    city= models.CharField(max_length=30,blank=True,null=True)
    date_of_birth = models.DateField(null=True,blank=True)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=6,null=True,blank=True)
    avatar = models.ImageField(upload_to='profile',blank=True,null=True)

    
class Vehicle(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='drivervehicle')
    driving_license_number = models.CharField(max_length=20,unique=True)
    vehicle_registration_number = models.CharField(max_length=50,unique=True)
    chassis_number = models.CharField(max_length=30,unique=True)
    verification_status = models.BooleanField(default=False)
    fare_per_meter = models.DecimalField(max_digits=6, decimal_places=2,default=0.00)

class Card(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    expiry_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return f"{self.user.username} - {self.card_number}"
    

class GeneratedOtp(BaseModel):

    REGISTRATION = "Reg"
    PASSWORD_RESET = "Pwd"
    OTP_RESENT = "OtpResent"

    OtpCodeChoices = (
        (REGISTRATION,REGISTRATION),
        (PASSWORD_RESET,PASSWORD_RESET),
        (OTP_RESENT,OTP_RESENT)
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    otp_type = models.CharField(choices=OtpCodeChoices,max_length=15,default=REGISTRATION)
    

    class Meta:
        ordering = ['-created_at']

