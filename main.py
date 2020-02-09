import pandas as pd
import IPython as ip
import numpy as np
import pyodbc as po
import re


# Pre-condition: char_list is a list a character digits.
def sum_char_list(char_list):
    sum = 0

    for element in char_list:
        sum += int(element)

    return sum


def convert_1_0_strings_to_true_false_strings(df, column_name_list):
    for x in np.arange(start=0, stop=len(column_name_list), step=1):
        df.loc[df[column_name_list[x]] == "1", column_name_list[x]] = True
        df.loc[df[column_name_list[x]] == "0", column_name_list[x]] = False

def sum_sequence(df, column_name_list):
    for x in np.arange(start=0, stop=len(column_name_list), step=1):
        for (index_label, row_value) in df[column_name_list[x]].items():
            df[column_name_list[x]][index_label] = sum_char_list(list(row_value))

# TO DO------------------------------------------------------
def export_dataframe_to_SQL_Server(df, table_name):
    connection_string = """
    driver=ODBC Driver 17 for SQL Server;
    server=SHADOW-LN4F5NUO;
    database=FBI_Crime_Data;
    trusted_connection=True;
    """

    connection = po.connect(connection_string)

    query = """
    
    """
    df.to_sql(name=table_name, con=connection, schema="fbi_crime_data", if_exists="append", index=false)

def validate(df):
    # Correct column names?
    assert(df.columns.equals(pd.Index(["Numeric State Code", "ORI Code", "Population Group (inclusive)", "Division",
                                     "Year", "Metropolitan Statistical Area Number", "Reported by Adult Male?",
                                     "Reported by Adult Female?", "Reported by Juvenile?", "Adjustment", "Offense Code",
                                     "Male Pre-Teens", "Male Teenagers", "Male Young Adults", "Male Adults",
                                     "Male Seniors", "Female Pre-Teens", "Female Teenagers", "Female Young Adults",
                                     "Female Adults", "Female Seniors"])))



    assert(df["Numeric State Code"].dropna().str.contains(pat="^[0-6][0-9]$", regex=True).all())
    assert(df["Population Group (inclusive)"].dropna().str.contains(pat="^[1-9][A-E]?$", regex=True).all())
    assert(df["Division"].dropna().str.contains(pat="^[0-9]$", regex=True).all())
    assert(df["Year"].dropna().between(left=2010, right=2016).all())
    assert(df["Adjustment"].dropna().str.contains(pat="^[0-6]$", regex=True).all())
    assert(df["Offense Code"].dropna().str.contains(pat="^[0-2][0-9][0-9]?$", regex=True).all())

def import_file(file_location):
    total_recrods = 0;
    with open(file_location, mode = "r") as file:
        line = file.readline()
        total_recrods += 1
        while line != "":
            total_recrods += 1
            line = file.readline()

    chunksize = 1000
    iteration = 0

    # Import data.
    for df in pd.read_fwf(filepath_or_buffer=file_location,
                             names=["Numeric State Code", "ORI Code", "Population Group (inclusive)", "Division",
                                     "Year", "Metropolitan Statistical Area Number", "Reported by Adult Male?",
                                     "Reported by Adult Female?", "Reported by Juvenile?", "Adjustment", "Offense Code",
                                     "Male Pre-Teens", "Male Teenagers", "Male Young Adults", "Male Adults",
                                     "Male Seniors", "Female Pre-Teens", "Female Teenagers", "Female Young Adults",
                                     "Female Adults", "Female Seniors"],
                             dtype="object",
                             colspecs=[(1, 3), (3, 10), (10, 12), (12, 13), (13, 15), (15, 18), (18, 19), (19, 20),
                                        (20, 21), (21, 22), (22, 25), (40, 58), (58, 94), (94, 166), (166, 220),
                                        (220, 238), (238, 256), (256, 292), (292, 364), (364, 418), (418, 436)],
                             chunksize=chunksize):
        iteration += 1

        # Remove headers.
        df = df.loc[pd.notna(df["Female Seniors"])].copy()

        # Assign full year name.
        df.loc[:, "Year"] = "20" + df["Year"]

        # Change 1/0 to True/False.
        convert_1_0_strings_to_true_false_strings(df, ["Reported by Adult Male?", "Reported by Adult Female?", "Reported by Juvenile?"])

        # Sum sequence each column's values representing number of criminals.
        sum_sequence(df, ["Male Pre-Teens", "Male Teenagers", "Male Young Adults", "Male Adults", "Male Seniors", "Female Pre-Teens", "Female Teenagers", "Female Young Adults", "Female Adults", "Female Seniors"])

        # Data type change.
        df = df.astype(dtype={"Year": "int",
                              "Reported by Adult Male?": "boolean",
                              "Reported by Adult Female?": "boolean",
                              "Reported by Juvenile?": "boolean",
                              "Male Pre-Teens": "int",
                              "Male Teenagers": "int",
                              "Male Young Adults": "int",
                              "Male Adults": "int",
                              "Male Seniors": "int",
                              "Female Pre-Teens": "int",
                              "Female Teenagers": "int",
                              "Female Young Adults": "int",
                              "Female Adults": "int",
                              "Female Seniors": "int"})

        validate(df)

        table_name = re.search("/[a-zA-Z0-9]+.", file_location)
        table_name = table_name.group(0)[1:-1]
        export_dataframe_to_SQL_Server(df=df, table_name=table_name)

        # Get progress report in console
        percent_complete = np.round(iteration * chunksize / total_recrods * 100, decimals=2)
        if percent_complete > 100:
            percent_complete = 100
        print(str(file_location) + ": " + str(percent_complete) + "%")

        pass

if __name__ == "__main__":
    import_file(file_location="data/ASR122016.TXT")








