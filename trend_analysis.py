import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the Data
# Replace 'vcdb_data.csv' with the path to your actual CSV file
df = pd.read_csv('/home/ohmkar/Downloads/vcdb.csv')

# Step 2: Clean the Data
# Let's assume we need to convert dates and filter out irrelevant columns
df['Breach Date'] = pd.to_datetime(df['Breach Date'], errors='coerce')

# Drop rows with invalid or missing dates
df = df.dropna(subset=['Breach Date'])

# Filter relevant columns (e.g., 'Breach Date', 'Breach Type', 'Industry', 'Vulnerabilities')
df = df[['Breach Date', 'Breach Type', 'Industry', 'Vulnerabilities']]

df = df[['timeline.incident.year','pattern','victim.industry.name']]

# Step 3: Trend Analysis - Count the number of breaches over time
# Group the data by year and count breaches
df['Year'] = df['Breach Date'].dt.year
breaches_per_year = df.groupby('Year').size()

# Step 4: Plot the Trend Over Time
plt.figure(figsize=(10,6))
plt.plot(breaches_per_year.index, breaches_per_year.values, marker='o')
plt.title('Number of Breaches Per Year')
plt.xlabel('Year')
plt.ylabel('Number of Breaches')
plt.grid(True)
plt.show()

# Step 5: Trend Analysis - Common Breach Types over Time
# Group by year and breach type to count occurrences
breach_type_trends = df.groupby(['Year', 'Breach Type']).size().unstack()

# Plot the breach type trends over time
breach_type_trends.plot(kind='area', stacked=True, figsize=(10,6), colormap='tab20')
plt.title('Breach Types Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Breaches')
plt.legend(title='Breach Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()

# Step 6: Analyzing Vulnerabilities Exploited
# Let's see which vulnerabilities were most common over time
vulnerabilities_trends = df.groupby(['Year', 'Vulnerabilities']).size().unstack()

# Plot vulnerabilities trends (top 10 most frequent)
top_vulnerabilities = vulnerabilities_trends.sum(axis=0).nlargest(10).index
vulnerabilities_trends[top_vulnerabilities].plot(kind='line', figsize=(12,6))
plt.title('Top 10 Vulnerabilities Exploited Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Breaches')
plt.legend(title='Vulnerabilities')
plt.grid(True)
plt.show()

# Optional: Heatmap of breaches across years and industries
industry_yearly_trends = df.groupby(['Year', 'Industry']).size().unstack()
plt.figure(figsize=(12,8))
sns.heatmap(industry_yearly_trends, cmap='YlGnBu', annot=True, fmt="d", linewidths=.5)
plt.title('Heatmap of Breaches by Industry and Year')
plt.xlabel('Industry')
plt.ylabel('Year')
plt.show()

