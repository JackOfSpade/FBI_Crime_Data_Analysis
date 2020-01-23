import pandas as pd
import IPython as ip

if __name__ == "__main__":
    df = pd.read_fwf(filepath_or_buffer = "data/ASR122016.TXT",
                     names = ["Numeric State Code", "ORI Code", "Population Group (inclusive)", "Division", "Year", "Metropolitan Statistical Area Number", "Adult Male Reported", "Adult Female Reported", "Juvenile Reported", "Adjustment", "Offense Code", "Male Pre-Teens", "Male Teenager", "Male Young Adults", "Male Adults", "Male Seniors", "Female Pre-Teens", "Female Teenager", "Female Young Adults", "Female Adults", "Female Seniors"],
                     colspecs = [(2, 4), (4, 11), (11, 13), (13, 14), (14, 16), (16, 19), (19, 20), (20, 21), (21, 22), (22, 23), (23, 26), (41, 59), (59, 95), (95, 167), (167, 221), (221, 239), (239, 257), (257, 293), (293, 365), (365, 419), (419, 437)],
                     nrows = 10)

    ip.display.display(df)


