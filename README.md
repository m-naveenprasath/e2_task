# Employee Tasks Analytics 

This project provides analytics and visualizations for employee task tracking using Django and Pandas.

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

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/upload-csv/` | `POST` | Upload and process employee-task CSV file |
| `/stats/` | `GET` | Get metrics and analytics data as JSON |
| `/visuals/` | `GET` | Render visual dashboard with charts and tables |
| `/analytics/<api>/` | `GET` | Serve all visuals and metrics as JSON API |

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

1. Upload a CSV file via `/upload-csv/`
2. View computed stats via `/stats/`
3. Check visualization dashboard at `/visuals/`
4. Fetch chart data and metrics programmatically from `/analytics/<api>/`

---
**Author:** Naveen Prasath  
**Version:** 1.0.0  
