from django.apps import AppConfig


class TasksappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasksApp'
    
    def ready(self):
        import tasksApp.signals  # 💡 Import the signals here
