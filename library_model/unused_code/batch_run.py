# This script runs the model each time with different parameters to compare between different parameters

import mesa
import pandas as pd

from model import LibraryModel

# constant for input_users, input_max_capacity, input_exam_season
# different for input_level_num -> to compare between different levels
params = {"input_level_num": [3, 4, 5, 6],
          "input_users": 500,
            "input_max_capacity": 100,
            "input_exam_season": True}

results_batch = mesa.batch_run(
    LibraryModel,
    parameters = params,
    iterations = 1,
    number_processes = 1,
    data_collection_period = 1,
    display_progress = False
)

results_batch_df = pd.DataFrame(results_batch)
results_batch_df.to_csv("results/results_diff_params.csv")
