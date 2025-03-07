import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the Data
df = pd.read_csv('vcdb_data.csv')  # Replace with the actual path to your dataset

# Step 2: Clean the Data
# Clean any missing values for columns related to impact analysis
df = df.dropna(subset=['Number of Records Exposed', 'Financial Impact'])

# Convert 'Breach Date' to datetime
df['Breach Date'] = pd.to_datetime(df['Breach Date'], errors='coerce')

# Step 3: Analyze the Impact

# 3.1: Quantify the Scale of Breaches
# Group by industry and sum the number of records exposed
industry_breach_scale = df.groupby('Industry')['Number of Records Exposed'].sum().sort_values(ascending=False)

# 3.2: Financial Impact of Breaches
# Group by industry and sum the financial losses
industry_financial_impact = df.groupby('Industry')['Financial Impact'].sum().sort_values(ascending=False)

# 3.3: Impact Over Time
# Group by year and sum the number of records exposed (or financial impact)
df['Year'] = df['Breach Date'].dt.year
impact_over_time = df.groupby('Year')['Number of Records Exposed'].sum()

# Step 4: Visualize the Results

# 4.1: Plot the Scale of Breaches by Industry
plt.figure(figsize=(12, 8))
industry_breach_scale.head(10).plot(kind='barh', color='lightblue')
plt.title('Top 10 Industries by Number of Records Exposed')
plt.xlabel('Number of Records Exposed')
plt.ylabel('Industry')
plt.grid(True)
plt.show()

# 4.2: Plot the Financial Impact by Industry
plt.figure(figsize=(12, 8))
industry_financial_impact.head(10).plot(kind='barh', color='lightcoral')
plt.title('Top 10 Industries by Financial Impact')
plt.xlabel('Financial Impact (in millions)')
plt.ylabel('Industry')
plt.grid(True)
plt.show()

# 4.3: Plot the Total Number of Records Exposed Over Time
plt.figure(figsize=(10, 6))
plt.plot(impact_over_time.index, impact_over_time.values, marker='o', color='green')
plt.title('Total Number of Records Exposed Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Records Exposed')
plt.grid(True)
plt.show()
