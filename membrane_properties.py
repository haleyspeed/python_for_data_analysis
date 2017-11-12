
# Author: Haley E. Speed, Ph.D.
# Function to calculate mean, ste, and std from raw data 
# Outputs both data per cell and data per mouse


#--------------------------------------------------------------------------------------------------------------------------------------#
# Import Packages 																									                                                        				   #
#--------------------------------------------------------------------------------------------------------------------------------------#

import pandas as pd
import os
import csv
import numpy as np


#--------------------------------------------------------------------------------------------------------------------------------------#
# Define variables 																												                                                        	   #
#--------------------------------------------------------------------------------------------------------------------------------------#
file_name = 'data.csv'
directory = 'C:\\Python'
treatment1 = 'vehicle'
treatment2 = 'drug'
genotype1 = 'W'
genotype2 = 'K'
step = -10


#--------------------------------------------------------------------------------------------------------------------------------------#
# Define functions 																						                                                         							   #
#--------------------------------------------------------------------------------------------------------------------------------------#

# Calculate Input Resistance 
def inputR (i, step):				# V = IR where V = -10 mV step and I is in pA
    return (step/(i/10**9)) / 10**6		# Converted to MOhm before return	

# Calculate Membrane Capacitance
def cm_q (q, step = -10):				# C = Q/V where Q = area under the current step and V = -10 mV step
    return (q * 0.001)/(step/1000) / 1000	# Converted to microF (nF) before being returned
	

def sample_size(raw_data, genotype1, genotype2, treatment1, treatment2):
	n1 = 0
	n2 = 0
	n3 = 0
	n4 = 0

	# Calculate sample sizes and assign genotype/treatment groups
	raw_data['group'] = 0
	raw_data['n'] = 0
	for index, row in raw_data.iterrows():
		if genotype1 in row['genotype']: 
			if treatment1 in row['treatment']:
				n1 = n1 + 1
				raw_data.loc[index:index:,'group'] = 1
			elif treatment2 in row['treatment']:
				n2 = n2 + 1 
				raw_data.loc[index:index:,'group'] = 2
		elif genotype2 in row['genotype']:
			if treatment1 in row['treatment']:
				n3 = n3 + 1
				raw_data.loc[index:index:,'group'] = 3
			elif treatment2 in row['treatment']:
				n4 = n4 + 1
				raw_data.loc[index:index:,'group'] = 4
	
	# Assign sample sizes
	for index, row in raw_data.iterrows():
		if genotype1 in row['genotype']: 
			if treatment1 in row['treatment']:
				raw_data.loc[index:index:,'n'] = n1
			elif treatment2 in row['treatment']:
				raw_data.loc[index:index:,'n'] = n2
		elif genotype2 in row['genotype']:
			if treatment1 in row['treatment']:
				raw_data.loc[index:index:,'n'] = n3
			elif treatment2 in row['treatment']:
				raw_data.loc[index:index:,'n'] = n4
	return(raw_data)
	

def per_cell (raw_data):
	# Aggregate according to genotype and treatment
	per_cell = raw_data.groupby(['genotype', 'treatment']).mean()
	per_cell_std = raw_data.groupby(['genotype', 'treatment']).std()
	
	per_cell = per_cell.reset_index()
	per_cell_std = per_cell_std.reset_index()
     
	# Calculate standard error 
	per_cell['inputR_ste'] = per_cell_std['inputR(MOhm)']/np.sqrt(per_cell['n'])
	per_cell['capacitance_q_ste'] = per_cell_std['capacitance_q(nF)']/np.sqrt(per_cell['n'])

	# Calculate standard deviation
	per_cell['inputR_std'] = per_cell_std['inputR(MOhm)']
	per_cell['capacitance_q_std'] = per_cell_std['capacitance_q(nF)']

	# Keep only the relevant columns and order them in a way that makes sense
	per_cell = per_cell.filter(['group', 'genotype', 'treatment','n', 'inputR(MOhm)', 'inputR_ste','inputR_std', 
                            'capacitance_q(nF)', 'capacitance_q_ste', 'capacitance_q_std'])

	# Sort data so that WT and vehicle come first
	per_cell = per_cell.sort_values(['group'])
	
	return per_cell

