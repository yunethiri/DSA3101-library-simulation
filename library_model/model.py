import mesa
import mesa_geo as mg

from agents import UserAgent, AreaAgent
from space import FloorPlan

from datetime import datetime, timedelta

# Functions needed for datacollector
def get_users_no_seats(model):
    return model.users_unable_to_find_seat

def get_users_on_floor(model):
    return len(model.schedule.agents)

def get_users_didnt_get_preferred_seat(model):
    return model.users_didnt_get_preferred_seat

def get_users_choped_seats(model):
    return model.current_users_chope_seat

def get_time(model):
    return model.current_time

def get_level(model):
    return model.input_level

def get_satisfaction_rate(model):
    return (len(model.schedule.agents) - model.users_didnt_get_preferred_seat)/len(model.schedule.agents) if len(model.schedule.agents) != 0 else 1

def get_occupancy_rate(model):
    total_max_seats = sum(model.max_capacity_dict.values())  # Sum up the maximum capacity of each seat section
    current_num_users_on_floor = get_users_on_floor(model)
    occupancy_rate = current_num_users_on_floor / total_max_seats if total_max_seats > 0 else 0
    return min(occupancy_rate,1) # cap the occupancy_rate at 1


# class for LibraryModel
class LibraryModel(mesa.Model):
    
    def __init__(self, input_users, input_exam_season, input_level_num, 
                 num_seats_discussion_cubicles, num_seats_soft_seats, num_seats_sofa, num_seats_moveable_seats,
                 num_seats_windowed_seats, num_seats_diagonal_seats, num_seats_cubicle_seats, num_seats_4man_seats, num_seats_8man_seats,
                 willingness_to_share_seats = 0.84, unique_id = "AREA_NUM"):
        """
        :param input_users:        number of users in library overall
        :param geojson_areas:   link to geojson file for level floorplan
        :param unique_id:      id to identify different rooms in level floorplan
        :param area_name_id:   name of different areas in level floorplan
        """
        super().__init__()

        self.schedule = mesa.time.BaseScheduler(self)
        self.space = FloorPlan()
        # geographical parameters for map

        # function to adjust max capacity according to willingess to share seats
        def adjust_max_cap(input_max_capacity):
             # actual max capacity is in a sense lower because some people don't want to share seats
            return round(input_max_capacity * willingness_to_share_seats)

        # dictionary to store max capacity for each seat section 
        self.max_capacity_dict = {}
        self.max_capacity_dict["Discussion Cubicles"] = adjust_max_cap(num_seats_discussion_cubicles)
        self.max_capacity_dict["Soft seats"] = adjust_max_cap(num_seats_soft_seats)
        self.max_capacity_dict["Sofa"] = adjust_max_cap(num_seats_sofa)
        self.max_capacity_dict["Moveable seats"] = adjust_max_cap(num_seats_moveable_seats)
        self.max_capacity_dict["Windowed Seats"] = adjust_max_cap(num_seats_windowed_seats)
        self.max_capacity_dict["Diagonal Seats"] = adjust_max_cap(num_seats_diagonal_seats)
        self.max_capacity_dict["Cubicle seats"] = adjust_max_cap(num_seats_cubicle_seats)
        self.max_capacity_dict["4-man tables"] = adjust_max_cap(num_seats_4man_seats)
        self.max_capacity_dict["8-man tables"] = adjust_max_cap(num_seats_8man_seats)
        #print(self.max_capacity_dict)

        self.input_level = input_level_num
        self.geojson_areas = f"clb_floor_plan/level{input_level_num}.geojson"
        self.unique_id = unique_id

        self.steps = 0

        # user parameters
        self.input_users = input_users
        self.users = []
        self.users_unable_to_find_seat = 0
        self.users_didnt_get_preferred_seat = 0
        self.current_users_chope_seat = 0
        
        self.counter = 0

        # time parameters
        self.is_exam_season = input_exam_season
        self.time_counter = 0
        
        if not self.is_exam_season: # not exam season, normal hours
            self.opening_time = datetime(2023, 4, 12, 9, 0) # 9 am
            self.closing_time = datetime(2023, 4, 12, 21, 0) # 9 pm
        elif self.is_exam_season: # exam season, adjust hours for l6 reading area
            if self.input_level == 6: # 24 hours
                self.opening_time = datetime(2023, 4, 12, 9, 0) # 9 am
                self.closing_time = datetime(2023, 4, 13, 9, 0) # 9 am
                #print(self.opening_time)
                #print(self.closing_time)
            else: # normal hours
                self.opening_time = datetime(2023, 4, 12, 9, 0) # 9 am
                self.closing_time = datetime(2023, 4, 12, 21, 0) # 9 pm

        self.current_time = self.opening_time  # Set the initial time to opening time
        # print(f"Initial Current Time: {self.current_time}")
        
        self.counterHour = self.current_time.hour
        # print(f"Counter: {self.counterHour}")

        self.running = True

        # Set up the Area patches for floorplan in file
        ac = mg.AgentCreator(AreaAgent, model=self)
        area_agents = ac.from_file(
                self.geojson_areas, unique_id=self.unique_id
                )
        self.space.add_areas(area_agents)
        # update agents max capacity
        for agent in area_agents:
            if agent.AREA_TYPE == "Open Area":
                new_max_cap = self.max_capacity_dict[agent.AREA_NAME]
                agent.change_max_capacity(new_max_cap)
            else:
                new_max_cap = agent.MAX_CAPACITY
                agent.change_max_capacity(new_max_cap)
            #print(agent.max_capacity)

        # Generate location from lift, add agent to grid and scheduler
        for i in range(input_users):
            starting_entrance_num = self.space.get_random_entrance_area_num() # get a random entrance to start at
            user = UserAgent(
                    unique_id = i,
                    model = self,
                    crs = self.space.crs,
                    geometry = self.space.get_area_by_id(starting_entrance_num).random_point(),
                    area_num = None, 
            )
            self.users.append(user) # keep track of all users created
            # print(f"Counter: {self.counter}")
            if self.current_time == user.arrival_time and self.input_level == user.level_preference:
                self.space.add_person_to_area(user, starting_entrance_num) # add to the starting entrance
                self.schedule.add(user)
        
        self.datacollector = mesa.DataCollector(
            model_reporters = {
                "time": get_time,
                "level": get_level,
                "current_num_users_on_floor": get_users_on_floor,
                "current_num_users_unable_to_find_seat": get_users_no_seats,
                "current_num_users_didnt_get_preferred_seat": get_users_didnt_get_preferred_seat,
                "current_num_seats_choped": get_users_choped_seats,
                "satisfaction_rate": get_satisfaction_rate,
                "occupancy_rate(level)": get_occupancy_rate,
            }
        )
            
        self.datacollector.collect(self)

    def get_current_time(self):
        # Simulate a continuous time counter (you can adapt this to your specific needs)
        # You can adjust the time step duration to control the speed of simulation.

        self.time_counter += 0.5 # time changes by 30 minutes at each step for now

        # Calculate the current time based on the time counter
        self.current_time = self.opening_time + timedelta(hours=self.time_counter)

        if self.current_time >= self.closing_time:
            self.current_time = self.closing_time

        return self.current_time
    
    def step(self):
        #print(self.current_users_chope_seat)
        """Run one step of the model."""
        self.current_time = self.get_current_time()  # at each step, update the current time with the current time function

        for user in self.users:
            if user not in self.schedule.agents and user.arrival_time == self.current_time and self.input_level == user.level_preference:
                self.space.add_person_to_area(user, self.space.get_random_entrance_area_num())  # add to the starting entrance
                self.schedule.add(user)
                #print("Added")

    # Check if users have exceeded their random length of stay and remove them from the area
        users_to_remove = []
        for user in self.users:
            if user in self.schedule.agents:
                stay_duration = user.length_of_stay  # You need to define this method for each user
                if self.current_time - user.arrival_time >= stay_duration:
                    users_to_remove.append(user)

        for user in users_to_remove:
            self.space.remove_person_from_area(user)  # Call your remove_person_from_area method to remove the user
            if user.seat_chopped: # if currently seat chopping
                if self.current_time - user.seat_chopping_time == user.seat_chopping_duration: # if seat chopping duration is hit
                    #print(f"RETURN Agent {user.unique_id} - Seat Chopping Time: {user.seat_chopping_time} - Seat Chopping: {user.seat_chopping_duration} - Current Time: {self.current_time}")
                    user.seat_choped = False # user will return
                    self.current_users_chope_seat -= 1 # current num of choped seats will decrease
            self.schedule.remove(user)
            #print(f"Agent {user.unique_id} is removed!")

        # reset the counter for num users_didnt_get_preferred_seat and users_unable_to_find_seat
        # once users have found their seats to get current counter instead of overall counter
        if self.current_time.minute == 0:
            self.users_didnt_get_preferred_seat = 0 
            self.users_unable_to_find_seat = 0

        #self.datacollector.collect(self)
        self.schedule.step()
        self.datacollector.collect(self)

        if self.current_time == self.closing_time:
            self.running = False
            results_df = self.datacollector.get_model_vars_dataframe()
            results_df.to_csv("results/results_one_run.csv", index = False)
