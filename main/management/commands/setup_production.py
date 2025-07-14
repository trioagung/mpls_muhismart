from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Setup production environment dengan database dan admin user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--admin-email',
            type=str,
            help='Email untuk admin user',
            default='admin@example.com'
        )
        parser.add_argument(
            '--admin-password',
            type=str,
            help='Password untuk admin user',
            default='admin123'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Setting up MPLS MuhiSmart Production Environment...')
        )

        # Run migrations
        self.stdout.write('📦 Running migrations...')
        call_command('migrate', verbosity=0)
        
        # Create cache table
        self.stdout.write('⚡ Setting up cache...')
        try:
            call_command('createcachetable', verbosity=0)
        except:
            pass  # Table might already exist

        # Collect static files
        self.stdout.write('📁 Collecting static files...')
        call_command('collectstatic', '--noinput', verbosity=0)

        # Create superuser if doesn't exist
        admin_email = options['admin_email']
        admin_password = options['admin_password']
        
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('👤 Creating admin user...')
            User.objects.create_superuser(
                username='admin',
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(
                self.style.WARNING(f'Admin user created: admin / {admin_password}')
            )
            self.stdout.write(
                self.style.WARNING('⚠️  PLEASE CHANGE PASSWORD IMMEDIATELY!')
            )
        else:
            self.stdout.write('👤 Admin user already exists.')

        # Show important URLs
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('✅ Production setup completed!'))
        self.stdout.write('\n📋 Important URLs:')
        self.stdout.write('   🔧 Admin Panel: /admin/')
        self.stdout.write('   🏠 Dashboard: /')
        self.stdout.write('   📊 Absensi: /panitia/absensi/')
        self.stdout.write('   🔐 Login: /accounts/login/')
        
        self.stdout.write('\n🔒 Security Checklist:')
        self.stdout.write('   ✓ Change admin password')
        self.stdout.write('   ✓ Set strong SECRET_KEY')
        self.stdout.write('   ✓ Configure ALLOWED_HOSTS')
        self.stdout.write('   ✓ Enable HTTPS in production')
        self.stdout.write('   ✓ Setup regular database backups')
        
        self.stdout.write('='*50)
