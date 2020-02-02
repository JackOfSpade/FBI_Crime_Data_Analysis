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
    # Import data.

    original_df = pd.DataFrame()

    for chunk in pd.read_fwf(filepath_or_buffer="data/ASR122016.TXT",
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
                             nrows=1000,
                             chunksize=100000):
        original_df = pd.concat(objs=[original_df, chunk])
    print("Import data done!")

    # Remove headers.
    df = original_df.loc[pd.notna(original_df["Female Seniors"])].copy()
    print("Remove headers done!")

    # Assign full year name.
    df.loc[:, "Year"] = "20" + df["Year"]
    print("Assign full year name done!")

    # Change 1/0 to True/False.
    convert_1_0_strings_to_true_false_strings(df, "Reported by Adult Male?")
    convert_1_0_strings_to_true_false_strings(df, "Reported by Adult Female?")
    convert_1_0_strings_to_true_false_strings(df, "Reported by Juvenile?")
    print("Change 1/0 to True/False done!")

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
    print("Sum sequence representing number of criminals done!")

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
    print("Data type change done!")

    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     ip.display.display(df)

    print(df)

pass



