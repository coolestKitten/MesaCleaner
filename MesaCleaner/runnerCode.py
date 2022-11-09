from cleanerRobot import *
import mesa
from mesa.visualization.modules import CanvasGrid, ChartModule
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


total_moves = []
filth_cleaned = []

##params = {"width": 10, "height": 10, "N": range(10, 500, 10)}

"""
results = mesa.batch_run(
    cleanerModel,
    parameters=params,
    iterations=5,
    max_steps=100,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

results_df = pd.DataFrame(results)
print(results_df.keys())


results_filtered = results_df[(results_df.AgentID == 0) & (results_df.Step == 100)]
N_values = results_filtered.N.values
gini_values = results_filtered.Gini.values
plt.scatter(N_values, gini_values)


"""


for j in range(25):
    # Run the model
    model = cleanerModel(50, 50, 10, 10)
    for i in range(25):
        model.step()

    
    for agent in model.schedule.agents:
        if type(agent) == CleanerAgent:
            filth_cleaned.append(agent.filthCleaned)
            total_moves.append(agent.movements)
    
   
"""
agent_counts = np.zeros((model.grid.width, model.grid.height))
for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    agent_count = len(cell_content)
    agent_counts[x][y] = agent_count
plt.imshow(agent_counts, interpolation="nearest")
plt.colorbar()

"""
##plt.hist(filth_cleaned, bins=range(max(filth_cleaned) + 1))
##plt.hist(filth_cleaned, bins=range(max(filth_cleaned) + 1))
##plt.show()

def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle",
                 "Filled": "true"}

    if type(agent) is CleanerAgent:
        portrayal["Color"] = "#FF0000"
        portrayal["r"] = 0.8
        portrayal["Layer"] = 0

    elif type(agent) is FilthAgent:
        if agent.dirty:
            portrayal["Color"] = "#008206"
            
        else:
            portrayal["Color"] = "#FFFFFF"
        portrayal["r"] = 0.8
        portrayal["Layer"] = 1
            

    return portrayal


canvas_element = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

chart_element = ChartModule([{"Label": "AgentMoves", "Color": "#FF0000"},
                             {"Label": "FilthAmount", "Color": "#008206"}])



server = mesa.visualization.ModularServer(
    cleanerModel, [canvas_element, chart_element], "cleanerModel" , {"N":50, "D": 50, "width":10, "height":10}
) 

server.port = 8521 # The default
server.launch()


"""
gini = model.datacollector.get_model_vars_dataframe()
gini.plot()

agent_wealth = model.datacollector.get_agent_vars_dataframe()
agent_wealth.head()

end_wealth = agent_wealth.xs(99, level="Step")["Wealth"]
end_wealth.hist(bins=range(agent_wealth.Wealth.max() + 1))

one_agent_wealth = agent_wealth.xs(14, level="AgentID")
one_agent_wealth.Wealth.plot()

# save the model data (stored in the pandas gini object) to CSV
gini.to_csv("model_data.csv")

# save the agent data (stored in the pandas agent_wealth object) to CSV
agent_wealth.to_csv("agent_data.csv")


# First, we filter the results
one_episode_wealth = results_df[(results_df.N == 10) & (results_df.iteration == 2)]
# Then, print the columns of interest of the filtered data frame
print(
    one_episode_wealth.to_string(
        index=False, columns=["Step", "AgentID", "Wealth"], max_rows=25
    )
)

results_one_episode = results_df[
    (results_df.N == 10) & (results_df.iteration == 1) & (results_df.AgentID == 0)
]
print(results_one_episode.to_string(index=False, columns=["Step", "Gini"], max_rows=25))
"""