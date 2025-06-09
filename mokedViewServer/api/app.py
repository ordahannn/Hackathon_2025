from flask import Flask, jsonify, request

from flask_cors import CORS

from processing.data_analysis import (
    load_data,
    tickets_by_entity,
    overdue_analysis_by_entity,
    workload_vs_overdue_by_entity,
    monthly_trends_by_entity,
    summary_status_by_entity,
    monthly_tickets_and_overdues
)

from processing.data_analysis_employee import (
    get_employees_closed_tickets_count, get_employees_closed_tickets_percentage_from_all_closed_tickets, get_employees_total_tickets_count, get_employees_total_tickets_percentage_from_all_tickets, get_current_tickets_status, get_employees_on_time_percentage, get_employees_overdue_percentage, get_employees_avg_handling_time, get_top_n_employees_scores,calculate_employee_z_scores_from_data, get_monthly_performance_trends, prepare_employees_performance_data
)

from processing.predict_high_tickets import predict_top_category

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

df = load_data()

# Tickets by Entity
@app.route('/api/tickets-by-entity', methods=['GET'])
def api_tickets_by_entity():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    group_by = request.args.get('group_by', 'department')  # ברירת מחדל ל-department
    result = tickets_by_entity(df, group_by=group_by, start_date=start_date, end_date=end_date)
    return jsonify(result)

# Overdue Analysis
@app.route('/api/overdue-analysis', methods=['GET'])
def api_overdue_analysis():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    group_by = request.args.get('group_by', 'department')
    result = overdue_analysis_by_entity(df, group_by=group_by, start_date=start_date, end_date=end_date)
    return jsonify(result)

# Workload vs Overdue
@app.route('/api/workload-vs-overdue', methods=['GET'])
def api_workload_vs_overdue():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    group_by = request.args.get('group_by', 'department')
    result = workload_vs_overdue_by_entity(df, group_by=group_by, start_date=start_date, end_date=end_date)
    return jsonify(result)

# Monthly Trends
@app.route('/api/monthly-trends', methods=['GET'])
def api_monthly_trends():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    group_by = request.args.get('group_by', 'department')
    result = monthly_trends_by_entity(df, group_by=group_by, start_date=start_date, end_date=end_date)
    return jsonify(result)

# Summary Status
@app.route('/api/summary-status', methods=['GET'])
def api_summary_status():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    group_by = request.args.get('group_by', 'department')
    result = summary_status_by_entity(df, group_by=group_by, start_date=start_date, end_date=end_date)
    return jsonify(result)

@app.route('/api/monthly-tickets-and-overdues', methods=['GET'])
def api_monthly_tickets_and_overdues():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    result = monthly_tickets_and_overdues(df, start_date=start_date, end_date=end_date)
    return jsonify(result)

# ---------------------------------------------------------------------

# # Number of closed inquiries per employee (GET)
# @app.route('/api/employees/closed-tickets', methods=['GET'])
# def api_employees_closed_tickets():
#     start_date = request.args.get('start_date')
#     end_date = request.args.get('end_date')
#     department = request.args.get('department')
#     sub_department = request.args.get('sub_department')

#     result = get_employees_closed_tickets_count(df, department, sub_department, start_date, end_date)
#     return jsonify(result)


# # Employee ranking (Top N) by Z-Score (GET):
# @app.route('/api/employees/top-scores', methods=['GET'])
# def api_employees_top_scores():
#     start_date = request.args.get('start_date')
#     end_date = request.args.get('end_date')
#     department = request.args.get('department')
#     sub_department = request.args.get('sub_department')
#     min_closed_tickets = int(request.args.get('min_closed_tickets', 10))
#     n = int(request.args.get('n', 5))

#     result = calculate_employee_z_scores_from_data(
#         df, department, sub_department, start_date, end_date,
#         alpha=0.5, beta=0.5, min_closed_tickets=min_closed_tickets, n=n
#     )
#     return jsonify(result)


# # Summary Status (GET):
# @app.route('/api/employees/summary-status', methods=['GET'])
# def api_employees_summary_status():
#     start_date = request.args.get('start_date')
#     end_date = request.args.get('end_date')
#     department = request.args.get('department')
#     sub_department = request.args.get('sub_department')

