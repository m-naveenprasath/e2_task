import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from .models import Employee, Task
from .utils import process_csv, compute_metrics
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# ✅ Prevent Tkinter “main thread” errors (use non-GUI backend)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt



@method_decorator(csrf_exempt, name='dispatch')
class UploadCSVView(View):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        # ✅ Save uploaded file to media/uploads/
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.name)

        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # ✅ Process CSV
        df = process_csv(file_path)
        employees_created, employees_updated = 0, 0
        tasks_created, tasks_updated = 0, 0

        for _, row in df.iterrows():
            # --- EMPLOYEE ---
            emp, created_emp = Employee.objects.get_or_create(
                employee_id=row['employeed_id'],
                defaults={
                    'name': row['employee_name'],
                    'department': row['department']
                }
            )

            # ✅ If existing, check for updates
            if not created_emp:
                updated = False
                if emp.name != row['employee_name']:
                    emp.name = row['employee_name']
                    updated = True
                if emp.department != row['department']:
                    emp.department = row['department']
                    updated = True
                if updated:
                    emp.save()
                    employees_updated += 1
            else:
                employees_created += 1

            # --- TASK ---
            task, created_task = Task.objects.update_or_create(
                task_id=row['task_id'],
                defaults={
                    'employee': emp,
                    'task_name': row['task_name'],
                    'hours_spent': row['hourspend'],
                    'deadline': row['deadline'],
                    'status': row['status']
                }
            )

            if created_task:
                tasks_created += 1
            else:
                tasks_updated += 1

        return JsonResponse({
            'message': 'CSV processed successfully!',
            'file_path': file_path,
            'employees_created': employees_created,
            'employees_updated': employees_updated,
            'tasks_created': tasks_created,
            'tasks_updated': tasks_updated
        })


class StatsView(View):
    def get(self, request):
        import pandas as pd
        qs = Task.objects.select_related('employee').values(
            'employee__employee_id', 'employee__name', 'employee__department',
            'task_id', 'task_name', 'hours_spent', 'deadline', 'status'
        )
        df = pd.DataFrame(qs)
        if df.empty:
            return JsonResponse({'error': 'No data in database'}, status=404)

        metrics = compute_metrics(df.rename(columns={
            'employee__employee_id': 'employeed_id',
            'employee__name': 'employee_name',
            'employee__department': 'department',
            'hours_spent': 'hourspend'
        }))
        return JsonResponse(metrics)



