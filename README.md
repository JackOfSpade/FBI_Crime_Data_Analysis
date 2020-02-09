# TO-DO:

![#00ff00](https://placehold.it/15/00ff00/000000?text=+) ` = done`

![#ffa500](https://placehold.it/15/ffa500/000000?text=+) ` = in progress`

![#f03c15](https://placehold.it/15/f03c15/000000?text=+) ` = not done`



```diff
Data Gathering:
+ Download all necessary data files from https://www.fbi.gov/services/cjis/ucr.  
```
![](https://i.imgur.com/ZxPmSzt.png) 
7 files, one for each year from 2010 to 2016, ~10,000,000 crimes in each file.
```diff
+ Parse the fixed-width format data files and import into pandas. 
+ Clean the data. 
+ Transform the data into easily-readable values and appropriate data types.
```
![](https://i.imgur.com/N3CWkgz.png) 
```diff
+ Validate the resulting data.
! Import the data into SQL Server using pyodbc + T-SQL

For each of the 3 experiments:
- Import the required table from SQL Server into pandas using pyodbc + T-SQL.
- Manipulate the table in pandas if necessary.
- Visualize data with matplotlib.
- Analyze the empirical distribution with SciPy.
- Model the empirical distribution with a theoretical distribution with SciPy for future estimates of the same case.
- Visualize the model with matplotlib.
- Publish both visualizations and analysis conclusions.
```
