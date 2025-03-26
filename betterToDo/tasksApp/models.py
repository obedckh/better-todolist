from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

TASK_NATURE_CHOICES = [
    ("project", "Project"),
    ("goal", "Goal"),
    ("problem", "Problem"),
    ("action", "Action"),
]

TASK_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("active", "Active"),
    #("complete", "Complete"),
]

COMMENT_NATURE_CHOICES = [
    ("general", "General"),
    ("decision", "Decision"),
    ("resources", "Resources"),
]


'''# a User model
    # name
    # email
    # '''
class User(AbstractUser):
    user_email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.username


'''# a Task model
    # nature : 1) goal 2) problem/ issue or 3) action - depends on nature, the other attributes are a bit different ?
    # title
    # prority : depending on number of tasks in the same branch
    # branch : superior tasks this task belongs to (action(s) that belongs to a problem that belongs to a goal)
    # dependency : another task(s) that need to be done before this
    # status : active(working)/ resolved/ pending/ omitted
    # date created
    # estimate work time
    # date finished
    # PIC : list of User(s)
    # comment/ review
    # decision/ reason
    # resources/ information
    '''
class Task(models.Model):
    task_nature = models.CharField(max_length=10, choices=TASK_NATURE_CHOICES, blank=False, null=False)
    task_name = models.CharField(max_length=50, blank=False, null=False)
    priority = models.IntegerField(default=0)
    
    parent_task = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="child_tasks")
    
    dependent_task = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="task_up_next")
    
    task_status = models.CharField(max_length=10, choices=TASK_STATUS_CHOICES, default="pending")
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_complete = models.DateTimeField(null=True, blank=True)
    estimate_time = models.IntegerField(default=0)  # In hours/ days?
    deadline = models.DateField(null=True, blank=True)

    person_in_charge = models.ManyToManyField("User", related_name="tasks_assigned", blank=True)
    
    manager = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name="managed_projects")
    
    collaborators = models.ManyToManyField("User", related_name="project_involved", blank=True)
    
    omitted = models.BooleanField(blank=False, null=False, default=False)
    complete = models.BooleanField(blank=False, null=False, default=False)

    # Removed task_comment, task_decision, task_resources
    
    def clean(self):
        """Validation logic to enforce rules based on `task_nature`."""
        if self.task_nature == "project":
            # A "Project" **must** have a manager
            if self.manager is None:
                raise ValidationError({"manager": "A project must have a manager."})
            # A "Project" **must not** have a parent task
            if self.parent_task is not None:
                raise ValidationError({"parent_task": "A project cannot have a parent task."})
        super().clean()

    def save(self, *args, **kwargs):
        """Ensure clean() is always called before saving."""
        self.clean()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.task_name} ({self.task_nature})"



class Comment(models.Model):
    comment_nature = models.CharField(max_length=10, choices=COMMENT_NATURE_CHOICES, blank=False, null=False)
    author = models.ForeignKey("User", on_delete=models.DO_NOTHING, related_name="comments_made")
    task = models.ForeignKey("Task", on_delete=models.DO_NOTHING, related_name="task_comments", null=True, blank=True)
    project = models.ForeignKey("Task", on_delete=models.DO_NOTHING, related_name="project_comments", null=True, blank=True)
    content = models.TextField(blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.task_name if self.task else self.project.task_name}"
