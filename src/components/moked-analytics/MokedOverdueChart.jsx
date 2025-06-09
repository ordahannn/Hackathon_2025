import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

const MokedOverdueChart = ({ data }) => {
    // sort by top 5 inefficient depts
    const sortedData = [...data]
    .sort((a, b) => b.avg_overdue_percentage - a.avg_overdue_percentage)
    .slice(0, 5);

    return (
        <div className="p-4 bg-gray-800 rounded-xl shadow-md text-center">
            <h3 className="text-xl font-bold mb-4 text-center">אחוז חריגות לפי אגף</h3>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={sortedData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#4B5563" />

                {/* No dataKey on XAxis */}
                <XAxis stroke="#D1D5DB" tick={false} />
                <YAxis stroke="#D1D5DB" />
                <Tooltip
                    formatter={(value, name, props) => [`${value}%`, "אחוז חריגות"]}
                    labelFormatter={(label) => {
                        const deptName = sortedData[label]?.department || "";
                        return `${deptName}`;
                    }}
                    contentStyle={{
                        backgroundColor: "white",
                        borderRadius: "8px",
                        border: "1px solid #ccc",
                        color: "black",
                    }}
                    labelStyle={{
                        color: "black",
                        fontWeight: "bold",
                    }}
                />
                <Bar
                    dataKey="avg_overdue_percentage"
                    fill="#EF4444"
                    radius={[4, 4, 0, 0]}
                    activeShape={() => null}
                />
            </BarChart>
        </ResponsiveContainer>
        </div>
    );
};

export default MokedOverdueChart;
