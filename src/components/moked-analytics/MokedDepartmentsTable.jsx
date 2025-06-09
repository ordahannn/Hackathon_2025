import { useNavigate } from "react-router-dom";

const MokedDepartmentsTable = ({ data }) => {
  const navigate = useNavigate();

  const handleRowClick = (departmentName) => {
    navigate(`/department-details/${encodeURIComponent(departmentName)}`);
  };

  const sortedData = [...data].sort((a, b) => {
    const totalA = a.closed_on_time + a.closed_overdue;
    const overdueRateA = totalA ? (a.closed_overdue / totalA) : 0;
    const totalB = b.closed_on_time + b.closed_overdue;
    const overdueRateB = totalB ? (b.closed_overdue / totalB) : 0;
    return overdueRateB - overdueRateA;
  });

  return (
    <div className="p-4 bg-gray-800 rounded-xl shadow-md text-center">
      <h3 className="text-xl font-bold mb-4 text-center">דירוג אגפים לפי אחוז חריגות</h3>
      <div className="overflow-x-auto text-center">
        <table className="min-w-full bg-gray-700 rounded-lg overflow-hidden text-sm text-center">
          <thead>
            <tr className="text-gray-300 uppercase bg-gray-600">
              <th className="px-4 py-3 text-center">אגף</th>
              <th className="px-4 py-3 text-center">פניות פתוחות</th>
              <th className="px-4 py-3 text-center">פניות סגורות בזמן</th>
              <th className="px-4 py-3 text-center">פניות סגורות בחריגה</th>
              <th className="px-4 py-3 text-center">% חריגות</th>
            </tr>
          </thead>
          <tbody>
            {sortedData.map((item, idx) => {
              const totalClosed = item.closed_on_time + item.closed_overdue;
              const overduePercentage = totalClosed ? ((item.closed_overdue / totalClosed) * 100).toFixed(2) : "0.00";

              return (
                <tr
                  key={idx}
                  className="border-t border-gray-600 hover:bg-gray-600 cursor-pointer transition-colors duration-200"
                  onClick={() => handleRowClick(item.department)}
                >
                  <td className="px-4 py-2">{item.department}</td>
                  <td className="px-4 py-2">{item.open_tickets}</td>
                  <td className="px-4 py-2">{item.closed_on_time}</td>
                  <td className="px-4 py-2">{item.closed_overdue}</td>
                  <td className={`px-4 py-2 ${overduePercentage >= 20 ? "text-red-400" : "text-green-400"}`}>
                    %{overduePercentage}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default MokedDepartmentsTable;
