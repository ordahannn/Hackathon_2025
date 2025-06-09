import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { predictTopCategory } from "../api";
import { useParams, useNavigate } from "react-router-dom";

const PredictHighTickets = () => {
  const [searchParams] = useSearchParams();
  const department = searchParams.get("department");
  const sub_department = searchParams.get("sub_department");

  const [prediction, setPrediction] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    if (department && sub_department) {
      predictTopCategory(department, sub_department)
        .then((data) => {
          if (data.predicted_category) {
            setPrediction(data.predicted_category);
          } else {
            setError("לא התקבלה תחזית.");
          }
        })
        .catch((err) => {
          console.error("Error fetching prediction:", err);
          setError("שגיאה בקבלת התחזית מהשרת.");
        });
    }
  }, [department, sub_department]);

  return (
    <div className="p-10 text-center z-10 h-full w-full text-center relative">
              <div className="absolute top-6 right-6 text-center">
        <button
          onClick={() => navigate("/")}
          className="px-6 py-2 bg-gradient-to-r from-green-400 to-green-600 text-white rounded-lg shadow-md hover:scale-105 transition-transform duration-300"
        >
          חזרה
        </button>
      </div>
      <h1 className="text-3xl font-bold mb-6">תחזית קטגוריה עם הכי הרבה פניות בחודש הקרוב</h1>
      {error && <p className="text-red-500">{error}</p>}
      {prediction && (
        <div className="mt-8 text-2xl text-green-400">
          ✨ הקטגוריה הצפויה <strong>{prediction}</strong>
        </div>
      )}
    </div>
  );
};

export default PredictHighTickets;
