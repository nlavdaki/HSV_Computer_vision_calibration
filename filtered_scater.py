import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

# Load the merged dataset
file_path = r'C:\Users\Nikos\Desktop\thesis\Paper\Data\merged_data.csv'
merged_data = pd.read_csv(file_path)

# Convert the 'Timestamp' column to datetime
merged_data['Timestamp'] = pd.to_datetime(merged_data['Timestamp'])

# Filter out values based on the time of the day
start_time = pd.to_datetime('10:00:00').time()
end_time = pd.to_datetime('14:30:00').time()

filtered_data = merged_data[(merged_data['Timestamp'].dt.time >= start_time) & (merged_data['Timestamp'].dt.time <= end_time)]

# Prepare the data for linear regression
X = filtered_data['Clear Sky GHI'].values.reshape(-1, 1)
y = filtered_data['Lux Value'].values

# Create and fit the model
model = LinearRegression()
model.fit(X, y)

# Make predictions
y_pred = model.predict(X)

# Calculate statistics
r2 = r2_score(y, y_pred)
r = np.sqrt(r2)
mae = mean_absolute_error(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))

# Extract the coefficients
slope = model.coef_[0]
intercept = model.intercept_
linear_function = f"y = {slope:.2f}x + {intercept:.2f}"

# Print the linear function
print(f"Linear function: {linear_function}")

# Plot the results
plt.figure(figsize=(10, 6))
plt.scatter(filtered_data['Clear Sky GHI'], filtered_data['Lux Value'], alpha=0.5, label='Data points')
plt.plot(filtered_data['Clear Sky GHI'], y_pred, color='red', label='Linear fit')
plt.title(f'Linear Regression of Lux Value vs. Clear Sky GHI Filtered: {start_time}-{end_time}\n{linear_function}\nR: {r:.2f}, R²: {r2:.2f}, MAE: {mae:.2f}, RMSE: {rmse:.2f}')
plt.xlabel('Clear Sky GHI (W/m²)')
plt.ylabel('Lux Value (hsv)')
plt.legend()
plt.grid(True)
plt.show()

r, r2, mae, rmse
