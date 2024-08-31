import mesa
import pandas as pd
from model import LibraryModel

def create_param_dict(input_values):
    default_value = 0
    param_keys = [
        "input_level_num", "input_users", "input_exam_season",
        "num_seats_discussion_cubicles", "num_seats_moveable_seats", "num_seats_soft_seats",
        "num_seats_sofa", "num_seats_windowed_seats", "num_seats_4man_seats",
        "num_seats_8man_seats", "num_seats_diagonal_seats", "num_seats_cubicle_seats"
    ]
    
    return {key: input_values.get(key, default_value) for key in param_keys}

# Base parameters
base_params = {
    "input_level_num": 6,
    "input_exam_season": True #change this to let it take input from slider
}

# Values from sliders (change to let it take input from slider)
input_users_values =  [500,1000]
num_seats_windowed_seats_values = [50, 7]
num_seats_diagonal_seats_values = [100, 200]
num_seats_cubicle_seats_values = [100, 120]

results = []
for users, windowed_seats, diagonal_seats, cubicle_seats  in zip(input_users_values, num_seats_windowed_seats_values, num_seats_diagonal_seats_values, num_seats_cubicle_seats_values):
    slider_values = {
        "input_users": users,
        "num_seats_windowed_seats": windowed_seats,
        "num_seats_diagonal_seats": diagonal_seats,
        "num_seats_cubicle_seats": cubicle_seats
    }
    param_dict = create_param_dict({**base_params, **slider_values})
    model_instance = LibraryModel(**param_dict)
    model_instance.run_model()
    results_df = model_instance.datacollector.get_model_vars_dataframe()
    results.append(results_df)

all_results_df = pd.concat(results, ignore_index=True)
all_results_df.to_csv("results/results_for_specific_combinations.csv")





