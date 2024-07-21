from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from utils.otp import generate_otp,send_otp
from .permissions import IsOwnerOrReadOnly
from django.utils import timezone
from .models import GeneratedOtp
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView
from .serializers import *
from rest_framework.parsers import FormParser,MultiPartParser
# Create your views here.
User = get_user_model()
# Create your views here.
class DriverRegistrationView(CreateAPIView):
    parser_classes = [FormParser,MultiPartParser]
    permission_classes = [AllowAny]
    serializer_class = CustomDriverCreationSerializer
    throttle_scope = 'registration'



class PassengerRegistrationView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = CustomUserCreationSerializer
    throttle_scope = 'registration'

class LoginView(TokenObtainPairView):
    
    serializer_class = CustomTokenObtainPairSerializer

class UserRetriveUpdateApiView(RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserUpdateSerializer
        return UserSerializer
    
class VerifyUserOtp(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = OtpVerifySerializer(data=request.data)
        if(serializer.is_valid(raise_exception=True)):
            print(request.data)
            user = User.objects.filter(phone_number=request.data.get('phone_number')).first()
            print("user===",user)
            print("timezone.now",timezone.now())
            if user:
                otp = GeneratedOtp.objects.filter(otp_type=request.data.get('otp_type'),user=user,otp_code=request.data.get('otp_code')).last()
                if otp and not otp.is_used and otp.expires_at > timezone.now():
                    otp.is_used = True
                    otp.save()
                    print("otp-not-expired")
                    user.is_active = True
                    user.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    print("otp-expired---")
                    return Response({'detail':'OTP couldnot be validated'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail':'OTP couldnot be validated'},status=status.HTTP_400_BAD_REQUEST)





class ResendOtpcode(APIView):
    permission_classes = [AllowAny]
    throttle_scope = 'otp_resent'
    def post(self,request):
        serializer = OtpCodeSerializer(data=request.data)
        try:
            if serializer.is_valid():
                print(request.data.get('phone_number'))
                # print(User.objects.all())
                user = User.objects.filter(phone_number=request.data.get('phone_number')).first()
                if user and not user.is_active:
                    print("user not active")
                    print(user.full_name)
                    print(user.phone_number)
                    otp_code = generate_otp()
                    message = f"Hello {user.full_name} thank you for registering to our site.Please verify your phone number. Your OTP code is {otp_code}. Please do not share the code with anyone else."
                    send_otp(otp_type=GeneratedOtp.OTP_RESENT,user=user,otp_code=otp_code,message=message,expire_minutes=1)
                    
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("server error",e)
            return Response(status=status.HTTP_200_OK)
