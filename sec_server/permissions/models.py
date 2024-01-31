from django.db import models
from group.models import Group
import uuid
# Create your models here.


class RolePermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_name = models.CharField(max_length=255)
    role_description = models.TextField()
    is_default = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='role_permissions')
    post_as_group = models.BooleanField(default=False)
    manage_members = models.BooleanField(default=False)
    manage_content = models.BooleanField(default=False)
    manage_metadata = models.BooleanField(default=False)
    can_post = models.BooleanField(default=True)
    manage_roles = models.BooleanField(default=False)
    reply_to_authors = models.BooleanField(default=True)
    attach_files = models.BooleanField(default=True)
    view_member_email_addresses = models.BooleanField(default=False)

    def __str__(self):
        return self.role_name + ' - ' + self.group.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['role_name', 'group'], name='unique_role_name'),
            models.UniqueConstraint(fields=['is_default', 'group'], condition=models.Q(is_default=True),  name='unique_default_role')
        ]
