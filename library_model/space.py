import random
from typing import Dict

import mesa_geo as mg

from agents import AreaAgent

class FloorPlan(mg.GeoSpace):
    _id_area_map: Dict[int, AreaAgent]

    def __init__(self):
        super().__init__(warn_crs_conversion=False)
        self._id_area_map = {}
        self.num_people = 0
    
    # add AreaAgents to the Map
    def add_areas(self, agents):
        super().add_agents(agents)
        for agent in agents:
            self._id_area_map[agent.unique_id] = agent

    # add a UserAgent to an area (AreaAgent)
    def add_person_to_area(self, person, area_num):
        person.area_num = area_num
        person.geometry = self._id_area_map[area_num].random_point()
        self._id_area_map[area_num].add_person()
        super().add_agents(person)
        self.num_people += 1

    # remove a UserAgent to an area (AreaAgent)
    def remove_person_from_area(self, person):
        self._id_area_map[person.area_num].remove_person()
        person.area_num = None
        super().remove_agent(person)
        self.num_people -= 1

    def get_area_max_capacity(self, agent):
        return agent.MAX_CAPACITY
    
    def get_area_name(self, area_num):
        agent = self._id_area_map.get(area_num)
        return agent.AREA_NAME
    
    def get_random_entrance_area_num(self) -> int:
        entrance_area_nums = [area_num for area_num in self._id_area_map.keys() if str(area_num).startswith('1')]
        return random.choice(entrance_area_nums)
    
    def get_random_area_num(self) -> int:
        return random.choice(list(self._id_area_map.keys()))
    
    def get_area_names_dict(self):
        result = {}
        for id, agent in self._id_area_map.items():
            result[id] = agent.AREA_NAME
        return result

    def get_area_by_id(self, area_num) -> AreaAgent:
        return self._id_area_map.get(area_num)
    
  