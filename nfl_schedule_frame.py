import pandas as pd

# Load the NFL schedule and scores from a CSV file
# Make sure to adjust the file path
df = pd.read_csv("nfl_schedule_scores.csv")

# Display the first few rows of the dataframe
print("Initial DataFrame:")
print(df.head())

# Step 1: Convert date columns to datetime format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Step 2: Create new columns for Year, Month, and Weekday
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Weekday'] = df['Date'].dt.day_name()

# Step 3: Create a 'Week' column from the 'GameWeek' or 'Week' column (if available)
if 'Week' not in df.columns:
    df['Week'] = (df.index // 16) + 1

# Step 4: Clean up team names (if necessary)
df['HomeTeam'] = df['HomeTeam'].str.strip()
df['AwayTeam'] = df['AwayTeam'].str.strip()

# Step 5: Create a 'Result' column to indicate home team win/loss
# Assuming 'HomeScore' and 'AwayScore' columns exist
df['Result'] = df.apply(lambda row: 'Win' if row['HomeScore'] > row['AwayScore'] else 'Loss', axis=1)

# Step 6: Calculate point difference
df['PointDifference'] = df['HomeScore'] - df['AwayScore']

# Step 7: Filter data for a specific team
team_name = 'Kansas City Chiefs'  # Change this to any team you want
team_games = df[(df['HomeTeam'] == team_name) | (df['AwayTeam'] == team_name)]

# Step 8: Calculate win/loss record for the specific team
team_wins = team_games[(team_games['HomeTeam'] == team_name) & (team_games['Result'] == 'Win')].shape[0]
team_losses = team_games.shape[0] - team_wins

# Display the filtered data
print(f"\n{team_name} Games:")
print(team_games)

print(f"\n{team_name} Record: {team_wins} Wins, {team_losses} Losses")

# Optional: Save the cleaned data to a new CSV file
df.to_csv("cleaned_nfl_schedule_scores.csv", index=False)
