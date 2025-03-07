import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the Data
# Replace 'vcdb_data.csv' with your actual data file path
df = pd.read_csv('vcdb_data.csv')

# Step 2: Clean the Data
# Drop rows with missing 'Attack Type' or 'Attack Method' for analysis
df = df.dropna(subset=['Attack Type', 'Attack Method'])

# Optionally, handle any other preprocessing based on your dataset (e.g., date conversion)
df['Breach Date'] = pd.to_datetime(df['Breach Date'], errors='coerce')
df = df.dropna(subset=['Breach Date'])

# Step 3: Group Data by Attack Type
# Grouping attack types by their occurrence
attack_type_counts = df['Attack Type'].value_counts()

# Step 4: Group Data by Year and Attack Method
# Extract the year from the 'Breach Date' column
df['Year'] = df['Breach Date'].dt.year

# Group by year and attack method to get the attack method trends over time
attack_method_trends = df.groupby(['Year', 'Attack Method']).size().unstack().fillna(0)

# Step 5: Visualize the Attack Patterns
# Plot the attack types frequency
plt.figure(figsize=(10,6))
attack_type_counts.plot(kind='bar', color='skyblue')
plt.title('Frequency of Attack Types')
plt.xlabel('Attack Type')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Plot the attack method trends over time (stacked area chart)
plt.figure(figsize=(12,6))
attack_method_trends.plot(kind='area', stacked=True, cmap='tab20')
plt.title('Attack Methods Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Attacks')
plt.legend(title='Attack Method', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 6: Heatmap of Attack Methods by Year and Industry
# Group data by year and industry to identify how attack methods are distributed across industries
industry_attack_method_trends = df.groupby(['Year', 'Industry', 'Attack Method']).size().unstack().unstack().fillna(0)

# Heatmap visualization (for a specific industry or top industries)
plt.figure(figsize=(12,8))
sns.heatmap(industry_attack_method_trends.loc[:, 'Retail'], cmap='YlGnBu', annot=True, fmt="d", linewidths=.5)
plt.title('Heatmap of Attack Methods in the Retail Industry')
plt.xlabel('Attack Method')
plt.ylabel('Year')
plt.show()
