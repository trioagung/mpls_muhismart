#!/usr/bin/env python3
"""
Script untuk deploy otomatis ke PythonAnywhere
Jalankan script ini untuk pull perubahan terbaru dari GitHub
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run command dan tampilkan output"""
    print(f"\n🔄 {description}...")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print("Output:", result.stdout)
        
        if result.stderr:
            print("Error/Warning:", result.stderr)
            
        if result.returncode != 0:
            print(f"❌ Command failed with return code {result.returncode}")
            return False
        else:
            print(f"✅ {description} berhasil!")
            return True
            
    except Exception as e:
        print(f"❌ Error executing command: {e}")
        return False

def main():
    print("🚀 Starting deployment to PythonAnywhere...")
    
    # Commands untuk deploy
    commands = [
        ("git status", "Checking git status"),
        ("git fetch origin", "Fetching latest changes from GitHub"),
        ("git pull origin main", "Pulling latest changes"),
        ("python manage.py collectstatic --noinput", "Collecting static files"),
        ("python manage.py migrate", "Running database migrations"),
    ]
    
    # Execute commands
    for command, description in commands:
        if not run_command(command, description):
            print(f"❌ Deployment failed at: {description}")
            sys.exit(1)
    
    print("\n✅ Deployment completed successfully!")
    print("\n📝 Next steps:")
    print("1. Login ke PythonAnywhere console")
    print("2. Navigate ke direktori project Anda")
    print("3. Jalankan script ini dengan: python deploy_to_pythonanywhere.py")
    print("4. Atau jalankan commands manual:")
    for command, _ in commands:
        print(f"   {command}")
    print("5. Restart web app di PythonAnywhere dashboard")

if __name__ == "__main__":
    main()
