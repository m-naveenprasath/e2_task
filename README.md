# Employee Tasks Analytics 

This project provides analytics and visualizations for employee task tracking using Django and Pandas.

### 🔗 Live Preview / Demo

🌐 **Live Demo**: [E2_Task](http://136.113.233.247/api/visuals/)

### Uploaded CSV Template:

 - [📥 Download Uploaded CSV Template](./docs/task_csv.csv)

## 📊 Data Processing & Logic

The following metrics are calculated and served through API responses:

- **Total hours per department**
- **Top 3 employees** with the highest workload (based on hours spent)
- **Task completion percentage** per department
- **Delayed tasks** (deadline passed but status not Completed)
- **Average hours per completed task**

## 📈 Visualization

The following visual insights are generated and saved as images:

- **Bar Chart:** Total hours spent per department  
- **Pie Chart:** Task completion percentage per department  
- **Line Chart:** Trend of tasks completed over deadlines  
- **Table View:** Top 3 employees by workload & pending tasks  

## 🧩 API Endpoints

    | Endpoint                                  | Method | Description                                    |
    | ----------------------------------------- | ------ | ---------------------------------------------- |
    | `/api/upload-csv/`                        | `POST` | Upload and process employee-task CSV file      |
    | `/api/stats/`                             | `GET`  | Get metrics and analytics data as JSON         |
    | `/api/visuals/`                           | `GET`  | Render visual dashboard with charts and tables |
    | `/api/analytics/total-hours/`             | `GET`  | Get total hours spent per department           |
    | `/api/analytics/completion-percentage/`   | `GET`  | Get task completion percentage per department  |
    | `/api/analytics/top-employees/`           | `GET`  | Get top 3 employees with highest workload      |
    | `/api/analytics/delayed-tasks/`           | `GET`  | Get list/count of delayed tasks                |
    | `/api/analytics/average-hours-completed/` | `GET`  | Get average hours per completed task           |
    | `/api/analytics/task-trend/`              | `GET`  | Get trend of tasks completed over time         |



## 🛠️ Tech Stack

- **Backend:** Django, Pandas, Matplotlib  
- **Database:** SQLite (can be configured for PostgreSQL/MySQL)  
- **Frontend (optional):** HTML templates dashboard  

## 📂 Project Structure

```
tasks/
│
├── models.py         # Employee & Task models
├── views.py          # Upload, Stats, and Visuals API Views
├── utils.py          # CSV processing & metric computation
├── templates/
│   └── tasks/
│       └── visuals.html  # Visualization dashboard
└── static/
    └── charts/           # Generated chart images
```

## ⚙️ Example Usage

1. Upload a CSV file via `api/upload-csv/`
2. View computed stats via `api/stats/`
3. Check visualization dashboard at `api/visuals/`
4. Fetch chart data and metrics programmatically from `api/analytics/<api>/`

 **Build and start the containers:**
```
docker build -t e2-task .
docker run -d -p 8000:8000 e2-task
```

**(Optional) volume mount:**
```
docker run -d -p 8000:8000 \
  -v $(pwd)/static:/app/static \
  e2-task
```
---
**Author:** Naveen Prasath  
**Version:** 1.0.0  
