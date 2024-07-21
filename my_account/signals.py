from django.dispatch import receiver

from utils.otp import generate_otp,send_otp
from .models import User,Card,UserProfile,GeneratedOtp
from django.db.models.signals import pre_save,post_save
from utils.card import generate_unique_card_number

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type == User.PASSENGER:
            # creates user profile on passenger save
            UserProfile.objects.create(user=instance)

        # creates user card on passenger save
        Card.objects.create(user=instance,card_number=generate_unique_card_number())


        otp_code = generate_otp()
        message = f"Hello {instance.full_name} thank you for registering to our site.Please verify your phone number. Your OTP code is {otp_code}. Please do not share the code with anyone else."
        send_otp(user=instance,expire_minutes=10,otp_code=otp_code,message=message,otp_type=GeneratedOtp.REGISTRATION)


