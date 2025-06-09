import pandas as pd

# load the data csv and return DataFrame                   
def load_data(filepath='data/DATA_MOKED.csv'):
    """
    טוען את קובץ הנתונים ומחזיר DataFrame.
    """
    df = pd.read_csv(filepath)
    return df


def get_employees_closed_tickets_count(df, department, sub_department, start_date, end_date):
    """
    מחזיר רשימה של עובדים עם כמות הפניות שנסגרו בפועל במחלקה מסוימת ובטווח תאריכים מוגדר.
    פנייה נחשבת סגורה אם יש לה ערך ב־closed_date (לא null).

    Args:
        df (pd.DataFrame): טבלת הנתונים.
        department (str): שם האגף.
        sub_department (str): שם המחלקה.
        start_date (str): תאריך התחלה בפורמט 'YYYY-MM-DD'.
        end_date (str): תאריך סיום בפורמט 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: טבלה עם שם העובד וכמות הפניות שנסגרו.
    """
    # המרת opened_date ו- closed_date לפורמט datetime אם עדיין לא מומש
    if df['opened_date'].dtype != 'datetime64[ns]':
        df['opened_date'] = pd.to_datetime(df['opened_date'], dayfirst=False, errors='coerce')
    if df['closed_date'].dtype != 'datetime64[ns]':
        df['closed_date'] = pd.to_datetime(df['closed_date'], dayfirst=False, errors='coerce')

    # סינון לפי אגף, מחלקה, טווח תאריכים, עובד לא ריק, ויש closed_date (פנייה סגורה)
    filtered_df = df[
        (df['department'] == department) &
        (df['sub_department'] == sub_department) &
        (df['employee'].notnull()) &
        (df['closed_date'].notnull()) &
        (df['opened_date'] >= pd.to_datetime(start_date)) &
        (df['opened_date'] <= pd.to_datetime(end_date))
    ]

    # ספירת פניות שנסגרו לכל עובד
    tickets_per_employee = (
        filtered_df.groupby('employee')
        .size()
        .reset_index(name='tickets_handled')
        .sort_values(by='tickets_handled', ascending=False)
    )

    # החזרת הפלט בפורמט רשימת מילונים
    return tickets_per_employee.to_dict(orient='records')


def get_employees_closed_tickets_percentage_from_all_closed_tickets(df, department, sub_department, start_date, end_date):
    """
    מחזיר רשימה של עובדים עם האחוז מתוך כלל הפניות שנסגרו במחלקה שהם סגרו בפועל.
    פנייה נחשבת סגורה אם יש לה ערך ב־closed_date (לא null).

    Args:
        df (pd.DataFrame): טבלת הנתונים.
        department (str): שם האגף.
        sub_department (str): שם המחלקה.
        start_date (str): תאריך התחלה בפורמט 'YYYY-MM-DD'.
        end_date (str): תאריך סיום בפורמט 'YYYY-MM-DD'.

    Returns:
        list of dict: רשימת עובדים עם אחוז הפניות שנסגרו מתוך כלל הפניות הסגורות במחלקה.
    """
    # המרת תאריכים
    df['opened_date'] = pd.to_datetime(df['opened_date'], errors='coerce')
    df['closed_date'] = pd.to_datetime(df['closed_date'], errors='coerce')

    # סינון למחלקה הרלוונטית ולפניות סגורות בלבד
    filtered_df = df[
        (df['department'] == department) &
        (df['sub_department'] == sub_department) &
        (df['employee'].notnull()) &
        (df['closed_date'].notnull()) &
        (df['opened_date'] >= pd.to_datetime(start_date)) &
        (df['opened_date'] <= pd.to_datetime(end_date))
    ]

    if filtered_df.empty:
        return []

    # סופרים כמה כל עובד סגר
    tickets_per_employee = (
        filtered_df.groupby('employee')
        .size()
        .reset_index(name='tickets_handled')
    )

    # סך כל הפניות הסגורות במחלקה
    total_closed_tickets = tickets_per_employee['tickets_handled'].sum()

    # חישוב אחוזים
    tickets_per_employee['closed_tickets_percentage'] = (
        tickets_per_employee['tickets_handled'] / total_closed_tickets * 100
    )

    # רק האחוזים — בלי מספר הפניות
    result = tickets_per_employee[['employee', 'closed_tickets_percentage']] \
        .sort_values(by='closed_tickets_percentage', ascending=False)

    return result.to_dict(orient='records')


