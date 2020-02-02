import pandas as pd
import IPython as ip
import numpy as np

# Pre-condition: char_list is a list a character digits.
def sum_char_list(char_list):
    sum = 0

    for element in char_list:
        sum += int(element)

    return sum

def convert_1_0_strings_to_true_false_strings(df, column_name):
    df.loc[df[column_name] == "1", column_name] = True
    df.loc[df[column_name] == "0", column_name] = False

if __name__ == "__main__":
    # Read data file into table.
    original_df = pd.read_fwf(filepath_or_buffer="data/ASR122016.TXT",
                     names=["Numeric State Code", "ORI Code", "Population Group (inclusive)", "Division", "Year", "Metropolitan Statistical Area Number", "Adult Male Reported?", "Adult Female Reported?", "Juvenile Reported?", "Adjustment", "Offense Code", "Male Pre-Teens", "Male Teenagers", "Male Young Adults", "Male Adults", "Male Seniors", "Female Pre-Teens", "Female Teenagers", "Female Young Adults", "Female Adults", "Female Seniors"],
                     dtype="object",
                     colspecs=[(1, 3), (3, 10), (10, 12), (12, 13), (13, 15), (15, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 25), (40, 58), (58, 94), (94, 166), (166, 220), (220, 238), (238, 256), (256, 292), (292, 364), (364, 418), (418, 436)],
                     nrows=10)

    # Remove headers.
    df = original_df.loc[pd.notna(original_df["Female Seniors"])]

    # Assign full year name.
    df["Year"] = "20" + df["Year"]

    # Change 1/0 to True/False.
    convert_1_0_strings_to_true_false_strings(df, "Adult Male Reported?")
    convert_1_0_strings_to_true_false_strings(df, "Adult Female Reported?")
    convert_1_0_strings_to_true_false_strings(df, "Juvenile Reported?")

    # Sum sequence representing number of criminals.
    for (index_label, row_value) in df["Male Pre-Teens"].items():
        df["Male Pre-Teens"][index_label] = sum_char_list(list(row_value))

    for (index_label, row_value) in df["Male Teenagers"].items():
        df["Male Teenagers"][index_label] = sum_char_list(list(row_value))

    for (index_label, row_value) in df["Male Young Adults"].items():
        df["Male Young Adults"][index_label] = sum_char_list(list(row_value))

    for (index_label, row_value) in df["Male Adults"].items():
        df["Male Adults"][index_label] = sum_char_list(list(row_value))

    for (index_label, row_value) in df["Male Seniors"].items():
        df["Male Seniors"][index_label] = sum_char_list(list(row_value))

    for (index_label, row_value) in df["Female Pre-Teens"].items():
        df["Female Pre-Teens"][index_label] = sum_char_list(list(row_value))

    for (index_label, row_value) in df["Female Teenagers"].items():
        df["Female Teenagers"][index_label] = sum_char_list(list(row_value))

    for (index_label, row_value) in df["Female Young Adults"].items():
        df["Female Young Adults"][index_label] = sum_char_list(list(row_value))

    for (index_label, row_value) in df["Female Adults"].items():
        df["Female Adults"][index_label] = sum_char_list(list(row_value))

    for (index_label, row_value) in df["Female Seniors"].items():
        df["Female Seniors"][index_label] = sum_char_list(list(row_value))


    df = df.astype(dtype={"Year":"int",
                          "Adult Male Reported?":"boolean",
                          "Adult Female Reported?":"boolean",
                          "Juvenile Reported?":"boolean",
                          "Male Pre-Teens":"int",
                          "Male Teenagers":"int",
                          "Male Young Adults":"int",
                          "Male Adults":"int",
                          "Male Seniors":"int",
                          "Female Pre-Teens":"int",
                          "Female Teenagers":"int",
                          "Female Young Adults":"int",
                          "Female Adults":"int",
                          "Female Seniors":"int"})

    pd.options.display.width = 0
    print(df.dtypes)
    print(df)
pass



