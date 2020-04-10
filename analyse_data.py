"""
A python script that basically visualizes data from the CSSE GitHub data set. 
The CSSE data can be found here: https://github.com/CSSEGISandData/COVID-19.git

Usage
-----
The script expects the data in a folder "COVID-19" which resides in the same root-folder as "covid19_anaylis":

    ./SomeRootFolder/
            |---> COVID-19
            |---> covid19_analysis

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

    def plot_time_series(self, ax=None, show_plot=False, show_xlabel=True):
        """Plots the time series of the selected country

        Parameters
        ----------
        ax : matplotlib.pyplot axes object, optional
            axes object used for plotting, if not provided the function will create
            a figure with axes (default is None)
        show_plot : boolean, optional
            controls if the plot is shown at the end of the method call (default is False)
        show_xlabel : boolean, optional
            controls if the x-label 'Date' is plotted (default is True)

        """
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
    # plot time series data of a single country
    single_country = CDataTimeSeries(country = 'Germany')
    single_country.plot_time_series(show_plot=True)
    # load data of several countries into a collection
    countries=('Germany','Italy','Spain','United Kingdom','France','Austria')
    dc = CDataTimeSeriesCollection(countries)
    # plot the collection data into a graph with one subplot per country   
    dc.plot_collection_subplots()
    # plot a comparison between the timeseries of two different countries into one plot
    dc.plot_country_comparison('Germany','Italy',show_plot=True)
    