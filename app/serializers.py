from rest_framework import serializers
from .models import Employee, Task


class TaskSerializer(serializers.ModelSerializer):
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    employee_name = serializers.CharField(source='employee.name', read_only=True)


class Meta:
    model = Task
    fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'department', 'tasks']