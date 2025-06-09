import pandas as pd
from sklearn.multioutput import MultiOutputRegressor
from xgboost import XGBRegressor
from datetime import datetime
import os

# === 1. Load and prepare data ===
base_path = os.path.dirname(os.path.dirname(__file__))  
filepath = os.path.join(base_path, 'data', 'DATA_MOKED.csv')
df = pd.read_csv(filepath, parse_dates=['opened_date'])
df['month'] = df['opened_date'].dt.to_period('M').dt.to_timestamp()

# === 2. Train one MultiOutputRegressor per (department, sub_department) ===
models = {}
category_cols = {}

for dept, sub in df[['department','sub_department']].drop_duplicates().values:
    sub_df = df[(df['department'] == dept) & (df['sub_department'] == sub)]
    if sub_df.empty:
        continue
    
    # Monthly counts per category
    monthly = sub_df.groupby(['month','category']).size().reset_index(name='ticket_count')
    pivot = (
        monthly
        .pivot(index='month', columns='category', values='ticket_count')
        .fillna(0)
        .reset_index()
    )
    
    # Create features
    pivot['month_num'] = pivot['month'].dt.month
    pivot['year']      = pivot['month'].dt.year
    
    X = pivot[['month_num','year']]
    Y = pivot.drop(columns=['month','month_num','year'])
    if Y.shape[1] < 1:
        continue
    
    # Train model on full history
    model = MultiOutputRegressor(
        XGBRegressor(n_estimators=100, random_state=42, verbosity=0)
    )
    model.fit(X, Y)
    
    key = (dept, sub)
    models[key] = model
    category_cols[key] = list(Y.columns)

# === 3. Prediction function ===
def predict_top_category(department: str, sub_department: str, year: int = None, month: int = None) -> str:
    """
    Returns the category predicted to have the most tickets for the given
    department and sub_department in the specified (or current) year/month.
    """
    key = (department, sub_department)
    if key not in models:
        raise ValueError(f"No model trained for ({department} / {sub_department})")
    
    # Default to current month/year if not provided
    today = datetime.today()
    year  = year  or today.year
    month = month or today.month
    
    X_new = pd.DataFrame({'month_num': [month], 'year': [year]})
    preds = models[key].predict(X_new)[0]
    idx   = int(preds.argmax())
    return category_cols[key][idx]

# # === 4. Example use ===
# if __name__ == "__main__":
#     dept = 'אגף תפעול'
#     sub  = 'מחלקת תברואה'
#     print(f"מסגרת: {dept} / {sub}")
#     print("קטגוריה צפויה למירב הפניות:", predict_top_category(dept, sub))