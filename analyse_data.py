"""
A python script that basically visualizes data from the CSSE GitHub data set. 
The CSSE data can be found here: https://github.com/CSSEGISandData/COVID-19.git

Usage
-----
The script expects the data in a folder "COVID-19" which resides in the same root-folder as "covid19_anaylis":

    ./SomeRootFolder/
            |---> COVID-19
            |---> covid19_analysis

The classes are organized in a doc-view model. Data is parsed and stored in the classes 
given by covid_doc.

Visualization is achieved by the views classes in covid_view

"""
import matplotlib.pyplot as plt
from covid_doc import CDataTimeSeries, CDataTimeSeriesCollection
from covid_view import CDataTimeSeriesView, CDataTimeSeriesCollectionView
from datetime import datetime as dt
from logzero import logger

def _save_figure(fig:plt.figure, save_file_name:str):
    if save_file_name != None:
        try:
            fig.savefig(save_file_name)
        except NotADirectoryError:
            logger.warning('Unable to save file ' + save_file_name)

def plot_single_country(country:str, start_date:dt=None, end_date:dt=None, save_file_name:str=None):
    single_country = CDataTimeSeries(country = country)
    single_country_view = CDataTimeSeriesView(cv_data=single_country)
    fig=single_country_view.plot_time_series(show_plot=False, from_date=start_date, to_date=end_date)
    _save_figure(fig,save_file_name)
    plt.show()

def plot_country_collection(countries:list, start_date:dt=None, end_date:dt=None, save_file_name:str=None):
    dc = CDataTimeSeriesCollection(countries)
    dc_view = CDataTimeSeriesCollectionView(cv_data_collection=dc)
    fig = dc_view.plot_collection_subplots(from_date=start_date, to_date=end_date, show_plot=False)
    _save_figure(fig,save_file_name)
    plt.show()

def plot_doubling_time_single_country(country:str, start_date:dt=None, end_date:dt=None, \
    save_file_name:str=None):
    sc = CDataTimeSeries(country)
    c_view = CDataTimeSeriesView(sc)
    fig = c_view.plot_doubling_time_over_days(from_date=start_date, to_date=end_date ,average_interval_days=1, show_plot=False)
    _save_figure(fig,save_file_name)
    plt.show()

def plot_simulated_data(start_date:dt=None, end_date:dt=None):
    # plot time series data of a single country
    single_country = CDataTimeSeries(country = 'Germany Sim', sim_data=True, \
        doubling_time_dict= \
        {
            '2020-02-01':8, \
            '2020-02-25':6, \
            '2020-02-28':3, \
            '2020-03-01':3, \
            '2020-03-06':2, \
            '2020-03-16':3, \
            '2020-03-19':2.5, \
            '2020-03-22':4.5, \
            '2020-03-27':5.0, \
            '2020-03-28':5.5, \
            '2020-03-29':8, \
            '2020-03-30':9, \
            '2020-04-03':9.5, \
            '2020-04-04':11.5, \
            '2020-04-05':15, \
            '2020-04-06':16, \
            '2020-04-07':17, \
            '2020-04-08':18, \
            '2020-04-10':18, \
            '2020-04-11':20, \
            '2020-04-12':22, \
            '2020-04-14':24, \
            '2020-04-15':26, \
            '2020-04-16':30, \
            '2020-04-18':30, \
            '2020-04-19':20, \
            '2020-04-21':40, \
            '2020-04-25':50, \
            '2020-05-01':70, \
            '2020-05-05':80, \
            '2020-05-10':100, \
            '2020-05-15':140, \
            '2020-05-20':160, \
            '2020-05-25':200, \
            '2020-05-30':220, \
            '2020-06-05':300, \
            '2020-06-10':350, \
            '2020-06-15':380, \
            '2020-06-30':500, \
            '2020-07-30':500, \
        },
        days_to_recovery=12.65, extrapolate_to_date=dt(2020,7,30), \
        mortality=0.045)

    # add simulated data to collection
    dc = CDataTimeSeriesCollection(['Germany'])    
    dc.add_data_time_series_to_collection(single_country)

    # plot a comparison between the timeseries of two different countries into one plot
    dc_view = CDataTimeSeriesCollectionView(dc)
    fig = dc_view.plot_country_comparison('Germany','Germany Sim',show_plot=False, 
        from_date=start_date, to_date=end_date)
    _save_figure(fig, './example_images/Compare_CDataTimeSeriesObjects.png')
    plt.show()

def plot_doubling_time_collection(countries, save_file_name=None):
    dc = CDataTimeSeriesCollection(country_list=countries)
    dc_view = CDataTimeSeriesCollectionView(dc)
    fig = dc_view.plot_doubling_time_from_date_as_bar_chart(show_plot = False)
    _save_figure(fig, save_file_name)
    plt.show()

if __name__ == "__main__":
    # select time range for plotting
    from_date = dt(2020,3,1)
    to_date = None #dt(2020,6,5)

    # simulate time series date by handing over a dict with doubling times
    plot_simulated_data(start_date=from_date, end_date=to_date)

    # plot time series data of a single country
    plot_single_country('Germany', start_date=from_date, end_date=to_date, save_file_name='./example_images/SingleData.png')

    # plot data of several countries into a collection
    plot_country_collection(['Germany', 'Sweden','Italy','Spain','United Kingdom','Denmark'], \
        start_date=from_date, end_date=to_date, save_file_name='./example_images/Collect_Subplots.png')
    
    # plot the progress of the doubling time
    plot_doubling_time_single_country('Italy', start_date=from_date, end_date=to_date, save_file_name='./example_images/Doubling_times.png')

    # plot doubling time for selected countries
    plot_doubling_time_collection(['Germany', 'Italy', 'United Kingdom', 'Spain', 'Netherlands', 'Austria', 'Switzerland'], \
        save_file_name='./example_images/doubling_time_collection.png')

