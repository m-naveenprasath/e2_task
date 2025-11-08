from django.db import models

class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.department})"

class Task(models.Model):
    task_id = models.CharField(max_length=20, unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tasks')
    task_name = models.CharField(max_length=100)
    hours_spent = models.FloatField(default=0)
    deadline = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.task_name} ({self.status})"
