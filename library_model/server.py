import mesa
import mesa_geo as mg

from agents import UserAgent, AreaAgent
from model import LibraryModel

#print(xyz.OpenStreetMap.keys())

# to display time
class ClockElement(mesa.visualization.TextElement):
    def __init__(self):
        super().__init__()
        pass

    def render(self, model):
        formatted_time = model.current_time.strftime("%H:%M:%S")
        return (f"Current time: {formatted_time}")
    
# to display seat colour legend
class SeatColourLegend(mesa.visualization.TextElement):
    def __init__(self):
        super().__init__()
        pass

    def render(self, model):
        colour_dict = {} # key: AREA_NAME, value: portrayal color 
        for agent in model.space.agents:
            if isinstance(agent, AreaAgent):
                if agent.AREA_TYPE == "Open Area":
                    portrayal = agent_portrayal(agent)
                    colour_dict[agent.AREA_NAME] = portrayal["color"]
        return (f"Seat Colour Legend: {colour_dict}")

# to determine shape, colour, etc. of the visualisation of each agent
def agent_portrayal(agent):
    """
    Portrayal Method for canvas
    """
    portrayal = {}
    if isinstance(agent, UserAgent):
        portrayal["radius"] = "1"
        portrayal["shape"] = "circle"
        if agent.seat_chopped:
            portrayal["color"] = "Red"
        elif not agent.seat_chopped:
            portrayal["color"] = "Black"
    elif isinstance(agent, AreaAgent):
        if agent.AREA_TYPE == "Entrance":
            portrayal["color"] = "Grey"
        else:
            if agent.num_people < agent.max_capacity:
                if agent.AREA_NAME == "Soft seats" or agent.AREA_NAME == "Windowed Seats":
                    portrayal["color"] = "Purple"
                elif agent.AREA_NAME == "Sofa" or agent.AREA_NAME == "8-man tables" or agent.AREA_NAME == "Diagonal Seats":
                    portrayal["color"] = "Blue"
                elif agent.AREA_NAME == "Moveable seats" or agent.AREA_NAME == "4-man tables":
                    portrayal["color"] = "Yellow"
                elif agent.AREA_NAME == "Discussion Cubicles" or agent.AREA_NAME == "Cubicle seats":
                    portrayal["color"] = "Pink"
                else:
                    portrayal["color"] = "Green"
            elif agent.num_people >= agent.max_capacity:
                portrayal["color"] = "Red"
    return portrayal

clock_element = ClockElement()
seat_colour_legend = SeatColourLegend()

# to display chart for whole numbers
users_chart = mesa.visualization.ChartModule(
    [
        {"Label": "current_num_users_unable_to_find_seat", "Color": "#7bb36e"},
        {"Label": "current_num_users_on_floor", "Color": "#c66657"}
    ],
    data_collector_name="datacollector"
)

# to display chart for percentages 
satisfaction_chart = mesa.visualization.ChartModule(
    [
        {"Label": "satisfaction_rate", "Color": "#7bb36e"},
        {"Label": "occupancy_rate(level)", "Color": "#c66657"}
    ],
    data_collector_name="datacollector"
)


# building the map
map_element = mg.visualization.MapModule(
    agent_portrayal,
    view = [1.2964537,103.7730378],
    zoom= 25,
    map_height=400,
    map_width=400,
    #tiles=xyz.OpenStreetMap.BlackAndWhite
    )

model_params = {
    "input_users": mesa.visualization.Slider("Overall Number of Users in the Library", 100, 100, 3000, 100),
    "input_exam_season": mesa.visualization.Choice("Exam Season?", value = False, 
                                                choices = [True,False]),
    "input_level_num":  mesa.visualization.Choice("Level", value = 3, 
                                                choices = [3, 4, 5, 6]),
    "num_seats_discussion_cubicles": mesa.visualization.Slider("Number of Seats for Discussion Cubicles (L3)", 0, 0, 500, 10),
    "num_seats_moveable_seats": mesa.visualization.Slider("Number of Seats for Moveable Seats (L3)", 0, 0, 500, 10),
    "num_seats_soft_seats": mesa.visualization.Slider("Number of Seats for Soft Seats (L3 / L4)", 0, 0, 500, 10),
    "num_seats_sofa": mesa.visualization.Slider("Number of Seats for Sofa (L3 / L4)", 0, 0, 500, 10),
    "num_seats_windowed_seats": mesa.visualization.Slider("Number of Seats for Windowed Seats (L5 & L6)", 0, 0, 500, 10),
    "num_seats_4man_seats": mesa.visualization.Slider("Number of Seats for 4-Man Tables (L5)", 0,0, 500, 10),
    "num_seats_8man_seats": mesa.visualization.Slider("Number of Seats for 8-Man Tables (L5)", 0, 0, 500, 10),
    "num_seats_diagonal_seats": mesa.visualization.Slider("Number of Seats for Diagonal Seats (L6)", 0, 0, 500, 10),
    "num_seats_cubicle_seats": mesa.visualization.Slider("Number of Seats for Cubicle Seats (L6)", 0, 0, 500, 10),
}

server = mesa.visualization.ModularServer(
    LibraryModel,
    [map_element, clock_element, seat_colour_legend, users_chart,satisfaction_chart],
    "Library Model",
    model_params,
    port = 8519,
)