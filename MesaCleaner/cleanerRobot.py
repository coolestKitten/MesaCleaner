import mesa

    

class CleanerAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    movements = 0

    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.movements = 0
        self.filthCleaned = 0

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        

    def clean(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 0:
            for i in cellmates:
                if type(i) == FilthAgent and i.dirty == True:
                    i.dirty = False
                    self.filthCleaned += 1


    def step(self):
        self.move()
        self.movements += 1
        self.clean()
        print("Hi, I am agent " + str(self.unique_id) + " and i have moved " + str(self.movements) + " times, i have cleaned " + str(self.filthCleaned) + " cells.")


    

class FilthAgent(mesa.Agent):
    """Filth logic and step"""

    def __init__(self, pos, model, dirty):
        super().__init__(pos, model)
        self.dirty = dirty
    
    def step(self):
        if self.dirty == False:
            return


class cleanerModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, N, D, width, height):
        self.num_agents = N
        self.dirtiness = D
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        

        # Create agents
        for i in range(self.num_agents):
            x = 1
            y = 1
            mrClean = CleanerAgent(i, self)
            
            self.grid.place_agent(mrClean, (x, y))
            self.schedule.add(mrClean)
        
        index = N + 1
        for k in range(self.dirtiness):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            DirtyDan = FilthAgent(index + k, self, True)

            
            self.grid.place_agent(DirtyDan, (x, y))
            self.schedule.add(DirtyDan)
        
        self.datacollector = mesa.DataCollector(
            agent_reporters={"FilthCleaned" : "filthCleaned", "TotalMovements" : "movements"}
        )
            

    def step(self):
        ##self.datacollector.collect(self)
        self.schedule.step()