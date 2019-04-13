import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime as dt, timedelta as td
import requests


def update_database_from_dotabuff():

    dota_stats = pd.read_csv('./dota_hero_stats.csv', index_col=0)

    bad_dict, good_dict = {}, {}
    for hero_name in dota_stats.localized_name:
        bad_against, good_against = [], []
        alt_hero_name = hero_name.lower().replace(' ', '-').replace("'", '')
        dotabuff_request = requests.get('https://www.dotabuff.com/heroes/{}/counters'.format(alt_hero_name),
                                        headers={'User-agent': 'test'})
        if dotabuff_request.status_code != 200:
            print(f'{hero_name} is broken.')
            continue
        html_text = BeautifulSoup(dotabuff_request.text, "lxml")
        counter_table = html_text.find_all('section', {'class': 'counter-outline'})
        counter_table = str(counter_table).split('"')
        for element in counter_table:
            if element[0].isupper() and len(element) < 20:
                if element not in bad_against and len(bad_against) < 5:
                    bad_against.append(element)
                elif element not in good_against and element not in bad_against:
                    good_against.append(element)
        bad_dict[hero_name] = bad_against
        good_dict[hero_name] = good_against
    print('Done')

    dota_stats['bad_against'] = None
    dota_stats['good_against'] = None

    for hero in bad_dict:
        ind = dota_stats[dota_stats['localized_name'] == hero].index[0]
        dota_stats.at[ind, 'bad_against'] = bad_dict[hero]
        dota_stats.at[ind, 'good_against'] = good_dict[hero]

    dota_stats.to_csv('./stats_dotabuff.csv')
    return dota_stats