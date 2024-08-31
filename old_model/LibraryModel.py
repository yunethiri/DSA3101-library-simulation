import mesa
import random
import datetime

class LibraryUser(mesa.Agent):
    def __init__(self, unique_id, model, time_interval):
        super().__init__(unique_id, model)
        self.time_interval = time_interval
        self.current_id = unique_id
    
class LibraryModel(mesa.Model):
    def __init__(self, num_users, width, height):
        self.num_users = num_users
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.time_counter = 0
        self.current_id = 0
        self.current_time = datetime.datetime(2023, 4, 12, 9, 0)  # Set the initial time to 9:00 AM
        self.schedule = mesa.time.BaseScheduler(self)
        self.running = False
        self.users = []

        for i in range(self.num_users // 3):
            # Add the agent to a random grid cell
            user = LibraryUser(i,self, self.current_time )
            self.schedule.add(user)
            self.users.append(user)
            self.current_id = i
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(user, (x, y))

    # Custom method to control agent count by time interval
    def adjust_agent_count(self, current_time):
        # Define logic to adjust agent count based on current time
        morning_time = datetime.datetime(2023, 4, 12, 12, 0)
        afternoon_time = datetime.datetime(2023, 4, 12, 17, 0)

        if current_time < morning_time:
            return self.num_users // 3  # Fewer users in the morning
        elif morning_time <= current_time < afternoon_time:
            return self.num_users // 2  # More users in the afternoon
        else:
            return self.num_users // 3  # Fewer users in the evening
        
    # Custom method to control agent behavior based on time interval
    def adjust_agent_behavior(self, current_time):
        # Define agent behavior based on current time interval
        for user in self.users:
            if user.time_interval == current_time:
                # Implement behavior specific to this time interval
                user.step()

    def get_current_time(self):
        # Define the library's opening hours
        library_opening_time = datetime.datetime(2023, 4, 12, 9, 0)  # 9 am
        library_closing_time = datetime.datetime(2023, 4, 12, 21, 0)  # 9 pm

        # Simulate a continuous time counter (you can adapt this to your specific needs)
        # This example uses a time counter that increases by 1 hour every time step.
        # You can adjust the time step duration to control the speed of simulation.
        self.time_counter += 1

        # Calculate the current time based on the time counter
        self.current_time = library_opening_time + datetime.timedelta(hours=self.time_counter)

        if self.current_time >= library_closing_time:
            self.current_time = library_closing_time

        return self.current_time

    
    def step(self): # for each step, what will happen 
        # Get the current time (you can implement a time tracking mechanism)
        current_time = self.get_current_time()

        # Adjust agent count based on the current time interval
        agent_count = self.adjust_agent_count(current_time)

         # Debugging output
        print(f"Current Time: {current_time}")
        print(f"Agent Count: {agent_count}")

        # If the agent count needs to be adjusted, create or remove agents
        current_agent_count = len(self.users)

        # Lists to track agents being added and removed
        grid_agents = grid_agents = []  # Initialize with existing agents on the grid
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell_contents = self.grid.get_cell_list_contents((x, y))
                grid_agents.extend(cell_contents)

        if current_agent_count < agent_count:
            users_to_add = agent_count - current_agent_count
            for _ in range(users_to_add):
                user = LibraryUser(self.next_id(), self, current_time)
                self.users.append(user)

                # Add the agent to a random grid cell
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(user, (x, y))

        elif current_agent_count > agent_count:
            users_to_remove = current_agent_count - agent_count
            users_to_remove_indices = random.sample(range(current_agent_count), users_to_remove)
            removed_users = [user for i, user in enumerate(self.users) if i in users_to_remove_indices]

            # Remove agents from the grid
            for agent in removed_users:
                self.grid.remove_agent(agent)

            self.users = [user for i, user in enumerate(self.users) if i not in users_to_remove_indices]
        
        self.grid.contents = grid_agents

        self.schedule.step()

    

