# Which hours of the day is the safest?
![](https://i.imgur.com/eGYJADE.png)

**Conclusion:** There is a sharp drop off of crimes after 11pm. The hours between 4am to 7am is the safest with a low crime rate of under 2%.

**Possible explanations:**

- Criminals need to sleep too.

- It is harder for some crimes to occur at night, such as burglary, when there is less ambient noise to mask sound.

- All night clubs close before 6:00am and the crowd usually disperse a few hours before that, leading to less chances of civilian conflicts.

# Is there a strong correlation between drug abuse and other crimes (excluding drug abuse)?
![](https://i.imgur.com/5E0BhCU.png)
![](https://i.imgur.com/CaFPPe7.png)

# Relation Between Each Crime Type and Convicts' Age Group
 ![](https://i.imgur.com/3VmvZ18.png)

# Other Preliminary Results to be Annotated
![](https://i.imgur.com/yO7F8S7.png)
![](https://i.imgur.com/ivaT3Pu.png)
![](https://i.imgur.com/YXRilmi.png)
![](https://i.imgur.com/Kl6q3i2.png)
![](https://i.imgur.com/0Jtmxuw.png)
![](https://i.imgur.com/ACjUpmN.png)
![](https://i.imgur.com/1RONXX7.png)
![](https://i.imgur.com/FOn3BcA.png)

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
+ Import the data into SQL Server using pyodbc + T-SQL

For each of the 3 experiments:
+ Import the required table from SQL Server into pandas using pyodbc + T-SQL.
+ Manipulate the table in pandas if necessary.
+ Visualize data with matplotlib.
+ Analyze the empirical distribution with SciPy.
+ Model the empirical distribution with a theoretical distribution with SciPy for future estimates of the same case.
+ Visualize the model with matplotlib.
! Publish both visualizations and analysis conclusions.
```
