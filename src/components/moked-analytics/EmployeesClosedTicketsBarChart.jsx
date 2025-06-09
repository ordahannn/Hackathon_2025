import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-2 rounded shadow-md">
          <p style={{ color: 'black', fontWeight: 'bold' }}>{label}</p>
          <p className="text-gray-700">{`${payload[0].value} פניות`}</p>
        </div>
      );
    }
    return null;
};

const EmployeesClosedTicketsBarChart = ({ data }) => {
  const chartData = data.map(emp => ({
    name: emp.employee,
    tickets: emp.tickets_handled,
  }));

  return (
    <div className="p-4 bg-gray-800 rounded-xl shadow-md mt-8">
      <h3 className="text-xl font-bold mb-4">פיזור פניות סגורות בין העובדים</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <XAxis 
            dataKey="name" tick={false}
          />
          <YAxis />
          <Tooltip
            content={<CustomTooltip />}
          />
          <Bar dataKey="tickets" fill="#6366F1" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default EmployeesClosedTicketsBarChart;
