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

    # select time range for plotting
    from_date = None#dt(2020,3,15)
    to_date = None#dt(2020,3,1)

    # plot time series data of a single country
    single_country = CDataTimeSeries(country = 'Germany Sim', sim_data=True, \
        infrate_dict={'22':1.13,'23':1.0,'40':1.25, '42':1.25 , '59':1.19, '61':1.19, '66':1.16, \
            '67':1.1, '71':1.065, '78':1.055, '79':1.03, '90':1.02, '100':1.01, '110':1.00}, \
            days_to_recovery=13, extrapolate_to_date=dt(2020,5,20), \
            mortality=0.045)
    single_country_view = CDataTimeSeriesView(cv_data=single_country)
    single_country_view.plot_time_series(show_plot=True, from_date=from_date, to_date=to_date)
     
    # load data of several countries into a collection
    countries=('Germany','Italy','Spain','United Kingdom','Austria')
    dc = CDataTimeSeriesCollection(countries)
    dc.add_data_times_series_to_collection(single_country)
    dc_view = CDataTimeSeriesCollectionView(cv_data_collection=dc)

    # plot the collection data into a graph with one subplot per country   
    dc_view.plot_collection_subplots(from_date=from_date, to_date=to_date)
    
    # plot a comparison between the timeseries of two different countries into one plot
    dc_view.plot_country_comparison('Germany','Germany Sim',show_plot=True, from_date=from_date, to_date=to_date)
    
    # plot the progress of the doubling time
    c_view = CDataTimeSeriesView(dc._get_data_from_country_name('Germany'))
    c_view.plot_doubling_time_over_days(from_date=dt(2020,3,1),average_interval_days=1)
