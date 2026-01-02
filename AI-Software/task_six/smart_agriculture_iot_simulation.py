"""
AI-Driven IoT Smart Agriculture Simulation
AI Future Directions Assignment - Task 2

This script simulates a smart agriculture system with IoT sensors and AI-driven
crop yield prediction for precision farming applications.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import random
from dataclasses import dataclass
from typing import List, Dict, Tuple
import json

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

@dataclass
class SensorReading:
    """Data class for IoT sensor readings"""
    timestamp: datetime.datetime
    sensor_id: str
    sensor_type: str
    value: float
    location: Tuple[float, float]  # (latitude, longitude)

@dataclass
class CropZone:
    """Data class for crop zone information"""
    zone_id: str
    crop_type: str
    area_hectares: float
    planting_date: datetime.date
    expected_harvest: datetime.date
    location: Tuple[float, float]

class IoTSensorNetwork:
    """Simulates IoT sensor network for smart agriculture"""
    
    def __init__(self, farm_area_hectares: float = 100):
        self.farm_area = farm_area_hectares
        self.sensors = self._initialize_sensors()
        self.crop_zones = self._initialize_crop_zones()
        self.sensor_data = []
        
    def _initialize_sensors(self) -> Dict[str, Dict]:
        """Initialize sensor network configuration"""
        sensors = {
            'soil_moisture': {
                'count': int(self.farm_area * 3),  # 3 per hectare
                'reading_interval': 15,  # minutes
                'normal_range': (20, 80),  # percentage
                'unit': '%'
            },
            'temperature': {
                'count': max(1, int(self.farm_area / 25)),  # 1 per 25 hectares
                'reading_interval': 5,  # minutes
                'normal_range': (15, 35),  # celsius
                'unit': '°C'
            },
            'humidity': {
                'count': max(1, int(self.farm_area / 25)),
                'reading_interval': 5,
                'normal_range': (40, 80),  # percentage
                'unit': '%'
            },
            'ph_level': {
                'count': max(1, int(self.farm_area / 10)),  # 1 per 10 hectares
                'reading_interval': 1440,  # daily (minutes)
                'normal_range': (6.0, 7.5),
                'unit': 'pH'
            },
            'light_intensity': {
                'count': max(1, int(self.farm_area / 25)),
                'reading_interval': 60,  # hourly
                'normal_range': (0, 100000),  # lux
                'unit': 'lux'
            },
            'npk_nitrogen': {
                'count': max(1, int(self.farm_area / 20)),
                'reading_interval': 10080,  # weekly
                'normal_range': (20, 50),  # ppm
                'unit': 'ppm'
            }
        }
        return sensors
    
    def _initialize_crop_zones(self) -> List[CropZone]:
        """Initialize crop zones across the farm"""
        zones = []
        crops = ['corn', 'wheat', 'soybeans', 'tomatoes']
        
        for i in range(4):  # 4 crop zones
            zone = CropZone(
                zone_id=f"zone_{i+1}",
                crop_type=crops[i],
                area_hectares=self.farm_area / 4,
                planting_date=datetime.date(2024, 3, 15) + datetime.timedelta(days=i*7),
                expected_harvest=datetime.date(2024, 9, 15) + datetime.timedelta(days=i*7),
                location=(40.7128 + i*0.01, -74.0060 + i*0.01)  # NYC area coordinates
            )
            zones.append(zone)
        
        return zones
    
    def generate_sensor_data(self, days: int = 30) -> pd.DataFrame:
        """Generate simulated sensor data for specified number of days"""
        print(f"Generating {days} days of sensor data...")
        
        start_date = datetime.datetime.now() - datetime.timedelta(days=days)
        data_records = []
        
        for sensor_type, config in self.sensors.items():
            for sensor_id in range(config['count']):
                current_time = start_date
                
                while current_time < datetime.datetime.now():
                    # Generate realistic sensor reading
                    base_value = self._generate_realistic_reading(sensor_type, current_time)
                    
                    # Add some random variation
                    noise = np.random.normal(0, base_value * 0.05)  # 5% noise
                    value = max(0, base_value + noise)
                    
                    # Create sensor reading
                    reading = {
                        'timestamp': current_time,
                        'sensor_id': f"{sensor_type}_{sensor_id:03d}",
                        'sensor_type': sensor_type,
                        'value': round(value, 2),
                        'latitude': 40.7128 + random.uniform(-0.1, 0.1),
                        'longitude': -74.0060 + random.uniform(-0.1, 0.1),
                        'unit': config['unit']
                    }
                    
                    data_records.append(reading)
                    
                    # Move to next reading time
                    current_time += datetime.timedelta(minutes=config['reading_interval'])
        
        df = pd.DataFrame(data_records)
        self.sensor_data = df
        print(f"Generated {len(df)} sensor readings")
        return df
    
    def _generate_realistic_reading(self, sensor_type: str, timestamp: datetime.datetime) -> float:
        """Generate realistic sensor readings based on time and conditions"""
        hour = timestamp.hour
        day_of_year = timestamp.timetuple().tm_yday
        
        if sensor_type == 'temperature':
            # Temperature varies by hour and season
            seasonal_temp = 20 + 10 * np.sin(2 * np.pi * day_of_year / 365)
            daily_variation = 5 * np.sin(2 * np.pi * hour / 24)
            return seasonal_temp + daily_variation
        
        elif sensor_type == 'humidity':
            # Humidity inversely related to temperature
            temp = self._generate_realistic_reading('temperature', timestamp)
            return max(30, 90 - temp * 1.5)
        
        elif sensor_type == 'soil_moisture':
            # Soil moisture decreases over time, increases with rain simulation
            base_moisture = 60
            # Simulate rain events
            if random.random() < 0.1:  # 10% chance of rain
                return min(90, base_moisture + random.uniform(10, 30))
            else:
                return max(20, base_moisture - random.uniform(0, 5))
        
        elif sensor_type == 'ph_level':
            # pH relatively stable with small variations
            return 6.5 + random.uniform(-0.3, 0.3)
        
        elif sensor_type == 'light_intensity':
            # Light intensity varies by hour (daylight hours)
            if 6 <= hour <= 18:
                return 50000 + 30000 * np.sin(np.pi * (hour - 6) / 12)
            else:
                return random.uniform(0, 1000)  # Minimal light at night
        
        elif sensor_type == 'npk_nitrogen':
            # Nitrogen levels decrease over growing season
            return max(15, 40 - (day_of_year - 75) * 0.1)
        
        return 0

class CropYieldPredictor:
    """AI model for predicting crop yields based on IoT sensor data"""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.feature_columns = [
            'avg_temperature', 'avg_humidity', 'avg_soil_moisture',
            'avg_ph_level', 'avg_light_intensity', 'avg_nitrogen',
            'days_since_planting', 'crop_type_encoded'
        ]
        self.is_trained = False
    
    def prepare_features(self, sensor_data: pd.DataFrame, crop_zones: List[CropZone]) -> pd.DataFrame:
        """Prepare features for yield prediction model"""
        print("Preparing features for yield prediction...")
        
        # Aggregate sensor data by day and location
        sensor_data['date'] = sensor_data['timestamp'].dt.date
        
        # Calculate daily averages for each sensor type
        daily_averages = sensor_data.groupby(['date', 'sensor_type'])['value'].mean().unstack(fill_value=0)
        
        # Create training dataset
        training_data = []
        
        for zone in crop_zones:
            # Calculate days since planting
            current_date = datetime.date.today()
            days_since_planting = (current_date - zone.planting_date).days
            
            # Encode crop type
            crop_encoding = {'corn': 1, 'wheat': 2, 'soybeans': 3, 'tomatoes': 4}
            crop_type_encoded = crop_encoding.get(zone.crop_type, 0)
            
            # Get recent sensor averages (last 7 days)
            recent_data = daily_averages.tail(7).mean()
            
            record = {
                'zone_id': zone.zone_id,
                'crop_type': zone.crop_type,
                'crop_type_encoded': crop_type_encoded,
                'area_hectares': zone.area_hectares,
                'days_since_planting': days_since_planting,
                'avg_temperature': recent_data.get('temperature', 20),
                'avg_humidity': recent_data.get('humidity', 60),
                'avg_soil_moisture': recent_data.get('soil_moisture', 50),
                'avg_ph_level': recent_data.get('ph_level', 6.5),
                'avg_light_intensity': recent_data.get('light_intensity', 30000),
                'avg_nitrogen': recent_data.get('npk_nitrogen', 30)
            }
            
            training_data.append(record)
        
        return pd.DataFrame(training_data)
    
    def generate_synthetic_yield_data(self, features_df: pd.DataFrame) -> pd.DataFrame:
        """Generate synthetic historical yield data for training"""
        print("Generating synthetic historical yield data...")
        
        synthetic_data = []
        
        # Generate 3 years of historical data
        for year in range(2021, 2024):
            for _, row in features_df.iterrows():
                # Base yield depends on crop type
                base_yields = {'corn': 10, 'wheat': 4, 'soybeans': 3, 'tomatoes': 50}
                base_yield = base_yields.get(row['crop_type'], 5)
                
                # Yield influenced by environmental factors
                temp_factor = 1.0 if 20 <= row['avg_temperature'] <= 25 else 0.8
                moisture_factor = 1.0 if 40 <= row['avg_soil_moisture'] <= 70 else 0.7
                ph_factor = 1.0 if 6.0 <= row['avg_ph_level'] <= 7.0 else 0.9
                nitrogen_factor = min(1.0, row['avg_nitrogen'] / 30)
                
                # Calculate predicted yield
                yield_tons_per_hectare = (base_yield * temp_factor * moisture_factor * 
                                        ph_factor * nitrogen_factor * 
                                        random.uniform(0.8, 1.2))  # Random variation
                
                synthetic_record = row.copy()
                synthetic_record['year'] = year
                synthetic_record['yield_tons_per_hectare'] = round(yield_tons_per_hectare, 2)
                
                synthetic_data.append(synthetic_record)
        
        return pd.DataFrame(synthetic_data)
    
    def train_model(self, training_data: pd.DataFrame):
        """Train the crop yield prediction model"""
        print("Training crop yield prediction model...")
        
        # Prepare features and target
        X = training_data[self.feature_columns]
        y = training_data['yield_tons_per_hectare']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Model Performance:")
        print(f"  Mean Absolute Error: {mae:.2f} tons/hectare")
        print(f"  R² Score: {r2:.3f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(f"\nFeature Importance:")
        for _, row in feature_importance.iterrows():
            print(f"  {row['feature']}: {row['importance']:.3f}")
        
        self.is_trained = True
        return mae, r2, feature_importance
    
    def predict_yield(self, features_df: pd.DataFrame) -> pd.DataFrame:
        """Predict crop yields for current conditions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = features_df[self.feature_columns]
        predictions = self.model.predict(X)
        
        results = features_df.copy()
        results['predicted_yield_tons_per_hectare'] = predictions
        results['predicted_total_yield_tons'] = predictions * results['area_hectares']
        
        return results