def get_employees_total_tickets_count(df, department, sub_department, start_date, end_date):
    """
    מחזיר רשימה של עובדים עם סך כל הפניות שהוקצו להם (סגורות + פתוחות)
    במחלקה מסוימת ובטווח תאריכים מוגדר (לפי opened_date).
    
    💡 מאפשר לזהות עומס עבודה לא פרופורציונלי על עובדים מסוימים.

    Args:
        df (pd.DataFrame): טבלת הנתונים.
        department (str): שם האגף.
        sub_department (str): שם המחלקה.
        start_date (str): תאריך התחלה בפורמט 'YYYY-MM-DD'.
        end_date (str): תאריך סיום בפורמט 'YYYY-MM-DD'.

    Returns:
        list of dict: רשימת עובדים עם שם העובד וכמות כלל הפניות שהוקצו לו.
    """
    # המרת opened_date לפורמט datetime
    df['opened_date'] = pd.to_datetime(df['opened_date'], errors='coerce')

    # סינון למחלקה, טווח תאריכים ועובדים שהוגדרו
    filtered_df = df[
        (df['department'] == department) &
        (df['sub_department'] == sub_department) &
        (df['employee'].notnull()) &
        (df['opened_date'] >= pd.to_datetime(start_date)) &
        (df['opened_date'] <= pd.to_datetime(end_date))
    ]

    if filtered_df.empty:
        return []

    # סופרים כמה פניות יש לכל עובד (סגורות ופתוחות)
    tickets_per_employee = (
        filtered_df.groupby('employee')
        .size()
        .reset_index(name='total_tickets')
        .sort_values(by='total_tickets', ascending=False)
    )

    return tickets_per_employee.to_dict(orient='records')


#
def get_employees_total_tickets_percentage_from_all_tickets(df, department, sub_department, start_date, end_date):
    """
    מחשב את האחוז מתוך כלל הפניות במחלקה שהוקצו לכל עובד (סגורות + פתוחות).

    Args:
        df (pd.DataFrame): טבלת הנתונים.
        department (str): שם האגף.
        sub_department (str): שם המחלקה.
        start_date (str): תאריך התחלה בפורמט 'YYYY-MM-DD'.
        end_date (str): תאריך סיום בפורמט 'YYYY-MM-DD'.

    Returns:
        list of dict: רשימת עובדים עם האחוז מכלל הפניות במחלקה.
    """
    # המרת תאריכים
    df['opened_date'] = pd.to_datetime(df['opened_date'], errors='coerce')

    # סינון לפי אגף, מחלקה, טווח תאריכים, ועובדים
    filtered_df = df[
        (df['department'] == department) &
        (df['sub_department'] == sub_department) &
        (df['employee'].notnull()) &
        (df['opened_date'] >= pd.to_datetime(start_date)) &
        (df['opened_date'] <= pd.to_datetime(end_date))
    ]

    if filtered_df.empty:
        return []

    # סופרים את כלל הפניות של כל עובד
    tickets_per_employee = (
        filtered_df.groupby('employee')
        .size()
        .reset_index(name='total_tickets')
    )

    # מחשבים את סך כל הפניות של המחלקה
    total_tickets_in_department = tickets_per_employee['total_tickets'].sum()

    # חישוב אחוז לכל עובד
    tickets_per_employee['total_tickets_percentage'] = (
        tickets_per_employee['total_tickets'] / total_tickets_in_department * 100
    )

    result = tickets_per_employee[['employee', 'total_tickets_percentage']] \
        .sort_values(by='total_tickets_percentage', ascending=False)

    return result.to_dict(orient='records')


