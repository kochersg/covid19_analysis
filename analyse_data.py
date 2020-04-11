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
    from_date = dt(2020,3,1)
    to_date = None

    # plot time series data of a single country
    single_country = CDataTimeSeries(country = 'Germany')
    single_country_view = CDataTimeSeriesView(cv_data=None)
    single_country_view.plot_time_series(show_plot=True, from_date=from_date, to_date=to_date)
    
    # load data of several countries into a collection
    countries=('Germany','Italy','Spain','United Kingdom','France','Austria')
    dc = CDataTimeSeriesCollection(countries)
    dc_view = CDataTimeSeriesCollectionView(cv_data_collection=dc)
    
    # plot the collection data into a graph with one subplot per country   
    dc_view.plot_collection_subplots(from_date=from_date, to_date=to_date)
    
    # plot a comparison between the timeseries of two different countries into one plot
    dc_view.plot_country_comparison('Germany','Italy',show_plot=True, from_date=from_date, to_date=to_date)
    