def mouse_avg (raw_data):
	# Aggregate according to genotype, treatment, and mouse
	collapse_per_mouse = raw_data.groupby(['genotype', 'treatment', 'mouse']).mean()
	collapse_per_mouse_std = raw_data.groupby(['genotype', 'treatment', 'mouse']).std()
        
	collapse_per_mouse = collapse_per_mouse.reset_index()
	collapse_per_mouse_std = collapse_per_mouse_std.reset_index()	
	
	# Calculate standard error
	collapse_per_mouse['inputR_ste'] = collapse_per_mouse['inputR(MOhm)']/np.sqrt(collapse_per_mouse['n'])
	collapse_per_mouse['capacitance_q_ste'] = collapse_per_mouse_std['capacitance_q(nF)']/np.sqrt(collapse_per_mouse['n'])

	# Calculate standard deviation
	collapse_per_mouse['inputR_std'] = collapse_per_mouse_std['inputR(MOhm)']
	collapse_per_mouse['capacitance_q_std'] = collapse_per_mouse_std['capacitance_q(nF)']

	# Keep only the relevant columns and order them in a way that makes sense
	collapse_per_mouse = collapse_per_mouse.filter(['group', 'genotype', 'treatment', 'mouse', 'n', 'inputR(MOhm)', 'inputR_ste','inputR_std',
                                                'capacitance_q(nF)', 'capacitance_q_ste', 'capacitance_q_std'])

	# Sort data so that WT and vehicle come first
	collapse_per_mouse = collapse_per_mouse.sort_values(['group'])
	
	return collapse_per_mouse

def per_mouse (collapse_per_mouse):
	# Aggregate according to genotype, treatment
	per_mouse = collapse_per_mouse.groupby(['genotype', 'treatment']).mean()
	per_mouse_std = collapse_per_mouse.groupby(['genotype', 'treatment']).std()
    
	per_mouse = per_mouse.reset_index()
	per_mouse_std = per_mouse_std.reset_index()
	
	#Calculate standard error
	per_mouse['inputR_ste'] = per_mouse_std['inputR(MOhm)']/np.sqrt(per_mouse['n'])
	per_mouse['capacitance_q_ste'] = per_mouse_std['capacitance_q(nF)']/np.sqrt(per_mouse['n'])

	# Calculate standard deviation
	per_mouse['inputR_std'] = per_mouse_std['inputR(MOhm)']
	per_mouse['capacitance_q_std'] = per_mouse_std['capacitance_q(nF)']

	# Sort data so that WT and vehicle come first
	per_mouse = per_mouse.sort_values(['group'])

	return per_mouse
	

#--------------------------------------------------------------------------------------------------------------------------------------#
# Main Program 								    																			                                                        		   #
#--------------------------------------------------------------------------------------------------------------------------------------#	

# Read the csv file into a pandas dataframe
os.chdir(directory)
raw_data = pd.read_csv(file_name)

# Calculate Input Resistance and Membrane capacitance
raw_data['inputR(MOhm)'] = inputR(raw_data['current(pA)'], step)
raw_data['capacitance_q(nF)'] = cm_q(raw_data['charge(pA*s)'], step)


#Get sample size for each group and assign group ID for sorting
raw_data = sample_size(raw_data, genotype1, genotype2, treatment1, treatment2) 

# Get descriptive stats per cell
per_cell_desc = per_cell(raw_data)
collapse_per_mouse = mouse_avg (raw_data)
per_mouse_desc = per_mouse(collapse_per_mouse)



#--------------------------------------------------------------------------------------------------------------------------------------#
# Save Data 								    																			                                                          		   #
#--------------------------------------------------------------------------------------------------------------------------------------#	

# Save raw data with Input Resistance and Capacitance to file
file_name = file_name.replace('.csv','')
raw_file = file_name + '_per_cell.csv'
raw_data.to_csv(raw_file, index = False)

# Save descriptive stats per cell to file
per_cell_file = file_name + '_per_cell_desc.csv'
per_cell_desc.to_csv(per_cell_file, index = False)

# Save average per mouse to file
collapsed_file = file_name + "_per_mouse.csv"
collapse_per_mouse.to_csv(collapsed_file, index = False)

# Save descriptive stats per mouse to file
per_mouse_file = file_name + '_per_mouse_desc.csv'
per_mouse_desc.to_csv(per_mouse_file, index = False)