def get_current_tickets_status(df, department, sub_department, start_date, end_date):
    """
    מחזיר תמונת מצב עכשווית של עומסים וביצועים:
    - כמות פניות פתוחות כרגע
    - כמות פניות סגורות בזמן
    - כמות פניות סגורות עם חריגה

    Args:
        df (pd.DataFrame): טבלת הנתונים.
        department (str): שם האגף.
        sub_department (str): שם המחלקה.
        start_date (str): תאריך התחלה בפורמט 'YYYY-MM-DD'.
        end_date (str): תאריך סיום בפורמט 'YYYY-MM-DD'.

    Returns:
        dict: תמונת מצב עם כמות פניות פתוחות, סגורות בזמן, וחריגות.
    """
    # המרת תאריכים
    df['opened_date'] = pd.to_datetime(df['opened_date'], errors='coerce')
    df['closed_date'] = pd.to_datetime(df['closed_date'], errors='coerce')

    # סינון לפי אגף, מחלקה, טווח תאריכים
    filtered_df = df[
        (df['department'] == department) &
        (df['sub_department'] == sub_department) &
        (df['opened_date'] >= pd.to_datetime(start_date)) &
        (df['opened_date'] <= pd.to_datetime(end_date))
    ]

    if filtered_df.empty:
        return {
            'open_tickets': 0,
            'closed_on_time': 0,
            'closed_overdue': 0
        }

    # חישובים:
    open_tickets = filtered_df['closed_date'].isnull().sum()

    closed_on_time = filtered_df[
        (filtered_df['closed_date'].notnull()) & (filtered_df['overdue_hours'] <= 0)
    ].shape[0]

    closed_overdue = filtered_df[
        (filtered_df['closed_date'].notnull()) & (filtered_df['overdue_hours'] > 0)
    ].shape[0]

    return {
        'open_tickets': int(open_tickets),
        'closed_on_time': int(closed_on_time),
        'closed_overdue': int(closed_overdue)
    }


def get_employees_on_time_percentage(df, department, sub_department, start_date, end_date):
    """
    מחשב את אחוז הסגירות בזמן (on time) של כל עובד מתוך הפניות שהוא סגר.
    פנייה נחשבת בזמן אם overdue_hours <= 0.
    """
    df['opened_date'] = pd.to_datetime(df['opened_date'], errors='coerce')
    df['closed_date'] = pd.to_datetime(df['closed_date'], errors='coerce')

    filtered_df = df[
        (df['department'] == department) &
        (df['sub_department'] == sub_department) &
        (df['employee'].notnull()) &
        (df['closed_date'].notnull()) &
        (df['opened_date'] >= pd.to_datetime(start_date)) &
        (df['opened_date'] <= pd.to_datetime(end_date))
    ]

    if filtered_df.empty:
        return []

    stats = (
        filtered_df.groupby('employee')
        .agg(
            total_closed=('employee', 'count'),
            on_time_closed=('overdue_hours', lambda x: (x <= 0).sum())
        )
        .reset_index()
    )

    stats['on_time_percentage'] = (stats['on_time_closed'] / stats['total_closed']) * 100

    return stats[['employee', 'on_time_percentage']].to_dict(orient='records')


def get_employees_overdue_percentage(df, department, sub_department, start_date, end_date):
    """
    מחשב את אחוז החריגות (overdue) של כל עובד מתוך הפניות שהוא סגר.
    פנייה בחריגה אם overdue_hours > 0.
    """
    df['opened_date'] = pd.to_datetime(df['opened_date'], errors='coerce')
    df['closed_date'] = pd.to_datetime(df['closed_date'], errors='coerce')

    filtered_df = df[
        (df['department'] == department) &
        (df['sub_department'] == sub_department) &
        (df['employee'].notnull()) &
        (df['closed_date'].notnull()) &
        (df['opened_date'] >= pd.to_datetime(start_date)) &
        (df['opened_date'] <= pd.to_datetime(end_date))
    ]

    if filtered_df.empty:
        return []

    stats = (
        filtered_df.groupby('employee')
        .agg(
            total_closed=('employee', 'count'),
            overdue_closed=('overdue_hours', lambda x: (x > 0).sum())
        )
        .reset_index()
    )

    stats['overdue_percentage'] = (stats['overdue_closed'] / stats['total_closed']) * 100

    return stats[['employee', 'overdue_percentage']].to_dict(orient='records')


