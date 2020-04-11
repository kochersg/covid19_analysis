"""
Doc-Classes of the doc-view model based approach. 
"""
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
    """
    Class representing and plotting time series data.
    ...
    Attributes
    ----------
    fname : namedTuple fnames 
        containing the file URLs to the data files
    country : str
        string containing the country name
    lattitude : float
        geographic lattitude of the country
    longitude : float
        geographic longitude of the country
    days : list of datetime objects
        dates on which the data points where taken
    n_confirmed : numpy array of floats
        total number of confirmed cases, every element represents the data of one day
    n_recovered : numpy array of floats
        total number of recovered patients
    n_deaths : numpy array of floats
        total number of deaths
    n_still_infected : numpy array of floats
        number of people who have not recovered or died, yet

    Methods
    -------
    plot_time_series(ax=None, show_plot=False, show_xlabel=True)
        Plots the time series data for a selected country. If a matplotlib.pyplot axes-Object is
        provided it will plot inside this axes. Argument show_plot controls if the pyplot.show() 
        command is called and the plot is shown. Argument show_xlabel controls, if the
        xlabel 'Date' is plotted (useful for many staggered subplots)

    """
    def __init__(self, country='Germany'):
        """
        Parameter
        ---------
        country : str, optional
            country to plot data from (default 'Germany')
        """
        self.fname = CFnames()
        self.country = country
        self.latitude = None
        self.longitude = None
        self.days = []
        self.n_confirmed = self.__read_csv_data(self.fname.confirmed)        
        self.n_deaths = self.__read_csv_data(self.fname.deaths)
        self.n_recovered = self.__read_csv_data(self.fname.recovered)
        self.n_still_infected = self.n_confirmed-self.n_deaths-self.n_recovered

    def _get_time_range_indices(self, start_date=None, end_date=None):
        """Retrieve start index and end index of a time range in self.days
        Parameter
        ---------
        start_date : datetime object, optional
            Start date of time range (default is None). In case of start_date=None the first index is 0.
        end_date: datetime object, optional
            End date of the time range (default is None). In case of end_data=None the second index is the
            one of the last data point
        """
        days = np.array(self.days)
        if start_date!=None:
            try:
                ix_start = np.where(days>=start_date)[0][0]
            except IndexError:
                logger.warn("Start date not found, using first date")
                ix_start = 0
        else:
            ix_start = 0
        if end_date!=None:
            try:
                ix_end=np.where(days>=end_date)[0][0]
            except IndexError:
                logger.warn("End date not found, using last date")
                ix_end = len(days)
        else:
            ix_end=len(days)
        return(ix_start,ix_end)
        

    def __read_csv_data(self,fname):
        try:
            with open(fname,'rt') as fh:
                csv_data=fh.readlines()
        except:
            raise NotADirectoryError(f"File {fname} not found. Make sure the \'COVID-19\' directory is in the same root directory as the \'covid19_analysis\' directory")
        if self.days == []:
            self.__parse_csv_data_header_for_dates(csv_data[0])
        return(self.__parse_csv_data(csv_data[1:]))

    def __parse_csv_data(self, data):
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
            
    def __parse_csv_data_header_for_dates(self, hdata):
        d = hdata.split(',')
        for day_str in d[4:]:
            # print(day_str)
            try:
                day_time=dt.strptime(day_str,'%m/%d/%y')
            except:
                day_time=dt.strptime(day_str[:-1],'%m/%d/%y')
            self.days.append(day_time)

class CDataTimeSeriesCollection:
    def __init__(self, country_list):
        self.country_list=country_list
        self.data_collection=[]
        self._collect_data_for_selected_countries()

    def _collect_data_for_selected_countries(self):
        for country in self.country_list:
            self.data_collection.append(CDataTimeSeries(country=country))
    
    def _get_data_from_country_name(self, c_name):
        for ds in self.data_collection:
            if ds.country==c_name:
                return(ds)
        return(None)
            

if __name__ == "__main__":
    pass