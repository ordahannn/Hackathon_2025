const EmployeesPerformanceTable = ({ data }) => {
    const sortedData = [...data].sort((a, b) => b.overdue_percentage - a.overdue_percentage);
  
    return (
      <div className="p-4 bg-gray-800 rounded-xl shadow-md text-center">
        <h3 className="text-xl font-bold mb-4">דירוג עובדים לפי אחוז חריגות</h3>
        <div className="overflow-x-auto text-center">
          <table className="min-w-full bg-gray-700 rounded-lg overflow-hidden text-sm text-center">
            <thead>
              <tr className="text-gray-300 uppercase bg-gray-600">
                <th className="px-4 py-3 text-center">עובד</th>
                <th className="px-4 py-3 text-center">סה״כ פניות</th>
                <th className="px-4 py-3 text-center">אחוז חריגות</th>
                <th className="px-4 py-3 text-center">משך טיפול ממוצע (שעות)</th>
              </tr>
            </thead>
            <tbody>
              {sortedData.map((item, idx) => (
                <tr
                  key={idx}
                  className="border-t border-gray-600 hover:bg-gray-600 cursor-pointer transition-colors duration-200"
                >
                  <td className="px-4 py-2 font-bold">{item.employee}</td>
                  <td className="px-4 py-2">{item.total_tickets}</td>
                  <td className={`px-4 py-2 ${item.overdue_percentage >= 20 ? "text-red-400" : "text-green-400"}`}>
                    {item.overdue_percentage.toFixed(2)}%
                  </td>
                  <td className="px-4 py-2">{item.avg_handling_time_hours?.toFixed(2) || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };
  
  export default EmployeesPerformanceTable;
  