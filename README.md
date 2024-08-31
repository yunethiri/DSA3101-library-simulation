# DSA3101 - Modeling Occupancy at NUS Central Library

## Overview

This project aims to optimize resource usage in the NUS Central Library by simulating occupancy across different levels. The project utilizes a Mesa agent-based model, where library users are assigned attributes and behaviors to simulate movements within the library. 

Users have the flexibility to adjust various parameters, such as the length of stay, number of seats on a level, exam season, overall number of users in the library, and the specific library level.

More information of the project is found in `Technical_Handover_Documentation.pdf`.

## Running the Model

To run the model, follow these steps:

#### Run Docker Compose:

```bash
docker-compose up -d
```

#### Access the Model:

Visit `http://localhost:8050` in your web browser.

## Interpreting the Model 
- Red-Shaded Areas: Indicates full occupancy (maximum capacity reached). If the number of seats in an area is set to 0, the area will also be shaded red.
  
- Red Agents: When library users (agents represented by dots) are red, seat is occupied.

## Model Parameters

#### Adjust Parameters:
Select parameters, including the overall number of users in the library.

Users are distributed across levels and different times following specific distributions.

#### Seat Configuration:
All seats are initially set to 0. Adjust the number of seats only for the selected level.

For example, if users select level 3 as the input level, adjust seats for level 3, leaving the seats on the rest of the levels as 0.

#### Frames per Second (FPS):
FPS determines the simulation speed, with each step representing 30 minutes.

## Model Output

Results of the simulation are updated in real time and saved in `library_model/results/results_one_run.csv`.

Two key metrics are provided:

#### 1. Satisfaction Rate:
Defined as the number of users who get their preferred seat divided by the total number of users on the floor.

#### 2. Occupancy Rate:
Defined as the number of users on the floor divided by the total number of seats on the floor.

## Additional Notes

The model is designed to represent and optimize resource usage in a library setting.

Users can experiment with different parameters to observe their impact on satisfaction and occupancy rates.

Feel free to explore and contribute to the project! If you encounter any issues or have suggestions, please refer to the Issues section or submit a pull request.




