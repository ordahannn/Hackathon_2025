import { Route, Routes } from "react-router-dom";

// import Sidebar from "./components/common/Sidebar";

import MokedMainDashboard from "./pages/MokedMainDashboard";
import DepartmentDetails from "./pages/DepartmentDetails";
import PredictHighTickets from "./pages/PredictHighTickets";

function App() {
	return (
		<div className='flex h-screen bg-gray-900 text-gray-100 overflow-hidden'>
			{/* BG */}
			<div className='fixed inset-0 z-0'>
				<div className='absolute inset-0 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 opacity-80' />
				<div className='absolute inset-0 backdrop-blur-sm' />
			</div>

			<Routes>
				<Route path='/' element={<MokedMainDashboard />} />
				<Route path='/department-details/:departmentName' element={<DepartmentDetails />} />
				<Route path="/PredictHighTickets" element={<PredictHighTickets />} />
			</Routes>
		</div>
	);
}

export default App;
