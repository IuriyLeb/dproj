import pandas as pd
from datetime import datetime as dt, timedelta as td
from dotabuff_update import update_database_from_dotabuff


with open('./update_time.txt', 'r') as file:
    for line in file:
        importing_date = line.strip()
date_to_update = dt.strptime(importing_date, '%Y, %m, %d -- %H:%M')
date_now = dt.today()
if date_now >= date_to_update:
    print('Updating...')
    dota_stats = update_database_from_dotabuff()
    date_to_update = date_now + td(days=10)
    print(dt.strftime(date_to_update, 'Next update at %d.%m.%Y'))
    with open('./update_time.txt', 'w') as file:
        file.write(dt.strftime(date_to_update, '%Y, %m, %d -- %H:%M'))
else:
    dota_stats = pd.read_csv('./stats_dotabuff.csv', index_col=0)

hero = input('Choose a hero:')
ind = dota_stats[dota_stats['localized_name'] == hero].index[0]
good_against = '\n\t'.join(dota_stats.at[ind, 'good_against'])
bad_against = '\n\t'.join(dota_stats.at[ind, 'bad_against'])
print('Good against:\n\t{}\nBad against:\n\t{}'.format(good_against, bad_against))
# TODO add functions
# TODO classes?
# TODO pick-helper
# TODO heroes pick priority
# TODO try block in team choosing
my_team = []
enemy_team = []
suggest_pick = dict.fromkeys(list(dota_stats['localized_name']), 0)
while True:
    temp_pick = input('Pick a hero:')
    des = input('This hero in your team?(0-n, 1-y)')
    if des == '1':
        my_team.append(temp_pick)
    elif des == '0':
        enemy_team.append(temp_pick)
    elif des == 'q':
        break
    for hero in enemy_team:
        ind = dota_stats[dota_stats['localized_name'] == hero].index[0]
        bad_against = dota_stats.at[ind, 'bad_against']
        for enemy in bad_against:
            suggest_pick[enemy] += 1
    print(suggest_pick)
print(suggest_pick)