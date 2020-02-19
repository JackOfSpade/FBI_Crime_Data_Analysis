import sys

import pandas as pd
import IPython as ip
import numpy as np
import pyodbc as po
import re
import sqlalchemy as sqlalchemy
import matplotlib.pyplot as plt
import scipy.stats as st


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
                                     "Female Adults", "Female Seniors", "Total Cases"])))



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

        # Sum column
        df["Total Cases"] = df["Male Pre-Teens"]\
            .add(other=df["Male Teenagers"], fill_value=0)\
            .add(other=df["Male Young Adults"], fill_value=0)\
            .add(other=df["Male Adults"], fill_value=0)\
            .add(other=df["Male Seniors"], fill_value=0)\
            .add(other=df["Female Pre-Teens"], fill_value=0)\
            .add(other=df["Female Teenagers"], fill_value=0)\
            .add(other=df["Female Young Adults"], fill_value=0)\
            .add(other=df["Female Adults"], fill_value=0)\
            .add(other=df["Female Seniors"], fill_value=0)

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
                              "Female Seniors": "int",
                              "Total Cases":"int"})

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

def graph_crime_by_hour(df, plural, crime=None):
    if crime is None:
        column2 = "Under 18"
        column3 = "18 and older"

    else:
        column2 = crime + " Under 18"
        column3 = crime + " 18 and older"

    df = df.astype(dtype={column2: "float",
                          column3: "float"})
    df = df[:-1]

    figure, axes = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
    axes.set_title(plural + " by Hour")
    axes.set_ylabel("Percentage of Total Daily " + plural)
    axes.set_xlabel("Hour of the Day")
    axes.plot(df["Time"].to_numpy(), df[column2].to_numpy()/1000, linestyle="-", color="c", label="Under 18")
    axes.plot(df["Time"].to_numpy(), df[column3].to_numpy()/1000, linestyle="-", color="b", label ="18 and Older")
    axes.legend()
    figure.savefig(fname="graphs/" + re.sub(pattern="\s+", repl="_", string=axes.get_title()))

def get_crime_numbers(cursor, table_name):
    total_crime_count__query = """
    SELECT SUM([Total Cases])
    FROM """ + table_name + """
    WHERE [Offense Code] != 18 OR [Offense Code] != 180 OR [Offense Code] != 181 OR [Offense Code] != 182 OR [Offense Code] != 183 OR [Offense Code] != 184
    """

    cursor.execute(total_crime_count__query)
    total_crime_count = cursor.fetchval()

    drug_crime_count_query = """
    SELECT SUM([Total Cases])
    FROM """ + table_name + """
    WHERE [Offense Code] = 18 OR [Offense Code] = 180 OR [Offense Code] = 181 OR [Offense Code] = 182 OR [Offense Code] = 183 OR [Offense Code] = 184
    """

    cursor.execute(drug_crime_count_query)
    drug_crime_count = cursor.fetchval()

    return (total_crime_count, drug_crime_count)

def graph_correlation_between_drug_abuse_and_total_crime():
    connection_String = """
        driver=ODBC Driver 17 for SQL Server;
        server=SHADOW-LN4F5NUO;
        database=FBI_Crime_Data;
        trusted_connection=yes;
        """

    connection = po.connect(connection_String)
    cursor = connection.cursor()
    temp_total_crime_count_list = []
    temp_drug_crime_count_list = []
    table_name_list = ["ASR1210", "ASR1211", "ASR1212", "ASR1213", "ASR1214", "ASR122016"]

    for table_name in table_name_list:
        (total_crime_count, drug_crime_count) = get_crime_numbers(cursor=cursor, table_name=table_name)
        temp_total_crime_count_list.append(total_crime_count)
        temp_drug_crime_count_list.append(drug_crime_count)

    total_crime_count_list = np.array(object=temp_total_crime_count_list)
    drug_crime_count_list = np.array(object=temp_drug_crime_count_list)

    figure, axes = plt.subplots(nrows = 1, ncols = 1, figsize=(15,10))
    axes.set_title("Correlation Between Drug Abuse and Total Crime Over Time")
    axes.plot([2011, 2012, 2013, 2014, 2015, 2016], total_crime_count_list, linestyle="-", color="r", label="Total Crime")
    axes.plot([2011, 2012, 2013, 2014, 2015, 2016], drug_crime_count_list, linestyle="-", color="m", label="Drug Abuse")
    axes.set_ylabel("Number of Cases")
    axes.set_xlabel("Year")
    axes.legend()

    figure.savefig(fname="graphs/" + re.sub(pattern="\s+", repl="_", string=axes.get_title()))
    print()
    pearsons_correlation_coefficient, p_value = st.pearsonr(x=total_crime_count_list, y=drug_crime_count_list)
    print("Pearson's Correlation Coefficient: " + str(pearsons_correlation_coefficient) +"\np-value: " + str(p_value))

