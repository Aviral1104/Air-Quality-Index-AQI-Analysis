#Air Quality Index (AQI) Analysis

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\Users\avi11\Downloads\AQI and Lat Long of Countries.csv\AQI and Lat Long of Countries.csv")

print("Column names:")
print(df.columns.tolist())

print("\nFirst few rows of the dataset:")
print(df.head())

# GeoDataFrame
gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.lng, df.lat), crs="EPSG:4326"
)

# specific AQI parameter
def create_aqi_map(parameter):
    column_name = f'{parameter} Value' if f'{parameter} Value' in gdf.columns else parameter
    fig, ax = plt.subplots(figsize=(12, 8))
    scatter = ax.scatter(gdf.geometry.x, gdf.geometry.y, c=gdf[column_name], cmap='YlOrRd', s=50)
    plt.colorbar(scatter, label=column_name)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title(f'Spatial Distribution of {parameter}')
    for idx, row in gdf.iterrows():
        ax.annotate(f"{row[column_name]:.0f}", 
                    (row.geometry.x, row.geometry.y), 
                    xytext=(3, 3), 
                    textcoords="offset points", 
                    fontsize=8)
    plt.savefig(f'{parameter.lower().replace(" ", "_")}_map.png', dpi=300, bbox_inches='tight')
    plt.close()

# maps for each AQI parameter
aqi_params = [col for col in df.columns if 'AQI' in col and 'Category' not in col]
for param in aqi_params:
    create_aqi_map(param)

# statistics for each AQI parameter
stats = gdf[aqi_params].agg(['mean', 'min', 'max', 'std'])
print("\nStatistics for AQI parameters:")
print(stats)

# Correlation analysis
correlation_matrix = gdf[aqi_params + ['lat', 'lng']].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix of AQI Parameters and Coordinates')
plt.savefig('aqi_correlation_matrix.png', dpi=300, bbox_inches='tight')
plt.close()

# Top 10 cities with highest overall AQI
overall_aqi_column = 'AQI Value' if 'AQI Value' in gdf.columns else aqi_params[0]
top_10_aqi = gdf.nlargest(10, overall_aqi_column)[['Country', 'City', overall_aqi_column]]
print("\nTop 10 cities with highest AQI:")
print(top_10_aqi)

# Distribution of AQI categories
category_column = [col for col in df.columns if 'AQI Category' in col][0]
category_counts = gdf[category_column].value_counts()
plt.figure(figsize=(10, 6))
category_counts.plot(kind='bar')
plt.title('Distribution of AQI Categories')
plt.xlabel('AQI Category')
plt.ylabel('Number of Cities')
plt.savefig('aqi_category_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

print("\nAnalysis complete. Check the generated PNG files for visualizations.")
