# User-Behavior-Mapping-Tool

Project aims to map out common user behavior on the computer.
Most of the code is based on the research by kacos2000 found here:
https://github.com/kacos2000/WindowsTimeline

TrustedSec blog about the research behind it:
https://www.trustedsec.com/blog/oh-behave-figuring-out-user-behavior/


# Installation
1. git clone the repo
2. pip3 install -r requirements.txt


# Getting started
To make use of this project you first need to copy out the ActivityCache.db file found on the users computer under:
```
C:\Users\%username%\AppData\Local\ConnectedDevicesPlatform\<GUID>
```

## UserBehaviorAnalyzer.py
To parse an ActivityCache.db file specify the path with the -f parameter.
If you only want the main exported data (one csv) you can specify -m.
Output folder is specified with the -o parameter. Folder will be created if it does not exist.
If no output folder is specified the output goes in the current working directory.


```
python3 UserBehaviourAnalyzer.py -f /mnt/c/ads/ActivitiesCache.db
Succesfully exported full raw database report
Report gen_report_useractivity_start_and_end.csv Generated successfully
Report gen_report_ApplicationLaunch_StartTime.csv Generated successfully
Paths_Unique.txt Generated successfully
Report gen_report_Activity_Applications.csv Generated successfully
Chart gen_fig_useractivity_heatmap.jpg Generated successfully
/mnt/c/gitlab/user-behavior/1. Extraction Script/UserBehaviorAnalyzer.py:565: UserWarning: FixedFormatter should only be used together with FixedLocator
  ax1.set_xticklabels(df1['Date'], rotation=90)
Chart gen_fig_useractivity_bar.jpg Generated successfully
Chart gen_fig_top10_apps_pie.jpg Generated successfully
Chart gen_fig_top10_apps_bars.jpg Generated successfully
```

## Reports

### gen_report_Activity_Applications.csv
This report contains the total of time the different application has been actively used based on all the data found in the database.

### gen_report_ApplicationLaunch_StartTime.csv
This reports shows the applications that are launched and parameters used (also filenames sometimes) and when it was launched. 
This is useful for understanding when the user starts his applications.

### gen_report_useractivity_start_and_end.csv
This report groups all times for each day and finds the first entry of the day and the last.
This report is useful for understanding when the user starts his day and when the last application was launched. 

## Charts

### gen_fig_top10_apps_bars.jpg
This shows the top 10 most used application visualized with Bars. Usage is in seconds.

### gen_fig_top10_apps_pie.jpg
This shows the top 10 most used application visualized as a pie chart. Usage is in seconds.

### gen_fig_useractivity_bar.jpg
This visualizes when the user is active and idle based on the first activity found per day and the last activity found per day. The y axis shows the time of day. 
The time is based on the timezone of the user
ex 500 = 0500 (5am)
ex 2000 (8pm)

### gen_fig_useractivity_heatmap.jpg
This visualized the users activity sorted on days. The brighter color the more activity. The time is based on the timezone of the user  

## Other

### Paths_Unique.txt
This file contains unique paths the for documents/files/folders the user works towards. Perfect targets for backdoors. 


# Issues
If you do encounter issues please create a github issue. You might need to provide the ActivitiesCache.db since it could be a case that has not been encountered. 