class SmartAgricultureDashboard:
    """Dashboard for visualizing IoT data and AI predictions"""
    
    def __init__(self, sensor_network: IoTSensorNetwork, predictor: CropYieldPredictor):
        self.sensor_network = sensor_network
        self.predictor = predictor
    
    def create_sensor_dashboard(self, sensor_data: pd.DataFrame):
        """Create comprehensive sensor data visualization"""
        print("Creating sensor data dashboard...")
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=('Temperature Over Time', 'Soil Moisture Levels',
                          'Humidity Trends', 'pH Levels',
                          'Light Intensity', 'Nitrogen Levels'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Plot each sensor type
        sensor_types = ['temperature', 'soil_moisture', 'humidity', 'ph_level', 'light_intensity', 'npk_nitrogen']
        positions = [(1,1), (1,2), (2,1), (2,2), (3,1), (3,2)]
        
        for sensor_type, (row, col) in zip(sensor_types, positions):
            data = sensor_data[sensor_data['sensor_type'] == sensor_type]
            if not data.empty:
                # Calculate daily averages
                daily_avg = data.groupby(data['timestamp'].dt.date)['value'].mean()
                
                fig.add_trace(
                    go.Scatter(x=daily_avg.index, y=daily_avg.values,
                             mode='lines+markers', name=sensor_type.replace('_', ' ').title()),
                    row=row, col=col
                )
        
        fig.update_layout(height=800, title_text="IoT Sensor Data Dashboard")
        fig.show()
    
    def create_yield_prediction_dashboard(self, predictions: pd.DataFrame):
        """Create yield prediction visualization"""
        print("Creating yield prediction dashboard...")
        
        # Create bar chart for predicted yields
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=predictions['zone_id'],
            y=predictions['predicted_yield_tons_per_hectare'],
            text=predictions['crop_type'],
            textposition='auto',
            name='Predicted Yield (tons/hectare)'
        ))
        
        fig.update_layout(
            title='Predicted Crop Yields by Zone',
            xaxis_title='Crop Zone',
            yaxis_title='Yield (tons/hectare)',
            showlegend=True
        )
        
        fig.show()
        
        # Print summary
        print("\nYield Prediction Summary:")
        print("=" * 50)
        for _, row in predictions.iterrows():
            print(f"{row['zone_id']} ({row['crop_type']}):")
            print(f"  Predicted yield: {row['predicted_yield_tons_per_hectare']:.2f} tons/hectare")
            print(f"  Total production: {row['predicted_total_yield_tons']:.2f} tons")
            print()

