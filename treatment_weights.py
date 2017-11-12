# Author: Haley E. Speed, Ph.D.
# Calculates descriptive statistics on mouse weights over time during drug or toxin administration


#--------------------------------------------------------------------------------------------------------------------------------------#
# Import Packages 																													   #
#--------------------------------------------------------------------------------------------------------------------------------------#

import pandas as pd
import os
import csv
import numpy as np

#--------------------------------------------------------------------------------------------------------------------------------------#
# Define variables 																													   #
#--------------------------------------------------------------------------------------------------------------------------------------#
file_name = 'mouse_weights.csv'
directory = 'D:\\Dropbox'
group1 = 'saline'
group2 = 'drug'


#--------------------------------------------------------------------------------------------------------------------------------------#
# Define functions 																													   #
#--------------------------------------------------------------------------------------------------------------------------------------#

def sample_size(data, group1, group2):

	n1 = 0
	n2 = 0

	for index,row in data.iterrows():
		if group1 in row['treatment']:
			n1 = n1 + 1
		elif group2 in row['treatment']:
			n2 = n2 + 1
	
	data['n'] = 0
	for index, row in data.iterrows():
		if group1 in row['treatment']:
			data['n'] = n1
		elif group2 in row['treatment']:
			data['n'] = n2
		
	return data

#--------------------------------------------------------------------------------------------------------------------------------------#
# Main Program 								    																					   #
#--------------------------------------------------------------------------------------------------------------------------------------#	

# Read data into a dataframe
os.chdir(directory)
raw_data = pd.read_csv(file_name)

weight_by_day = raw_data.groupby(['treatment', 'day']).mean()
weight_by_day_std = raw_data.groupby(['treatment', 'day']).std()

weight_by_day = weight_by_day.reset_index()
weight_by_day_std = weight_by_day_std.reset_index()

weight_by_day = sample_size(weight_by_day, group1, group2)

weight_by_day['weight_std'] = weight_by_day_std['weight']
weight_by_day['weight_ste'] = weight_by_day['weight_std']/np.sqrt(weight_by_day['n'])

weight_by_day = weight_by_day.filter(['treatment', 'day', 'n', 'weight', 'weight_ste', 'weight_std'])
weight_by_day = weight_by_day.sort_values(['treatment','day'], ascending = [False, True])

#--------------------------------------------------------------------------------------------------------------------------------------#
# Save Data 								    																					   #
#--------------------------------------------------------------------------------------------------------------------------------------#	

save_file = file_name.replace('.csv','')
save_file = save_file + '_desc.csv'
weight_by_day.to_csv(save_file, index = False)
