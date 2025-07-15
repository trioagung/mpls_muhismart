import subprocess
import sys

# Jalankan command untuk memberikan permission
commands = [
    'python manage.py shell -c "from django.contrib.auth.models import User; from panitia.models import AksesMenu; admin = User.objects.filter(username=\'admin\').first(); print(f\'Admin user: {admin}\')"',
]

for cmd in commands:
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"Command: {cmd}")
        print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Error running command: {e}")
