# TO-DO:

![#00ff00](https://placehold.it/15/00ff00/000000?text=+) ` = done`

![#ffa500](https://placehold.it/15/ffa500/000000?text=+) ` = in progress`

![#f03c15](https://placehold.it/15/f03c15/000000?text=+) ` = not done`



```diff
Data Gathering:
+ Download all necessary data files from https://www.fbi.gov/services/cjis/ucr.  (completed 1/22/2020)
+ Parse fixed-width format data files and import into pandas.  (completed 1/23/2020)
! Clean data. (started 1/23/2020)
- Transform data into human-readable values and appropriate data types.
- Validate data.
- Import data into SQL Server using pyodbc + T-SQL

For each of the 3 experiments:
- Import required table from SQL Server into pandas using pyodbc + T-SQL.
- Manipulate table in pandas if necessary.
- Visualize data with matplotlib.
- Analyze empirical distribution with SciPy.
- Model the empirical distribution with a theoretical distribution (parametrically or non-parametrically) with SciPy for future estimates of the same case.
- Visualize model with matplotlib.
- Publish both visualizations and analysis conclusions.
```
