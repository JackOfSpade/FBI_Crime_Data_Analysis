import sys

import pandas as pd
import IPython as ip
import numpy as np
import pyodbc as po
import re
import sqlalchemy as sqlalchemy
import matplotlib.pyplot as plt
import scipy.stats as st
import find_best_distribution as fbd

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
                                    "Female Adults", "Female Seniors", "Male < 10", "Male 10-12", "Male 13-14",
                                    "Male 15", "Male 16", "Male 17", "Male 18", "Male 19", "Male 20", "Male 21",
                                    "Male 22", "Male 23", "Male 24", "Male 25-29", "Male 30-34", "Male 35-39",
                                    "Male 40-44", "Male 45-49", "Male 50-54", "Male 55-59", "Male 60-64", "Male 65-80",
                                    "Female < 10", "Female 10-12", "Female 13-14", "Female 15", "Female 16",
                                    "Female 17", "Female 18", "Female 19", "Female 20", "Female 21", "Female 22",
                                    "Female 23", "Female 24", "Female 25-29", "Female 30-34", "Female 35-39",
                                    "Female 40-44", "Female 45-49", "Female 50-54", "Female 55-59", "Female 60-64",
                                    "Female 65-80", "Total Cases"])))

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
                                    "Female Adults", "Female Seniors", "Male < 10", "Male 10-12", "Male 13-14",
                                    "Male 15", "Male 16", "Male 17", "Male 18", "Male 19", "Male 20", "Male 21",
                                    "Male 22", "Male 23", "Male 24", "Male 25-29", "Male 30-34", "Male 35-39",
                                    "Male 40-44", "Male 45-49", "Male 50-54", "Male 55-59", "Male 60-64", "Male 65-80",
                                    "Female < 10", "Female 10-12", "Female 13-14", "Female 15", "Female 16",
                                    "Female 17", "Female 18", "Female 19", "Female 20", "Female 21", "Female 22",
                                    "Female 23", "Female 24", "Female 25-29", "Female 30-34", "Female 35-39",
                                    "Female 40-44", "Female 45-49", "Female 50-54", "Female 55-59", "Female 60-64",
                                    "Female 65-80"],
                             dtype="object",
                             colspecs=[(1, 3), (3, 10), (10, 12), (12, 13), (13, 15), (15, 18), (18, 19), (19, 20),
                                       (20, 21), (21, 22), (22, 25), (40, 58), (58, 94), (94, 166), (166, 220),
                                       (220, 238), (238, 256), (256, 292), (292, 364), (364, 418), (418, 436),
                                       (40, 49), (49, 58), (58, 67), (67, 76), (76, 85), (85, 94), (94, 103),
                                       (103, 112), (112, 121), (121, 130), (130, 139), (139, 148), (148, 157),
                                       (157, 166), (166, 175), (175, 184), (184, 193), (193, 202), (202, 211),
                                       (211, 220), (220, 229), (229, 238), (238, 247), (247, 256), (256, 265),
                                       (265, 274), (274, 283), (283, 292), (292, 301), (301, 310), (310, 319),
                                       (319, 328), (328, 337), (337, 346), (346, 355), (355, 364), (364, 373),
                                       (373, 382), (382, 391), (391, 400), (400, 409), (409, 418), (418, 427),
                                       (427, 436)],
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
                          "Female Seniors", "Male < 10", "Male 10-12", "Male 13-14", "Male 15", "Male 16", "Male 17",
                          "Male 18", "Male 19", "Male 20", "Male 21", "Male 22", "Male 23", "Male 24", "Male 25-29",
                          "Male 30-34", "Male 35-39", "Male 40-44", "Male 45-49", "Male 50-54", "Male 55-59",
                          "Male 60-64", "Male 65-80", "Female < 10", "Female 10-12", "Female 13-14", "Female 15",
                          "Female 16", "Female 17", "Female 18", "Female 19", "Female 20", "Female 21", "Female 22",
                          "Female 23", "Female 24", "Female 25-29", "Female 30-34", "Female 35-39", "Female 40-44",
                          "Female 45-49", "Female 50-54", "Female 55-59", "Female 60-64", "Female 65-80"])

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
                              "Total Cases":"int",
                              "Male < 10" : "int",
                              "Male 10-12" : "int",
                              "Male 13-14" : "int",
                              "Male 15" : "int",
                              "Male 16" : "int",
                              "Male 17" : "int",
                              "Male 18" : "int",
                              "Male 19" : "int",
                              "Male 20" : "int",
                              "Male 21" : "int",
                              "Male 22" : "int",
                              "Male 23" : "int",
                              "Male 24" : "int",
                              "Male 25-29" : "int",
                              "Male 30-34" : "int",
                              "Male 35-39" : "int",
                              "Male 40-44" : "int",
                              "Male 45-49" : "int",
                              "Male 50-54" : "int",
                              "Male 55-59" : "int",
                              "Male 60-64" : "int",
                              "Male 65-80" : "int",
                              "Female < 10" : "int",
                              "Female 10-12" : "int",
                              "Female 13-14" : "int",
                              "Female 15" : "int",
                              "Female 16" : "int",
                              "Female 17" : "int",
                              "Female 18" : "int",
                              "Female 19" : "int",
                              "Female 20" : "int",
                              "Female 21" : "int",
                              "Female 22" : "int",
                              "Female 23" : "int",
                              "Female 24" : "int",
                              "Female 25-29" : "int",
                              "Female 30-34" : "int",
                              "Female 35-39" : "int",
                              "Female 40-44" : "int",
                              "Female 45-49" : "int",
                              "Female 50-54" : "int",
                              "Female 55-59" : "int",
                              "Female 60-64" : "int",
                              "Female 65-80" : "int"})

        validate(df)


        table_name = re.search("/[a-zA-Z0-9]+.", file_location)
        table_name = table_name.group(0)[1:-1]
        export_dataframe_to_SQL_Server(df=df, table_name=table_name)

        # Get progress report in console
        percent_complete = np.round(iteration * chunksize / total_recrods * 100, decimals=2)
        if percent_complete > 100:
            percent_complete = 100
        print(str(file_location) + ": " + str(percent_complete) + "%")


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
    axes.set_title("Correlation Between Drug Abuse and Other Crimes Over Time")
    axes.plot([2011, 2012, 2013, 2014, 2015, 2016], total_crime_count_list, linestyle="-", color="r", label="Crimes Excluding Drug Abuse")
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
            SELECT [Male < 10], [Male 10-12], [Male 13-14], [Male 15], [Male 16], [Male 17], [Male 18], [Male 19], [Male 20], [Male 21], [Male 22], [Male 23], [Male 24], [Male 25-29], [Male 30-34], [Male 35-39], [Male 40-44], [Male 45-49], [Male 50-54], [Male 55-59], [Male 60-64], [Male 65-80], [Female < 10], [Female 10-12], [Female 13-14], [Female 15],[Female 16], [Female 17], [Female 18], [Female 19], [Female 20], [Female 21], [Female 22], [Female 23], [Female 24], [Female 25-29], [Female 30-34], [Female 35-39], [Female 40-44], [Female 45-49], [Female 50-54], [Female 55-59], [Female 60-64], [Female 65-80]
            FROM """ + table_name + """
            WHERE [Offense Code] = """ + offense_code + """
            """)

    s10 = 0
    f10t12 = 0
    f13t14 = 0
    e15 = 0
    e16 = 0
    e17 = 0
    e18 = 0
    e19 = 0
    e20 = 0
    e21 = 0
    e22 = 0
    e23 = 0
    e24 = 0
    f25t29 = 0
    f30t34 = 0
    f35t39 = 0
    f40t44 = 0
    f45t49 = 0
    f50t54 = 0
    f55t59 = 0
    f60t64 = 0
    f65t80 = 0

    # For every variant of the same offense...
    for query in query_list:
        # For each chunk of a variant
        for chunk in pd.read_sql(sql=query, con=connection, chunksize=1000):
            df = chunk
            s10 += df["Male < 10"].sum() + df["Female < 10"].sum()
            f10t12 += df["Male 10-12"].sum() + df["Female 10-12"].sum()
            f13t14 += df["Male 13-14"].sum() + df["Female 13-14"].sum()
            e15 += df["Male 15"].sum() + df["Female 15"].sum()
            e16 += df["Male 16"].sum() + df["Female 16"].sum()
            e17 += df["Male 17"].sum() + df["Female 17"].sum()
            e18 += df["Male 18"].sum() + df["Female 18"].sum()
            e19 += df["Male 19"].sum() + df["Female 19"].sum()
            e20 += df["Male 20"].sum() + df["Female 20"].sum()
            e21 += df["Male 21"].sum() + df["Female 21"].sum()
            e22 += df["Male 22"].sum() + df["Female 22"].sum()
            e23 += df["Male 23"].sum() + df["Female 23"].sum()
            e24 += df["Male 24"].sum() + df["Female 24"].sum()
            f25t29 += df["Male 25-29"].sum() + df["Female 25-29"].sum()
            f30t34 += df["Male 30-34"].sum() + df["Female 30-34"].sum()
            f35t39 += df["Male 35-39"].sum() + df["Female 35-39"].sum()
            f40t44 += df["Male 40-44"].sum() + df["Female 40-44"].sum()
            f45t49 += df["Male 45-49"].sum() + df["Female 45-49"].sum()
            f50t54 += df["Male 50-54"].sum() + df["Female 50-54"].sum()
            f55t59 += df["Male 55-59"].sum() + df["Female 55-59"].sum()
            f60t64 += df["Male 60-64"].sum() + df["Female 60-64"].sum()
            f65t80 += df["Male 65-80"].sum() + df["Female 65-80"].sum()


    return (s10, f10t12, f13t14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, f25t29, f30t34, f35t39, f40t44, f45t49, f50t54, f55t59, f60t64, f65t80)

def generate_data(repetition_list, data_range_list):
    generated_data = np.empty(shape=(0, 0))
    for index, value in enumerate(repetition_list):
        generated_data = np.append(generated_data, np.linspace(start=data_range_list[index][0], stop=data_range_list[index][1]+1, num=value))
    return generated_data


def get_center_of_bin_edges(bin_edges):
    bin_centers = []

    for x in np.arange(start=0, stop=len(bin_edges) - 1, step=1):
        bin_centers.append((bin_edges[x] + bin_edges[x + 1]) / 2.0)

    return bin_centers

def graph_and_analyze_type_of_crime_vs_age(graph_title, offense_code_list):
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

    s10, f10t12, f13t14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, f25t29, f30t34, f35t39, f40t44, f45t49, f50t54, f55t59, f60t64, f65t80  = get_crime_type_vs_age(connection=connection, offense_code_list=offense_code_list, table_name_list=table_name_list)

    generated_data = generate_data([s10, f10t12, f13t14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, f25t29, f30t34, f35t39, f40t44, f45t49, f50t54, f55t59, f60t64, f65t80],
                                   [[5, 10], [10, 12], [13, 14], [15, 15], [16, 16], [17, 17], [18, 18], [19, 19], [20, 20], [21, 21], [22, 22],
                                    [23, 23], [24, 24], [25, 29], [30, 34], [35, 39], [40, 44], [45, 49], [50, 54], [55, 59], [60, 64], [65, 80]])

    s10, f10t12, f13t14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, f25t29, f30t34, f35t39, f40t44, f45t49, f50t54, f55t59, f60t64, f65t80
    figure, axes = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
    axes.set_title(graph_title)
    # bins=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 80]
    # bins=np.arange(start=1, stop=81, step=1)
    height_of_bins, bin_edges, patches = axes.hist(x=generated_data, bins=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 80], edgecolor="#a5c8e1", density=True)
    axes.set_ylabel("Percentage of Cases")
    axes.set_xlabel("Age")

    bin_centers = get_center_of_bin_edges(bin_edges)

    # Analysis
    file_path = "graphs/" + re.sub(pattern="\s+", repl="_", string=axes.get_title())
    best_distribution, best_parameters, best_residual_sum_of_squares = fbd.best_fit_distribution(file_name=file_path, data=generated_data, bin_heights=height_of_bins, bin_centers=bin_centers)
    shape_parameters, location_parameter, scale_parameter = best_parameters

    x = np.linspace(start=0, stop=80, num=10000)
    y = best_distribution.pdf(x, shape_parameters, loc=location_parameter, scale=scale_parameter)

    axes.plot(x, y, linewidth=2, label=best_distribution.name)
    axes.legend()
    figure.savefig(fname=file_path)
    print("Graph: " + re.sub(pattern="\s+", repl="_", string=axes.get_title()))
    print("Shape parameters: " + str(str(shape_parameters)))
    print("Location parameter: " + str(location_parameter))
    print("Scale parameter: " + str(scale_parameter))
    print("Residual sum of squares: " + str(best_residual_sum_of_squares))

    #TO DO: PRINT LEAST RESIDUAL SUM OF SQUARES, MAKE LINES THICKER, SAVE DATA

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

    graph_and_analyze_type_of_crime_vs_age("Murder", ["011", "012"])
    # graph_and_analyze_type_of_crime_vs_age("Sex Offenses", ["020", "160", "170"])
    # graph_and_analyze_type_of_crime_vs_age("Assault", ["040", "080"])
    # graph_and_analyze_type_of_crime_vs_age("Theft and Robbery", ["030", "050", "060", "070", "130", "120"])
    # graph_and_analyze_type_of_crime_vs_age("Destruction of Property", ["090", "140"])
    # graph_and_analyze_type_of_crime_vs_age("Fraud", ["100", "110"])
    # graph_and_analyze_type_of_crime_vs_age("Drug Abuse", ["18", "180", "181", "182", "183", "184", "185", "186", "187", "188", "189"])
    # graph_and_analyze_type_of_crime_vs_age("Gambling", ["19", "191", "192", "193"])
    # graph_and_analyze_type_of_crime_vs_age("Driving Under the Influence", ["210"])

    print("Done!")







