const BASE_URL = "http://127.0.0.1:5000/api";

// build query params
function buildQueryParams(groupBy = "department", startDate = null, endDate = null) {
    const params = new URLSearchParams();
    params.append("group_by", groupBy);
    if (startDate) params.append("start_date", startDate);
    if (endDate) params.append("end_date", endDate);
    return params.toString();
}  

// fetch all tickets by dept/all dept
export async function getTicketsByEntity(groupBy = "department", startDate = null, endDate = null) {
    const response = await fetch(`${BASE_URL}/tickets-by-entity?${buildQueryParams(groupBy, startDate, endDate)}`);
    if (!response.ok) throw new Error("Failed to fetch tickets by entity");
    return response.json();
}

// fetch overdue by dept/sub dept analysis
export async function getOverdueAnalysis(groupBy = "department", startDate = null, endDate = null) {
    const response = await fetch(`${BASE_URL}/overdue-analysis?${buildQueryParams(groupBy, startDate, endDate)}`);
    if (!response.ok) throw new Error("Failed to fetch overdue analysis");
    return response.json();
}

// fetch workload vs overdues by dept/sub dept
export async function getWorkloadVsOverdue(groupBy = "department", startDate = null, endDate = null) {
    const response = await fetch(`${BASE_URL}/workload-vs-overdue?${buildQueryParams(groupBy, startDate, endDate)}`);
    if (!response.ok) throw new Error("Failed to fetch workload vs overdue");
    return response.json();
}

// fetch monthly trend by dept/sub dept
export async function getMonthlyTrends(groupBy = "department", startDate = null, endDate = null) {
    const response = await fetch(`${BASE_URL}/monthly-trends?${buildQueryParams(groupBy, startDate, endDate)}`);
    if (!response.ok) throw new Error("Failed to fetch monthly trends");
    return response.json();
}

// fetch current state of dept/sub dept
export async function getSummaryStatus(groupBy = "department", startDate = null, endDate = null) {
    const response = await fetch(`${BASE_URL}/summary-status?${buildQueryParams(groupBy, startDate, endDate)}`);
    if (!response.ok) throw new Error("Failed to fetch summary status");
    return response.json();
}

// fetch tickets and overduetickest 
export async function getMonthlyTicketsAndOverdues(startDate = null, endDate = null) {
    const params = new URLSearchParams();
    if (startDate) params.append("start_date", startDate);
    if (endDate) params.append("end_date", endDate);
  
    const response = await fetch(`${BASE_URL}/monthly-tickets-and-overdues?${params.toString()}`);
    if (!response.ok) throw new Error("Failed to fetch monthly tickets and overdues");
    return response.json();
}

// ----------------------------------------------------------------
// בניית פרמטרים משותפים
function buildEmployeeQueryParams(department, subDepartment, startDate, endDate) {
    const params = new URLSearchParams();
    if (department) params.append("department", department);
    if (subDepartment) params.append("sub_department", subDepartment);
    if (startDate) params.append("start_date", startDate);
    if (endDate) params.append("end_date", endDate);
    return params.toString();
}

// פונקציית עזר לקריאות API
async function fetchFromApi(endpoint, queryParams = "") {
    const response = await fetch(`${BASE_URL}${endpoint}?${queryParams}`);
    if (!response.ok) throw new Error(`Failed to fetch data from ${endpoint}`);
    return response.json();
}

// פונקציות לקריאה לכל אחד מה־APIים:

export async function getEmployeesClosedTickets(department, subDepartment, startDate, endDate) {
    const queryParams = buildEmployeeQueryParams(department, subDepartment, startDate, endDate);
    return fetchFromApi("/employees/closed-tickets", queryParams);
}

export async function getEmployeesClosedTicketsPercentage(department, subDepartment, startDate, endDate) {
    const queryParams = buildEmployeeQueryParams(department, subDepartment, startDate, endDate);
    return fetchFromApi("/employees/closed-tickets-percentage", queryParams);
}

export async function getEmployeesTotalTickets(department, subDepartment, startDate, endDate) {
    const queryParams = buildEmployeeQueryParams(department, subDepartment, startDate, endDate);
    return fetchFromApi("/employees/total-tickets", queryParams);
}

export async function getEmployeesTotalTicketsPercentage(department, subDepartment, startDate, endDate) {
    const queryParams = buildEmployeeQueryParams(department, subDepartment, startDate, endDate);
    return fetchFromApi("/employees/total-tickets-percentage", queryParams);
}

export async function getEmployeesSummaryStatus(department, subDepartment, startDate, endDate) {
    const queryParams = buildEmployeeQueryParams(department, subDepartment, startDate, endDate);
    return fetchFromApi("/employees/summary-status", queryParams);
}

export async function getEmployeesOnTimePercentage(department, subDepartment, startDate, endDate) {
    const queryParams = buildEmployeeQueryParams(department, subDepartment, startDate, endDate);
    return fetchFromApi("/employees/on-time-percentage", queryParams);
}

export async function getEmployeesOverduePercentage(department, subDepartment, startDate, endDate) {
    const queryParams = buildEmployeeQueryParams(department, subDepartment, startDate, endDate);
    return fetchFromApi("/employees/overdue-percentage", queryParams);
}

export async function getEmployeesAvgHandlingTime(department, subDepartment, startDate, endDate) {
    const queryParams = buildEmployeeQueryParams(department, subDepartment, startDate, endDate);
    return fetchFromApi("/employees/avg-handling-time", queryParams);
}

export async function getEmployeesTopScores(department, subDepartment, startDate, endDate, minClosedTickets = 10, n = 5) {
    const queryParams = buildEmployeeQueryParams(department, subDepartment, startDate, endDate) +
        `&min_closed_tickets=${minClosedTickets}&n=${n}`;
    return fetchFromApi("/employees/top-scores", queryParams);
}

export async function getEmployeesTopNScores(department, subDepartment, startDate, endDate, minClosedTickets = 10, n = 5) {
    const queryParams = buildEmployeeQueryParams(department, subDepartment, startDate, endDate) +
        `&n=${n}&min_closed_tickets=${minClosedTickets}`;
    return fetchFromApi("/employees/top-n-scores", queryParams);
}

export async function getEmployeesMonthlyTrends(department, subDepartment, startDate, endDate) {
    const queryParams = buildEmployeeQueryParams(department, subDepartment, startDate, endDate);
    return fetchFromApi("/employees/monthly-trends", queryParams);
}
  
  // הפונקציה ששלפת:
  export async function getEmployeesPerformanceTable(department, subDepartment, startDate, endDate) {
    const queryParams = buildEmployeeQueryParams(department, subDepartment, startDate, endDate);
    const response = await fetch(`${BASE_URL}/employees/performance-table?${queryParams}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch employees performance data: ${response.statusText}`);
    }
    return response.json();
  }

// בקריאה ל־/api/predict-top-category
export async function predictTopCategory(department, subDepartment) {
    const params = new URLSearchParams();
    if (department) params.append("department", department);
    if (subDepartment) params.append("sub_department", subDepartment);
  
    const response = await fetch(`http://127.0.0.1:5000/api/predict-top-category?${params.toString()}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch prediction: ${response.statusText}`);
    }
    return response.json();
  }