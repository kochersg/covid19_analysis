"""
View-Classes of the doc-view model based approach. 
"""

from covid_doc import CDataTimeSeries, CDataTimeSeriesCollection
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

        plot_doubling_time_over_days(self, ax:plt.axes=None, show_plot:bool=True,...
                from_date:dt=None, to_date:dt=None,average_interval_days:int=1)
            Plots the time interval needed to double the number of confirmed cases for the selected country
    )

    """

    def __init__(self, cv_data: CDataTimeSeries = None):
        """
        Parameter
        ---------
        cv_data : CDataTimeSeries, optional
            Time series to plot data from (default is None)
        """
        self.cv_data = cv_data

    def plot_time_series(
        self,
        ax: plt.axes = None,
        show_plot: bool = False,
        show_xlabel: bool = True,
        use_scientific_notation: bool = False,
        from_date: dt = None,
        to_date: dt = None,
    ) -> plt.figure:
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
        Returns
        -------
        fig : matplotlib.pyplot figure object

        """
        if self.cv_data == None:
            logger.warning(
                "No data available, initialize self.cv_data with CDataTimeSeries object"
            )
            return
        if ax == None:
            fh = plt.figure(figsize=[10, 8])
            ax = fh.add_subplot(111)
        ixs, ixe = self.cv_data._get_time_range_indices(
            start_date=from_date, end_date=to_date
        )
        ax.plot(
            self.cv_data.days[ixs:ixe],
            self.cv_data.n_confirmed[ixs:ixe],
            color="red",
            label="total confirmed",
        )
        ax.plot(
            self.cv_data.days[ixs:ixe],
            self.cv_data.n_recovered[ixs:ixe],
            color="green",
            label="total recovered",
        )
        ax.plot(
            self.cv_data.days[ixs:ixe],
            self.cv_data.n_deaths[ixs:ixe],
            color="black",
            label="total deaths",
        )
        ax.plot(
            self.cv_data.days[ixs:ixe],
            self.cv_data.n_still_infected[ixs:ixe],
            color="blue",
            linewidth=2,
            label="still infected",
        )
        ax.grid(True)
        if show_xlabel:
            ax.set_xlabel("Date")
        ax.set_ylabel("Number of cases")
        ax.text(
            0.5,
            0.9,
            self.cv_data.country,
            horizontalalignment="center",
            verticalalignment="center",
            transform=ax.transAxes,
            fontsize=12,
            fontweight="bold",
            bbox=dict(facecolor="white", alpha=1.0, edgecolor="None"),
        )
        if use_scientific_notation:
            ax.ticklabel_format(style="scientific", axis="y", scilimits=(0, 3))
        self._nicely_format_date_ticks(ax)
        plt.legend()
        if show_plot:
            plt.show()
        if "fh" in locals():
            return fh
        return plt.gcf()

    def plot_doubling_time_over_days(
        self,
        ax: plt.axes = None,
        show_plot: bool = True,
        from_date: dt = None,
        to_date: dt = None,
        average_interval_days: int = 1,
    ) -> plt.figure:
        """Plots the time interval needed to double the number of confirmed cases for the selected country

        Parameters
        ----------
        ax : matplotlib.pyplot axes object, optional
            axes object used for plotting, if not provided the function will create
            a figure with axes (default is None)
        show_plot : boolean, optional
            controls if the plot is shown at the end of the method call (default is False)
        from_date : datetime object, optional
            controls the start date for plotting (default is None)
        to_date : datetime object, optional
            controls the end date for plotting (default is None)
        average_interval_days : int, optional
            sets the number of days to look back into past from given date. Returned value
            is the average value over the selected time range
        Returns
        -------
        fig : matplotlib.pyplot figure object
        """
        if ax == None:
            fh = plt.figure(figsize=[10, 8])
            ax = fh.add_subplot(111)

        ixs, ixe = self.cv_data._get_time_range_indices(
            start_date=from_date, end_date=to_date
        )
        ax.bar(
            self.cv_data.days[ixs:ixe],
            self.cv_data._calc_doubling_time_over_interval(
                start_date=from_date, end_date=to_date
            ),
            label="doubling time",
        )

        ax.grid(True)
        ax.set_xlabel("Date")
        ax.set_ylabel("Doubling time (days)")
        ax.text(
            0.5,
            0.9,
            self.cv_data.country,
            horizontalalignment="center",
            verticalalignment="center",
            transform=ax.transAxes,
            fontsize=12,
            fontweight="bold",
            bbox=dict(facecolor="white", alpha=1.0, edgecolor="None"),
        )
        self._nicely_format_date_ticks(ax)
        plt.legend()

        if show_plot:
            plt.show()
        if "fh" in locals():
            return fh
        return plt.gcf()

    @staticmethod
    def _nicely_format_date_ticks(ax: plt.axes):
        """Nicely formats the date ticks for time series plots

        Parameters
        ----------
        ax : matplotlib.pyplot axes object, optional
            axes object used for plotting.
        """
        # format the ticks
        months = mdates.MonthLocator()  # every month
        days = mdates.DayLocator()  # every day
        months_fmt = mdates.DateFormatter("%b")
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(months_fmt)
        ax.xaxis.set_minor_locator(days)
        # format the coords message box
        ax.format_xdata = mdates.DateFormatter("%Y-%m-%d")
        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        plt.gcf().autofmt_xdate()


