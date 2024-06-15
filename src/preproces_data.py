import os
import pandas as pd

# Data directory
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

class GokadaDataPreprocessor:
    def __init__(self, completed_orders_path, drivers_location_path):
        self.completed_orders = pd.read_csv(completed_orders_path)
        self.drivers_location = pd.read_csv(drivers_location_path)

    def preprocess_data(self):
        self.completed_orders.rename(columns={'Trip ID': 'order_id'}, inplace=True)
        self.completed_orders['order_id'] = self.completed_orders['order_id'].astype(str)
        self.drivers_location['order_id'] = self.drivers_location['order_id'].astype(str)
        self.drivers_location.drop(columns=['created_at', 'updated_at'], inplace=True)
        self.drivers_location.rename(columns={'lat': 'drivers_lat', 'lng': 'drivers_lon'}, inplace=True)
        self.merged_df = self.completed_orders.merge(self.drivers_location, on='order_id', how='left')
        self.merged_df.dropna(subset=['driver_action'], inplace=True)
        self._handle_missing_times()
        self._convert_timestamps_and_extract_features()
        self._extract_coordinates()
        self._remove_outliers()
        self.merged_df.columns = self.merged_df.columns.str.lower().str.replace(' ', '_')
        return self.merged_df

    def _handle_missing_times(self):
        self.merged_df['Trip Start Time'] = pd.to_datetime(self.merged_df['Trip Start Time'])
        median_start_time = self.merged_df['Trip Start Time'].median()
        self.merged_df['Trip Start Time'].fillna(median_start_time, inplace=True)

    def _convert_timestamps_and_extract_features(self):
        for df in [self.merged_df]:
            df['Trip Start Time'] = pd.to_datetime(df['Trip Start Time'])
            df['Trip End Time'] = pd.to_datetime(df['Trip End Time'])
            df['day_of_week'] = df['Trip Start Time'].dt.day_name()
            df['hour_of_day'] = df['Trip Start Time'].dt.hour
            df['day_of_month'] = df['Trip Start Time'].dt.day
            df['month'] = df['Trip Start Time'].dt.month_name()
            df['trip_start_date'] = pd.to_datetime(df['Trip Start Time']).dt.date
            df['trip_end_date'] = pd.to_datetime(df['Trip End Time']).dt.date

    def _extract_coordinates(self):
        for col in ['Trip Origin', 'Trip Destination']:
            for df in [self.merged_df]:
                df[[f'{col}_latitude', f'{col}_longitude']] = df[col].str.split(',', expand=True).astype(float)

    def _remove_outliers(self):
        self.merged_df['trip_duration'] = (self.merged_df['Trip End Time'] - self.merged_df['Trip Start Time']).dt.total_seconds() / 60
        q1 = self.merged_df['trip_duration'].quantile(0.25)
        q3 = self.merged_df['trip_duration'].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        self.merged_df = self.merged_df[(self.merged_df['trip_duration'] >= lower_bound) & (self.merged_df['trip_duration'] <= upper_bound)]

    def save_to_csv(self, df, filename):
        df.to_csv(os.path.join(data_dir, filename), index=False)

    def preprocess_and_save(self, filename):
        preprocessed_df = self.preprocess_data()
        self.save_to_csv(preprocessed_df, filename)
        return preprocessed_df

# Example usage
completed_orders_path = os.path.join(data_dir, 'nb.csv')
drivers_location_path = os.path.join(data_dir, 'driver_locations_during_request.csv')

preprocessor = GokadaDataPreprocessor(completed_orders_path, drivers_location_path)
preprocessed_df = preprocessor.preprocess_and_save('preprocessed_data.csv')
print(preprocessed_df.head().to_markdown(index=False, numalign="left", stralign="left"))
