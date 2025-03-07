import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

# Step 1: Load the Data
# Replace 'vcdb_data.csv' with the path to your actual CSV file
# df = pd.read_csv('/home/ohmkar/Downloads/vcdb.csv')
# Directory containing JSON files
json_dir = 'C:/Users/sudharshan.acharya/Downloads/VCDB-master/VCDB-master/data/json/validated/'

# Read all JSON files in the directory and concatenate them into a single DataFrame
json_files = [f for f in os.listdir(json_dir) if f.lower().endswith('.json')]
df_list = []

COLUMN_BREACH_YEAR = 'timeline.incident.year'
COLUMN_BREACH_TYPE = 'new_breach_type'
COLUMN_INDUSTRY = 'victim.industry'
COLUMN_VULNERABILITY = 'new_vulnerabilities'

def transformJson(jsonData:dict):
    # jsonData['action'] = jsonData['action'].keys()
    jsonData[COLUMN_BREACH_TYPE] = list(jsonData['action'].keys())
    jsonData[COLUMN_VULNERABILITY] = []

    try:
        for type in jsonData['action'].keys():
            if 'vector' in jsonData['action'][type].keys():
                if isinstance(jsonData['action'][type]['vector'], list):
                    jsonData[COLUMN_VULNERABILITY].extend(jsonData['action'][type]['vector'])
                else:
                    jsonData[COLUMN_VULNERABILITY].append(jsonData['action'][type]['vector'])

                # print(f"\r Vulnerability list : {jsonData[COLUMN_VULNERABILITY]}")

        industry_value = jsonData['victim']['industry']
        try:
            industry_value = int(industry_value)
            while industry_value >= 100:
                industry_value //= 100
            jsonData['victim']['industry'] = industry_value
        except ValueError:
            print(f"\nSkipping non-integer industry value: {industry_value}")

    except KeyError as e:
        print(f"KeyError: {e} ")

    return jsonData

FROM_PREPROCESSED_FILE = True

if not FROM_PREPROCESSED_FILE:
    for file in json_files:
        with open(os.path.join(json_dir, file), 'r') as f:
            data = json.load(f)
            data = transformJson(data)
            df_list.append(pd.json_normalize(data))

    df = pd.concat(df_list, ignore_index=True)

    # Save the preprocessed DataFrame to a CSV file

    preprocessed_file_path = 'preprocessed_vcdb_data.csv'
    print(f'saving the processed json to csv file.')
    df.to_csv(preprocessed_file_path, index=False)

if FROM_PREPROCESSED_FILE:
    preprocessed_file_path = 'preprocessed_vcdb_data.csv'
    df = pd.read_csv(preprocessed_file_path)


# Step 2: Clean the Data
# Let's assume we need to convert dates and filter out irrelevant columns
df[COLUMN_BREACH_YEAR] = pd.to_datetime(df[COLUMN_BREACH_YEAR], format='%Y', errors='coerce')


# Drop rows with invalid or missing dates
df = df.dropna(subset=[COLUMN_BREACH_YEAR])


# Filter relevant columns (e.g., 'Breach Date', 'Breach Type', 'Industry', 'Vulnerabilities')
# df = df[['Breach Date', 'Breach Type', 'Industry', 'Vulnerabilities']]

df = df[[COLUMN_BREACH_YEAR, COLUMN_BREACH_TYPE, COLUMN_INDUSTRY, COLUMN_VULNERABILITY]]

print(df[COLUMN_BREACH_YEAR].unique())

# Step 3: Trend Analysis - Count the number of breaches over time
# Group the data by year and count breaches
df['Year'] = df[COLUMN_BREACH_YEAR].dt.year
breaches_per_year = df.groupby('Year').size()

if True:
    # Step 4: Plot the Trend Over Time
    plt.figure(figsize=(10,6))
    plt.plot(breaches_per_year.index, breaches_per_year.values, marker='o')
    plt.title('Number of Breaches Per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Breaches')
    # plt.xticks(breaches_per_year.index)  # Ensure x-axis values iterate in 1 year
    plt.grid(True)
    # plt.xlim(left=1995)  # Start x-axis from 1995
    plt.show()


# def breach_type_ranking():



if True:
    # Step 5: Trend Analysis - Common Breach Types over Time
    # Group by year and breach type to count occurrences
    breach_type_trends = df.groupby(['Year', COLUMN_BREACH_TYPE]).size()
    print(breach_type_trends)
    breach_type_trends = df.groupby(['Year', COLUMN_BREACH_TYPE]).size().unstack()
    print(breach_type_trends)

    # Plot the breach type trends over time    
    breach_type_trends.plot(kind='area', stacked=True, figsize=(10,6), colormap='tab20')
    plt.title('Breach Types Over Time')
    plt.xlabel('Year')
    plt.ylabel('Number of Breaches')
    plt.xlim(left=2000)
    plt.legend(title=COLUMN_BREACH_TYPE, bbox_to_anchor=(1.2, 1), loc='upper right', fontsize='x-small')
    plt.grid(True)
    # plt.subplots_adjust(left=0.05, right=0.95)
    plt.show()


# Step 6: Analyzing Vulnerabilities Exploited
# Let's see which vulnerabilities were most common over time
vulnerabilities_trends = df.groupby(['Year', COLUMN_VULNERABILITY]).size().unstack()

# Plot vulnerabilities trends (top 10 most frequent)
top_vulnerabilities = vulnerabilities_trends.sum(axis=0).nlargest(10).index
vulnerabilities_trends[top_vulnerabilities].plot(kind='line', figsize=(12,6))
plt.title('Top 10 Vulnerabilities Exploited Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Breaches')
plt.legend(title='Vulnerabilities')
plt.grid(True)
plt.show()


print('existing..')
exit()

# Optional: Heatmap of breaches across years and industries
industry_yearly_trends = df.groupby(['Year', 'Industry']).size().unstack()
plt.figure(figsize=(12,8))
sns.heatmap(industry_yearly_trends, cmap='YlGnBu', annot=True, fmt="d", linewidths=.5)
plt.title('Heatmap of Breaches by Industry and Year')
plt.xlabel('Industry')
plt.ylabel('Year')
plt.show()

