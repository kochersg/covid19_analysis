"""
View-Classes of the doc-view model based approach. 
"""

from covid_doc import CDataTimeSeries, CDataTimeSeriesCollection
import numpy as np 
import matplotlib.pyplot as plt
from datetime import datetime as dt
from collections import namedtuple
from logzero import logger

class CDataTimeSeriesView:
    """
    Class representing and plotting time series data.
    ...
    Attributes
    ----------
    cv_data : CDataTimeSeries object of the doc-class

    Methods
    -------
    plot_time_series(ax=None, show_plot=False, show_xlabel=True)
        Plots the time series data for a selected country. If a matplotlib.pyplot axes-Object is
        provided it will plot inside this axes. Argument show_plot controls if the pyplot.show() 
        command is called and the plot is shown. Argument show_xlabel controls, if the
        xlabel 'Date' is plotted (useful for many staggered subplots)

    """
    def __init__(self, cv_data=None):
        """
        Parameter
        ---------
        cv_data : CDataTimeSeries, optional
            Time series to plot data from (default is None)
        """
        self.cv_data = cv_data

    def plot_time_series(self, ax=None, show_plot=False, show_xlabel=True, use_scientific_notation=False, \
        from_date=None,to_date=None):
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
        use_scientific_notation : boolean, optional
            controls if the y-axis is plotted in scientific notatiom 1e... (default is False)
        from_date : datetime object, optional
            controls the start date for plotting (default is None)
        to_date : datetime object, optional
            controls the end date for plotting (default is None)

        """
        if ax == None:
            fh=plt.figure(figsize = [10,8])
            ax=fh.add_subplot(111)
        ixs,ixe = self.cv_data._get_time_range_indices(start_date=from_date, end_date=to_date)
        print(ixs,ixe)
        ax.plot(self.cv_data.days[ixs:ixe], self.cv_data.n_confirmed[ixs:ixe], color='red', label='total confirmed')
        ax.plot(self.cv_data.days[ixs:ixe], self.cv_data.n_recovered[ixs:ixe], color='green', label='total recovered')
        ax.plot(self.cv_data.days[ixs:ixe], self.cv_data.n_deaths[ixs:ixe], color='black', label='total deaths')
        ax.plot(self.cv_data.days[ixs:ixe], self.cv_data.n_still_infected[ixs:ixe], \
            color='blue', linewidth=2, label='still infected')
        ax.grid(True)
        if show_xlabel:
            ax.set_xlabel('Date')
        ax.set_ylabel('Number of cases')
        ax.text(0.5, 0.9, self.cv_data.country, horizontalalignment='center', \
            verticalalignment='center', transform=ax.transAxes, \
            fontsize = 12, fontweight = 'bold', \
            bbox=dict(facecolor='white', alpha=1.0, edgecolor='None'))
        if use_scientific_notation:
            ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,3))
        plt.legend()
        if show_plot:
            plt.show()

class CDataTimeSeriesCollectionView:
    def __init__(self, cv_data_collection=None):
        self.cv_data_collection=cv_data_collection

    def plot_collection_subplots(self):
        if len(self.cv_data_collection.country_list)<2:
            subplot_str='11'
        elif len(self.cv_data_collection.country_list)<3:
            subplot_str='21'
        elif len(self.cv_data_collection.country_list)<5:
            subplot_str='22'
        elif len(self.cv_data_collection.country_list)<7:
            subplot_str='32'
        elif len(self.cv_data_collection.country_list)<10:
            subplot_str='33'
        fh = plt.figure(figsize=(15,10))
        for ix, data in enumerate(self.cv_data_collection.data_collection):
            if ix>int(subplot_str[0])*(int(subplot_str[1])-1):
                show_x_label=True
            else:
                show_x_label=False
            ax = fh.add_subplot(subplot_str+str(ix+1))
            data_view = CDataTimeSeriesView(cv_data=data)
            data_view.plot_time_series(ax=ax,show_plot=False, show_xlabel=show_x_label, use_scientific_notation=True)
        plt.show()

    def plot_country_comparison(self, country_name_1, country_name_2, ax=None, show_plot=False):
        ds1=self.cv_data_collection._get_data_from_country_name(country_name_1)
        ds2=self.cv_data_collection._get_data_from_country_name(country_name_2)
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


if __name__ == "__main__":
    pass