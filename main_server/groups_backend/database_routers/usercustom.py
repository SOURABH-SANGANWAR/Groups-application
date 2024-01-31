# # import database names from settings
# from django.conf import settings
from usercustom.models import CustomUser
# class UserCustomRouter:
#     def db_for_read(self, model, **hints):
#         if model._meta.app_label == 'usercustom':
#             return settings.DATABASES['default']
#         return None
    
#     def db_for_write(self, model, **hints):
#         if model._meta.app_label == 'usercustom':
#             return settings.DATABASES['default']
#         return None

# class GroupCustomRouter:
#     def db_for_read(self, model, **hints):
#         if model._meta.app_label == 'groupcustom':
#             return settings.DATABASES['default']
#         return None
    
#     def db_for_write(self, model, **hints):
#         if model._meta.app_label == 'groupcustom':
#             return settings.DATABASES['default']
#         return None

# class GroupCustomRouter1:
#     def db_for_read(self, model, **hints):
#         if model._meta.app_label == 'groupcustom':
#             return settings.DATABASES['groups_1']
#         return None
    
#     def db_for_write(self, model, **hints):
#         if model._meta.app_label == 'groupcustom':
#             return settings.DATABASES['groups_1']
#         return None

# class ThreadRouter:
#     def db_for_read(self, model, **hints):
#         if model._meta.app_label == 'thread':
#             return settings.DATABASES['default']
#         return None


class GroupsRouter:
    def db_for_read(self, model, **hints):
        return 'default'
    
    def db_for_write(self, model, **hints):
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        return True
