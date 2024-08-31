import mesa
import pandas as pd
from model import LibraryModel
from flask import Flask, request, json, jsonify
import os

app = Flask(__name__)

def create_param_dict(input_values):
    default_value = 0
    param_keys = [
        "input_level_num", "input_users", "input_exam_season",
        "num_seats_discussion_cubicles", "num_seats_moveable_seats", "num_seats_soft_seats",
        "num_seats_sofa", "num_seats_windowed_seats", "num_seats_4man_seats",
        "num_seats_8man_seats", "num_seats_diagonal_seats", "num_seats_cubicle_seats"
    ]
    
    return {key: input_values.get(key, default_value) for key in param_keys}

results_directory = "results"
results_file = "results_for_specific_combinations.csv"
results_path = os.path.join(results_directory, results_file)

@app.route('/run_model', methods=['POST'])
def run_model():
    # Receive JSON payload
        json_string = request.get_json()
        input_params = json.loads(json_string)

        # Extract values from JSON payload
        iln = input_params["input_level_num"]
        ies = input_params["input_exam_season"]
        ss1, ss2 = input_params["input_users_values"]
        dcs1, dcs2 = input_params["num_seats_discussion_cubicles_values"]
        mvs1, mvs2 = input_params["num_seats_moveable_seats_values"]
        sss1, sss2 = input_params["num_seats_soft_seats_values"]
        sos1, sos2 = input_params["num_seats_sofa_values"]

        # Use the extracted values as needed
        # For example, you can pass them to your Mesa model
        base_params = {
            "input_level_num": iln,
            "input_exam_season": ies
        }

        input_users_values = [ss1, ss2]
        num_seats_discussion_cubicles_values = [dcs1, dcs2]
        num_seats_moveable_seats_values = [mvs1, mvs2]
        num_seats_soft_seats_values = [sss1, sss2]
        num_seats_sofa_values = [sos1, sos2]
# Base parameters
# base_params = {
#     "input_level_num": 3,
#     "input_exam_season": True #change this to let it take input from slider
# }

# # Values from sliders (change to let it take input from slider)
# input_users_values =  [500,1000]
# num_seats_discussion_cubicles_values = [50, 7]
# num_seats_moveable_seats_values = [100, 200]
# num_seats_soft_seats_values = [4, 60]
# num_seats_sofa_values = [20,40]

        results = []
        for users, discussion_cubicles, moveable_seats, soft_seats, sofa in zip(input_users_values, num_seats_discussion_cubicles_values, 
                                                                                            num_seats_moveable_seats_values, num_seats_soft_seats_values, num_seats_sofa_values):
            slider_values = {
                "input_users": users,
                "num_seats_discussion_cubicles": discussion_cubicles,
                "num_seats_moveable_seats": moveable_seats,
                "num_seats_soft_seats": soft_seats,
                "num_seats_sofa": sofa
            }
            param_dict = create_param_dict({**base_params, **slider_values})
            model_instance = LibraryModel(**param_dict)
            model_instance.run_model()
            results_df = model_instance.datacollector.get_model_vars_dataframe()
            results.append(results_df)

        all_results_df = pd.concat(results, ignore_index=True)
        all_results_df.to_csv(results_path)
        return jsonify({"status": "success"})

@app.route('/run_model4', methods=['POST'])
def run_model4():
    # Receive JSON payload
        json_string = request.get_json()
        input_params = json.loads(json_string)

        # Extract values from JSON payload
        iln = input_params["input_level_num"]
        ies = input_params["input_exam_season"]
        ss1, ss2 = input_params["input_users_values"]
        sss1, sss2 = input_params["num_seats_soft_seats_values"]
        sos1, sos2 = input_params["num_seats_sofa_values"]

        # Use the extracted values as needed
        # For example, you can pass them to your Mesa model
        base_params = {
            "input_level_num": iln,
            "input_exam_season": ies
        }

        input_users_values = [ss1, ss2]
        num_seats_soft_seats_values = [sss1, sss2]
        num_seats_sofa_values = [sos1, sos2]

        results = []
        for users, soft_seats, sofa in zip(input_users_values, num_seats_soft_seats_values, num_seats_sofa_values):
            slider_values = {
                "input_users": users,
                "num_seats_soft_seats": soft_seats,
                "num_seats_sofa": sofa
            }
            param_dict = create_param_dict({**base_params, **slider_values})
            model_instance = LibraryModel(**param_dict)
            model_instance.run_model()
            results_df = model_instance.datacollector.get_model_vars_dataframe()
            results.append(results_df)

        # Concatenate results into a single DataFrame and save to CSV
        all_results_df = pd.concat(results, ignore_index=True)
        all_results_df.to_csv(results_path)
        return jsonify({"status": "success"})

@app.route('/run_model5', methods=['POST'])
def run_model5():
    # Receive JSON payload
        json_string = request.get_json()
        input_params = json.loads(json_string)

        # Extract values from JSON payload
        iln = input_params["input_level_num"]
        ies = input_params["input_exam_season"]
        ss1, ss2 = input_params["input_users_values"]
        wss1, wss2 = input_params["num_seats_windowed_values"]
        fmt1, fmt2 = input_params["num_seats_4"]
        emt1, emt2 = input_params["num_seats_8"]
# Base parameters
        base_params = {
            "input_level_num": iln,
            "input_exam_season": ies #change this to let it take input from slider
        }

        # Values from sliders (change to let it take input from slider)
        input_users_values =  [ss1,ss2]
        num_seats_windowed_seats_values = [wss1, wss2]
        num_seats_4man_seats_values = [fmt1, fmt2]
        num_seats_8man_seats_values = [emt1, emt2]

        results = []
        for users, seats_4man, seats_8man, windowed_seats in zip(input_users_values, num_seats_4man_seats_values, num_seats_8man_seats_values, num_seats_windowed_seats_values):
            slider_values = {
                "input_users": users,
                "num_seats_windowed_seats": windowed_seats,
                "num_seats_4man_seats": seats_4man,
                "num_seats_8man_seats": seats_8man
            }
            param_dict = create_param_dict({**base_params, **slider_values})
            model_instance = LibraryModel(**param_dict)
            model_instance.run_model()
            results_df = model_instance.datacollector.get_model_vars_dataframe()
            results.append(results_df)

        all_results_df = pd.concat(results, ignore_index=True)
        all_results_df.to_csv(results_path)
        return jsonify({"status": "success"})

@app.route('/run_model6', methods=['POST'])
def run_model6():
    # Receive JSON payload
        json_string = request.get_json()
        input_params = json.loads(json_string)

        # Extract values from JSON payload
        iln = input_params["input_level_num"]
        ies = input_params["input_exam_season"]
        ss1, ss2 = input_params["input_users_values"]
        wss1, wss2 = input_params["num_seats_window"]
        dss1, dss2 = input_params["num_seats_diagonal"]
        css1, css2 = input_params["num_seats_cubicles"]        
        # Base parameters
        base_params = {
            "input_level_num": iln,
            "input_exam_season": ies #change this to let it take input from slider
        }

        # Values from sliders (change to let it take input from slider)
        input_users_values =  [ss1,ss2]
        num_seats_windowed_seats_values = [wss1, wss2]
        num_seats_diagonal_seats_values = [dss1, dss2]
        num_seats_cubicle_seats_values = [css1, css2]

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
        all_results_df.to_csv(results_path)
        return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8520, debug=True)