def get_crime_type_vs_age(connection, offense_code_list, table_name_list):
    query_list = []

    # Make query for every variant of the same offense
    for offense_code in offense_code_list:
        for table_name in table_name_list:
            query_list.append("""
            SELECT [Offense Code], [Male Pre-Teens], [Male Teenagers], [Male Young Adults], [Male Adults], [Male Seniors], [Female Pre-Teens], [Female Teenagers], [Female Young Adults], [Female Adults], [Female Seniors]
            FROM """ + table_name + """
            WHERE [Offense Code] = """ + offense_code + """
            """)

    pre_teen_count = 0
    teenager_count = 0
    young_adult_count = 0
    adult_count = 0
    senior_count = 0

    # For every variant of the same offense...
    for query in query_list:
        # For each chunk of a variant
        for chunk in pd.read_sql(sql=query, con=connection, chunksize=1000):
            df = chunk
            pre_teen_count += df["Male Pre-Teens"].sum() + df["Female Pre-Teens"].sum()
            teenager_count += df["Male Teenagers"].sum() + df["Female Teenagers"].sum()
            young_adult_count += df["Male Young Adults"].sum() + df["Female Young Adults"].sum()
            adult_count += df["Male Adults"].sum() + df["Female Adults"].sum()
            senior_count += df["Male Seniors"].sum() + df["Female Seniors"].sum()


    return (pre_teen_count, teenager_count, young_adult_count, adult_count, senior_count)

def graph_type_of_crime_vs_age(graph_title, offense_code_list):
    connection_String = """
        driver=ODBC Driver 17 for SQL Server;
        server=SHADOW-LN4F5NUO;
        database=FBI_Crime_Data;
        trusted_connection=yes;
        """

    connection = po.connect(connection_String)
    cursor = connection.cursor()
    table_name_list = ["ASR1210", "ASR1211", "ASR1212", "ASR1213", "ASR1214", "ASR122016"]
    # 0–12 pre-teen
    # 13–17 teenager
    # 18–29 young adult
    # 30–59 adult
    # 60+ senior

    pre_teen_count, teenager_count, young_adult_count, adult_count, senior_count = get_crime_type_vs_age(connection=connection, offense_code_list=offense_code_list, table_name_list=table_name_list)

    generated_data = []

    for x in np.arange(start=0, stop=pre_teen_count, step=1):
        generated_data.append(6)

    for x in np.arange(start=0, stop=teenager_count, step=1):
        generated_data.append(15)

    for x in np.arange(start=0, stop=young_adult_count, step=1):
        generated_data.append(23)

    for x in np.arange(start=0, stop=adult_count, step=1):
        generated_data.append(45)

    for x in np.arange(start=0, stop=senior_count, step=1):
        generated_data.append(80)

    figure, axes = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
    axes.set_title(graph_title)
    axes.hist(x=generated_data, bins=[0, 13, 18, 30, 60, 100])
    axes.set_ylabel("Cases")
    axes.set_xlabel("Age")

    figure.savefig(fname="graphs/" + re.sub(pattern="\s+", repl="_", string=axes.get_title()))

if __name__ == "__main__":
    user_input = input("Reset Database?\n")

    if re.search(pattern="^(1|true|yes)$", string=user_input, flags=re.IGNORECASE):
        reset_database()
        import_file(file_location="data/ASR1210.DAT")
        import_file(file_location="data/ASR1211.DAT")
        import_file(file_location="data/ASR1212.DAT")
        import_file(file_location="data/ASR1213.DAT")
        import_file(file_location="data/ASR1214.DAT")
        import_file(file_location="data/ASR122016.TXT")

    df1 = pd.read_csv(filepath_or_buffer="data\\individual_crime_by_hour.csv", delimiter=",", dtype=str)
    df2 = pd.read_csv(filepath_or_buffer="data\\total_crime_by_hour.csv", delimiter=",", dtype=str)

    graph_crime_by_hour(df=df2, plural="Violent Crimes")

    graph_correlation_between_drug_abuse_and_total_crime()

    graph_type_of_crime_vs_age("Murder", ["011", "012"])
    graph_type_of_crime_vs_age("Sex Offenses", ["020", "160", "170"])
    graph_type_of_crime_vs_age("Assault", ["040", "080"])
    graph_type_of_crime_vs_age("Theft and Robbery", ["030", "050", "060", "070", "130", "120"])
    graph_type_of_crime_vs_age("Destruction of Property", ["090", "140"])
    graph_type_of_crime_vs_age("Fraud",  ["100", "110"])
    graph_type_of_crime_vs_age("Drug Abuse", ["18", "180", "181", "182", "183", "184", "185", "186", "187", "188", "189"])
    graph_type_of_crime_vs_age("Gambling", ["19", "191", "192", "193"])
    graph_type_of_crime_vs_age("Driving Under the Influence", "210")

    print("Done!")







