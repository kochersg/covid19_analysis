import numpy as np 
import matplotlib.pyplot as plt
from datetime import datetime as dt
from collections import namedtuple
from logzero import logger

CFnames = namedtuple('fnames',['confirmed','recovered','deaths'], \
    defaults=[ \
    '../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', \
    '../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv', \
    '../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'])

class CDataTimeSeries:
    def __init__(self, country = "Germany"):
        self.fname = CFnames()
        self.country = country
        self.latitude = None
        self.longitude = None
        self.days = []
        self.n_confirmed = self._read_csv_data(self.fname.confirmed)        
        self.n_deaths = self._read_csv_data(self.fname.deaths)
        self.n_recovered = self._read_csv_data(self.fname.recovered)
        self.n_still_infected = self.n_confirmed-self.n_deaths-self.n_recovered

    def _read_csv_data(self,fname):
        with open(fname,'rt') as fh:
            csv_data=fh.readlines()
        if self.days == []:
            self._parse_csv_data_header_for_dates(csv_data[0])
        return(self._parse_csv_data(csv_data[1:]))

    def _parse_csv_data(self, data):
        n_data=[]
        for d in data:
            n_strs = d.split(',')
            if n_strs[1]==self.country and n_strs[0]=='':
                self.latitude = float(n_strs[2])
                self.longitude = float(n_strs[3])
                for n_str in n_strs[4:]:
                    n_data.append(int(n_str))
                break
        return(np.array(n_data))
            
    def _parse_csv_data_header_for_dates(self, hdata):
        d = hdata.split(',')
        for day_str in d[4:]:
            # print(day_str)
            try:
                day_time=dt.strptime(day_str,'%m/%d/%y')
            except:
                day_time=dt.strptime(day_str[:-1],'%m/%d/%y')
            self.days.append(day_time)

    def plot_time_series(self, ax=None, show_plot = False, show_xlabel = True):
        if ax == None:
            fh=plt.figure(figsize = [10,8])
            ax=fh.add_subplot(111)
        ax.plot(self.days, self.n_confirmed, color='red', label='total confirmed')
        ax.plot(self.days, self.n_recovered, color='green', label='total recovered')
        ax.plot(self.days, self.n_deaths, color='black', label='total deaths')
        ax.plot(self.days, self.n_still_infected, \
            color='blue', linewidth=2, label='still infected')
        ax.grid(True)
        if show_xlabel:
            ax.set_xlabel('Date')
        ax.set_ylabel('Number of cases')
        ax.text(0.5, 0.9, self.country, horizontalalignment='center', \
            verticalalignment='center', transform=ax.transAxes, \
            fontsize = 12, fontweight = 'bold', \
            bbox=dict(facecolor='white', alpha=1.0, edgecolor='None'))
        plt.legend()
        if show_plot:
            plt.show()

class CDataTimeSeriesCollection:
    def __init__(self, country_list):
        self.county_list=country_list
        self.data_collection=[]
        self._collect_data_for_selected_countries()

    def _collect_data_for_selected_countries(self):
        for country in self.county_list:
            self.data_collection.append(CDataTimeSeries(country=country))

    def plot_collection_subplots(self):
        if len(self.county_list)<2:
            subplot_str='11'
        elif len(self.county_list)<3:
            subplot_str='21'
        elif len(self.county_list)<5:
            subplot_str='22'
        elif len(self.county_list)<7:
            subplot_str='32'
        elif len(self.county_list)<10:
            subplot_str='33'
        fh = plt.figure(figsize=(15,10))
        for ix, data in enumerate(self.data_collection):
            if ix>int(subplot_str[0])*(int(subplot_str[1])-1):
                show_x_label=True
            else:
                show_x_label=False
            ax = fh.add_subplot(subplot_str+str(ix+1))
            data.plot_time_series(ax=ax,show_plot=False, show_xlabel=show_x_label)
        plt.show()

    def plot_country_comparison(self, country_name_1, country_name_2, ax=None, show_plot=False):
        ds1=self._get_data_from_country_name(country_name_1)
        ds2=self._get_data_from_country_name(country_name_2)
        if not ds1 or not ds2:
            logger.info('Country does not exist')
            return
        if ax==None:
            fh=plt.figure(figsize=(10,7))
            ax=fh.add_subplot(111)
        
        ax.plot(ds1.days,ds1.n_confirmed,color='red',label=ds1.country+' confirmed')
        ax.plot(ds2.days,ds2.n_confirmed,color='darkred', linestyle='-.', label=ds2.country+' confirmed')
        ax.plot(ds1.days,ds1.n_recovered,color='green',label=ds1.country+' recovered')
        ax.plot(ds2.days,ds2.n_recovered,color='darkgreen', linestyle='-.', label=ds2.country+' recovered')
        ax.plot(ds1.days,ds1.n_deaths,color='darkgrey',label=ds1.country+' deaths')
        ax.plot(ds2.days,ds2.n_deaths,color='black', linestyle='-.', label=ds2.country+' deaths')
        ax.plot(ds1.days,ds1.n_still_infected,color='blue',label=ds1.country+' still infected')
        ax.plot(ds2.days,ds2.n_still_infected,color='darkblue', linestyle='-.', label=ds2.country+' still infected')

        ax.grid(True)
        ax.set_xlabel('Date')
        ax.set_ylabel('Cases')
        plt.legend()
        ax.text(0.6, 0.9, ds1.country+' vs. '+ ds2.country, horizontalalignment='center', \
            verticalalignment='center', transform=ax.transAxes, \
            fontsize = 12, fontweight = 'bold', \
            bbox=dict(facecolor='white', alpha=1.0, edgecolor='None'))

        if show_plot:
            plt.show()        

    
    def _get_data_from_country_name(self, c_name):
        for ds in self.data_collection:
            if ds.country==c_name:
                return(ds)
        return(None)
            

if __name__ == "__main__":
    countries=('Germany','Italy','Spain','United Kingdom','France','Austria','Netherlands')
    # single_country = CDataTimeSeries(country = 'Germany')
    # single_country.plot_time_series(show_plot=True)
    dc = CDataTimeSeriesCollection(countries)
    # dc.plot_collection_subplots()
    dc.plot_country_comparison('Germany','France',show_plot=True)
    