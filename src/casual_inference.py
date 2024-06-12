import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from causalinference import CausalModel

class CausalInference:
    def __init__(self, data):
        self.data = data

    def create_causal_graph(self):
        G = nx.DiGraph()
        G.add_edges_from([
            ("hour", "driver_action"),
            ("distance", "driver_action"),
            ("weather", "driver_action")
        ])
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=15, font_color='black')
        plt.title('Causal Graph')
        plt.show()

    def perform_inference(self):
        model = CausalModel(
            Y=self.data['driver_action'].values,  # Outcome variable (change this to your actual outcome variable)
            D=self.data['driver_id'].values,      # Treatment variable (change this to your actual treatment variable)
            X=self.data[['hour', 'distance', 'weather']].values  # Covariates
        )
        model.est_via_matching(bias_adj=True)  # Estimate treatment effects via matching
        return model

data = pd.read_csv('C:/Users/dell/Desktop/10Academy/gokada-delivery-optimization/data/driver_locations_during_request.csv')

causal_inference = CausalInference(data)

causal_inference.create_causal_graph()

causal_model = causal_inference.perform_inference()

print(causal_model.estimates)
