#!/usr/bin/env python
# coding: utf-8

# # Pymaceuticals Inc.
# ---
# 
# ### Analysis
# 
# - Add your analysis here.
# observations1- the data is 51% male where 49% female, so both sexes are acounted for rather equally  
#observations2- Capomulin and provriva tends to have the greatest number of time points showing that they are most effective 
#observations3- zoniferol has the least number of time points showing it is least effective
# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st 
import numpy as np


# In[2]:


# Study data files
mouse_metadata_path = "Mouse_metadata.csv"
study_results_path = "Study_results.csv"


# In[3]:


# Read the mouse data and the study results
mouse_metadata = pd.read_csv(mouse_metadata_path)
study_results = pd.read_csv(study_results_path)


# In[4]:


# Combine the data into a single DataFrame
merged_df = pd.merge(study_results, mouse_metadata, on ='Mouse ID', how = "left")

# Display the data table for preview
merged_df.head()
#--- why does this look different the the output?


# In[5]:


# Checking the number of mice.
mouse_num_d = merged_df['Mouse ID'].unique()
mouse_num = len(set(mouse_num_d))
mouse_num


# In[6]:


# Our data should be uniquely identified by Mouse ID and Timepoint
# Get the duplicate mice by ID number that shows up for Mouse ID and Timepoint. 
# Check for duplicate mice based on Mouse ID and Timepoint
duplicates = merged_df.duplicated(subset=['Mouse ID', 'Timepoint'], keep=False)

# Filter the DataFrame to show only the duplicate mice
duplicate_mice = merged_df[duplicates]

# Get the unique Mouse IDs of the duplicate mice
duplicate_mouse_ids = duplicate_mice['Mouse ID'].unique()

# Display the duplicate mice
duplicate_mouse_ids


# In[7]:


# Optional: Get all the data for the duplicate mouse ID.
duplicate_mouse_id = 'g989'
duplicate_mouse_data = merged_df[merged_df["Mouse ID"] == duplicate_mouse_id]
duplicate_mouse_data


# In[8]:


# Create a clean DataFrame by dropping the duplicate mouse by its ID.
merged_df_no_dups = merged_df.drop_duplicates(subset = "Mouse ID")
merged_df_no_dups


# In[9]:


# Checking the number of mice in the clean DataFrame.
# Create a clean DataFrame by dropping duplicate mice by their ID
merged_df_no_dups = merged_df[merged_df['Mouse ID'] != 'g989']

merged_df_no_dups


# In[10]:


## Checking the number of mice.

merged_df_no_dups_d = merged_df_no_dups['Mouse ID'].unique()
mouse_nun_nod = len(set(merged_df_no_dups_d))
mouse_nun_nod


# In[11]:


#Get the array of drugs for below
merged_df_no_dups["Drug Regimen"].unique()


# ## Summary Statistics

# In[12]:


# Generate a summary statistics table of mean, median, variance, standard deviation, 
#and SEM of the tumor volume for each regimen
#i want ot goup by the drug then calculate the drug
mean_df = merged_df_no_dups.groupby(['Drug Regimen'])['Tumor Volume (mm3)'].mean()
median_df = merged_df_no_dups.groupby(['Drug Regimen'])['Tumor Volume (mm3)'].median()
var_df = merged_df_no_dups.groupby(['Drug Regimen'])['Tumor Volume (mm3)'].var()
std_df = merged_df_no_dups.groupby(['Drug Regimen'])['Tumor Volume (mm3)'].std()
sem_df = merged_df_no_dups.groupby(['Drug Regimen'])['Tumor Volume (mm3)'].sem()
# Use groupby and summary statistical methods to calculate the following properties of each drug regimen: 


# mean, median, variance, standard deviation, and SEM of the tumor volume. 
# Assemble the resulting series into a single summary DataFrame.

summary_stat = pd.DataFrame({'Mean': mean_df, 'Median': median_df, 'Variance': var_df, 'Std': std_df, 'SEM': sem_df})

summary_stat


# In[13]:


