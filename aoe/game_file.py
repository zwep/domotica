menu = {"villager": {"cost": "50 food", "time": 20}}

class Villager:
    def __init__(self, task=None):
        self.resource = 0
        # If task is None == Idle
        self.task = task

    def gather_resource(self):
        self.resource += 20/60

    def deposit_resource(self):
        temp_resource = self.resource
        self.resource = 0
        return temp_resource


class TownCenter:
    def __init__(self):
        self.build_villager_time = 20
        self.resource_cost_villager = {"food": 50}

    def build_villager(self, task=None):
        return self.resource_cost_villager, Villager(task=task)


class Sheep:
    def __init__(self):
        self.food = 100


class Boar:
    def __init__(self):
        self.food = 340


class Game:
    def __init__(self):
        self.town_center = TownCenter()
        self.population = [Villager('food') for _ in range(4)]
        self.resource = {"wood": 200 - 2*25, "food": 200, "gold": 100, "stone": 200}
        self.n_sheep = 8
        self.n_boar = 2
        self.population_space = 15  # TC + 2 houses
        # self.wood = 200
        # self.food = 200
        # self.gold = 100
        # self.stone = 200

    def run(self, time):
        for itime in range(time):
            for i_villager in self.population:
                i_villager.gather_resource()
                if i_villager.resource >= 10:
                    resource = i_villager.deposit_resource()
                    self.resource[i_villager.task] += resource

            # Always make villagers..
            if itime % self.town_center.build_villager_time == 0:
                resource_cost, temp_farmer = self.town_center.build_villager('food')
                for k, v in resource_cost.items():
                    self.resource[k] -= v
                self.population.append(temp_farmer)

            # Make a house..
            if len(self.population) == (self.population_space-1):
                self.population_space += 5
                self.resource['wood'] -= 25

if __name__ == "__main__":
    game_obj = Game()
    game_obj.run(800)