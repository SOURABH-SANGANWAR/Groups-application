import os
import subprocess

# Run command 1
subprocess.call("ls -l", shell=True)

# Delete all migration files except for __init__.py
for app in ['group', 'usercustom', 'member', 'permissions']:
    if os.path.isdir(app) and os.path.exists(os.path.join(app, 'migrations')):
        subprocess.call(f'python manage.py migrate {app} zero')