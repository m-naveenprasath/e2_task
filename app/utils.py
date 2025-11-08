import pandas as pd
from datetime import date

def process_csv(file):
    """Parse CSV and return cleaned DataFrame."""
    df = pd.read_csv(file)
    df.columns = [c.strip().lower() for c in df.columns]

    # Drop missing required IDs
    df.dropna(subset=['employeed_id', 'task_id'], inplace=True)

    # Normalize data
    df['hourspend'] = pd.to_numeric(df['hourspend'], errors='coerce').fillna(0)
    df['deadline'] = pd.to_datetime(df['deadline'], errors='coerce').dt.date

    return df


def compute_metrics(df):
    """Compute analytics with robust handling for edge cases."""
    df.columns = [col.lower() for col in df.columns]
    df['deadline'] = pd.to_datetime(df['deadline'], errors='coerce').dt.date
    df['hourspend'] = df['hourspend'].fillna(0)
    df['status'] = df['status'].fillna('').astype(str)

    # 1️⃣ Total hours per department
    total_hours = df.groupby('department')['hourspend'].sum().to_dict()

    # 2️⃣ Top 3 employees by workload
    emp_hours = (
        df.groupby('employee_name')['hourspend']
        .sum()
        .sort_values(ascending=False)
        .head(3)
    )
    top_employees = emp_hours.reset_index().to_dict(orient='records')

    # 3️⃣ Completion percentage per department
    completed = df[df['status'].str.lower() == 'completed']
    completion_percent = (
        (completed.groupby('department').size() / df.groupby('department').size() * 100)
        .round(2)
        .fillna(0)
        .to_dict()
    )

    # 4️⃣ Delayed tasks (past deadline, not completed)
    df = df.dropna(subset=['deadline'])
    today = date.today()
    delayed = df[
        (df['deadline'] < today) &
        (df['status'].str.lower() != 'completed')
    ]
    delayed_tasks = delayed[
        ['task_id', 'task_name', 'employee_name', 'deadline', 'status']
    ].to_dict(orient='records') if not delayed.empty else []

    # 5️⃣ Average hours per completed task
    avg_hours_completed = round(completed['hourspend'].dropna().mean(), 2) if not completed.empty else 0

    return {
        "total_hours_per_department": total_hours,
        "top_3_employees": top_employees,
        "completion_percentage": completion_percent,
        "delayed_tasks": delayed_tasks,
        "average_hours_per_completed_task": avg_hours_completed
    }
