#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


pd.read_csv(r"C:/Users/ABC/Desktop/Project/csv/911.csv")


# In[5]:


df = pd.read_csv(r"C:/Users/ABC/Desktop/Project/csv/911.csv")


# In[6]:


print(df)


# # Q1) What are the top 5 zipcodes for 911 calls?

# In[7]:


df['zip'].value_counts().head(5)


# # Q2) In the titles column there are "Reasons/Departments" specified before the title code. These are EMS, Fire, and Traffic. Use .apply() with a custom lambda expression to create a new column called "Reason" that contains this string value.

# In[9]:


df['Reason'] = df['title'].apply(lambda s:s.split(':')[0])
df['Reason'].head(5)


# #  Q3) What is the most common Reason for a 911 call based off of this new column?

# In[10]:


df['Reason'].value_counts()


# # Q4) Now use seaborn to create a countplot of 911 calls by Reason.
# 
# 

# In[22]:


palette='Blues'sns.countplot(x = 'Reason', data = df, palette='Blues')


# # Q5) What is the data type of the objects in the timeStamp column?

# In[23]:


type(df['timeStamp'].iloc[0])


# # Q6) You should have seen that these timestamps are still strings. Use pd.to_datetime to convert the column from strings to DateTime objects.

# In[24]:


df['timeStamp'] = pd.to_datetime(df['timeStamp'])
type(df['timeStamp'].iloc[0])


# # Q7) You can now grab specific attributes from a Datetime object by calling them. 

# In[25]:


time = df['timeStamp'].iloc[0]
time.hour


# # You can use Jupyter's tab method to explore the various attributes you can call. Now that the timestamp column are actually DateTime objects, use .apply() to create 3 new columns called Hour, Month, and Day of Week. You will create these columns based off of the timeStamp column, reference the solutions if you get stuck on this step.

# In[28]:


df['Hour'] = df['timeStamp'].apply(lambda time:time.hour)
df['Month'] = df['timeStamp'].apply(lambda time:time.month)
df['Day of Week'] = df['timeStamp'].apply(lambda time:time.dayofweek)
df.head()


# # Q8) Notice how the Day of Week is an integer 0-6. Use the .map() with this dictionary to map the actual string names to the day of the week

# In[43]:


dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}


# In[47]:


df['Day of Week'] = df['Day of Week'].apply(lambda x: dmap[x])

df.head()


# # Q9) Now use seaborn to create a countplot of the Day of Week column with the hue based off of the Reason column.

# In[37]:


sns.countplot(x='Day of Week',data=df, palette='Blues', hue='Reason')
plt.legend(bbox_to_anchor=(1,1))


# # Q10) You should have noticed it was missing some months. Let's see if we can maybe fill in this information by plotting the information in another way, possibly a simple line plot that fills in the missing months, in order to do this, we'll need to do some work with pandas...
# 
# Now create a gropuby object called byMonth, where you group the DataFrame by the month column and use the count() method for aggregation. Use the head() method on this returned DataFrame.

# In[40]:


byMonth = df.groupby('Month').count()
byMonth.head()


# # Q11) Now create a simple plot off of the dataframe indicating the count of calls per month.

# In[41]:


byMonth['lat'].plot()


# # Q12) Now see if you can use seaborn's lmplot() to create a linear fit on the number of calls per month. Keep in mind you may need to reset the index to a column.

# In[48]:


byMonth = byMonth.reset_index()
byMonth.head()


# # Q13) Create a new column called 'Date' that contains the date from the timeStamp column. You'll need to use apply along with the .date() method.

# In[50]:


df['Date'] = df['timeStamp'].apply(lambda x: x.date())
df.head()


# # Q14) Now groupby this Date column with the count() aggregate and create a plot of counts of 911 calls.

# In[57]:


df.groupby(by='Date').count()['lat'].plot()
plt.tight_layout()


# # Q15) Now recreate this plot but create 3 separate plots with each plot representing a Reason for the 911 call

# In[58]:


df_traffic = df[df['Reason'] == 'Traffic']
df_traffic.groupby('Date').count()['twp'].plot()
plt.title('Traffic')
plt.tight_layout()


# In[59]:


df_traffic = df[df['Reason'] == 'Fire']
df_traffic.groupby('Date').count()['twp'].plot()
plt.title('Fire')
plt.tight_layout()


# In[60]:


df_traffic = df[df['Reason'] == 'EMS']
df_traffic.groupby('Date').count()['twp'].plot()
plt.title('EMS')
plt.tight_layout()


# # Q16) Now let's move on to creating heatmaps with seaborn and our data. We'll first need to restructure the dataframe so that the columns become the Hours and the Index becomes the Day of the Week. There are lots of ways to do this, but I would recommend trying to combine groupby with an unstack method. Reference the solutions if you get stuck on this!

# In[65]:


dayHour = df.groupby(['Day of Week','Hour']).count().unstack()['Reason']
dayHour.head()


# In[69]:


plt.figure(figsize=(12,6))
sns.heatmap(dayHour,cmap='Blues')


# In[ ]:




