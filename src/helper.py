from datetime import datetime as dTime
import calendar
import datetime
import pandas as pd
import decimal


def unix_to_date(u):
    if isinstance(u, str):
        ux = int(u)
    else:
        ux = u
    if len(str(ux)) == 13:
        ux = ux / 1000
    return dTime.utcfromtimestamp(ux)

def date_to_unix(d, time_only=False):
    """Return a time in seconds from 1/1/1970"""
    if time_only:
        return calendar.timegm(dTime.strptime(d, '%H:%M:%S').timetuple())
    elif isinstance(d, str) and len(d) == 10:
        return calendar.timegm(dTime.strptime(d, '%Y-%m-%d').timetuple())
    elif isinstance(d, str) and len(d) == 16:
        return calendar.timegm(dTime.strptime(f'{d}:00', '%Y-%m-%d %H:%M:%S').timetuple())
    elif isinstance(d, str) and len(d) == 19:
        return calendar.timegm(dTime.strptime(d, '%Y-%m-%d %H:%M:%S').timetuple())
    elif isinstance(d, dTime):
        return calendar.timegm(d.timetuple())
    else:
        raise 'Not a valid date or time'

def dtNow():
    a = dTime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(a)

def is_datetime(my_string):
    # List of common date time formats to check against
    date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%m-%d-%Y', '%d-%m-%Y', '%d/%m/%Y', '%Y%m%d', '%m%d%Y', '%d%m%Y']
    time_formats = ['%H:%M:%S', '%I:%M:%S %p', '%H%M%S']
    # Loop through formats and try to parse string as datetime
    if isinstance(my_string, datetime.datetime) or isinstance(my_string, datetime.date):
        return True
    if my_string is not None and isinstance(my_string, str):
        if len(my_string) >= 8:
            for date_fmt in date_formats:
                for time_format in time_formats:
                    for ty in ['date_only', 'time_only', 'both']:
                        if ty == 'date_only':
                            try:
                                dt = datetime.datetime.strptime(my_string, f'{date_fmt}')
                                return True
                            except ValueError:
                                pass
                        elif ty == 'time_only':
                            try:
                                dt = datetime.datetime.strptime(my_string, f'{time_format}')
                                return True
                            except ValueError:
                                pass
                        elif ty == 'both':
                            try:
                                dt = datetime.datetime.strptime(my_string, f'{date_fmt} {time_format}')
                                return True
                            except ValueError:
                                pass
                            try:
                                dt = datetime.datetime.strptime(my_string, f'{date_fmt}{time_format}')
                                return True
                            except ValueError:
                                pass
    return False

def get_type(my_string, pandas=False):
    """Will return an interpreted data type of any Py variable"""
    if my_string is None:
        return None
    elif is_datetime(my_string) and pandas:
        return 'datetime64[ns]'
    elif is_datetime(my_string):
        return 'datetime'
    elif isinstance(my_string, str):
        try:
            int_val = int(my_string)
            return 'int'
        except ValueError:
            try:
                float_val = float(my_string)
                return 'float'
            except ValueError:
                return 'str'
    elif isinstance(my_string, int):
        return 'int'
    elif isinstance(my_string, float):
        return 'float'
    elif isinstance(my_string, decimal.Decimal):
        return 'decimal'
    elif isinstance(my_string, list):
        return 'list'
    elif isinstance(my_string, dict):
        return 'dict'
    elif isinstance(my_string, tuple):
        return 'tuple'
    else:
        return type(my_string)

def list_to_df(my_list, first_row_is_header=True):
    """Give me a list and I will look at the first row of data and PROPERLY coerce
    and convert it to a DataFrame with proper column data types.
    """
    if first_row_is_header:
        column_names = my_list[0]
        data = my_list[1:]
    else:
        column_names = [f'col{x}' for x in range(len(my_list[0]))]
        data = my_list
    column_types = [get_type(x, True) for x in data[0]]
    column_dict = dict(zip(column_names, column_types))
    df = pd.DataFrame(data, columns=column_names)
    for col_name, data_type in column_dict.items():
        if data_type == 'decimal':
            df[col_name] = df[col_name].astype('float')
        elif data_type == 'datetime64[ns]':
            df[col_name] = pd.to_datetime(df[col_name], errors='ignore')
        else:
            df[col_name] = df[col_name].astype(data_type)
    return df
