import csv
import re

with open('FIFA17_official_data.csv', 'r') as f:
    all_rows = csv.DictReader(f)
    data_rows = [x for x in all_rows]

for row in data_rows:
    del row['Photo']
    del row['Flag']
    del row['Club Logo']

    row['Position'] = re.sub(r"<.+>", "", row['Position'])

    row['Name'] = re.sub(r"[0-9]", "", row['Name'])
    row['Name'] = re.sub(r"^ ", "", row['Name'])
    row['Name'] = re.sub(r"\xa0", "", row['Name'])

with open('fifa17-players-cleaned.csv', 'w') as f:
    fieldnames = ['ID','Name','Age','Nationality','Overall','Potential','Club','Value','Wage','Special','Preferred Foot','International Reputation','Weak Foot','Skill Moves','Work Rate','Body Type','Real Face','Position','Jersey Number','Joined','Loaned From','Contract Valid Until','Height','Weight','Crossing','Finishing','HeadingAccuracy','ShortPassing','Volleys','Dribbling','Curve','FKAccuracy','LongPassing','BallControl','Acceleration','SprintSpeed','Agility','Reactions','Balance','ShotPower','Jumping','Stamina','Strength','LongShots','Aggression','Interceptions','Positioning','Vision','Penalties','Composure','Marking','StandingTackle','SlidingTackle','GKDiving','GKHandling','GKKicking','GKPositioning','GKReflexes','Best Position','Best Overall Rating','Release Clause','DefensiveAwareness']
    write_f = csv.DictWriter(f, fieldnames=fieldnames)
    write_f.writeheader()
    write_f.writerows(data_rows)