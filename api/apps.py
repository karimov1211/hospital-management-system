from django.apps import AppConfig
import os
import sys

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Only run when serving the application (not during management commands like makemigrations)
        is_manage = any(cmd in sys.argv for cmd in ['makemigrations', 'migrate', 'collectstatic'])
        if not is_manage:
            # Avoid double execution with Django reloader
            if os.environ.get('RUN_MAIN') != 'true':
                import threading
                def seed_db():
                    from django.core.management import call_command
                    try:
                        print("Auto-migration and database seeding started...")
                        call_command('migrate', interactive=False)
                        
                        from api.models import Doctor, Patient, Queue
                        # Clear old records to prevent old entries showing up
                        Queue.objects.all().delete()
                        Doctor.objects.all().delete()
                        Patient.objects.all().delete()
                        
                        # Load data
                        call_command('loaddata', 'api/fixtures/initial_data.json', interactive=False)
                        print("Database successfully migrated and seeded with 24 student records!")
                    except Exception as e:
                        print(f"Auto-seeding error: {e}")
                
                threading.Thread(target=seed_db, daemon=True).start()

