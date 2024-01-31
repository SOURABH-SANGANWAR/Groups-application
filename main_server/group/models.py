from django.db import models
from usercustom.models import CustomUser
import datetime
import uuid
from django.conf import settings

# Create your models here.
database_choices = settings.DATABASES.keys()
database_choices = list(database_choices)
database_choices.remove('default')
database_choices = tuple([(database, database) for database in database_choices])

class DeletedManager(models.Manager):
    """
    This class is a manager for deleted groups.
    """
    def get_queryset(self):
        """
        This function is used to get deleted groups.
        
        Returns:
            QuerySet: The deleted groups.
        """
        return super().get_queryset().filter(is_deleted=True)

class ActiveManager(models.Manager):
    """
    This class is a manager for active groups.
    """
    def get_queryset(self):
        """
        This function is used to get active groups.
        
        Returns:
            QuerySet: The active groups.
        """
        return super().get_queryset().filter(is_deleted=False)
    

def get_groups_image_name(instance, name):
    """
    This function is used to get the image name of a group.

    Parameters:
        instance (Group): The group.
        name (str): The name of the image.

    Returns:
        str: The path where the image will be stored.
    """
    extension = name.split('.')[-1]
    current_timestamp = datetime.datetime.now().timestamp()
    return f'groups/{instance.name}/{str(instance.created_by)}/{current_timestamp}.{extension}'

class Group(models.Model):
    """
    This class is a model for a group.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='updated_groups', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='deleted_groups', null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_public_view = models.BooleanField(default=False)
    is_public_join = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    email = models.EmailField(blank = True, null=True)
    email_password = models.CharField(max_length=255, blank=True, null=True)
    is_email_validated = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to=get_groups_image_name, blank=True, null=True)
    db_region = models.CharField(max_length=255, blank=True, null=True, choices=database_choices)

    objects = ActiveManager()
    deleted_objects = DeletedManager()

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['name', 'created_by', 'is_deleted'], name='unique_group_name_per_creator')
        ]
    
    def soft_delete(self, user):
        """
        This function is used to soft delete a group.

        Parameters:
            user (CustomUser): The user who is deleting the group.
        """
        self.is_deleted = True
        self.deleted_by = user
        self.deleted_at = datetime.datetime.now()
        self.save()
    

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """
        This function is used to save a group.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        
        Returns:
            Void
        """
        print("Saving group")
        if(self.db_region is not None):
            if self.created_by is not None:
                self.created_by.save(using = self.db_region)
            if self.updated_by is not None:
                self.updated_by.save(using = self.db_region)
            if self.deleted_by is not None:
                self.deleted_by.save(using = self.db_region)
            super(Group, self).save(using = self.db_region)
        super(Group, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """
        This function is used to delete a group.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            VOid
        """
        if self.db_region is not None:
            super(Group, self).delete(using = self.db_region)
        super(Group, self).delete(*args, **kwargs)
        
