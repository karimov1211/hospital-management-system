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
                        print("Auto-migration started...")
                        call_command('migrate', interactive=False)
                        
                        from api.seeder import seed_database
                        seed_database()
                    except Exception as e:
                        print(f"Auto-seeding error: {e}")
                
                threading.Thread(target=seed_db, daemon=True).start()


