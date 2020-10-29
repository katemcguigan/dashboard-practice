#!/usr/bin/env python
# coding: utf-8

# # Visualizing Baseball Salaries
# 
# This is a small notebook that does a simple visualization of Major League Baseball players' salary trends, using a dataset we've seen in previous weeks of this course.
# 
# ## Load the dataset
# 
# First, we load the dataset we're familiar with, and remember what it contains.

# In[1]:

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv( 'baseball-salaries-simplified.csv' )
df.head()

# ## Filter the dataset
# 
# Just as an example, we'll focus our attention on third basemen in the years from 2000 to 2010, inclusive.

# In[2]:

first_year=st.sidebar.slider("Choose the first year to view: ", 1988, 2016, 2000, 1)
last_year=st.sidebar.slider("Choose the last year to view: ", 1989, 2020, 2010, 1)
position=st.sidebar.selectbox("Choose position: ", ["OF", "1B", "P", "2B", "3B", "C", "SS"])


just_2000s = (df.year >= 2000) & (df.year <= 2010)
just_third_base = df.pos == '3B'
focus = df[just_2000s & just_third_base]
focus.head()


# ## Create a table of percentiles


#st.dataframe( focus.nlargest( 10, 'salary' ).reset_index( drop=True ) )

# I'm interested in seeing trends in the entire dataset.  There are so many data points that if we plotted them all, the graph would be quite busy.  So I'll plot the various percentiles of the data over time instead.  To do so, we must first compute what those percentiles are.

# In[3]:


# Which years do we care about?
years = range( 2000, 2011 )

# We'll store the results in a new DataFrame.
df_pcts = pd.DataFrame( { "year" : years } )

# How to compute a percentile in a given year:
def percentile_in_year ( year, percent ):
    return focus[focus.year == year].salary.quantile( percent/100 )

# Fill the DataFrame using that function.
for percent in range( 0, 110, 10 ):
    df_pcts[percent] = [ percentile_in_year( year, percent ) for year in years ]

# Make years the index.
df_pcts.index = df_pcts.year
del df_pcts['year']

# Change units to millions of dollars.
df_pcts /= 1000000

# See result.
#df_pcts


# ## Plot the data
# 
# Now we can view the trends in the salary distribution over time.

# In[6]:

df_pcts.plot( legend='upper left' )
plt.gcf().set_size_inches(8,10)
plt.title( f'Salaries for Third Basement only, {len(focus)} players', fontsize=20 )
plt.xticks( df_pcts.index, rotation=90 )
plt.ylabel( 'Salary percentiles in $1M', fontsize=14 )
plt.xlabel( None )
st.pyplot(plt.gcf())


# ## Investigate Extreme Values
# 
# Makes you wonder who created the spikes on the graph...Let's find out.

# In[5]:


focus.nlargest( 10, 'salary' ).reset_index( drop=True )

