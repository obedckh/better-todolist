from django.db import models
from django.contrib.auth.models import AbstractUser

TASK_NATURE = ("goal", "problem", "action")
TASK_STATUS = ("active", "resolved", "pending", "omitted")
# Create your models here.

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
    task_nature = models.CharField()
    task_name = models.CharField(max_length=20, blank=False, null=False)
    priority = models.IntegerField()
    parent_task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="child_tasks")
    dependent_task = models.ManyToManyField("Task", related_name="task_up_next")
    task_status = models.CharField()
    date_created = models.DateTimeField(auto_created=True)
    date_complete = models.DateTimeField()
    estimate_time = models.IntegerField()
    deadline = models.DateField()
    person_in_charger = models.ManyToManyField("User", related_name="task_involved")
    task_comment = models.TextField()
    task_decision = models.TextField()
    task_resources = models.TextField()
    
    def __str__(self):
        return self.task_name


