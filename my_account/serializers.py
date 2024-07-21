from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from my_account.models import User,Vehicle,DriverProfile
import re
from django.core.exceptions import ValidationError

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data.update({
                "id": self.user.id,
                "username":self.user.username,
                'phone_number':self.user.phone_number,
                'is_superuser':self.user.is_superuser,
                'full_name':self.user.full_name,
                'email':self.user.email,
                'is_staff':self.user.is_staff,
                'user_type':self.user.user_type
                
            }),
            
        return data
    

class OtpVerifySerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=10)
    phone_number = serializers.CharField(max_length=10)
    otp_type = serializers.CharField(max_length=10)


class OtpCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=10)

    def validate_phone_number(self,value):
        try:
            int(value)
            if len(value) < 10:
                raise serializers.ValidationError("Please enter valid phone number")
            return value
        except Exception as e:
            print(e)
            raise serializers.ValidationError("Please enter valid phone number")
        print("phone validate called")




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        
        exclude = ['password']

class UserUpdateSerializer(serializers.ModelSerializer):

    """
        Not for admin site for general user
    """
    class Meta:
        model = User
        fields = ('username','full_name','email','phone_number','gender','date_of_birth')
       



class CustomUserCreationSerializer(serializers.ModelSerializer):

    phone_number = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True) 
    class Meta:
        model = User
        fields = ('id','username','phone_number','full_name','password1','password2')
       
       

    # def clean_username(self):
        
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get('email')
    #     check_username = re.findall("[a-zA-Z]",cleaned_data.get('username'))
    #     if not check_username:
    #         raise ValidationError('Enter valid username')
    #     return username

    def validate_phone_number(self,phone_number):
        if not phone_number.isdigit():
            raise ValidationError('Phone number should contain only digits')
        
        if len(str(phone_number)) != 10:
            raise ValidationError('Phone number should be of 10 digits')
        
        return phone_number

    def validate_password2(self,password2):
        
        pwd = password2
        if len(pwd) >= 8:
            reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
            pat = re.compile(reg)
            mat = re.search(pat, pwd)
            if not mat:
                raise ValidationError('Password must contain atleats one digit special characrers and uppercase letter')
            return pwd
        
    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data.get('username'),
            password = validated_data['password1'],
            phone_number = validated_data.get('phone_number'),
            is_active=False
        )

        
        user.set_password(validated_data['password1'])
        user.save()

        return user
 
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['driving_license_number','vehicle_registration_number','chassis_number']        
   

class DriverProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverProfile
        fields = ['province','city','date_of_birth','gender','citizenship_number','avatar']
        
class CustomDriverCreationSerializer(serializers.ModelSerializer):
    driverprofile = DriverProfileSerializer()
    drivervehicle = VehicleSerializer()

    phone_number = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True) 
    class Meta:
        model = User
        fields = ('id','username','phone_number','full_name','password1','password2','driverprofile','drivervehicle')
    

    def create(self, validated_data):
        print(validated_data)
        profile_data = validated_data.pop('driverprofile')
        vehicle_data = validated_data.pop('drivervehicle')

        user = User.objects.create_user(
            username=validated_data.get('username'),
            full_name=validated_data.get('full_name'),
            password = validated_data['password1'],
            phone_number = validated_data.get('phone_number'),
            user_type = User.DRIVER,
            is_active=False
        )

        
        user.set_password(validated_data['password1'])
        user.save()

        
        DriverProfile.objects.create(user=user,**profile_data)
        Vehicle.objects.create(user=user,**vehicle_data)
        return user
  
    def validate_phone_number(self,phone_number):
        if not phone_number.isdigit():
            raise ValidationError('Phone number should contain only digits')
        
        if len(str(phone_number)) != 10:
            raise ValidationError('Phone number should be of 10 digits')
        
        return phone_number

    def validate_password2(self,password2):
        
        pwd = password2
        if len(pwd) >= 8:
            reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
            pat = re.compile(reg)
            mat = re.search(pat, pwd)
            if not mat:
                raise ValidationError('Password must contain atleats one digit special characrers and uppercase letter')
            return pwd
        
    # def create(self, validated_data):
        
    #     user = User.objects.create_user(
    #         username=validated_data.get('username'),
    #         password = validated_data['password1'],
    #         phone_number = validated_data.get('phone_number'),
    #         is_active=False
    #     )

        
    #     user.set_password(validated_data['password1'])
    #     user.save()

    #     return user
