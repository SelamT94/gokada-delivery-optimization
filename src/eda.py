import matplotlib.pyplot as plt
import seaborn as sns

class EDA:
    def __init__(self, data):
        self.data = data

    def plot_histograms(self, columns):
        for column in columns:
            plt.figure(figsize=(10, 6))
            sns.histplot(self.data[column].dropna(), kde=True)
            plt.title(f'Histogram of {column}')
            plt.xlabel(column)
            plt.ylabel('Frequency')
            plt.show()

    def plot_bar_charts(self, columns):
        for column in columns:
            plt.figure(figsize=(10, 6))
            sns.countplot(data=self.data, x=column)
            plt.title(f'Bar Chart of {column}')
            plt.xlabel(column)
            plt.ylabel('Count')
            plt.show()

    def plot_spatial_distributions(self):
        if 'lng' in self.data.columns and 'lat' in self.data.columns:
            plt.figure(figsize=(10, 6))
            plt.scatter(self.data['lng'], self.data['lat'], alpha=0.5)
            plt.title('Spatial Distribution of Driver Locations')
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            plt.grid(True)
            plt.show()
        else:
            print("The required columns for spatial distribution ('lng' and 'lat') are not in the data.")

    def plot_temporal_patterns(self):
        if 'created_at' in self.data.columns:
            self.data['created_at'] = pd.to_datetime(self.data['created_at'], errors='coerce')
            self.data['hour'] = self.data['created_at'].dt.hour
            plt.figure(figsize=(10, 6))
            sns.histplot(self.data['hour'].dropna(), bins=24, kde=True)
            plt.title('Temporal Distribution of Driver Requests by Hour')
            plt.xlabel('Hour of Day')
            plt.ylabel('Number of Requests')
            plt.show()
        else:
            print("The 'created_at' column is not in the data.")
