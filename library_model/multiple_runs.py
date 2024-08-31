# This script runs the model multiple times with the SAME parameters to get the average and confidence intervals

import mesa
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

from model import LibraryModel

# USER INPUTS 
# constant parameters
params = {"input_level_num": 3,
          "input_users": 500,
            "input_max_capacity": 100,
            "input_exam_season": True}
 
# number of times to run the model
input_iterations = 50
# confidence level for finding average and confidence intervals 
input_confidence_level = 0.90  # e.g. 0.9 is 90%
# metric that they want to find (e.g. current number of users on the floor, number of users unable to find seat)
input_metric = 'current_num_users_on_floor'

# RUN THE MODEL
# run the model with the specified number of iterations 
results_multiple_runs = mesa.batch_run(
    LibraryModel,
    parameters = params,
    iterations = input_iterations,
    number_processes = 1,
    data_collection_period = 1,
    display_progress = True
)

results_multiple_runs_df = pd.DataFrame(results_multiple_runs)
# save the raw data into a new csv
results_multiple_runs_df.to_csv("results/results_multiple_runs_raw.csv")

# CALCULATE AVERGAE AND CONFIDENCE INTERVAL
# Function to calculate the confidence interval
def calculate_ci(data):
    mean = data.mean()
    std = data.std()
    n = len(data)
    z = critical_value # 95% confidence interval
    lower = mean - (z * (std / np.sqrt(n)))
    upper = mean + (z * (std / np.sqrt(n)))
    return lower, upper

# calculate critical value with the input confidence level 
tail_probability = (1 - input_confidence_level) / 2  # Calculate tail probability for a two-tailed interval
critical_value = norm.ppf(1 - tail_probability)  # Find the critical value

grouped = results_multiple_runs_df.groupby('Step')[input_metric] # group by step and the metric
average_data = grouped.mean().reset_index()
ci_data = grouped.apply(calculate_ci).apply(pd.Series).rename(columns={0: 'ci_lower', 1: 'ci_upper'}).reset_index()

result_data = average_data.merge(ci_data, on='Step')
# save the calculated average data into a new csv
result_data.to_csv('results/results_multiple_runs_averaged.csv', index=False)

# PLOT THE GRAPH FOR AVERAGE AND CONFIDENCE INTERVAL
x = result_data['Step']
y = result_data[input_metric]

ci_lower = result_data['ci_lower']
ci_upper = result_data['ci_upper']

# Create a line plot for the average
plt.plot(x, y, label='Average', color='blue')
# Fill the area between the confidence intervals
plt.fill_between(x, ci_lower, ci_upper, color='lightgray', label='Confidence Interval', alpha=0.5)

# Add labels and a legend
plt.xlabel('Step')
plt.ylabel(input_metric)
plt.title('Average and Confidence Intervals Over Time')
plt.legend()

# Save the plot as an image (e.g., PNG)
plt.savefig('results/results_average_with_confidence_intervals.png', dpi=300, bbox_inches='tight')

# Don't forget to close the plot
plt.close()





