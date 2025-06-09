import pandas as pd
import os

# load the data csv and return DataFrame                   
def load_data(filepath=None):
    if filepath is None:
        base_path = os.path.dirname(os.path.dirname(__file__))  
        filepath = os.path.join(base_path, 'data', 'DATA_MOKED.csv')
    df = pd.read_csv(filepath)
    return df

# filter by date (for each function)
def filter_by_date(df, start_date=None, end_date=None):
    if df['opened_date'].dtype != 'datetime64[ns]':
        df['opened_date'] = pd.to_datetime(df['opened_date'], errors='coerce')
    if start_date:
        df = df[df['opened_date'] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df['opened_date'] <= pd.to_datetime(end_date)]
    return df

# calc num of tickets by dept/sub dept
def tickets_by_entity(df, group_by='department', start_date=None, end_date=None):
    df_filtered = filter_by_date(df, start_date, end_date)
    result = df_filtered.groupby(group_by).size().reset_index(name='total_tickets')
    return result.to_dict(orient='records')

# calc overdue percentage by dept/sub dept
def overdue_analysis_by_entity(df, group_by='department', start_date=None, end_date=None):
    df_filtered = filter_by_date(df, start_date, end_date)
    result = df_filtered.groupby(group_by).agg(
        total_tickets=('ticket_status', 'count'),
        overdue_tickets=('overdue_hours', lambda x: (x > 0).sum())
    ).reset_index()
    result['avg_overdue_percentage'] = round((result['overdue_tickets'] / result['total_tickets']) * 100, 2)
    return result.to_dict(orient='records')

# calc load of overdue by dept/sub dept
def workload_vs_overdue_by_entity(df, group_by='department', start_date=None, end_date=None):
    df_filtered = filter_by_date(df, start_date, end_date)
    result = df_filtered.groupby(group_by).agg(
        tickets_handled=('ticket_status', 'count'),
        overdue_percentage=('overdue_hours', lambda x: (x > 0).sum() / len(x) * 100)
    ).reset_index()
    return result.to_dict(orient='records')

# monthly trends by dept/sub dept
def monthly_trends_by_entity(df, group_by='department', start_date=None, end_date=None):
    df_filtered = filter_by_date(df, start_date, end_date)
    df_filtered ['month'] = pd.to_datetime(df_filtered ['opened_date']).dt.to_period('M').astype(str)
    result = df_filtered.groupby(['month', group_by]).agg(
        avg_overdue_percentage=('overdue_hours', lambda x: (x > 0).sum() / len(x) * 100),
        avg_time_hours=('handling_time_hours', 'mean')
    ).reset_index()
    return result.to_dict(orient='records')

# curren state of dept/sub dept
def summary_status_by_entity(df, group_by='department', start_date=None, end_date=None):
    df_filtered = filter_by_date(df, start_date, end_date)
    open_tickets = df_filtered[df_filtered['ticket_status'] != 'הטיפול הסתיים'].groupby(group_by).size().reset_index(name='open_tickets')
    closed_df = df_filtered[df_filtered['ticket_status'] == 'הטיפול הסתיים']
    closed_on_time = closed_df[closed_df['overdue_hours'] == 0].groupby(group_by).size().reset_index(name='closed_on_time')
    closed_overdue = closed_df[closed_df['overdue_hours'] > 0].groupby(group_by).size().reset_index(name='closed_overdue')
    
    summary = pd.merge(open_tickets, closed_on_time, on=group_by, how='outer')
    summary = pd.merge(summary, closed_overdue, on=group_by, how='outer').fillna(0)

    summary[['open_tickets', 'closed_on_time', 'closed_overdue']] = summary[['open_tickets', 'closed_on_time', 'closed_overdue']].astype(int)

    return summary.to_dict(orient='records')

# returns total tickets and overdue tickets
def monthly_tickets_and_overdues(df, start_date=None, end_date=None):
    df_filtered = filter_by_date(df, start_date, end_date)
    df_filtered['month'] = pd.to_datetime(df_filtered['opened_date']).dt.to_period('M').astype(str)

    result = df_filtered.groupby('month').agg(
        total_tickets=('ticket_status', 'count'),
        overdue_tickets=('overdue_hours', lambda x: (x > 0).sum())
    ).reset_index()

    return result.to_dict(orient='records')