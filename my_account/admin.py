from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
from .models import  *
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    list_display = ('id','username','email', 'full_name','date_joined','is_active')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('username','full_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        # (_('Important dates'), {'fields': ( 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','password1', 'password2'),
        }),
    )
    ordering = ['phone_number']


admin.site.register(User, CustomUserAdmin)


@admin.register(GeneratedOtp)
class GeneratedOtpAdmin(admin.ModelAdmin):
    list_display = ['id','user','otp_code','otp_type','expires_at','is_used','created_at']

@admin.register(UserProfile)
class PassengerProfileAdmin(admin.ModelAdmin):
    list_display = ['user','province','city','date_of_birth','gender','avatar']
 

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ['user','province','city','date_of_birth','gender','citizenship_number','avatar']
 
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['id','user','fare_per_meter','driving_license_number','vehicle_registration_number','chassis_number','verification_status']

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['user','card_number','balance','expiry_date']