class VisualsView(View):
    def get(self, request):
        # 1️⃣ Fetch task data
        qs = Task.objects.select_related('employee').values(
            'employee__department', 'employee__name',
            'hours_spent', 'deadline', 'status',
            'task_id', 'task_name'
        )
        df = pd.DataFrame(qs)
        if df.empty:
            return JsonResponse({'error': 'No data available'}, status=404)

        # 2️⃣ Rename columns for consistency
        df.rename(columns={
            'employee__name': 'employee_name',
            'employee__department': 'department',
            'hours_spent': 'hourspend'
        }, inplace=True)

        # 3️⃣ Compute analytics
        metrics = compute_metrics(df)

        # 4️⃣ Chart directory
        img_dir = os.path.join(settings.BASE_DIR, 'static', 'charts')
        os.makedirs(img_dir, exist_ok=True)

        # 5️⃣ Bar Chart – Total Hours per Department (includes 0-hour departments)
        print(df['department'],'dataframe')
        departments = sorted(df['department'].unique())
        print(departments,'departments')  
        total_hours = (
            df.groupby('department')['hourspend']
            .sum()
            .reindex(departments, fill_value=0)
        )

        plt.figure(figsize=(8, 5))
        plt.bar(total_hours.index, total_hours.values, color='teal')
        plt.title("Total Hours per Department", fontsize=14, fontweight='bold')
        plt.xlabel("Department", fontsize=12)
        plt.ylabel("Total Hours", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(img_dir, 'bar_chart.png'))
        plt.close()

        # 6️⃣ Pie Chart – Completion %
        if metrics['completion_percentage']:
            plt.figure(figsize=(6, 6))
            plt.pie(metrics['completion_percentage'].values(),
                    labels=metrics['completion_percentage'].keys(),
                    autopct='%1.1f%%', startangle=140)
            plt.title('Task Completion % per Department', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.savefig(os.path.join(img_dir, 'pie_chart.png'))
            plt.close()

        # 7️⃣ Line Chart – Completed Task Trend
        completed = df[df['status'].str.lower() == 'completed'].copy()
        completed['deadline'] = pd.to_datetime(completed['deadline'], errors='coerce')
        trend = completed.groupby(completed['deadline'].dt.date).size().sort_index()

        if not trend.empty:
            plt.figure(figsize=(10, 5))
            plt.plot(trend.index, trend.values, marker='o', linestyle='-', linewidth=2, color='seagreen')
            plt.title('Trend of Tasks Completed Over Deadlines', fontsize=14, fontweight='bold')
            plt.xlabel('Deadline Date', fontsize=12)
            plt.ylabel('Tasks Completed', fontsize=12)
            plt.xticks(rotation=45, ha='right', fontsize=9)
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.tight_layout()
            plt.savefig(os.path.join(img_dir, 'line_chart.png'))
            plt.close()

        # 8️⃣ Context for Template
        context = {
            "bar_chart": "charts/bar_chart.png",
            "pie_chart": "charts/pie_chart.png",
            "line_chart": "charts/line_chart.png",
            "top_employees": metrics['top_3_employees'],
            "delayed_tasks": metrics['delayed_tasks'],
            "avg_hours_completed": metrics['average_hours_per_completed_task'],
            "total_hours": metrics['total_hours_per_department'],
            "completion_percent": metrics['completion_percentage'],
        }

        # 9️⃣ Render page
        return render(request, 'tasks/visuals.html', context)


class AnalyticsBaseView(View):
    """Common base view for all analytics API endpoints."""

    def get_dataframe(self):
        qs = Task.objects.select_related('employee').values(
            'employee__department', 'employee__name',
            'hours_spent', 'deadline', 'status',
            'task_id', 'task_name'
        )
        df = pd.DataFrame(qs)
        if df.empty:
            return None
        df.rename(columns={
            'employee__name': 'employee_name',
            'employee__department': 'department',
            'hours_spent': 'hourspend'
        }, inplace=True)
        return df


@method_decorator(csrf_exempt, name='dispatch')
class TotalHoursPerDepartmentAPI(AnalyticsBaseView):
    """GET total working hours per department."""
    def get(self, request):
        df = self.get_dataframe()
        if df is None:
            return JsonResponse({'error': 'No data available'}, status=404)

        departments = sorted(df['department'].unique())
        total_hours = (
            df.groupby('department')['hourspend']
            .sum()
            .reindex(departments, fill_value=0)
            .to_dict()
        )

        return JsonResponse({'total_hours_per_department': total_hours})


@method_decorator(csrf_exempt, name='dispatch')
class CompletionPercentageAPI(AnalyticsBaseView):
    """GET completion percentage per department."""
    def get(self, request):
        df = self.get_dataframe()
        if df is None:
            return JsonResponse({'error': 'No data available'}, status=404)

        metrics = compute_metrics(df)
        return JsonResponse({'completion_percentage': metrics['completion_percentage']})


@method_decorator(csrf_exempt, name='dispatch')
class TopEmployeesAPI(AnalyticsBaseView):
    """GET top 3 employees with most completed task hours."""
    def get(self, request):
        df = self.get_dataframe()
        if df is None:
            return JsonResponse({'error': 'No data available'}, status=404)

        metrics = compute_metrics(df)
        return JsonResponse({'top_3_employees': metrics['top_3_employees']})


@method_decorator(csrf_exempt, name='dispatch')
class DelayedTasksAPI(AnalyticsBaseView):
    """GET all delayed (overdue) tasks."""
    def get(self, request):
        df = self.get_dataframe()
        if df is None:
            return JsonResponse({'error': 'No data available'}, status=404)

        metrics = compute_metrics(df)
        return JsonResponse({'delayed_tasks': metrics['delayed_tasks']})


@method_decorator(csrf_exempt, name='dispatch')
class AverageHoursCompletedAPI(AnalyticsBaseView):
    """GET average hours per completed task."""
    def get(self, request):
        df = self.get_dataframe()
        if df is None:
            return JsonResponse({'error': 'No data available'}, status=404)

        metrics = compute_metrics(df)
        return JsonResponse({'average_hours_per_completed_task': metrics['average_hours_per_completed_task']})


@method_decorator(csrf_exempt, name='dispatch')
class TaskTrendAPI(AnalyticsBaseView):
    """GET number of completed tasks grouped by deadline date."""
    def get(self, request):
        df = self.get_dataframe()
        if df is None:
            return JsonResponse({'error': 'No data available'}, status=404)

        completed = df[df['status'].str.lower() == 'completed'].copy()
        completed['deadline'] = pd.to_datetime(completed['deadline'], errors='coerce')
        trend = completed.groupby(completed['deadline'].dt.date).size().sort_index()
        trend_dict = {str(k): int(v) for k, v in trend.items()}

        return JsonResponse({'completed_task_trend': trend_dict})
