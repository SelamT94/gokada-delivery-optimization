import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class FeatureEngineering:
    @staticmethod
    def create_temporal_features(data):
        data['created_at'] = pd.to_datetime(data['created_at'])
        data['hour_of_day'] = data['created_at'].dt.hour
        data['day_of_week'] = data['created_at'].dt.dayofweek  # Monday=0, Sunday=6
        data['month'] = data['created_at'].dt.month
        return data
    
    @staticmethod
    def calculate_distances(data, fixed_location):
        data['distance_to_fixed_location'] = np.sqrt((data['lat'] - fixed_location[0])**2 + (data['lng'] - fixed_location[1])**2)
        return data
    
    @staticmethod
    def normalize_features(data, features):
        for feature in features:
            data[feature] = (data[feature] - data[feature].mean()) / data[feature].std()
        return data
    
    @staticmethod
    def plot_heatmap(data):
        plt.figure(figsize=(10, 8))
        sns.heatmap(data.groupby(['lat', 'lng']).size().unstack(), cmap='YlGnBu')
        plt.title('Driver Locations Heatmap')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show()