def get_employees_avg_handling_time(df, department, sub_department, start_date, end_date):
    """
    מחשב את משך הטיפול הממוצע (בשעות עבודה) לכל עובד מתוך הפניות שהוא סגר.
    """
    df['opened_date'] = pd.to_datetime(df['opened_date'], errors='coerce')
    df['closed_date'] = pd.to_datetime(df['closed_date'], errors='coerce')

    filtered_df = df[
        (df['department'] == department) &
        (df['sub_department'] == sub_department) &
        (df['employee'].notnull()) &
        (df['closed_date'].notnull()) &
        (df['opened_date'] >= pd.to_datetime(start_date)) &
        (df['opened_date'] <= pd.to_datetime(end_date))
    ]

    if filtered_df.empty:
        return []

    avg_time = (
        filtered_df.groupby('employee')
        .agg(avg_handling_time_hours=('handling_time_hours', 'mean'))
        .reset_index()
    )

    return avg_time.to_dict(orient='records')


def prepare_employees_performance_data(df, department, sub_department, start_date, end_date):
    """
    מאחד את כל נתוני הביצועים לעובדים:
    - כמות פניות סגורות (tickets_handled)
    - אחוז חריגות (overdue_percentage)
    - משך טיפול ממוצע (avg_handling_time_hours)
    - כמות כלל הפניות שהוקצו (total_tickets)
    - אחוז סגירה בזמן (on_time_percentage)

    Returns:
        list of dict: טבלת ביצועים מאוחדת לפי עובד, מוכנה לדירוג או לדשבורד.
    """
    # שליפת הנתונים מהפונקציות הקיימות:
    closed_tickets = get_employees_closed_tickets_count(df, department, sub_department, start_date, end_date)
    overdue_percentage = get_employees_overdue_percentage(df, department, sub_department, start_date, end_date)
    avg_handling_time = get_employees_avg_handling_time(df, department, sub_department, start_date, end_date)
    total_tickets = get_employees_total_tickets_count(df, department, sub_department, start_date, end_date)
    on_time_percentage = get_employees_on_time_percentage(df, department, sub_department, start_date, end_date)

    # המרה ל-DataFrame:
    df_closed = pd.DataFrame(closed_tickets)
    df_overdue = pd.DataFrame(overdue_percentage)
    df_time = pd.DataFrame(avg_handling_time)
    df_total = pd.DataFrame(total_tickets)
    df_on_time = pd.DataFrame(on_time_percentage)

    # איחוד לפי employee:
    merged = df_closed.merge(df_overdue, on='employee', how='inner') \
                      .merge(df_time, on='employee', how='inner') \
                      .merge(df_total, on='employee', how='inner') \
                      .merge(df_on_time, on='employee', how='inner')

    # החזרת הפלט בפורמט list of dict:
    return merged.to_dict(orient='records')


def get_top_n_employees_scores(
    df,
    department,
    sub_department,
    start_date,
    end_date,
    n=5,
    weight_tickets=0.5,
    weight_overdue=0.3,
    weight_time=0.2,
    min_closed_tickets=10
):
    """
    מחשב ניקוד משוקלל לכל העובדים לפי:
    - כמות סגירות
    - אחוז חריגות
    - משך טיפול ממוצע
    ומחזיר את N העובדים עם הציונים הגבוהים ביותר.

    Args:
        df (pd.DataFrame): טבלת הנתונים המלאה.
        department (str): שם האגף.
        sub_department (str): שם המחלקה.
        start_date (str): תאריך התחלה.
        end_date (str): תאריך סיום.
        n (int): כמה מצטיינים להחזיר (ברירת מחדל 5).
        weight_tickets (float): משקל לעומס.
        weight_overdue (float): משקל לחריגות.
        weight_time (float): משקל למשך טיפול.
        min_closed_tickets (int): סף מינימום לפניות סגורות.

    Returns:
        list of dict: חמשת העובדים עם הציונים הגבוהים ביותר.
    """
    import pandas as pd

    # שלב 1: איחוד הנתונים:
    performance_data = prepare_employees_performance_data(
        df, department, sub_department, start_date, end_date
    )

    if not performance_data:
        return [{'message': 'אין עובדים עם נתוני ביצועים בטווח התאריכים והמחלקה המבוקשים.'}]

    df_perf = pd.DataFrame(performance_data)

    # שלב 2: סינון לפי סף פניות סגורות:
    df_perf = df_perf[df_perf['tickets_handled'] >= min_closed_tickets]

    if df_perf.empty:
        return [{'message': 'אין עובדים שעומדים בסף המינימום של פניות סגורות.'}]

    # שלב 3: נירמול:
    def normalize(series):
        if series.max() == series.min():
            return series.apply(lambda x: 1)
        return (series - series.min()) / (series.max() - series.min())

    df_perf['norm_tickets'] = normalize(df_perf['tickets_handled'])
    df_perf['norm_overdue'] = normalize(df_perf['overdue_percentage'])
    df_perf['norm_time'] = normalize(df_perf['avg_handling_time_hours'])

    # שלב 4: חישוב ציון משוקלל:
    df_perf['score'] = (
        weight_tickets * df_perf['norm_tickets'] -
        weight_overdue * df_perf['norm_overdue'] -
        weight_time * df_perf['norm_time']
    )

    # שלב 5: מיון והחזרת החמישה הראשונים:
    top_n = df_perf.sort_values(by='score', ascending=False).head(n)

    return top_n.to_dict(orient='records')