#     result = get_current_tickets_status(df, department, sub_department, start_date, end_date)
#     return jsonify(result)

# @app.route('/api/employees/monthly-trends', methods=['GET'])
# def api_employees_monthly_trends():
#     start_date = request.args.get('start_date')
#     end_date = request.args.get('end_date')
#     department = request.args.get('department')
#     sub_department = request.args.get('sub_department')

#     result = get_monthly_performance_trends(df, department, sub_department, start_date, end_date)
#     return jsonify(result)


def get_common_params():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    department = request.args.get('department')
    sub_department = request.args.get('sub_department')
    if not all([start_date, end_date, department, sub_department]):
        return None, jsonify({'error': 'Missing one or more required parameters: start_date, end_date, department, sub_department'}), 400
    return (start_date, end_date, department, sub_department), None, None

def jsonify_with_params(func):
    params, error_response, status = get_common_params()
    if error_response:
        return error_response, status
    start_date, end_date, department, sub_department = params
    result = func(df, department, sub_department, start_date, end_date)
    return jsonify(result)

@app.route('/api/employees/closed-tickets', methods=['GET'])
def api_employees_closed_tickets():
    return jsonify_with_params(get_employees_closed_tickets_count)

@app.route('/api/employees/closed-tickets-percentage', methods=['GET'])
def api_employees_closed_tickets_percentage():
    return jsonify_with_params(get_employees_closed_tickets_percentage_from_all_closed_tickets)

@app.route('/api/employees/total-tickets', methods=['GET'])
def api_employees_total_tickets():
    return jsonify_with_params(get_employees_total_tickets_count)

@app.route('/api/employees/total-tickets-percentage', methods=['GET'])
def api_employees_total_tickets_percentage():
    return jsonify_with_params(get_employees_total_tickets_percentage_from_all_tickets)

@app.route('/api/employees/summary-status', methods=['GET'])
def api_employees_summary_status():
    return jsonify_with_params(get_current_tickets_status)

@app.route('/api/employees/on-time-percentage', methods=['GET'])
def api_employees_on_time_percentage():
    return jsonify_with_params(get_employees_on_time_percentage)

@app.route('/api/employees/overdue-percentage', methods=['GET'])
def api_employees_overdue_percentage():
    return jsonify_with_params(get_employees_overdue_percentage)

@app.route('/api/employees/avg-handling-time', methods=['GET'])
def api_employees_avg_handling_time():
    return jsonify_with_params(get_employees_avg_handling_time)

@app.route('/api/employees/top-scores', methods=['GET'])
def api_employees_top_scores():
    params, error_response, status = get_common_params()
    if error_response:
        return error_response, status
    start_date, end_date, department, sub_department = params
    min_closed_tickets = int(request.args.get('min_closed_tickets', 10))
    n = int(request.args.get('n', 5))
    result = calculate_employee_z_scores_from_data(
        df, department, sub_department, start_date, end_date,
        alpha=0.5, beta=0.5, min_closed_tickets=min_closed_tickets, n=n
    )
    return jsonify(result)

@app.route('/api/employees/top-n-scores', methods=['GET'])
def api_employees_top_n_scores():
    params, error_response, status = get_common_params()
    if error_response:
        return error_response, status
    start_date, end_date, department, sub_department = params
    n = int(request.args.get('n', 5))
    min_closed_tickets = int(request.args.get('min_closed_tickets', 10))
    result = get_top_n_employees_scores(
        df, department, sub_department, start_date, end_date,
        n=n, min_closed_tickets=min_closed_tickets
    )
    return jsonify(result)

@app.route('/api/employees/monthly-trends', methods=['GET'])
def api_employees_monthly_trends():
    return jsonify_with_params(get_monthly_performance_trends)

@app.route('/api/employees/performance-table', methods=['GET'])
def api_employees_performance_table():
    params, error_response, status = get_common_params()
    if error_response:
        return error_response, status
    start_date, end_date, department, sub_department = params
    result = prepare_employees_performance_data(df, department, sub_department, start_date, end_date)
    return jsonify(result)

@app.route('/api/predict-top-category', methods=['GET'])
def api_predict_top_category():
    department = request.args.get('department')
    sub_department = request.args.get('sub_department')
    try:
        prediction = predict_top_category(department, sub_department)
        return jsonify({'predicted_category': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)