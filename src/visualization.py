import pandas as pd
import folium
import seaborn as sns
import matplotlib.pyplot as plt

class Visualization:
    def __init__(self, data):
        self.data = data

    def plot_routes(self):
        map = folium.Map(location=[self.data['latitude'].mean(), self.data['longitude'].mean()], zoom_start=12)
        for _, row in self.data.iterrows():
            folium.Marker([row['origin_lat'], row['origin_lng']], popup='Origin').add_to(map)
            folium.Marker([row['dest_lat'], row['dest_lng']], popup='Destination').add_to(map)
            folium.PolyLine([(row['origin_lat'], row['origin_lng']), (row['dest_lat'], row['dest_lng'])], color='blue').add_to(map)
        return map

    def plot_density(self):
        plt.figure(figsize=(10, 6))
        sns.kdeplot(x='longitude', y='latitude', data=self.data, fill=True)
        plt.title('Density Plot of Orders')
        plt.show()

# Example usage
if __name__ == "__main__":
    data = pd.read_csv('C:/Users/dell/Desktop/10Academy/gokada-delivery-optimization/data/driver_locations_during_request.csv')
    visualization = Visualization(data)
    visualization.plot_routes()
    visualization.plot_density()