# #
# def get_top_employees_by_on_time_percentage(df, department, sub_department, start_date, end_date):
#     """
#     מחזיר רשימה של עובדים עם אחוז הסגירה בזמן הגבוה ביותר במחלקה מסוימת ובטווח תאריכים מוגדר.
#     פנייה נחשבת סגורה אם יש לה ערך ב־closed_date (לא null).
#     פנייה נחשבת שנסגרה בזמן אם overdue_hours <= 0.

#     Args:
#         df (pd.DataFrame): טבלת הנתונים.
#         department (str): שם האגף.
#         sub_department (str): שם המחלקה.
#         start_date (str): תאריך התחלה בפורמט 'YYYY-MM-DD'.
#         end_date (str): תאריך סיום בפורמט 'YYYY-MM-DD'.

#     Returns:
#         list of dict: רשימת מילונים עם שם העובד ואחוז הסגירה בזמן.
#     """

#     # המרת תאריכים
#     df['opened_date'] = pd.to_datetime(df['opened_date'], errors='coerce')
#     df['closed_date'] = pd.to_datetime(df['closed_date'], errors='coerce')

#     # סינון לפי אגף, מחלקה, טווח תאריכים, עובד לא ריק, ופניות סגורות בלבד
#     filtered_df = df[
#         (df['department'] == department) &
#         (df['sub_department'] == sub_department) &
#         (df['employee'].notnull()) &
#         (df['closed_date'].notnull()) &
#         (df['opened_date'] >= pd.to_datetime(start_date)) &
#         (df['opened_date'] <= pd.to_datetime(end_date))
#     ]

#     if filtered_df.empty:
#         return []

#     # חישוב אחוז סגירה בזמן לכל עובד
#     grouped = filtered_df.groupby('employee').apply(
#         lambda x: (x['overdue_hours'] <= 0).sum() / len(x) * 100
#     ).reset_index(name='on_time_percentage')

#     # מיון לפי אחוז סגירה בזמן מהגבוה לנמוך
#     grouped = grouped.sort_values(by='on_time_percentage', ascending=False)

#     return grouped.to_dict(orient='records')


# def calculate_employee_z_scores(performance_data, alpha=0.5, beta=0.5):
#     """
#     מחשב Z-Score לכל עובד גם על כמות פניות סגורות וגם על אחוז סגירה בזמן,
#     ומחזיר ציון משוקלל (score) של שניהם.

#     Args:
#         performance_data (list of dict): הפלט של הפונקציה הקודמת (כולל total_closed_tickets ו-on_time_percentage).
#         alpha (float): משקל ל-Z-Score של on_time_percentage.
#         beta (float): משקל ל-Z-Score של total_closed_tickets.

#     Returns:
#         list of dict: רשימת עובדים עם z_score_on_time, z_score_total_closed, ו-score.
#     """
#     df = pd.DataFrame(performance_data)

