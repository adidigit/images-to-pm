import json
import pandas

class PM_Data:
    def __init__(self, file):
        self.pm_file = file

    def load(self, pollutant_standard = 'PM25 24-hour 2012' ):
        with open(self.pm_file) as f:
            pm_data =json.load(f)['Data']
            pm_data_daily = pandas.DataFrame(pm_data)
            #  take only 1 measurement - daily. according to a specific standard that all station has
            pm_daily_clean = pm_data_daily.loc[(pm_data_daily['pollutant_standard']== pollutant_standard)]# & (pm_data_daily['date_local'] =='2021-01-21')][['site_number','date_local']]
            return pm_daily_clean
        
    def load_all(self):
        with open(self.pm_file) as f:        
            pm_data =json.load(f)['Data']
            pm_data_daily = pandas.DataFrame(pm_data)
        return pm_data_daily

