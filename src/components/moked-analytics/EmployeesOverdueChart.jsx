import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

const EmployeesOverdueChart = ({ data }) => {
  const sortedData = [...data]
    .sort((a, b) => b.overdue_percentage - a.overdue_percentage)
    .slice(0, 5); // מציג את הטופ 5

  return (
    <div className="p-4 bg-gray-800 rounded-xl shadow-md">
      <h3 className="text-xl font-bold mb-4">אחוז פניות חריגות לפי עובד</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={sortedData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#4B5563" />
          <XAxis dataKey="employee" stroke="#D1D5DB" />
          <YAxis stroke="#D1D5DB" />
          <Tooltip
            formatter={(value) => [`${value.toFixed(2)}%`, "אחוז פניות חריגות"]}
            labelStyle={{ color: "black", fontWeight: "bold" }}
          />
          <Bar dataKey="overdue_percentage" fill="#EF4444" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default EmployeesOverdueChart;
