import pandas as pd

# Step 1: Load the Data
# Replace 'vcdb_data.csv' with the actual path to your dataset
df = pd.read_csv('vcdb_data.csv')

# Step 2: Clean the Data
# Ensure 'Vulnerabilities' column is properly formatted and handle missing values
df = df.dropna(subset=['Vulnerabilities'])  # Drop rows where 'Vulnerabilities' is missing

# Step 3: Count the Occurrences of Each Vulnerability
# We can split the 'Vulnerabilities' column if it contains multiple vulnerabilities (e.g., comma-separated)
# Let's assume the vulnerabilities are stored in a single column as text (comma-separated)

# Step 3.1: Split vulnerabilities if they are in a comma-separated format
vulnerabilities = df['Vulnerabilities'].str.split(',', expand=True).stack()

# Step 3.2: Clean the extracted vulnerabilities (strip spaces and convert to lowercase)
vulnerabilities = vulnerabilities.str.strip().str.lower()

# Step 3.3: Count the most common vulnerabilities
vulnerability_counts = vulnerabilities.value_counts()

# Step 4: Display the Most Common Vulnerabilities
print("Most Common Vulnerabilities:")
print(vulnerability_counts.head(10))  # Display top 10 most common vulnerabilities