# A more advanced method to generate a summary statistics table of mean, median, variance, standard deviation,
# and SEM of the tumor volume for each regimen (only one method is required in the solution)

# Using the aggregation method, produce the same summary statistics in a single line
merged_df_no_dups.groupby('Drug Regimen')['Tumor Volume (mm3)'].agg(['mean','median','var','std','sem'])


# ## Bar and Pie Charts

# In[14]:


# Generate a bar plot showing the total number of rows (Mouse ID/Timepoints) for each drug regimen using Pandas.

# Group the data by 'Drug' and calculate the count or number of times 'Time Point'
drug_timepoint = merged_df_no_dups.groupby('Drug Regimen')['Timepoint'].count()

# Create the bar plot, fig size 10 by 4 scince thers 10 x values and 4 y values
drug_timepoint.plot(kind='bar', figsize=(10, 4))

# Customize the plot
plt.title('Mean Time Point by Drug')  # Set the title of the plot
plt.xlabel('Drug Regimen')  # Set the label for the x-axis
plt.ylabel('# of Observed Mouse Timepoints')  # Set the label for the y-axis

# Display the plot
plt.show()


# In[15]:


drugs = ['Capomulin', 'Ketapril', 'Naftisol', 'Infubinol', 'Stelasyn',
       'Ramicane', 'Zoniferol', 'Propriva', 'Placebo', 'Ceftamin']
users =  merged_df_no_dups.groupby('Drug Regimen')['Timepoint'].count()
x_axis = np.arange(len(users))
tick_locations = [value for value in x_axis]
plt.xticks(tick_locations, drugs, rotation = 'vertical')
# Customize the plot
plt.title('Mean Time Point by Drug')  # Set the title of the plot
plt.xlabel('Drug Regimen')  # Set the label for the x-axis
plt.ylabel('# of Observed Mouse Timepoints')  # Set the label for the y-axis
plt.bar(x_axis, users)


# In[16]:


# Generate a pie plot showing the distribution of female versus male mice using Pandas
sex_counts = merged_df_no_dups['Sex'].value_counts()
percentage = merged_df_no_dups['Sex'].value_counts()/merged_df_no_dups['Sex'].value_counts().sum() *100
color = ['LightBlue', 'Orange']
percentage.plot(kind = 'pie', autopct = '%1.1f%%', colors = color)


# In[17]:


# Generate a pie plot showing the distribution of female versus male mice using pyplot
sex_counts = merged_df_no_dups['Sex'].value_counts()
percentage = merged_df_no_dups['Sex'].value_counts()/merged_df_no_dups['Sex'].value_counts().sum() *100
sexs =[ 'Male', 'Female']
color = ['LightBlue', 'Orange']
plt.pie(percentage, labels = sexs, colors = color, autopct = '%1.1f%%')
plt.title("Sex")
plt.show()


# ## Quartiles, Outliers and Boxplots

# In[18]:


# Calculate the final tumor volume of each mouse across four of the treatment regimens:  
# Capomulin, Ramicane, Ramicane, and Ceftamin
target_cap = merged_df_no_dups[merged_df_no_dups['Drug Regimen'] == 'Capomulin']
target_ram = merged_df_no_dups[merged_df_no_dups['Drug Regimen'] == 'Ramicane']
target_infu = merged_df_no_dups[merged_df_no_dups['Drug Regimen'] == 'Infubinol']
target_ceft = merged_df_no_dups[merged_df_no_dups['Drug Regimen'] == 'Ceftamin']
# Start by getting the last (greatest) timepoint for each mouse 
time_cap = merged_df_no_dups.groupby('Mouse ID')['Timepoint'].max()

# Convert the series to a dataframe
time_cap_df = pd.DataFrame({'Mouse ID': time_cap.index, 'Last Timepoint': time_cap.values})

# Merge the dataframe with the original dataframe to get the tumor volume at the last timepoint
merged_df = pd.merge(merged_df_no_dups, time_cap_df, on='Mouse ID')

# Print the merged dataframe
merged_df


# In[19]:


