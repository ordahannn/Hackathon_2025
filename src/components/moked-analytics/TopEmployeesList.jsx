const TopEmployeesList = ({ data }) => {
    const top5 = [...data]
      .sort((a, b) => b.on_time_percentage - a.on_time_percentage)
      .slice(0, 5);
  
    return (
      <div className="p-4 bg-gray-800 rounded-xl shadow-md mt-8">
        <h3 className="text-xl font-bold mb-4">🏆 טופ 5 העובדים המצטיינים</h3>
        <ul className="space-y-3">
          {top5.map((emp, idx) => (
            <li key={idx} className="flex justify-between items-center bg-gray-700 p-2 rounded">
              <span>{emp.employee}</span>
              <span className="text-green-400">{emp.on_time_percentage.toFixed(2)}%</span>
            </li>
          ))}
        </ul>
      </div>
    );
  };
  
  export default TopEmployeesList;
  