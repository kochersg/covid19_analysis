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
from covid_doc import CDataTimeSeries, CDataTimeSeriesCollection
from covid_view import CDataTimeSeriesView, CDataTimeSeriesCollectionView
from datetime import datetime as dt


if __name__ == "__main__":
    # # select time range for plotting
    # from_date = None  #dt(2020,3,1)
    # to_date = None    #dt(2020,4,5)


    # # plot time series data of a single country
    # single_country = CDataTimeSeries(country = 'Germany')
    # single_country_view = CDataTimeSeriesView(cv_data=single_country)
    # single_country_view.plot_time_series(show_plot=True, from_date=from_date, to_date=to_date)
     
    # # # load data of several countries into a collection
    # countries=('Germany','Italy','Spain','United Kingdom','Austria')
    # dc = CDataTimeSeriesCollection(countries)
    # dc_view = CDataTimeSeriesCollectionView(cv_data_collection=dc)

    # # # plot the collection data into a graph with one subplot per country   
    # dc_view.plot_collection_subplots(from_date=from_date, to_date=to_date)
    
    # # # plot the progress of the doubling time
    # c_view = CDataTimeSeriesView(dc._get_data_from_country_name('Italy'))
    # c_view.plot_doubling_time_over_days(from_date=dt(2020,3,1),average_interval_days=1)


    # ## Simulate time series date by handing over a dict with doubling times

    # # plot time series data of a single country
    # single_country = CDataTimeSeries(country = 'Germany Sim', sim_data=True, \
    #     doubling_time_dict= \
    #     {
    #         '2020-02-01':8, \
    #         '2020-02-25':6, \
    #         '2020-02-28':3, \
    #         '2020-03-01':3, \
    #         '2020-03-06':2, \
    #         '2020-03-16':3, \
    #         '2020-03-19':2.5, \
    #         '2020-03-22':4.5, \
    #         '2020-03-27':5.0, \
    #         '2020-03-28':5.5, \
    #         '2020-03-29':8, \
    #         '2020-03-30':9, \
    #         '2020-04-03':9.5, \
    #         '2020-04-04':11.5, \
    #         '2020-04-05':15, \
    #         '2020-04-06':16, \
    #         '2020-04-07':17, \
    #         '2020-04-08':18, \
    #         '2020-04-12':22, \
    #         '2020-04-15':30, \
    #         '2020-04-20':60, \
    #         '2020-04-25':120, \
    #         '2020-04-30':240, \
    #         '2020-05-05':480, \
    #         '2020-05-10':1000, \
    #         '2020-05-15':2000, \
    #         '2020-05-20':4000, \
    #     },
    #     days_to_recovery=12.65, extrapolate_to_date=dt(2020,5,20), \
    #     mortality=0.045)

    # # add simulated data to collection     
    # dc.add_data_time_series_to_collection(single_country)

    # # # plot a comparison between the timeseries of two different countries into one plot
    # dc_view.plot_country_comparison('Germany','Germany Sim',show_plot=True, from_date=from_date, to_date=to_date)

    dc = CDataTimeSeriesCollection(['Germany', 'Italy', 'United Kingdom', 'Spain', 'Netherlands', 'Austria', 'Switzerland'])
    dc_view = CDataTimeSeriesCollectionView(dc)
    dc_view.plot_doubling_time_from_date_as_bar_chart()

