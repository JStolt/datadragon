import pandas as pd
import os
import sys

def read_csv(path):
    return pd.read_csv(path)

"""Schema utilites"""

# Next up:
# schema enforcement
# expanding system offerings


data_type_map = {
    'system': ['pandas', 'postgres'],
    'string': ['object', 'varchar'],
    'int': ['int64', 'bigint'],
    'float': ['float64', 'float']
}

# :TODO Option 2 - still considering
# data_type_map = {
#     # 'system': ['pandas', 'postgres'],
#     'string': {
#         'pandas': 'object',
#         'postgres': 'varchar'},
#     'int': {
#         'pandas': 'int64',
#         'postgres': 'bigint'},
#     'float': {
#         'pandas': 'float64',
#         'postgres': 'float'}
# }

create_stmt_map = {
    'postgres': """CREATE TABLE {} ({});""",
    'mysql': """""",
    'sqlserver': """""",
    'oracle': """""",
    'snowflake': """""",
    'redshift': """""",
    'teradata': """""",
    'bigquery': """"""
}

def convert_data_types(src_system: str, dest_system: str,
                       src_types: list) -> list:
    """
    Converts field data types from source system to destination system types
    :param src_system: The name of the source system
    :param dest_system: The name of the destination system
    :param src_types: List of source field data types
    :return: List of destination field data types
    """
    try:
        src_system_index = data_type_map['system'].index(src_system.lower())
    except ValueError:
        raise ValueError("Source system is wrong or not supported.")
    try:
        dest_system_index = data_type_map['system'].index(dest_system.lower())
    except ValueError:
        raise ValueError("Destination system is wrong or not supported.")
    dest_types = []

    for item in src_types:
        for k, v in data_type_map.items():
            if v[src_system_index] == item:
                dest_types.append(v[dest_system_index])
            #:TODO fix error handling
            # else:
            #     raise ValueError(f"Source type {item} not currently supported.")

    return dest_types


def build_create_statement(dest_system: str, table_name: str,
                           field_names: list, field_types: list) -> str:
    """
    Builds 'Create table' statement given destination system, table name,
        field names, and field types.
    :param dest_system: The name of the destination system
    :param table_name: The name of the table to be created
    :param field_names: The names of the fields to be in the table
    :param field_types: The data types of the fields to be in the table
    :return: Create statement for table in destination system given field names
        and data types
    """
    name_type = zip(field_names, field_types)
    name_type = [a + " " + b for a, b in name_type]

    if dest_system not in create_stmt_map.keys():
        raise ValueError("Destination system is wrong or not supported.")

    return create_stmt_map[dest_system].format(table_name, ', '.join(name_type))

directory = '/data'

for file in os.listdir(directory):
    f = os.path.join(directory, file)
    df = read_csv(f)
    new_dtypes = convert_data_types('pandas', 'postgres', [str(x) for x in df.dtypes])
    table_name = os.path.splitext(file)[0]
    print(build_create_statement('postgres', table_name, list(df.columns), new_dtypes))