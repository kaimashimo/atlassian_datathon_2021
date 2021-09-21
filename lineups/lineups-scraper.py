from bs4 import BeautifulSoup as bs
import requests
import re
import csv

def get_page(country):
    page = requests.get(f'https://en.wikipedia.org/wiki/{country}_national_soccer_team')
    if page.status_code == 200:
        return page
    
    page = requests.get(f'https://en.wikipedia.org/wiki/{country}_national_football_team')
    if page.status_code == 200:
        return page
    
    return False

def get_players(country):
    print(f'Getting players for {country}')

    country = country.replace(' ', '_')
    page = get_page(country)
    if not page:
        print('Error when retrieving page')
        return False
    
    soup = bs(page.content, 'html.parser')

    # Get the first table after "Current squad" heading
    squad_heading = soup.find(lambda x: x.name in ['h2', 'h3'] and x.text.startswith('Current squad'))
    if not squad_heading:
        print('Cannot find current squad')
        return False
    squad_table = squad_heading.find_next_sibling('table')
    squad_table_body = squad_table.find('tbody')
    
    # Get the rows of the table and add data to all_players
    rows = squad_table_body.find_all('tr')
    all_players = []
    for row in rows:
        cols = row.find_all(['td', 'th'])
        cols = [c.text.strip() for c in cols]

        if len(cols) < 2:
            continue
        if len(cols) != 7:
            print('Unexpected number of columns')
            continue
        # skip header
        if cols[0] == 'No.':
            continue
        
        # Remove number from position
        cols[1] = re.sub(r"[0-9]", "", cols[1])

        age_cell = cols[3]
        # Extract age
        try:
            age = re.search(r"\xa0([0-9]+)", age_cell).group(1)
            cols[3] = age
        except:
            cols[3] = age_cell
            print('Match failed')

        # Extract birthday
        try:
            birthday = re.search(r"([0-9]{4}-[0-9]{2}-[0-9]{2})", age_cell).group()
            cols = cols[:3] + [birthday] + cols[3:]
        except:
            cols = cols[:3] + [age_cell] + cols[3:]
            print('Match failed')

        all_players.append(cols)
    
    return all_players


def create_players_csv(country, dir='teams'):
    all_players = get_players(country)
    if not all_players:
        return False

    country_basename = country.replace(' ', '-').lower()
    with open(f'{dir}/{country_basename}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['No.', 'Position', 'Player', 'DOB', 'Current age', 'Caps', 'Goals', 'Club'])
        writer.writerows(all_players)

    return True
    
if __name__ == '__main__':
    failed = []
    with open('all-countries.txt', 'r') as f:
        for line in f.readlines():
            country = line.strip()
            if not create_players_csv(country):
                failed.append(country)

    with open('fail-logs.txt', 'w') as f:
        print('\n'.join(failed), file=f)