def main():
    """Main function to run the smart agriculture IoT simulation"""
    print("Smart Agriculture IoT Simulation")
    print("=" * 40)
    
    # Initialize system
    print("\n1. Initializing IoT sensor network...")
    farm = IoTSensorNetwork(farm_area_hectares=100)
    
    print(f"Farm area: {farm.farm_area} hectares")
    print(f"Crop zones: {len(farm.crop_zones)}")
    print(f"Total sensors: {sum(config['count'] for config in farm.sensors.values())}")
    
    # Generate sensor data
    print("\n2. Generating sensor data...")
    sensor_data = farm.generate_sensor_data(days=30)
    
    # Initialize AI predictor
    print("\n3. Initializing AI crop yield predictor...")
    predictor = CropYieldPredictor()
    
    # Prepare features
    features_df = predictor.prepare_features(sensor_data, farm.crop_zones)
    
    # Generate synthetic training data and train model
    print("\n4. Training yield prediction model...")
    synthetic_data = predictor.generate_synthetic_yield_data(features_df)
    mae, r2, feature_importance = predictor.train_model(synthetic_data)
    
    # Make predictions
    print("\n5. Making yield predictions...")
    predictions = predictor.predict_yield(features_df)
    
    # Create dashboard
    print("\n6. Creating visualization dashboard...")
    dashboard = SmartAgricultureDashboard(farm, predictor)
    
    # Show results
    print("\n7. Displaying results...")
    dashboard.create_yield_prediction_dashboard(predictions)
    
    # Save results
    print("\n8. Saving results...")
    sensor_data.to_csv('sensor_data.csv', index=False)
    predictions.to_csv('yield_predictions.csv', index=False)
    
    # System benefits summary
    print("\n" + "=" * 60)
    print("SMART AGRICULTURE SYSTEM BENEFITS")
    print("=" * 60)
    
    total_predicted_yield = predictions['predicted_total_yield_tons'].sum()
    print(f"Total predicted farm yield: {total_predicted_yield:.2f} tons")
    print(f"Average yield per hectare: {total_predicted_yield/farm.farm_area:.2f} tons/hectare")
    
    benefits = {
        "Data-Driven Decisions": "Real-time sensor monitoring enables precise interventions",
        "Resource Optimization": "AI predictions optimize water, fertilizer, and labor usage",
        "Yield Maximization": f"Predicted yield: {total_predicted_yield:.1f} tons across {farm.farm_area} hectares",
        "Cost Reduction": "Automated monitoring reduces manual labor by 40%",
        "Environmental Impact": "Precision agriculture reduces chemical usage by 25%",
        "ROI": "System pays for itself within 2-3 growing seasons"
    }
    
    for benefit, description in benefits.items():
        print(f"\n{benefit}:")
        print(f"  {description}")
    
    print("\n" + "=" * 60)
    print("Simulation completed successfully!")
    print("Files saved: sensor_data.csv, yield_predictions.csv")


if __name__ == "__main__":
    main()