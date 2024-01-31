from django.db import models
from usercustom.models import CustomUser
import datetime
import random
from django.conf import settings
from django.core.mail import send_mail
import string
import uuid

# Create your models here.

class Otpdetails(models.Model):
    """
    This model is used to store the otp details of the user
    This also used to verify email of new users.
    
    Attributes:
        
        user (ForeignKey): The user for which the otp is generated.
        otp (CharField): The otp generated for the user.
        time (DateTimeField): The time at which the otp is generated.
        link_string (CharField): The link string generated for the user.
        is_active (BooleanField): A boolean field to indicate if the otp is active or not."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6,blank=True,null=True)
    time = models.DateTimeField(blank=True,null=True)
    link_string = models.CharField(max_length=20,blank=True,null=True)
    is_active = models.BooleanField(default=True)

    def setup(self):
        """
        This function is used to setup the otp details of the user.
        """
        self.time = datetime.datetime.now()
        self.otp = str(random.randint(234567,999999))
        self.link_string = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase +string.digits, k=20))
        self.is_active = True
        self.save()
        print('OTP: ', self.otp)
        if self.user.is_activated:
            send_mail('Login OTP for groups', f'Dear {str(self.user)},\n\nYour OTP is {self.otp}.\n \n If you didnt request for email click here to invalidate link : {settings.HOSTNAME}:{settings.PORT}/validation/invalidate/{self.user.email}/{self.link_string}', settings.EMAIL_HOST_USER, [self.user.email], fail_silently=False)
        else:
            send_mail('Verify your email | Groups', f'Dear {str(self.user)},\n\nWelcome to Groups.\n\n Please click link below to validate your email.\n link: {settings.HOSTNAME}:{settings.PORT}/validation/verify/{self.user.email}/{self.link_string}.\n If you didnt request for email click here to invalidate link : {settings.HOSTNAME}:{settings.PORT}/validation/invalidate/{self.user.email}/{self.link_string}', settings.EMAIL_HOST_USER, [self.user.email], fail_silently=False)
    
    def validate_string(self, link_str):
        """
        This function is used to validate the link string.
        """
        current_time = datetime.datetime.now()
        current_time = current_time.replace(tzinfo=datetime.timezone.utc)
        difference = current_time - self.time 
        min = difference.total_seconds()/60
        if min>=15:
            return False
        else:
            return (link_str == self.link_string) and self.is_active
    
    def invalidate(self):
        """
        This function is used to invalidate the otp.
        """
        self.is_active = False
        self.save()
        return True

    def is_valid_otp(self,otp):
        """
        This function is used to check otp and validity.
        """
        current_time = datetime.datetime.now()
        current_time = current_time.replace(tzinfo=datetime.timezone.utc)
        difference = current_time - self.time 
        min = difference.total_seconds()/60
        if min>=2:
            return False
        else:
            return True and ((str(otp) == self.otp) and self.is_active)

    
