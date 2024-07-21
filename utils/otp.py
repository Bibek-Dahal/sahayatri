import random
from django.utils import timezone
from datetime import timedelta  
from my_account.models import GeneratedOtp

def generate_otp():
    otp = random.randint(100000, 999999)
    return otp

def send_otp(user,message,expire_minutes,otp_code,otp_type):
    print("send_otp_called")
    
    expires_at = timezone.now() + timedelta(minutes=expire_minutes)

    try:
        message = message
        # res = requests.post(f"https://sarbatrasms.com/sms/api?action=send-sms&api_key={otp_obj.api_key}&to={user.phone_number}&sms={message}")
        otp_instance = GeneratedOtp(
                        user=user,
                        otp_code=otp_code,
                        expires_at=expires_at,
                        otp_type=otp_type
                    )
        
        otp_instance.save()
        print("Otp sent successfully")
        # print("otp_status_code",res.status_code)
    except Exception as e:
        print("cant send sms",e)
        
  