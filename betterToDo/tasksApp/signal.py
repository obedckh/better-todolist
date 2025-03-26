from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Comment

@receiver(pre_save, sender=Comment)
def auto_assign_project(sender, instance, **kwargs):
    """
    Automatically assigns the correct project based on where the comment is created.
    """
    if instance.task:
        task = instance.task
        # Traverse up to find the first-level project
        while task.parent_task:
            if task.parent_task.task_nature == "project":
                instance.project = task.parent_task
                break
            task = task.parent_task
    elif instance.project:
        # If created inside a project container, ensure task is None
        instance.task = None
