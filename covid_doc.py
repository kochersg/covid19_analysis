"""
Doc-Classes of the doc-view model based approach. 
"""
import numpy as np
from datetime import datetime as dt
from datetime import timedelta as tdelta
from collections import namedtuple, OrderedDict
from logzero import logger

CFnames = namedtuple(
    "fnames",
    ["confirmed", "recovered", "deaths"],
    defaults=[
        "../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
        "../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
        "../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
    ],
)


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
    sim_data : boolean, optional
        data will be simulated by using the doubling_time_dict (default is False)
    sim_mortality : float, optional
        mortality (rate of people dying once confirmed) (default is 0.01)
    sim_days_to_recovery: float, optional
        time in days it takes to recover or die (default is 0.045)
    sim_extrapolate_to_date : datetime.datetime, optional
        used for simulation, if set to None only dates reported by CSSE will be taken
        into account

    Methods
    -------
        _calc_doubling_time_on_date(self, date:dt, average_interval_days:int=1):
            Calculates the time interval needed to double the number of confirmed cases
        _calc_doubling_time_over_interval(self, start_date:dt=None, end_date:dt=None, average_interval_days:int=1):
            Calculates the time interval needed to double the number of confirmed cases
            over a given time range from start_date to end_date
        _get_doubling_time_dict_over_interval(self, start_date:dt=None, end_date:dt=None, average_interval_days:int=1):
            Calculates the time interval needed to double the number of confirmed cases
            over a given time range from start_date to end_date and returns it as dict.
            Can be used as input for simulated data.
        _get_time_range_indices(self, start_date=None, end_date=None):
            Retrieve start index and end index of a time range in self.days
    """

    def __init__(
        self,
        country: str = "Germany",
        sim_data: bool = False,
        doubling_time_dict={"2020-02-01": 3, "2020-03-01": 1.37, "2020-04-01": 1.22},
        mortality: float = 0.045,
        days_to_recovery: float = 12.65,
        extrapolate_to_date: dt = None,
    ):
        """
        Parameter
        ---------
        country : str, optional
            country to plot data from (default 'Germany')
        sim_data : boolean, optional
            Flag indicating if time series set shall be simulated using doubling_time_dict
            (default is False)
        doubling_time_dict : dict, optional
            dict with keys '%Y-%m-%d' formatted strings to indicate the date and float values with
            corresponding doubling times
        mortality : float, optional
            mortality (rate of people dying once confirmed) (default is 0.01)
        days_to_recovery: float, optional
            time in days it takes to recover or die (default is 0.045)
        extrapolate_to_date : datetime.datetime, optional
            used for simulation, if set to None only dates reported by CSSE will be taken
            into account
        """
        self.fname = CFnames()
        self.country = country
        self.latitude = None
        self.longitude = None
        self.sim_data = sim_data
        self.sim_doubling_dict = doubling_time_dict
        self.sim_mortality = mortality
        self.sim_days_to_recovery = days_to_recovery
        self.sim_extrapolate_to_date = extrapolate_to_date
        self.days = []
        # load one data set to fill self.days
        self.n_confirmed = self.__read_csv_data(self.fname.confirmed)
        if not self.sim_data:
            self.n_confirmed = self.__read_csv_data(self.fname.confirmed)
            self.n_deaths = self.__read_csv_data(self.fname.deaths)
            self.n_recovered = self.__read_csv_data(self.fname.recovered)
        else:
            if self.sim_extrapolate_to_date != None:
                self.__extend_days_to_date()
            self.__sim_data()

        self.n_still_infected = self.n_confirmed - self.n_deaths - self.n_recovered
        self.n_still_infected[self.n_still_infected < 0] = 0

    def _calc_doubling_time_on_date(self, date: dt, average_interval_days: int = 1):
        """Calculates the time interval needed to double the number of confirmed cases

        Parameters
        ----------
        date : datetime object, optional
            date to calculate the doubling time for (default is None)
        average_interval_days : int, optional
            sets the number of days to look back into past from given date. Returned value
            is the average value over the selected time range (defaul is 1)

        """
        if date == None:
            date = self.days[-1]
        ixs, ixe = self._get_time_range_indices(
            start_date=date - tdelta(days=average_interval_days), end_date=date
        )
        nc2 = self.n_confirmed[ixe]
        nc1 = self.n_confirmed[ixs]
        daily_increase_rate = 1 + (nc2 / nc1 - 1) / average_interval_days
        return np.log(2) / np.log(daily_increase_rate)

    def _calc_doubling_time_over_interval(
        self, start_date: dt = None, end_date: dt = None, average_interval_days: int = 1
    ):
        """Calculates the time interval needed to double the number of confirmed cases
        over a given time range from start_date to end_date

        Parameters
        ----------
        start_date : datetime object, optional
            Start date of the time interval to calculate the doubling time for (default is None)
        end_date : datetime object, optional
            Start date of the time interval to calculate the doubling time for (default is None)
        average_interval_days : int, optional
            sets the number of days to look back into past from given date. Returned value
            is the average value over the selected time range (defaul is 1)

        """
        ixs, ixe = self._get_time_range_indices(
            start_date=start_date, end_date=end_date
        )
        double_t = []
        for day in self.days[ixs:ixe]:
            double_t.append(
                self._calc_doubling_time_on_date(
                    day, average_interval_days=average_interval_days
                )
            )
        return np.array(double_t)

    def _get_doubling_time_dict_over_interval(
        self, start_date: dt = None, end_date: dt = None, average_interval_days: int = 1
    ):
        """Calculates the time interval needed to double the number of confirmed cases
        over a given time range from start_date to end_date and returns it as dict.
        Can be used as input for simulated data.

        Parameters
        ----------
        start_date : datetime object, optional
            Start date of the time interval to calculate the doubling time for (default is None)
        end_date : datetime object, optional
            Start date of the time interval to calculate the doubling time for (default is None)
        average_interval_days : int, optional
            sets the number of days to look back into past from given date. Returned value
            is the average value over the selected time range (defaul is 1)

        """
        ixs, ixe = self._get_time_range_indices(
            start_date=start_date, end_date=end_date
        )
        dt_dict = {}
        for day in self.days[ixs:ixe]:
            double_t = self._calc_doubling_time_on_date(
                day, average_interval_days=average_interval_days
            )
            if np.isinf(double_t) or np.isnan(double_t) or double_t == 0:
                continue
            dt_dict[day.strftime("%Y-%m-%d")] = self._calc_doubling_time_on_date(
                day, average_interval_days=average_interval_days
            )
        return dt_dict

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
        if start_date != None:
            try:
                ix_start = np.where(days >= start_date)[0][0]
            except IndexError:
                logger.warn("Start date not found, using first date")
                ix_start = 0
        else:
            ix_start = 0
        if end_date != None:
            try:
                ix_end = np.where(days >= end_date)[0][0]
            except IndexError:
                logger.warn("End date not found, using last date")
                ix_end = len(days)
        else:
            ix_end = len(days)
        return (ix_start, ix_end)

    def __extend_days_to_date(self):
        while True:
            if self.days[-1] < self.sim_extrapolate_to_date:
                self.days.append(self.days[-1] + tdelta(days=1))
            else:
                break

    def __sim_data(self):
        self.n_confirmed = np.zeros((len(self.days), 1))
        self.n_recovered = np.zeros((len(self.days), 1))
        self.n_deaths = np.zeros((len(self.days), 1))
        self.n_confirmed[0] = 1
        for ix in range(len(self.days) - 1):
            day = ix + 1
            inf_rate = self._doubling_time_to_infrate(
                self.__get_doubling_time_from_dict(self.days[day])
            )
            self.n_confirmed[day] = (self.n_confirmed[day - 1]) * inf_rate
            if day >= self.sim_days_to_recovery:
                d_to_recv = int(np.round(self.sim_days_to_recovery))
                self.n_deaths[day] = (
                    self.n_confirmed[day - d_to_recv] * self.sim_mortality
                )
                self.n_recovered[day] = self.n_confirmed[day - d_to_recv] * (
                    1 - self.sim_mortality
                )

    def __get_doubling_time_from_dict(self, day):
        dict_days = [
            dt.strptime(d_str, "%Y-%m-%d") for d_str in self.sim_doubling_dict.keys()
        ]
        # print(dict_days)
        for d_day in dict_days:
            if day <= d_day:
                return self.sim_doubling_dict[d_day.strftime("%Y-%m-%d")]
        return self.sim_doubling_dict[list(self.sim_doubling_dict.keys())[-1]]

    @staticmethod
    def _infrate_to_doubling_time(infrate):
        return np.log(2) / np.log(infrate)

    @staticmethod
    def _doubling_time_to_infrate(doubling_time):
        return np.exp(np.log(2) / doubling_time)

    def __read_csv_data(self, fname):
        try:
            with open(fname, "rt") as fh:
                csv_data = fh.readlines()
        except:
            raise NotADirectoryError(
                f"File {fname} not found. Make sure the 'COVID-19' directory is in the same root directory as the 'covid19_analysis' directory"
            )
        if self.days == []:
            self.__parse_csv_data_header_for_dates(csv_data[0])
        return self.__parse_csv_data(csv_data[1:])

    def __parse_csv_data(self, data):
        n_data = []
        for d in data:
            n_strs = d.split(",")
            if n_strs[1] == self.country and n_strs[0] == "":
                self.latitude = float(n_strs[2])
                self.longitude = float(n_strs[3])
                for n_str in n_strs[4:]:
                    n_data.append(int(n_str))
                break
        return np.array(n_data)

    def __parse_csv_data_header_for_dates(self, hdata):
        d = hdata.split(",")
        for day_str in d[4:]:
            # print(day_str)
            try:
                day_time = dt.strptime(day_str, "%m/%d/%y")
            except:
                day_time = dt.strptime(day_str[:-1], "%m/%d/%y")
            self.days.append(day_time)


class CDataTimeSeriesCollection:
    """
    Class representing and plotting several time series data sets in a collection.
    ...
    Attributes
    ----------
    country_list : list of strings
        list of strings containing the country names
    data_collection : list of CDataTimeSeries objects
        Times series objects of the countries defined in country_list.

    Methods
    -------
    _collect_data_for_selected_countries(self)
        loads the data for the selected countries
    _get_data_from_country_name(self, c_name:str)
        returns the CDataTimeSeriesObject from the collection where country = c_name
    add_data_time_series_to_collection(self, ds:CDataTimeSeries)
        append a data set to the collection
    """

    def __init__(self, country_list):
        self.country_list = list(country_list)
        self.data_collection = []
        self._collect_data_for_selected_countries()

    def _collect_data_for_selected_countries(self):
        for country in self.country_list:
            self.data_collection.append(CDataTimeSeries(country=country))

    def _get_data_from_country_name(self, c_name: str):
        for ds in self.data_collection:
            if ds.country == c_name:
                return ds
        return None

    def add_data_time_series_to_collection(self, ds: CDataTimeSeries):
        self.country_list.append(ds.country)
        self.data_collection.append(ds)

    def _get_actual_doubling_time_for_date(
        self, date=None, average_interval_days=1
    ) -> OrderedDict:
        dt_dict = dict()
        for ds in self.data_collection:
            dt_dict[ds.country] = ds._calc_doubling_time_on_date(
                date=date, average_interval_days=1
            )
        sorted_dt = sorted(dt_dict.items(), key=lambda kv: kv[1], reverse=True)
        dt_dict_sorted = OrderedDict(sorted_dt)
        return dt_dict_sorted


if __name__ == "__main__":
    pass
