import mesa_geo as mg
import math

import random
import ast
import pandas as pd
from datetime import datetime, timedelta
from shapely.geometry import Point

seat_pref_csv = pd.read_csv('results/seat_pref.csv')

# helper function 
def get_key_from_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None  # Return None if the value is not found

class UserAgent(mg.GeoAgent):
    '''
    UserAgent:
    - has a preferred time of arrival, preferred length of stay
    '''
    def __init__(self, unique_id, model, geometry, crs, area_num, moore = True):
        super().__init__(unique_id, model, geometry, crs)
        # Agent parameters 
        # time-related 
        self.arrival_time = self.arrival_time()
        self.length_of_stay = self.random_length_of_stay()

        # level-related
        self.level_preference = self.predict_users_by_level()

        # seat-related
        self.seat_preference = self.assign_seat_perf()
        self.found_seat = False

        # seat-chopping
        self.seat_chopping_duration = self.assign_seat_chopping_duration() # how long seat is chopped
        self.seat_chopping_time = self.assign_seat_chopping_time() # starting from what time seat is chopped
        self.seat_chopped = False

        self.area_num = area_num # current location of the UserAgent
        self.moore = moore
        # self.mobility_range = mobility_range
        #print(f"Agent {self.unique_id} - Arrival Time: {self.arrival_time}")
        #print(f"Agent {self.unique_id} - Length of stay: {self.length_of_stay}")
        #print(f"Agent {self.unique_id} - Level Pref: {self.level_preference}")
        #print(f"Agent {self.unique_id} - Seat Pref: {self.seat_preference}")
        #print(f"Agent {self.unique_id} - Seat Chopping: {self.seat_chopping_duration}")
        #print(f"Agent {self.unique_id} - Seat Chopping Time: {self.seat_chopping_time}")

    def arrival_time(self):
        current_hour = self.model.counterHour

        # Assume that proportion remains the same for BOTH exam and non-exam periods
        #arrival_distribution_exam = {8:1.8, 9:10.5, 10:9.2, 11:10.1, 12:12.2, 13:12.8, 14:9.6, 15:7.8, 16:6.1, 17:5.6, 18:6.6, 19:5.5, 20:2.1}
        arrival_distribution_exam = {9:12.3, 10:9.2, 11:10.1, 12:12.2, 13:12.8, 14:9.6, 15:7.8, 16:6.1, 17:5.6, 18:6.6, 19:5.5, 20:2.1}
        #arrival_distribution_non_exam = {8:1.3, 9:8.2, 10:9.3, 11:9.1, 12:13.2, 13:15.2, 14:12.2, 15:10.0, 16:6.5, 17:6.7, 18:5.4, 19:2.6, 20:0.39}
        arrival_distribution_non_exam = {9:9.5, 10:9.3, 11:9.1, 12:13.2, 13:15.2, 14:12.2, 15:10.0, 16:6.5, 17:6.7, 18:5.4, 19:2.6, 20:0.39}

        arrival_time_percentages = arrival_distribution_exam if self.model.is_exam_season else arrival_distribution_non_exam
        total_users = self.model.input_users

        if current_hour in arrival_time_percentages:
            percentage = arrival_time_percentages[current_hour]
            num_agents = math.floor((percentage / 100) * total_users)
            
            if self.model.counter <= num_agents:
                arrival_times = [self.model.current_time.replace(hour=current_hour, minute=0) for _ in range(num_agents)]
                if self.model.counter == num_agents:
                    self.model.counter = 0
                    self.model.counterHour += 1
                else:
                    self.model.counter += 1
                return arrival_times[self.unique_id % num_agents]  # Assign agents sequentially within the hour

        return None
    
    def random_length_of_stay(self):
        closing_time = self.model.closing_time

        # Define the stay distributions for exam and non-exam seasons
        #stay_distribution_exam = {0.0: 2, 1.0: 23, 2.0: 22, 4.0: 50, 6.0: 145, 10.0: 1}
        #stay_distribution_non_exam = {0.0: 1, 1.0: 44, 2.0: 49, 4.0: 92, 6.0: 63}
        stay_distribution_non_exam = {1.0: 826, 2.0: 1183, 3.0: 1060, 4.0: 951, 5.0: 931, 6.0: 783, 7.0: 608, 
                                      8.0: 370, 9.0: 222, 10.0: 124, 11.0: 40, 12.0: 1}
        stay_distribution_exam = {1.0: 851, 2.0: 1028, 3.0: 1138, 4.0: 1275, 5.0: 1498, 6.0: 1542, 7.0: 1504, 
                                  8.0: 1192, 9.0: 700, 10.0: 402, 11.0: 141, 12.0: 69, 13.0: 31, 14.0: 5, 15.0: 4, 16.0: 3, 
                                  17.0: 2, 18.0: 6, 19.0: 6, 20.0: 7, 21.0: 7, 22.0: 8, 23.0: 4, 24.0: 2}
        
        # Choose the appropriate distribution based on the season
        stay_distribution = stay_distribution_exam if self.model.is_exam_season else stay_distribution_non_exam

        # Get the list of stay durations and their corresponding frequencies from the distribution
        stay_durations, frequencies = zip(*stay_distribution.items())

        # Choose a random duration based on the frequency distribution
        while True:
            random_duration = random.choices(stay_durations, frequencies)[0]
            # check if the random duration chosen exceeds the closing time of the library,
            # if it does, choose another random duration 
            #print(self.arrival_time)
            max_duration = (closing_time - self.arrival_time).total_seconds()
            max_duration = max_duration // 3600
            if random_duration <= max_duration:
                break

        # Convert the random duration (in hours) to a timedelta
        random_timedelta = timedelta(hours=random_duration)

        return random_timedelta

    def predict_users_by_level(self): 
        #eda_distribution = {3: 70, 4: 122, 5: 103, 6: 117, 61: 69}
        eda_distribution = {3: 70, 4: 122, 5: 103, 6: 186}

        # Get the list of level and their corresponding frequencies from the distribution
        level, frequencies = zip(*eda_distribution.items())

        # Choose a random duration based on the frequency distribution
        random_duration = random.choices(level, frequencies)[0]

        return random_duration

    def assign_seat_perf(self):
        seat_pref_dict = seat_pref_csv['seat_pref_dict']
        frequencies = seat_pref_csv['count']

        # Choose a random seat_pref based on the frequency distribution
        seat_pref = random.choices(seat_pref_dict, weights= frequencies)[0]

        # to change seat_pref dict from string type to dict type
        seat_pref = ast.literal_eval(seat_pref)

        # sort the seat preference
        seat_pref = dict(sorted(seat_pref.items(), key=lambda item: item[1], reverse=True))

        return seat_pref
    
    def assign_seat_chopping_duration(self):
    
        seat_chopping_distribution = {0.0: 38, 1.0: 176, 2.0: 26, 3.0: 13}

        # Get the list of seat_chopping_duration and their corresponding frequencies from the distribution
        seat_chopping_duration, frequencies = zip(*seat_chopping_distribution.items())

        # Choose a random duration based on the frequency distribution
        while True:
            random_duration = random.choices(seat_chopping_duration, frequencies)[0]
            random_duration = timedelta(hours=random_duration)
            if random_duration < self.length_of_stay: # check if seat choping duration is lesser than length of stay
                if random_duration == timedelta(hours= 1.0): # check those assigned lunch time
                    if self.arrival_time < datetime(2023, 4, 12, 14, 0): # needs to arrive before lunch
                        break  
                    else: # if didn't arrive before lunch, continue to find another situation duration
                        continue 
                else: # not assigned lunch time
                    break # the arrival time doesn't matter
            else: 
                continue

        return random_duration
    
    # assign the time where user is choping the seat
    def assign_seat_chopping_time(self):

        if self.seat_chopping_duration == timedelta(hours= 1.0): # if the user chope seats for lunch time (1 hour)
            lunch_time_distribution = {11: 40, 12: 91, 13: 41, 14: 4}

            # Get the list of seat_chopping_duration and their corresponding frequencies from the distribution
            lunch_time, frequencies = zip(*lunch_time_distribution.items())

            while True:
                random_lunch_time = random.choices(lunch_time, frequencies)[0]
                random_lunch_time = datetime(2023, 4, 12, random_lunch_time, 0)
                if random_lunch_time > self.arrival_time: # lunch time shld be after arrival time of agent
                    seat_chopping_time = random_lunch_time
                    break

        else: # if user is choping seats for other reasons 

            # get a random number of hours from the length of stay of the user minus the seat_chopping_duration
            random_hours = random.choice(range(1, (self.length_of_stay.seconds // 3600) - (self.seat_chopping_duration.seconds // 3600) + 1, 1)) 
            seat_chopping_time = self.arrival_time + timedelta(hours=random_hours)

        return seat_chopping_time

    # function to replicate a user finding seat - user behaviour, taking into account seat preference
    # need to settle user input
    def find_seat(self):

        area_names_dict = self.model.space.get_area_names_dict()
        #print(area_names_dict)
    
        # to find users first seat preference for that level
        for area_name in self.seat_preference.keys(): # loop through user's seat preferences 
            if area_name in area_names_dict.values(): # check if seat type exist on the level
                first_seat_preference = area_name
                break
        #print(self.seat_preference.keys())

        for area_name in self.seat_preference.keys(): # loop through user's seat preferences 
            if area_name in area_names_dict.values(): # check if seat type exist on the level
                area_num = get_key_from_value(area_names_dict, area_name) # get area_num from the area_name
                area = self.model.space.get_area_by_id(area_num) # get the area agent

                if area.num_people < area.max_capacity:  # If the area is not full
                    # Move the person to the non-full area
                    self.model.space.remove_person_from_area(self) # moving from lift
                    self.model.space.add_person_to_area(self, area_num) # to area
                    self.found_seat = True
                    if area_name != first_seat_preference:
                        self.model.users_didnt_get_preferred_seat += 1 # if seat user found is not most preferred seat
                    break  # Exit the loop once the person is placed
        
        # if can't find seat according to seat preference, user will be put into the discussion room randomly
        if not self.found_seat:
            areas_in_order = sorted(self.model.space._id_area_map.keys())
            random.shuffle(areas_in_order) 
            areas_in_order = [area_num for area_num in areas_in_order if str(area_num).startswith('3')] # only the discussion rooms

            for area_num in areas_in_order:
                area = self.model.space.get_area_by_id(area_num)

                if area.num_people < area.max_capacity:  # If the area is not full
                    # Move the person to the non-full area
                    self.model.space.remove_person_from_area(self) # moving from lift
                    self.model.space.add_person_to_area(self, area_num) # to area
                    self.found_seat = True
                    break  # Exit the loop once the person is placed
        
        # if unable to find seat at all, user will leave the level 
        if not self.found_seat:
            self.model.space.remove_person_from_area(self)
            self.model.schedule.remove(self)
            # to keep track of how many users unable to find seat on that floor
            self.model.users_unable_to_find_seat += 1
    
    def step(self): 
        # Advance one step
        if self.model.current_time > self.arrival_time: # if arrived
            if not self.found_seat: 
                self.find_seat()

            elif self.found_seat:# found a seat already
                if self.seat_chopping_duration > timedelta(hours= 0): # if user is choping seat
                    if not self.seat_chopped: # havent gone for seat chopping or came back from seat chopping
                        if self.model.current_time == self.seat_chopping_time: # if it's time for seat to be chopped
                            #print(f"GO Agent {self.unique_id} - Seat Chopping Time: {self.seat_chopping_time} - Seat Chopping: {self.seat_chopping_duration} - Arrival Time: {self.arrival_time} - Length of stay: {self.length_of_stay}")
                            self.seat_chopped = True # user will chope seat and leave the library
                            self.model.current_users_chope_seat += 1 # current num of choped seats will increase
                    elif self.seat_chopped: # if currently seat chopping
                        if self.model.current_time - self.seat_chopping_time == self.seat_chopping_duration: # if seat chopping duration is hit
                            #print(f"RETURN Agent {self.unique_id} - Seat Chopping Time: {self.seat_chopping_time} - Seat Chopping: {self.seat_chopping_duration} - Current Time: {self.model.current_time}")
                            self.seat_choped = False # user will return
                            self.model.current_users_chope_seat -= 1 # current num of choped seats will decrease

class AreaAgent(mg.GeoAgent):
    """Area agent. Changes color according to number of UserAgents inside it."""
    
    def __init__(self, unique_id, model, geometry, crs):
        """
        Create a new Neighbourhood agent.
        :param unique_id:   Unique identifier for the agent
        :param model:       Model in which the agent runs
        :param geometry:    Shape object for the agent
        :param max_capacity:   Max number of user agents that can be in the room
        """
        super().__init__(unique_id, model, geometry, crs)
       # self.area_name_id = area_name_id

        self.num_people = 0
        self.max_capacity = 5 # to initialise, to be changed later

        #self.model.counts[self.capacity] += 1  # Count agent type
    
    # function to change max capacity -> maybe can even be used as user_input
    def change_max_capacity(self, new_max_cap):
        self.max_capacity = new_max_cap
    
    # to get a random point within the area
    def random_point(self):
        min_x, min_y, max_x, max_y = self.geometry.bounds
        while not self.geometry.contains(
            random_point := Point(
                random.uniform(min_x, max_x), random.uniform(min_y, max_y)
            )
        ):
            continue
        return random_point
    
    def add_person(self):
        self.num_people += 1
    
    def remove_person(self):
        self.num_people -= 1

