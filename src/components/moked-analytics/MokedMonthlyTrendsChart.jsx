import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { getMonthlyTicketsAndOverdues } from "../../api";

const MokedMonthlyTicketsChart = () => {
  const [data, setData] = useState([]);

  const generateLastSixMonths = () => {
    const result = [];
    const today = new Date();

    for (let i = 5; i >= 0; i--) {
      const d = new Date(today.getFullYear(), today.getMonth() - i, 1);
      const monthStr = d.toISOString().slice(0, 7); // 'YYYY-MM'
      result.push(monthStr);
    }

    return result;
  };

  useEffect(() => {
    getMonthlyTicketsAndOverdues()
      .then((res) => {
        const months = generateLastSixMonths();
        const prepared = months.map((month) => {
          const found = res.find((item) => item.month === month);
          return found || { month, total_tickets: 0, overdue_tickets: 0 };
        });
        setData(prepared);
      })
      .catch((err) => console.error("Error fetching monthly tickets and overdues:", err));
  }, []);

  return (
    <div className="p-4 bg-gray-800 rounded-xl shadow-md text-center">
      <h3 className="text-xl font-bold mb-4 text-center">סה״כ פניות מול פניות חורגות (חצי שנה אחרונה)</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#4B5563" />
          <XAxis
            dataKey="month"
            stroke="#D1D5DB"
            tick={false}        
            axisLine={false}     
        />
          <YAxis stroke="#D1D5DB" />
          <Tooltip
            formatter={(value, name) => [`${value}`, name]}
            labelStyle={{ color: "black", fontWeight: "bold" }}
          />
          <Legend verticalAlign="top" align="right" />
          <Line
            type="monotone"
            dataKey="total_tickets"
            name="סה״כ פניות"
            stroke="#6366F1"
            strokeWidth={2}
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="overdue_tickets"
            name="פניות חורגות"
            stroke="#EF4444"
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default MokedMonthlyTicketsChart;