# Put treatments into a list for for loop (and later for plot labels)
treatments = ['Capomulin', 'Ramicane', 'Infubinol', 'Ceftamin']

# Create empty list to fill with tumor vol data (for plotting)
tumor_vol = []

# Calculate the IQR and quantitatively determine if there are any potential outliers. 
    
    # Locate the rows which contain mice on each drug and get the tumor volumes
for treatment in treatments:
    treatment_data = merged_df.loc[merged_df['Drug Regimen'] == treatment, 'Tumor Volume (mm3)']
    
    # Add the tumor volume data for the current treatment to the tumor_vol list
    quartiles = treatment_data.quantile([.25,.5,.75])
    lowerq = quartiles[0.25]
    upperq = quartiles[0.75]
    iqr = upperq-lowerq
    lower_bound = lowerq - (1.5*iqr)
    upper_bound = upperq + (1.5*iqr)
    # add subset 
    tumor_vol.append(tumor_vol)
    outliers = treatment_data[(treatment_data <  lower_bound) | (treatment_data > upper_bound)]
    
    
    
    
    # Determine outliers using upper and lower bounds
    print(f'{treatment}\ `s potential outliers: {outliers}')
    print(f'The lower is {lower_bound}, the upper is {upper_bound}')


# In[20]:


# Generate a box plot that shows the distrubution of the tumor volume for each treatment group.

#NOTE HAD ISSUE RUNNING THIS BLOCK MAY HAVE TO SKIP----  I SPOKE TO THE INSTUCTOR 
fig1, ax1 = plt.subplots()
ax1.set_title('Drug vs Tumor Size')
ax1.set_ylabel('Tumor Volume (mm3)')
ax1.boxplot(tumor_vol)
plt.show()


# ## Line and Scatter Plots

# In[ ]:





# In[21]:


# Generate a line plot of tumor volume vs. time point for a single mouse treated with Capomulin
target_mouse = merged_df_no_dups.groupby('Mouse ID').get_group('l509')
timepoints_x = target_mouse['Timepoint']
tumor_volume_y = target_mouse['Tumor Volume (mm3)']

plt.plot(timepoints_x, tumor_volume_y)


# In[22]:


# Filter the dataframe for Capomulin regimen
target_drug = merged_df_no_dups.loc[merged_df_no_dups['Drug Regimen'] == 'Capomulin']

# Group by mouse weight and calculate the average tumor volume
capomulin_average = target_drug.groupby(['Mouse ID'])[['Weight (g)', 'Tumor Volume (mm3)']].mean()
# Generate the scatter plot
plt.scatter(capomulin_average['Weight (g)'], capomulin_average['Tumor Volume (mm3)'])
plt.xlabel('Mouse Weight (g)')
plt.ylabel('Average Tumor Volume (mm3)')
plt.title('Mouse Weight vs. Average Tumor Volume (Capomulin Regimen)')
plt.show()


# In[ ]:





# ## Correlation and Regression

# In[23]:


# Filter the dataframe for Capomulin regimen
target_drug = merged_df_no_dups.loc[merged_df_no_dups['Drug Regimen'] == 'Capomulin']

# Group by mouse weight and calculate the average tumor volume
capomulin_average = target_drug.groupby(['Mouse ID'])[['Weight (g)', 'Tumor Volume (mm3)']].mean()
# Generate the scatter plot
mice_weight = capomulin_average['Weight (g)']
mice_tumor = capomulin_average['Tumor Volume (mm3)']


(t_slope, t_int, t_r, t_p, t_std_err) = st.linregress(mice_weight, mice_tumor)
best_fit = t_slope * mice_weight + t_int 
plt.plot(mice_weight, best_fit)


plt.scatter(capomulin_average['Weight (g)'], capomulin_average['Tumor Volume (mm3)'])
plt.plot(mice_weight, best_fit, '--') #---------------------------
plt.xlabel('Mouse Weight (g)')
plt.ylabel('Average Tumor Volume (mm3)')
plt.title('Mouse Weight vs. Average Tumor Volume (Capomulin Regimen)')
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




