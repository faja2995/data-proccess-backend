import io
import json
import re

import numpy as np
import pandas as pd
from datetime import datetime
from typing import BinaryIO


def check_if_categorical(column, df):
    real_col = column.copy()
    if column.dtype == 'object':
        if column.nunique() / len(df) < 0.5:
            column = column.astype('category')
            return column, True
    return real_col, False


def append_dtype_to_column_names(df, dtypes):
    pattern = r'\(.*?\)'

    remove_parentheses = lambda x: re.sub(pattern, '', x)

    # Remove parentheses from column names
    df.columns = [remove_parentheses(col) for col in df.columns]
    new_column_names = [f"{col}({dtype})" for col, dtype in zip(df.columns, dtypes)]
    df.columns = new_column_names
    return df


def check_if_numerical(column):
    real_col = column.copy()
    numeric_values = pd.to_numeric(column, errors='coerce')
    numeric_count = np.sum(~np.isnan(numeric_values))
    total_count = len(column)
    if total_count > 0:
        if (numeric_count / total_count) >= 0.75:
            column = pd.to_numeric(column, errors='coerce')
            if column.dtype == 'float64':

                if not column.isnull().any():
                    column = column.astype('float32')
            elif column.dtype == 'int64':
                if column.min() > -128 and column.max() < 127:
                    column = column.astype('int8')
                elif column.min() > -32768 and column.max() < 32767:
                    column = column.astype('int16')
                elif column.min() > -2147483648 and column.max() < 2147483647:
                    column = column.astype('int32')
            return column, True
    return real_col, False


def is_date_time(column):
    def is_valid_date(date_str):
        formats = [
            '%Y/%m/%d', '%Y-%m-%d', '%m/%d/%Y', '%m-%d-%Y', '%d/%m/%Y', '%d-%m-%Y',
            '%Y/%m/%d %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M:%S', '%m-%d-%Y %H:%M:%S',
            '%d/%m/%Y %H:%M:%S', '%d-%m-%Y %H:%M:%S'
        ]
        for fmt in formats:
            try:
                datetime.strptime(date_str, fmt)
                return fmt
            except ValueError:
                pass
        return None

    real_col = column.copy()
    if column.dtype == 'object':
        datetime_format = is_valid_date(column.iloc[0])  # Get the format of the first valid date
        if datetime_format:
            temp_datetime = pd.to_datetime(column, errors='coerce', format=datetime_format)
            datetime_count = temp_datetime.notnull().sum()
            total_count = len(column)
            percentage = datetime_count / total_count * 100
            if percentage >= 75:
                column = temp_datetime
                return column, True
    return real_col, False


def is_boolean(column):
    real_col = column.copy()
    if column.dtype == 'object':
        column = column.apply(lambda x: x if x in ['True', 'False'] else pd.NA)

        column = column.map({'True': True, 'False': False})

        boolean_count = column.count()
        total_count = len(column)
        if boolean_count / total_count > 0.74:
            column = column.astype('boolean')
            return column, True
    return real_col, False


def filter_and_convert_complex(column):
    def is_complex(val):
        try:
            complex(val)
            return True
        except ValueError:
            return False

    is_complex_column = column.apply(lambda x: is_complex(x))

    percentage_complex = is_complex_column.sum() / len(is_complex_column) * 100

    if percentage_complex > 75:
        column = column[is_complex_column].apply(complex)

        return column, True
    return column, False


def infer_types(file: BinaryIO):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")
        for col in df.columns:
            converted, can_pass = is_boolean(df[col])
            if can_pass:
                df[col] = converted
                continue
            converted, can_pass = check_if_categorical(df[col], df)
            if can_pass:
                df[col] = converted
                continue
            converted, can_pass = check_if_numerical(df[col])
            if can_pass:
                df[col] = converted
                continue
            converted, can_pass = is_date_time(df[col])
            if can_pass:
                df[col] = converted
                continue
            converted, can_pass = filter_and_convert_complex(df[col])
            if can_pass:
                df[col] = converted
                continue
        output = io.BytesIO()
        df = append_dtype_to_column_names(df, df.dtypes)

        df.to_csv(output, index=False)
        output.seek(0)
        return output
    except Exception as e:
        print(e)
        return e


def change_types(file: BinaryIO, types: str):


    try:
        json_data = json.loads(types)
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")

        for col in df.columns:
            converted, can_pass = is_boolean(df[col])
            if can_pass:
                df[col] = converted
                continue
            converted, can_pass = check_if_categorical(df[col], df)
            if can_pass:
                df[col] = converted
                continue
            converted, can_pass = check_if_numerical(df[col])
            if can_pass:
                df[col] = converted
                continue
            converted, can_pass = is_date_time(df[col])
            if can_pass:
                df[col] = converted
                continue
            converted, can_pass = filter_and_convert_complex(df[col])
            if can_pass:
                df[col] = converted
                continue
        is_numeric = False
        for col, suggested_type in json_data.items():

            try:
                if suggested_type == "int32":
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int32")
                    is_numeric = True
                elif suggested_type == "int64":
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
                    is_numeric = True
                elif suggested_type == "int16":
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int16")
                    is_numeric = True
                elif suggested_type == "int8":
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int8")
                    is_numeric = True
                # float
                elif suggested_type == "float64":
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")
                    is_numeric = True
                elif suggested_type == "float32":
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("float32")
                    is_numeric = True
                elif suggested_type == "float16":
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("float16")
                    is_numeric = True
                # boolean
                elif suggested_type == "bool":
                    df[col] = df[col].astype("boolean")
                # datetime
                elif suggested_type == "datetime64":
                    df[col] = pd.to_datetime(df[col], errors="coerce")
                # timedelta
                elif suggested_type == "timedelta":
                    df[col] = pd.to_timedelta(df[col], errors="coerce")
                # category
                elif suggested_type == "category":
                    df[col] = df[col].astype("category")
                # object
                elif suggested_type == "object":
                    df[col] = df[col].astype("object")
                else:
                    raise ValueError(f"Unsupported type: {suggested_type}")
            except:

                if is_numeric:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(suggested_type)
                    is_numeric = False
                continue
        df = append_dtype_to_column_names(df, df.dtypes)
        output = io.BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return output
    except Exception as e:
        print(e)
        return e


