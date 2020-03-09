# Data Source
- 2011-2016 crime data provided by the Federal Bureau of Investigation.
- https://crime-data-explorer.fr.cloud.gov/downloads-and-docs

# Which hours of the day is the safest?
![](https://i.imgur.com/eGYJADE.png)

**Conclusion:** There is a sharp drop off of crimes after 11pm. The hours between 4am to 7am is the safest with a low crime rate of under 2%.

**Possible explanations:**

- Almost all night clubs close before 6:00am and the crowd usually disperse a few hours before that, leading to less chances of civilian conflicts.

- It is harder to successfully carry out some crimes at night, such as burglary, when there is less ambient noise to mask sound, and the high possibility that the owner is at home.

- Criminals need to sleep too.

# Is there a strong correlation between drug abuse and other crimes?
![](https://i.imgur.com/5E0BhCU.png)
![](https://i.imgur.com/Yv3pnwu.png)

# Relations Between Different Crime Types and Convicts' Age Group
 ![](https://i.imgur.com/3VmvZ18.png)
This empirical histogram can be modelled by an exponentially modified normal distribution. 

Specifically, ~exponnorm(μ = 15.70, σ = 3.36, K = 4.77)

![](https://i.imgur.com/yO7F8S7.png)
This empirical histogram can be modelled by an exponentially modified normal distribution. 

Specifically, ~exponnorm(μ = 13.94, σ = 2.86, K = 4.63)

![](https://i.imgur.com/ivaT3Pu.png)
This empirical histogram can be modelled by an exponentially modified normal distribution. 

Specifically, ~exponnorm(μ = 18.98, σ = 1.66, K = 10.42)

![](https://i.imgur.com/YXRilmi.png)
This empirical histogram can be modelled by an exponentially modified normal distribution. 

Specifically, ~exponnorm(μ = 16.65, σ = 2.27, K = 5.73)

![](https://i.imgur.com/Kl6q3i2.png)
This empirical histogram can be modelled by a skew-normal distribution. 

Specifically, ~skewnorm(ξ = 17.89, ω = 19.97, α = 8.35)

![](https://i.imgur.com/0Jtmxuw.png)
This empirical histogram can be modelled by a skew-normal distribution. 

Specifically, ~skewnorm(ξ = 15.73, ω = 25.66, α = 12.85)

![](https://i.imgur.com/ACjUpmN.png)
This empirical histogram can be modelled by an exponentially modified normal distribution. 

Specifically, ~exponnorm(μ = 17.33, σ = 2.09, K = 6.30)

![](https://i.imgur.com/1RONXX7.png)
This empirical histogram can be modelled by a skew-normal distribution. 

Specifically, ~skewnorm(ξ = 13.53, ω = 24.24, α = 9.36)

![](https://i.imgur.com/FOn3BcA.png)
This empirical histogram can be modelled by an exponentially modified normal distribution. 

Specifically, ~exponnorm(μ = 15.24, σ = 2.57, K = 5.46)

**Conclusion:** All of the distribution models are right-skewed, meaning people from the 10-year age group of 15 to 25 commit the most crimes. This is especially predominate in crimes such as driving under the influence, drug abuse and theft/robbery, which drops off significantly after age 25.

**Possible explanations:** 

- According to economist Jeffrey Grogger, low-paying entry-level jobs repulse the younger age groups to seek criminal opportunities that offer higher payoffs.

- The tendency to use physical force to resolve conflicts is more prevalent in younger age groups because communication skills have not yet been fully developed.

- Evidence from neuropsychology also discovered that brain development relating to maturity, decision making, impulse control, emotional regulation, delay of gratification, anticipation of consequences and resistance to peer influence continue into the mid-20s (Farrington, Loeber & Howell, 2012).

- Declining physical strength and energy with age make crimes too dangerous or unlikely to be successful, explaining the very low invlvement in the elderly and small children.


# Project Workflow

![#00ff00](https://placehold.it/15/00ff00/000000?text=+) ` = done`

![#ffa500](https://placehold.it/15/ffa500/000000?text=+) ` = in progress`

![#f03c15](https://placehold.it/15/f03c15/000000?text=+) ` = not done`

```diff
Data Gathering Phase:
+ Download all necessary data files from https://www.fbi.gov/services/cjis/ucr.  
```
![](https://i.imgur.com/ZxPmSzt.png) 
6 files, one for each year from 2011 to 2016, ~1,000,000 aggregate records in each file.
```diff
+ Parse the fixed-width format data files and import into pandas. 
+ Clean the data. 
+ Transform the data into easily-readable values and appropriate data types.
```
![](https://i.imgur.com/N3CWkgz.png) 
```diff
+ Validate the resulting data.
+ Import the data into SQL Server using pyodbc + T-SQL

Data Analysis Phase (for each data set):
+ Import the required table from SQL Server into pandas using pyodbc + T-SQL.
+ Manipulate the table in pandas if necessary.
+ Visualize data with matplotlib.
+ Analyze the empirical distribution with SciPy.
+ Model the empirical distribution with a theoretical distribution with SciPy for future estimates of the same case.
+ Visualize the model with matplotlib.
+ Publish all visualizations and analysis conclusions.
```
