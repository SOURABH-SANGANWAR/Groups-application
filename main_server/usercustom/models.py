from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from .manager import *
import uuid

def get_image_name(instance, filename):
    """
    This is a function to manage profile images names.
    It will be used as a parameter in the upload_to field of the profile_picture field.

    Parameters:
        instance (User): The user instance.
        filename (str): The name of the file.
    
    Returns:
        str: The path where the image will be stored.
    """
    print(filename)
    if filename == '' or filename == None:
        return f'profile_pictures/default.png'
    extension = filename.split('.')[-1]
    current_timestamp = datetime.datetime.now().timestamp()
    email_prefix = instance.email.split('@')[0]
    return f'profile_pictures/{email_prefix}/{current_timestamp}.{extension}'

class CustomUser(AbstractUser):
    """
    This class is a custom user model.
    It inherits from the AbstractUser class.
    
    Attributes:
        email (EmailField): The user's email.
        username (CharField): The user's username.
        is_active (BooleanField): A boolean field to indicate if the user is active or not.
        first_name (CharField): The user's first name.
        last_name (CharField): The user's last name.
        profile_picture (ImageField): The user's profile picture.
        password (CharField): The user's password.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.TextField(null=True, blank = True)
    profile_picture = models.ImageField(upload_to=get_image_name, default = 'profile_pictures/default.png')
    is_activated = models.BooleanField(default=True)

    USERNAME_FIELD =  'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    objectsall = UserManager()
    objects = UserManagerfiltered()