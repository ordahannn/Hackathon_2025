import { useEffect, useState } from "react";
import { motion } from "framer-motion";

import Header from "../components/common/Header";
import StatCard from "../components/common/StatCard";
import { Users, AlertTriangle, Clock, BarChart2 } from "lucide-react";

// Import API functions
import { 
  getTicketsByEntity, 
  getOverdueAnalysis, 
  getSummaryStatus 
} from "../api";

// Import dashboard components
import MokedOverdueChart from "../components/moked-analytics/MokedOverdueChart";
import MokedMonthlyTrendsChart from "../components/moked-analytics/MokedMonthlyTrendsChart";
import MokedDepartmentsTable from "../components/moked-analytics/MokedDepartmentsTable";

// Function to generate the date range for the last six months
const getHalfYearRange = () => {
  const end = new Date();
  const start = new Date();
  start.setMonth(end.getMonth() - 5); // 6 months back including the current month
  return {
    startDate: start.toISOString().slice(0, 10), // Format: YYYY-MM-DD
    endDate: end.toISOString().slice(0, 10),
  };
};

const MokedMainDashboard = () => {
  const [ticketsData, setTicketsData] = useState([]);
  const [overdueData, setOverdueData] = useState([]);
  const [summaryStatus, setSummaryStatus] = useState([]);

  useEffect(() => {
    const { startDate, endDate } = getHalfYearRange();

    // Fetch data only for the last six months (filtered by start and end dates)
    getTicketsByEntity("department", startDate, endDate).then(setTicketsData);
    getOverdueAnalysis("department", startDate, endDate).then(setOverdueData);
    getSummaryStatus("department", startDate, endDate).then(setSummaryStatus);
  }, []);

  // Calculating total values for the StatCards
  const totalTickets = ticketsData.reduce((sum, item) => sum + item.total_tickets, 0);
  const totalOverdue = overdueData.reduce((sum, item) => sum + (item.avg_overdue_percentage || 0), 0) / (overdueData.length || 1);

  return (
    <div className="w-full h-full flex-1 overflow-auto relative z-10 text-center">
      <Header title= "MokedView" />

      <main className="max-w-7xl mx-auto py-6 px-4 lg:px-8 text-center">
        {/* Stat Cards Section */}
        <motion.div
          className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8 text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
        >
          <StatCard 
            name="סה״כ פניות"
            icon={Users} 
            value={totalTickets.toLocaleString()} 
            color="#6366F1" 
          />
          <StatCard 
            name="אחוז חריגות ממוצע" 
            icon={AlertTriangle} 
            value={`${totalOverdue.toFixed(2)}%`} 
            color="#EF4444" 
          />
          <StatCard 
            name="פניות פתוחות" 
            icon={Clock} 
            value={summaryStatus.reduce((sum, item) => sum + item.open_tickets, 0)} 
            color="#F59E0B" 
          />
          <StatCard 
            name="פניות שנסגרו בזמן" 
            icon={BarChart2} 
            value={summaryStatus.reduce((sum, item) => sum + item.closed_on_time, 0)} 
            color="#10B981" 
          />
        </motion.div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <MokedOverdueChart data={overdueData} />
          <MokedMonthlyTrendsChart />
        </div>

        {/* Departments Table Section */}
        <MokedDepartmentsTable data={summaryStatus} />
      </main>
    </div>
  );
};

export default MokedMainDashboard;
