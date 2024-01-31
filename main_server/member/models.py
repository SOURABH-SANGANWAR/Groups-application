from django.db import models
from usercustom.models import CustomUser
from group.models import Group
from permissions.models import RolePermission
import uuid
# Create your models here.


class GroupMember(models.Model):
    """
    This class is a model for a group member instance.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='group_members', blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_members')
    role = models.ForeignKey(RolePermission, on_delete=models.CASCADE, related_name='group_members')
    email_id = models.EmailField(max_length=254, blank=True, null=True)
    username = models.CharField(max_length=254, blank=True, null=True)
    is_banned = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=False)
    is_invited = models.BooleanField(default=False)
    profile_picture = models.CharField(max_length=254, blank=True, null=True)

    def __str__(self):
        if self.user == None:
            return self.group.name
        return self.user.username + ' - ' + self.group.name
            

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'group'], name='unique_group_member')
        ]
    
    def save(self, *args, **kwargs):
        """
        This method overrides the save method of the model.
        It saves the user instance in the group's database region.
        """
        super(GroupMember, self).save(*args, **kwargs)
        self.user.save(using = self.group.db_region)
        super(GroupMember, self).save(using = self.group.db_region)
