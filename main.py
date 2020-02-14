import sys

import pandas as pd
import IPython as ip
import numpy as np
import pyodbc as po
import re
import sqlalchemy as sqlalchemy
import matplotlib.pyplot as plt


# Pre-condition: char_list is a list of character digits.
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
    engine = sqlalchemy.create_engine("mssql+pyodbc://@" + "SHADOW-LN4F5NUO" + "/" + "FBI_Crime_Data" +
                                      "?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server")

    df.to_sql(name=table_name, con=engine, if_exists="append", index=False)

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

def number_sequence_only(df, column_list):
    for x in column_list:
        df = df[df[x].str.contains(pat="^\d+$", regex=True)].copy()

    return df

def import_file(file_location):
    total_recrods = 0;
    with open(file_location, mode = "r") as file:
        line = file.readline()
        total_recrods += 1
        while line != "":
            total_recrods += 1
            line = file.readline()

    chunksize = 10000
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
        df = number_sequence_only(df, ["Male Pre-Teens", "Male Teenagers", "Male Young Adults", "Male Adults",
                                       "Male Seniors", "Female Pre-Teens", "Female Teenagers", "Female Young Adults",
                                       "Female Adults", "Female Seniors"])

        # Assign full year name.
        df.loc[:, "Year"] = "20" + df["Year"]

        # Change 1/0 to True/False.
        convert_1_0_strings_to_true_false_strings(df, ["Reported by Adult Male?", "Reported by Adult Female?",
                                                       "Reported by Juvenile?"])

        # Sum sequence each column's values representing number of criminals.
        sum_sequence(df, ["Male Pre-Teens", "Male Teenagers", "Male Young Adults", "Male Adults", "Male Seniors",
                          "Female Pre-Teens", "Female Teenagers", "Female Young Adults", "Female Adults",
                          "Female Seniors"])

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


def reset_database():
    connection_string = """
        driver=ODBC Driver 17 for SQL Server;
        server=SHADOW-LN4F5NUO;
        database=FBI_Crime_Data;
        trusted_connection=yes;
        """

    connection = po.connect(connection_string)
    cursor = connection.cursor()

    # Reset Tables
    statement_list = []

    statement_list.append("""
        DROP TABLE IF EXISTS ASR1210;   
        """)

    statement_list.append("""
           DROP TABLE IF EXISTS ASR1211;   
           """)

    statement_list.append("""
           DROP TABLE IF EXISTS ASR1212;   
           """)

    statement_list.append("""
           DROP TABLE IF EXISTS ASR1213;   
           """)

    statement_list.append("""
               DROP TABLE IF EXISTS ASR1214;   
               """)

    statement_list.append("""
           DROP TABLE IF EXISTS ASR122016;   
           """)

    for statement in statement_list:
        cursor.execute(statement)

    cursor.commit()

def graph_crime_by_hour():
    df = pd.read_csv(filepath_or_buffer="data\individual_crime_by_hour.csv", delimiter=",", dtype=str)
    df = df[:-1]
    df = df.astype(dtype={"Robbery Under 18":"float",
                          "Robbery 18 and older":"float",
                          "Aggravated assault Under 18":"float",
                          "Aggravated assault 18 and older":"float",
                          "Sexual assault Under 18": "float",
                          "Sexual assault 18 and older": "float"})

    figure, axes = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
    axes.set_title("Robberies by Hour")
    axes.set_ylabel("Percentage of Total Daily Robberies")
    axes.set_xlabel("Hour of the Day")
    axes.plot(df["Time"].to_numpy(), df["Robbery Under 18"].to_numpy()/1000, linestyle="-", color="c", label="Under 18")
    axes.plot(df["Time"].to_numpy(), df["Robbery 18 and older"].to_numpy()/1000, linestyle="-", color="b", label ="18 and Older")
    axes.legend()
    figure.savefig(fname="crime_by_hour.png")
    pass
if __name__ == "__main__":
    user_input = input("Reset Database?\n")

    if re.search("^(1|true|yes)$", user_input, flags=re.IGNORECASE):
        reset_database()
        import_file(file_location="data/ASR1210.DAT")
        import_file(file_location="data/ASR1211.DAT")
        import_file(file_location="data/ASR1212.DAT")
        import_file(file_location="data/ASR1213.DAT")
        import_file(file_location="data/ASR1214.DAT")
        import_file(file_location="data/ASR122016.TXT")

    graph_crime_by_hour()








