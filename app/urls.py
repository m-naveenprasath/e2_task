from django.urls import path
from .views import (
    UploadCSVView, StatsView, VisualsView,
    TotalHoursPerDepartmentAPI, CompletionPercentageAPI,
    TopEmployeesAPI, DelayedTasksAPI, AverageHoursCompletedAPI,
    TaskTrendAPI
)

urlpatterns = [
    path('upload/', UploadCSVView.as_view(), name='upload_csv'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('visuals/', VisualsView.as_view(), name='visuals'),

    # 🔹 New JSON analytics endpoints
    path('analytics/total-hours/', TotalHoursPerDepartmentAPI.as_view()),
    path('analytics/completion-percentage/', CompletionPercentageAPI.as_view()),
    path('analytics/top-employees/', TopEmployeesAPI.as_view()),
    path('analytics/delayed-tasks/', DelayedTasksAPI.as_view()),
    path('analytics/average-hours-completed/', AverageHoursCompletedAPI.as_view()),
    path('analytics/task-trend/', TaskTrendAPI.as_view()),
]
