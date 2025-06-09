import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';

const OverduePieChart = ({ data }) => {
  const total = data.reduce((sum, emp) => sum + (emp.tickets_handled || 0), 0);
  const overdueTotal = data.reduce((sum, emp) => sum + ((emp.overdue_percentage || 0) * (emp.tickets_handled || 0)) / 100, 0);
  const onTimeTotal = total - overdueTotal;

  const chartData = [
    { name: 'סגור בזמן', value: onTimeTotal },
    { name: 'חריגות', value: overdueTotal },
  ];

  const COLORS = ['#10B981', '#EF4444'];

  return (
    <div className="p-4 bg-gray-800 rounded-xl shadow-md mt-8">
      <h3 className="text-xl font-bold mb-4">התפלגות פניות עומדות בצפי מול פניות חורגות</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie data={chartData} dataKey="value" nameKey="name" outerRadius={100}>
            {chartData.map((entry, idx) => (
              <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default OverduePieChart;
