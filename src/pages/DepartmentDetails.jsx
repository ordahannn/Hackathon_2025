import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import Papa from "papaparse";

import { getEmployeesPerformanceTable } from "../api";
import StatCard from "../components/common/StatCard";
import { Users, CheckCircle, AlertTriangle, Clock } from "lucide-react";

import EmployeesClosedTicketsBarChart from "../components/moked-analytics/EmployeesClosedTicketsBarChart";
import OverduePieChart from "../components/moked-analytics/OverduePieChart";
import TopEmployeesList from "../components/moked-analytics/TopEmployeesList";
import EmployeesPerformanceTable from "../components/moked-analytics/EmployeesPerformanceTable";

const DepartmentDetails = () => {
  const { departmentName } = useParams();
  const navigate = useNavigate();

  const [subDepartments, setSubDepartments] = useState([]);
  const [selectedSubDepartment, setSelectedSubDepartment] = useState("");
  const [employeesData, setEmployeesData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [stats, setStats] = useState({
    totalTickets: 0,
    closedTickets: 0,
    avgOverdue: 0,
    avgHandlingTime: 0,
    onTimePercentage: 0,
  });

  // שליפת מחלקות מה־CSV
  useEffect(() => {
    if (departmentName) {
      setLoading(true);
      setError("");
      Papa.parse("/data/DEPT_LIST.csv", {
        download: true,
        header: true,
        complete: (result) => {
          const filtered = result.data.filter((item) => item.department === departmentName);
          const uniqueSubDepartments = Array.from(
            new Set(filtered.map((item) => item.sub_department))
          ).map((uniqueName) =>
            filtered.find((item) => item.sub_department === uniqueName)
          );
          setSubDepartments(uniqueSubDepartments);
          setLoading(false);
        },
        error: (err) => {
          console.error("Error loading CSV:", err);
          setError("שגיאה בטעינת רשימת המחלקות.");
          setLoading(false);
        },
      });
    }
  }, [departmentName]);

  // שליפת נתוני ביצועים
  useEffect(() => {
    if (selectedSubDepartment) {
      const startDate = "2023-10-01"; // אפשר לחשב חצי שנה אחורה דינאמית אם תרצי
      const endDate = new Date().toISOString().slice(0, 10);

      getEmployeesPerformanceTable(departmentName, selectedSubDepartment, startDate, endDate)
        .then((data) => {
          setEmployeesData(data);

          const totalTickets = data.reduce((sum, emp) => sum + (emp.total_tickets || 0), 0);
          const closedTickets = data.reduce((sum, emp) => sum + (emp.tickets_handled || 0), 0);
          const avgOverdue = data.reduce((sum, emp) => sum + (emp.overdue_percentage || 0), 0) / (data.length || 1);
          const avgHandlingTime = data.reduce((sum, emp) => sum + (emp.avg_handling_time_hours || 0), 0) / (data.length || 1);
          const avgOnTime = data.reduce((sum, emp) => sum + (emp.on_time_percentage || 0), 0) / (data.length || 1);

          setStats({
            totalTickets,
            closedTickets,
            avgOverdue,
            avgHandlingTime,
            onTimePercentage: avgOnTime,
          });
        })
        .catch((err) => {
          console.error("Error fetching employees performance table:", err);
          setError("שגיאה בשליפת נתוני העובדים.");
        });
    }
  }, [selectedSubDepartment]);

  if (loading) {
    return <div className="p-6 text-center text-gray-300">טוען מחלקות...</div>;
  }

  if (error) {
    return <div className="p-6 text-center text-red-500">{error}</div>;
  }

  return (
    <div className="w-full h-full overflow-auto p-6 text-center z-10 text-center relative">
      <div className="absolute top-6 right-6 text-center">
        <button
          onClick={() => navigate("/")}
          className="px-6 py-2 bg-gradient-to-r from-green-400 to-green-600 text-white rounded-lg shadow-md hover:scale-105 transition-transform duration-300"
        >
          חזרה
        </button>
      </div>

      <div className="absolute top-6 left-6 text-center"> 
        <button
          onClick={() => {
            if (selectedSubDepartment) {
              navigate(`/PredictHighTickets?department=${departmentName}&sub_department=${selectedSubDepartment}`);
            } else {
              alert("בחרי קודם מחלקה לפני המעבר לחיזוי!");
            }
          }}
          className="px-6 py-2 bg-gradient-to-r from-purple-400 to-purple-600 text-white rounded-lg shadow-md hover:scale-105 transition-transform duration-300"
        >
          חיזוי
        </button>
      </div>

      {/* כותרת */}
      <h1 className="text-3xl mt-10 mb-8 font-bold text-center">{departmentName}</h1>

      {/* בחירת מחלקה */}
      {subDepartments.length > 0 ? (
        <select
          className="p-2 rounded bg-gray-800 text-white border border-gray-600 text-center"
          value={selectedSubDepartment}
          onChange={(e) => setSelectedSubDepartment(e.target.value)}
        >
          <option disabled value="">בחר מחלקה</option>
          {subDepartments.map((item, idx) => (
            <option key={idx} value={item.sub_department}>
              {item.sub_department}
            </option>
          ))}
        </select>
      ) : (
        <p className="text-gray-400 text-center mt-4">אין מחלקות זמינות לאגף זה.</p>
      )}

      {/* סטטיסטיקות */}
      {selectedSubDepartment && (
        <>
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8 mt-8">
            <StatCard name="סה״כ פניות" icon={Users} value={stats.totalTickets.toLocaleString()} color="#6366F1" />
            <StatCard name="סה״כ פניות סגורות" icon={CheckCircle} value={stats.closedTickets.toLocaleString()} color="#10B981" />
            <StatCard name="אחוז חריגות ממוצע" icon={AlertTriangle} value={`${stats.avgOverdue.toFixed(2)}%`} color="#EF4444" />
            <StatCard name="משך טיפול ממוצע (שעות)" icon={Clock} value={`${stats.avgHandlingTime.toFixed(2)}`} color="#F59E0B" />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
            <EmployeesClosedTicketsBarChart data={employeesData} />
            <TopEmployeesList data={employeesData} />  {/* כאן במקום ה־PieChart */}
          </div>

          <div className="mt-8">
            <EmployeesPerformanceTable data={employeesData} />  {/* כאן במקום TopEmployeesList */}
          </div>
        </>
      )}
    </div>
  );
};

export default DepartmentDetails;
