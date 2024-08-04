import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

# Load the merged dataset
merged_data = pd.read_csv(r'C:\Users\Nikos\Desktop\thesis\Paper\Data\merged_data.csv')

# Prepare the data for linear regression
X = merged_data['Clear Sky GHI'].values.reshape(-1, 1)
y = merged_data['Lux Value'].values

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
plt.scatter(merged_data['Clear Sky GHI'], merged_data['Lux Value'], alpha=0.5, label='Data points')
plt.plot(merged_data['Clear Sky GHI'], y_pred, color='red', label='Linear fit')
plt.title(f'Linear Regression of Lux Value vs. Clear Sky GHI\n{linear_function}\nR: {r:.2f}, R²: {r2:.2f}, MAE: {mae:.2f}, RMSE: {rmse:.2f}', fontsize=25)
plt.xlabel('Clear Sky GHI (W/m²)')
plt.ylabel('Lux Value (hsv)')
plt.legend()
plt.grid(True)
plt.show()

r, r2, mae, rmse

