# MokedView

**Moked View** is a real-time analytics dashboard designed for municipal support centers.
It provides management and department heads with clear, actionable insights into service performance using real-time data, employee metrics, and visual trends.
The system was developed during a hackathon for the Emek Hefer Regional Council.

---

## Hackathon Context
This project was developed as part of a civic-tech hackathon in collaboration with Emek Hefer Regional Council.
The challenge: create an innovative tool to help the municipality analyze and improve the response and performance of their citizen support center.

### The Problem:
- The regional call center receives a large volume of service requests (פניות).
- Performance data is buried in CSV files and hard to interpret.
- There's a need for smarter ways to monitor trends, track SLA compliance, and evaluate employee and department performance.

### Our Mission:
Build a system that:
- Transforms raw request data into meaningful KPIs and visual insights.
- Helps managers make faster, data-informed decisions.
- Supports filtering by department, sub-department, and date range.
- Is clear, fast, and accessible even for non-technical staff.

---

## Purpose
The goal of Moked View is to simplify the analysis of support request data by transforming raw CSV records into an intuitive BI dashboard.
It helps identify bottlenecks, track SLA compliance, and recognize top-performing employees — all in a visually compelling and filterable interface.

## Technologies Used
- **Frontend**: React, Tailwind CSS, Recharts, React Table  
- **Backend**: Python (Flask), Pandas  
- **Data Source**: Static CSV files (mocked for demo)  
- **Hosting**: GitHub Pages (client) + Local/Cloud Flask server (API)

## Main Features

- **KPI Cards:** Total tickets, SLA compliance, avg. handling time
- **Graphs:** Monthly trends, SLA breakdowns, ticket volumes
- **Employee Dashboard:** Individual performance and ranking
- **Department Filtering:** By date, department, and sub-department
- **Extensible:** Easy to plug in real data sources in place of CSV

## Notes
- The dataset used in this demo is a mocked version based on real formats.
- The project was created as a hackathon MVP and is not yet production-ready.
- Future versions may include real-time integration with live municipal systems.