#     # חישוב Z-Score לכל שדה
#     df['z_score_on_time'] = (df['on_time_percentage'] - df['on_time_percentage'].mean()) / df['on_time_percentage'].std(ddof=0)
#     df['z_score_total_closed'] = (df['total_closed_tickets'] - df['total_closed_tickets'].mean()) / df['total_closed_tickets'].std(ddof=0)

#     # חישוב ציון משוקלל
#     df['score'] = alpha * df['z_score_on_time'] + beta * df['z_score_total_closed']

#     # מיון לפי הציון המשוקלל
#     df = df.sort_values(by='score', ascending=False)

#     return df.to_dict(orient='records')


def calculate_employee_z_scores_from_data(
    df,
    department,
    sub_department,
    start_date,
    end_date,
    alpha=0.5,
    beta=0.5,
    min_closed_tickets=10,
    n=5
):
    """
    מאחד נתוני ביצועים, מחשב Z-Score על אחוז סגירה בזמן ועל כמות פניות סגורות,
    ומחזיר את N העובדים עם הציון הגבוה ביותר.

    Args:
        df (pd.DataFrame): טבלת הנתונים.
        department (str): שם האגף.
        sub_department (str): שם המחלקה.
        start_date (str): תאריך התחלה.
        end_date (str): תאריך סיום.
        alpha (float): משקל ל־on_time_percentage.
        beta (float): משקל ל־total_closed_tickets.
        min_closed_tickets (int): סף מינימום לפניות סגורות.
        n (int): כמות העובדים המובילים להחזיר (Top N).

    Returns:
        list of dict: רשימת העובדים עם הציונים.
    """
    # שלב 1: מאחדים את הנתונים:
    performance_data = prepare_employees_performance_data(
        df, department, sub_department, start_date, end_date
    )

    if not performance_data:
        return [{'message': 'אין עובדים עם נתוני ביצועים בטווח התאריכים והמחלקה המבוקשים.'}]

    df_perf = pd.DataFrame(performance_data)

    # שלב 2: סינון לפי סף מינימום פניות סגורות:
    df_perf = df_perf[df_perf['tickets_handled'] >= min_closed_tickets]

    if df_perf.empty:
        return [{'message': 'אין עובדים שעומדים בסף המינימום של פניות סגורות.'}]

    # שלב 3: חישוב Z-Score:
    def z_score(series):
        if series.std(ddof=0) == 0:
            return pd.Series([0] * len(series))  # אם אין שונות בכלל
        return (series - series.mean()) / series.std(ddof=0)

    df_perf['z_score_on_time'] = z_score(df_perf['on_time_percentage'])
    df_perf['z_score_total_closed'] = z_score(df_perf['tickets_handled'])

    # שלב 4: חישוב ציון משוקלל:
    df_perf['score'] = alpha * df_perf['z_score_on_time'] + beta * df_perf['z_score_total_closed']

    # שלב 5: מיון והחזרת Top N:
    top_n = df_perf.sort_values(by='score', ascending=False).head(n)
    top_n['rank'] = range(1, len(top_n) + 1)  # הוספת מיקום

    return top_n.to_dict(orient='records')


def get_monthly_performance_trends(df, department, sub_department, start_date, end_date):
    df['opened_date'] = pd.to_datetime(df['opened_date'], errors='coerce')
    df['closed_date'] = pd.to_datetime(df['closed_date'], errors='coerce')

    filtered_df = df[
        (df['department'] == department) &
        (df['sub_department'] == sub_department) &
        (df['opened_date'] >= pd.to_datetime(start_date)) &
        (df['opened_date'] <= pd.to_datetime(end_date)) &
        (df['closed_date'].notnull())
    ].copy()

    if filtered_df.empty:
        return []

    filtered_df['month'] = filtered_df['opened_date'].dt.to_period('M').astype(str)

    monthly_stats = (
        filtered_df.groupby('month')
        .agg(
            avg_overdue_percentage=('overdue_hours', lambda x: (x > 0).sum() / len(x) * 100),
            avg_handling_time_hours=('handling_time_hours', 'mean')
        )
        .reset_index()
    )

    return monthly_stats.to_dict(orient='records')