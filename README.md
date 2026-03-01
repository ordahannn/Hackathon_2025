# MokedView - Call Center Analytics Platform
**MokedView** is a data analysis and visualization system developed during a hackathon project.  
The system is designed for monitoring, analyzing, and presenting service requests (tickets) data from a regional council’s contact center.  
It provides clear, interactive dashboards to support decision-making for departments, divisions, and management.

---

## Project Goals
- Provide **real-time insights** into the volume and status of service requests.
- Present **clear and actionable** insights from service request data.
- Identify **performance trends** across departments, sub-departments, and employees.
- Enable **data-driven decisions** by presenting KPIs and visual analytics.
- Improve **efficiency** in handling requests through better visibility.
- **Measure and compare** the performance of departments, sub-departments, and employees.

---

## Main Features
- **Central Dashboard**:
  - Total number of requests in a selected date range.
  - Percentage of on-time vs. overdue requests.
  - Average handling time (in working hours).
  - Active employees count.
  - Distribution of requests by department/division.
- **Employee Dashboard**:
  - Requests handled per employee.
  - Percentage closed on time vs. overdue.
  - Average handling time.
  - Top and bottom 5 performers.
- **Filtering Options**:
  - Filter by department, sub-department, and date range.
- **Interactive Charts**:
  - Pie charts and bar charts.
  - KPI cards for quick overview.

---

## Technologies Used
**Frontend:**
- React
- Tailwind CSS
- Recharts (data visualization)
- React Table (tables)

**Backend:**
- Python (Flask)
- Pandas (data processing)
- Flask-CORS (API CORS handling)

**Data:**
- CSV dataset from the regional council’s contact center (anonymized for privacy).
  
---

## 📂 Project Structure

```
MokedView/
├── client/               # React frontend
│   ├── src/
│   │   ├── components/   # Dashboard components and charts
│   │   └── pages/        # Central & Employee dashboards
├── server/               # Flask backend
│   ├── app.py            # API routes
│   └── data/             # CSV data files
└── README.md
```

---

## 👥 Hackathon Team
- Or Dahan
- Roni Ronen
- Mor Edri

---

**This project was developed for educational purposes as part of a hackathon and is not intended for production use.**

---
