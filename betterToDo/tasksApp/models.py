from django.db import models
from django.contrib.auth.models import AbstractUser

TASK_NATURE_CHOICES = [
    ("goal", "Goal"),
    ("problem", "Problem"),
    ("action", "Action"),
]

TASK_STATUS_CHOICES = [
    ("active", "Active"),
    ("resolved", "Resolved"),
    ("pending", "Pending"),
    ("omitted", "Omitted"),
]

COMMENT_NATURE_CHOICES = [
    ("comment", "Comment"),
    ("decision", "Decision"),
    ("resources", "Resources"),
]

PROJECT_STATUS_CHOICES = [
    
]


'''# a User model
    # name
    # email
    # '''
class User(AbstractUser):
    user_email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.username

''' # a Project model
    # title
    # Task models that belong to this project
    # collaborators : list of Users
    # manager: 1 User
'''
class Project(models.Model):
    project_title = models.CharField(max_length=20, blank=False, null=False)
    child_tasks = models.ManyToManyField("Task", related_name="parent_project")
    collaborators = models.ManyToManyField(User, related_name="project_involved")
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, related_name="projects_managed") 
    '''# additional feature in future: if manager is NULL 
        # either prompt action to set new manager in message
        # add a function to get the oldest collaborator to be the manager (if there is collaborator)'''
    
    def __str__(self):
        return self.project_title


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
    task_name = models.CharField(max_length=255, blank=False, null=False)
    priority = models.IntegerField(default=0)
    parent_task = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="child_tasks")
    dependent_task = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="task_up_next")
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="project_tasks", null=True, blank=True)
    task_status = models.CharField(max_length=10, choices=TASK_STATUS_CHOICES, default="pending")
    date_created = models.DateTimeField(auto_now_add=True)
    date_complete = models.DateTimeField(null=True, blank=True)
    estimate_time = models.IntegerField(default=0)  # In hours/ days?
    deadline = models.DateField(null=True, blank=True)

    person_in_charge = models.ManyToManyField("User", related_name="tasks_assigned", blank=True)

    # Removed task_comment, task_decision, task_resources

    def __str__(self):
        return f"{self.task_name} ({self.task_nature})"



class Comment(models.Model):
    comment_nature = models.CharField(max_length=10, choices=COMMENT_NATURE_CHOICES, blank=False, null=False)
    author = models.ForeignKey("User", on_delete=models.DO_NOTHING, related_name="comments_made")
    task = models.ForeignKey("Task", on_delete=models.DO_NOTHING, related_name="task_comments", null=True, blank=True)
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="project_comments", null=True, blank=True)
    content = models.TextField(blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.task_name if self.task else self.project.project_title}"
