from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from LibraryModel import LibraryModel

def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {
        "Shape": "circle",
        "Color": "red",  # You can choose any color you like
        "Filled": "true",
        "Layer": 0,
        "r": 0.5,  # Agent radius
    }

    return portrayal


def model_portrayal(agent):
    # Define how agents are displayed on the grid
    if agent is None:
        return

    portrayal = {
        "Shape": "rect",
        "w": 1,  # Width of the grid cell
        "h": 1,  # Height of the grid cell
        "Color": "red",  # Customize the color of agents
        "Filled": "true",
    }
    return portrayal


grid_width = 10
grid_height = 10
canvas_element = CanvasGrid(agent_portrayal, grid_width, grid_height, 500, 500)
#num_users_slider = Slider("Number of Users", 0, 100, 50)  # Example values, adjust as needed

# Set up the server to display the grid visualization
server = ModularServer(
    LibraryModel,
    [canvas_element],
    "Library Simulation Model",
    model_params={
        "num_users": 100,  # Set an initial number of users
        "width": grid_width,
        "height": grid_height,
    },
)


# Start the server
server.port = 8521  # You can choose a different port if needed
server.launch()