class CDataTimeSeriesCollectionView:
    """
    Class representing and plotting collections of time series data.
    ...
    Attributes
    ----------
    cv_data_collection : CDataTimeSeriesCollection object of the doc-class

    Methods
    -------
    plot_collection_subplots(from_date=None, to_date=None)
        Plots the time series data for a set of selected countries.
    """

    def __init__(self, cv_data_collection: CDataTimeSeriesCollection = None):
        """
        Parameter
        ---------
        cv_data_collection : CDataTimeSeriesCollection, optional
            Time series to plot data from (default is None)
        """
        self.cv_data_collection = cv_data_collection

    def plot_collection_subplots(
        self, from_date: dt = None, to_date: dt = None, show_plot: bool = True
    ) -> plt.figure:
        """All time series data of a collection in a figure with subplots
        Parameters
        ----------
        from_date : datetime object, optional
            controls the start date for plotting (default is None)
        to_date : datetime object, optional
            controls the end date for plotting (default is None)
        show_plot : boolean, optional
            controls if the plot is shown at the end of the method call (default is True)
        Returns
        -------
        fig : matplotlib.pyplot figure object
        """
        if self.cv_data_collection == None:
            logger.warning(
                "No collection available, initialize self.cv_data_collection with CDataTimeSeriesCollection object"
            )
            return
        if len(self.cv_data_collection.country_list) < 2:
            subplot_str = "11"
        elif len(self.cv_data_collection.country_list) < 3:
            subplot_str = "21"
        elif len(self.cv_data_collection.country_list) < 5:
            subplot_str = "22"
        elif len(self.cv_data_collection.country_list) < 7:
            subplot_str = "32"
        elif len(self.cv_data_collection.country_list) < 10:
            subplot_str = "33"
        fh = plt.figure(figsize=(15, 8))
        for ix, data in enumerate(self.cv_data_collection.data_collection):
            # if ix>int(subplot_str[0])*(int(subplot_str[1])-1):
            #     show_x_label=True
            # else:
            #     show_x_label=False
            show_x_label = True
            ax = fh.add_subplot(subplot_str + str(ix + 1))
            data_view = CDataTimeSeriesView(cv_data=data)
            data_view.plot_time_series(
                ax=ax,
                show_plot=False,
                show_xlabel=show_x_label,
                use_scientific_notation=True,
                from_date=from_date,
                to_date=to_date,
            )
        if show_plot:
            plt.show()
        return fh

    def plot_country_comparison(
        self,
        country_name_1: str,
        country_name_2: str,
        ax: plt.axes = None,
        show_plot: bool = False,
        from_date: dt = None,
        to_date: dt = None,
    ) -> plt.figure:
        """Plot the time series curves of two selected countries from a collection
        into one plot for comparison purposes.
        Parameters
        ----------
        country_name_1 : str
            Name of the first country selected for compare
        country_name_2 : str
            Name of the second country selected for compare
        from_date : datetime object, optional
            controls the start date for plotting (default is None)
        to_date : datetime object, optional
            controls the end date for plotting (default is None)
        ax : matplotlib.pyplot axes object, optional
            axes object used for plotting, if not provided the function will create
            a figure with axes (default is None)
        show_plot : boolean, optional
            controls if the plot is shown at the end of the method call (default is False)
        Returns
        -------
        fig : matplotlib.pyplot figure object
        """
        if self.cv_data_collection == None:
            logger.warning(
                "No collection available, initialize self.cv_data_collection with CDataTimeSeriesCollection object"
            )
            return
        ds1 = self.cv_data_collection._get_data_from_country_name(country_name_1)
        ds2 = self.cv_data_collection._get_data_from_country_name(country_name_2)
        if not ds1 or not ds2:
            logger.info("Country does not exist")
            return
        if ax == None:
            fh = plt.figure(figsize=(10, 7))
            ax = fh.add_subplot(111)

        ixs1, ixe1 = ds1._get_time_range_indices(start_date=from_date, end_date=to_date)
        ixs2, ixe2 = ds2._get_time_range_indices(start_date=from_date, end_date=to_date)
        ax.plot(
            ds1.days[ixs1:ixe1],
            ds1.n_confirmed[ixs1:ixe1],
            color="red",
            linewidth=2,
            label=ds1.country + " confirmed",
        )
        ax.plot(
            ds2.days[ixs2:ixe2],
            ds2.n_confirmed[ixs2:ixe2],
            color="darkred",
            linestyle="-.",
            label=ds2.country + " confirmed",
        )
        ax.plot(
            ds1.days[ixs1:ixe1],
            ds1.n_recovered[ixs1:ixe1],
            color="green",
            linewidth=2,
            label=ds1.country + " recovered",
        )
        ax.plot(
            ds2.days[ixs2:ixe2],
            ds2.n_recovered[ixs2:ixe2],
            color="darkgreen",
            linestyle="-.",
            label=ds2.country + " recovered",
        )
        ax.plot(
            ds1.days[ixs1:ixe1],
            ds1.n_deaths[ixs1:ixe1],
            color="darkgrey",
            linewidth=2,
            label=ds1.country + " deaths",
        )
        ax.plot(
            ds2.days[ixs2:ixe2],
            ds2.n_deaths[ixs2:ixe2],
            color="black",
            linestyle="-.",
            label=ds2.country + " deaths",
        )
        ax.plot(
            ds1.days[ixs1:ixe1],
            ds1.n_still_infected[ixs1:ixe1],
            color="blue",
            linewidth=2,
            label=ds1.country + " still infected",
        )
        ax.plot(
            ds2.days[ixs2:ixe2],
            ds2.n_still_infected[ixs2:ixe2],
            color="darkblue",
            linestyle="-.",
            label=ds2.country + " still infected",
        )

        ax.grid(True)
        ax.set_xlabel("Date")
        ax.set_ylabel("Cases")
        plt.legend()
        ax.text(
            0.6,
            0.9,
            ds1.country + " vs. " + ds2.country,
            horizontalalignment="center",
            verticalalignment="center",
            transform=ax.transAxes,
            fontsize=12,
            fontweight="bold",
            bbox=dict(facecolor="white", alpha=1.0, edgecolor="None"),
        )
        CDataTimeSeriesView._nicely_format_date_ticks(ax)

        if show_plot:
            plt.show()
        if "fh" in locals():
            return fh
        return plt.gcf()

    def plot_doubling_time_from_date_as_bar_chart(
        self,
        ax: plt.axes = None,
        show_plot: bool = True,
        date: dt = None,
        average_interval_days: int = 1,
    ) -> plt.figure:
        """Plot the doubling times of a given date for countries from a collection.
        Parameters
        ----------
        ax : matplotlib.pyplot axes object, optional
            axes object used for plotting, if not provided the function will create
            a figure with axes (default is None)
        show_plot : boolean, optional
            controls if the plot is shown at the end of the method call (default is False)
        date : datetime object, optional
            controls the date for plotting (default is None)
        average_interval_days : int, optional
            sets the number of days to look back into past from given date. Returned value
            is the average value over the selected time range
        Returns
        -------
        fig : matplotlib.pyplot figure object
        """
        if ax == None:
            fh = plt.figure(figsize=(10, 7))
            ax = fh.add_subplot(111)
        dt_dict = self.cv_data_collection._get_actual_doubling_time_for_date(
            date=date, average_interval_days=average_interval_days
        )
        ax.bar(*zip(*dt_dict.items()), facecolor="darkgray", edgecolor="black")
        ax.set_ylabel("Doubling time (days)")
        ax.grid(True, which="both", axis="y")

        if date == None:
            date = self.cv_data_collection.data_collection[0].days[-1]
        ax.text(
            0.75,
            0.9,
            date.strftime("%d-%b-%Y"),
            horizontalalignment="center",
            verticalalignment="center",
            transform=ax.transAxes,
            fontsize=12,
            fontweight="bold",
            bbox=dict(facecolor="white", alpha=1.0, edgecolor="None"),
        )

        if show_plot:
            plt.show()
        if "fh" in locals():
            return fh
        return plt.gcf()


if __name__ == "__main__":
    pass
