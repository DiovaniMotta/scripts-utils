from datetime import datetime
from dateutil.relativedelta import relativedelta

def datetime_to_str(value: datetime):
    if value:
        return value.strftime('%Y-%m-%d')
    return ''

def calculate_diff_dates_as_string(date1_str: str, date2_str: str):
    date1 = datetime.strptime(date1_str, "%Y-%m-%d")
    date2 = datetime.strptime(date2_str, "%Y-%m-%d")
    diff = relativedelta(date2, date1) if date2 >= date1 else relativedelta(date1, date2)
    return {
       'years': diff.years,
       'months': diff.months
    }