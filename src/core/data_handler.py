import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

class DataHandler:
    def __init__(self):
        self.data = None
        self.available_indicators = None
        self.load_data()

    def load_data(self):
        """Load and preprocess the economic data"""
        try:
            # Read the KNN-filled CSV file with explicit encoding and error handling
            file_path = 'attached_assets/economic_data_filled_knn (1).csv'
            self.data = pd.read_csv(file_path, encoding='utf-8')
            
            # Print column names for debugging
            print("Available columns:", self.data.columns.tolist())
            
            # Create Date column for visualization
            self.data['Date'] = self.data.apply(lambda row: f"{int(row['Year'])}-{int(row['Month']):02d}", axis=1)
            
            # Also create a YearMonth column for easier filtering
            self.data['YearMonth'] = self.data.apply(lambda row: f"{int(row['Year'])}-{int(row['Month']):02d}", axis=1)
            
            # Get available indicators (all columns except Year, Month, Date, YearMonth)
            self.available_indicators = [col for col in self.data.columns if col not in ['Year', 'Month', 'Date', 'YearMonth']]
            
            print("Data loaded successfully")
            print(f"Available indicators: {self.available_indicators}")
            print(f"Data shape: {self.data.shape}")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            print(f"Current working directory: {os.getcwd()}")
            self.data = pd.DataFrame()
            self.available_indicators = []

    def get_available_indicators(self):
        """Get list of available economic indicators"""
        if self.data is None or self.data.empty:
            return []
        return [col for col in self.data.columns if col not in ['Year', 'Month', 'Date', 'YearMonth']]

    def get_date_range(self):
        """Get the date range of the data"""
        if self.data is None or self.data.empty or 'Date' not in self.data.columns:
            return None, None
        return self.data['Date'].min(), self.data['Date'].max()

    def filter_data(self, start_year=None, end_year=None, indicators=None):
        """Filter data by year range and indicators"""
        if self.data is None or self.data.empty:
            return pd.DataFrame()

        filtered_data = self.data.copy()

        if start_year:
            filtered_data = filtered_data[filtered_data['Year'] >= start_year]
        if end_year:
            filtered_data = filtered_data[filtered_data['Year'] <= end_year]
        if indicators:
            # Always include Year, Month, Date and YearMonth columns
            cols_to_include = ['Year', 'Month', 'Date', 'YearMonth'] + indicators
            filtered_data = filtered_data[cols_to_include]

        return filtered_data

    def create_correlation_data(self, indicators=None):
        """Calculate correlation matrix for selected indicators"""
        if not indicators or len(indicators) < 2:
            return pd.DataFrame()

        data_subset = self.data[indicators]
        corr_matrix = data_subset.corr()
        return corr_matrix

    def get_seasonal_data(self, indicator):
        """Get seasonal analysis data for an indicator"""
        if not indicator or indicator not in self.available_indicators:
            return pd.DataFrame()

        monthly_avg = self.data.groupby('Month')[indicator].mean().reset_index()
        monthly_std = self.data.groupby('Month')[indicator].std().reset_index()[indicator]
        monthly_avg['std'] = monthly_std
        return monthly_avg

    def to_json(self, data):
        """Convert data to JSON format"""
        if isinstance(data, pd.DataFrame):
            return data.to_json(orient='records', date_format='iso')
        elif isinstance(data, pd.Series):
            return data.to_json()
        return json.dumps(data)

    def get_indicator_stats(self, indicator):
        """Get statistical information about an indicator"""
        if not indicator or indicator not in self.available_indicators:
            return {}

        stats = {
            'mean': float(self.data[indicator].mean()),
            'median': float(self.data[indicator].median()),
            'std': float(self.data[indicator].std()),
            'min': float(self.data[indicator].min()),
            'max': float(self.data[indicator].max()),
            'current': float(self.data[indicator].iloc[-1]),
            'previous': float(self.data[indicator].iloc[-2]),
            'change': float(self.data[indicator].iloc[-1] - self.data[indicator].iloc[-2]),
            # Add percentiles
            'percentile_25': float(self.data[indicator].quantile(0.25)),
            'percentile_50': float(self.data[indicator].quantile(0.50)),
            'percentile_75': float(self.data[indicator].quantile(0.75))
        }
        return stats

    def get_trend_analysis(self, indicator, window=12):
        """Analyze trend for an indicator"""
        if not indicator or indicator not in self.available_indicators:
            return pd.DataFrame()

        df = self.data.copy()
        df['MA'] = df[indicator].rolling(window=window).mean()
        df['Trend'] = np.where(df['MA'] > df['MA'].shift(1), 'Increasing', 'Decreasing')
        return df[['Year', 'Month', 'Date', indicator, 'MA', 'Trend']].dropna()
    
    def get_yearly_summary(self, indicator):
        """Get yearly summary statistics for an indicator"""
        if not indicator or indicator not in self.available_indicators:
            return pd.DataFrame()
        
        yearly_data = self.data.groupby('Year')[indicator].agg(['mean', 'min', 'max', 'std']).reset_index()
        return yearly_data
    
    def get_related_indicators(self, indicator, threshold=0.7):
        """Get indicators that are highly correlated with the given indicator"""
        if not indicator or indicator not in self.available_indicators:
            return []
        
        # Calculate correlation with all other indicators
        correlations = self.data[self.available_indicators].corr()[indicator]
        
        # Filter correlations above threshold (absolute value)
        related = correlations[abs(correlations) > threshold]
        
        # Exclude the indicator itself
        related = related[related.index != indicator]
        
        # Return as a dictionary with indicator names and correlation values
        return related.to_dict()

# Initialize global data handler
data_handler = DataHandler() 