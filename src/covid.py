import os
from requests import Request, Session, packages
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from dataclasses import dataclass
from datetime import datetime as dTime
import pytz, calendar
from dataclasses import field
from typing import Dict
from src import postgres
from src import log
from typing import List, Set
import configparser
import pandas as pd
from IPython.display import display

tz_pac_str = 'America/Los_Angeles'
tz_pac = pytz.timezone('America/Los_Angeles')  # replace with your local timezone

@dataclass
class Covid(object):
    epi_data_url: str = ''
    va_data_url: str = ''
    mit_data_url: str = ''

    def __post_init__(self):
        self.log = log.logg()
        if os.name == 'nt':
            # Am on laptop or PC?
            parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
            self.ini_file = os.path.join(parent_dir, 'unifi.ini')
        else:
            self.ini_file = '/home/user/user.ini'
        config = configparser.ConfigParser()
        config.read(self.ini_file)
        self.user = config['covid']['user']
        self.password = config['covid']['password']
        self.pg = postgres.Postgres()

    def predict_data(self):
        # Predictions
        dates = ['2020-06-10', '2020-06-17', '2020-07-17', '2020-08-15']
        rows = []
        for date in dates:
            out = "Predictions for spreadsheet/report for " + date
            print(out)
            rows.append([out])
            headers = ['county', 'total cases', 'new cases', 'Total deaths', 'new deaths', 'Deaths PM']
            print(chr(9).join(headers))
            rows.append(headers)
            sql = """SELECT s.county,total,new,death,new_death,(death*1.00/population*1.00)*1000000 "
                       FROM stat_nc s,pop_nc p "
                      WHERE s.county=p.county AND s.catch=1 AND stat_date='" + date + "' ORDER BY 1,2 """
            for row in self.pg.get_rows(sql):
                rows.append(row)
                for cel in row:
                    print(cel, end=chr(9))
                print('')

            out = "Catchment totals"
            print(out)
            rows.append([out])
            sql = """SELECT 'Catchment Total',sum(total),sum(new),sum(death),sum(new_death),(sum(death*1.00)/sum(population*1.00))*1000000 "
                       FROM stat_nc s,pop_nc p "
                      WHERE s.county=p.county AND s.catch=1 AND stat_date='" + date + "' ORDER BY 1,2 """
            for row in self.pg.get_rows(sql):
                rows.append(row)
                for cel in row:
                    print(cel, end=chr(9))
                print('')

            out = "Non Catchment totals"
            print(out)
            rows.append([out])
            sql = """SELECT 'Non Catchment Total',sum(total),sum(new),sum(death),sum(new_death),(sum(death*1.00)/sum(population*1.00))*1000000 "
                       FROM stat_nc s,pop_nc p "
                      WHERE s.county=p.county AND s.catch=0 AND stat_date='" + date + "' ORDER BY 1,2 """
            for row in self.pg.get_rows(sql):
                rows.append(row)
                for cel in row:
                    print(cel, end=chr(9))
                print('')

        df = pd.DataFrame(rows)
        display(df)
