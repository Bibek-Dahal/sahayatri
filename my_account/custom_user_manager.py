from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given phone number, username, and password.
        """
        if not phone_number:
            raise ValueError(_("Phone number must be set."))
        
        if not username:
            raise ValueError(_("Username must be set."))
        
        # Check if user with the same username already exists
        if self.model.objects.filter(username=username).exists():
            raise ValueError(_("User with this username already exists."))
    
        # Check if user with the same phone number already exists
        if self.model.objects.filter(phone_number=phone_number).exists():
            raise ValueError(_("User with this phone number already exists."))
        
        user = self.model(
            phone_number=phone_number,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given phone number, username, and password.
        """
        from .models import User
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', User.PASSENGER)

        try:
            return self.create_user(phone_number, username, password, **extra_fields)
        except ValueError as e:
            raise ValidationError(str(e))  # or use str(e) for the error message

