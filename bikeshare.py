## import all necessary packages and functions
import time
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta


chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'


def return_city():
    '''Asks the user for a city and returns the filename for
    that city's bike share data.

    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''
    city = input('\nHello! Let\'s analyze some US bikeshare data!\n'
                 '\nCan i show you data for Chicago, New York, or Washington?\n')

    city = city.lower()

    while True:
        if city == "new york":
            print('\nNew York City it is! Let\'s explore its bikeshare data\n')
            return new_york_city
        if city == "chicago":
            print('\nChicago it is! let\'s explore its bikeshare data\n')
            return chicago
        elif city == "washington":
            print('\nWashington it is! let\'s explore its bikeshare data\n')
            return washington

        city = input("Sorry i do not understand your input.Please choose between Chicago, New York, or Washington")
        city = city.lower()


def return_time_period():
    '''Asks the user for a time period and returns the specified filter.
    Args:
        none.
    Returns:
        (str) Time period information.
    '''
    time_period = input('\nCan i filter the data by month (m) and day of the month, day of the week (d), or no? Type "none" for no time filter.\n')

    time_period = time_period.lower()

    while True:
        if time_period == 'm' or time_period == "month":

            while True:
                filterByDayOfMonth = input("\n Do you wish to filter by day of the month? Type 'YES' or 'NO'\n").lower()

                if filterByDayOfMonth == "no":
                    print('\n ok, we are filtering data by month...\n')

                    return 'month'

                elif filterByDayOfMonth == "yes":
                   print ('\n We are filtering data by month and day of the month...\n')
                   return 'day_of_month'

        if time_period == "d" or time_period == "day":
            print('\n We are now filtering data by day of the week...\n')
            return 'day_of_week'
        elif time_period == "none" or time_period == "n":
            print('\n We are not applying any time filter to the data\n')
            return "none"
        time_period = input("\n Please choose a time filter option between month (M), day of the week (d), or none (n) \n").lower()


def return_month(month_):
    '''Asks the user for a month and returns the specified month.

    Args:
        month_ - the output from return_time_period()
    Returns:
        (str) Month information.
    '''
    if month_ == 'month':

        month = input('\nChoose month? January, February, March, April, May, or June? Please type the full month name.\n')
        while month.strip().lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('\nPlease choose between January, February, March, April, May, or June? Please type the full month name.\n')
        return month.strip().lower()
    else:
        return 'none'

def return_day_of_month(df, dayOfMonth_):
    """Asks the user for a month and a day of month, and returns the specified day

    Args:
        dayOfMonth_ - the ouput of return_time_period()
        df - the dataframe with all bikedata

    Returns:
        list with Month and day information

    """
    monthAndDay = []

    if dayOfMonth_ == "day_of_month":

        month = return_month("month")
        monthAndDay.append(month)

        maxDayOfMonth = return_max_day_of_month(df, month)

        while (True):

            promptString = """\n Which day of the month? \n
            Please type your response as an integer """


            promptString  = promptString + str(maxDayOfMonth) + "\n"

            dayOfMonth = input(promptString)

            try:

                dayOfMonth = int(dayOfMonth)

                if 1 <= dayOfMonth <= maxDayOfMonth:
                    monthAndDay.append(dayOfMonth)
                    return monthAndDay

            except ValueError:

                print("This not an integer")

    else:
        return 'none'



def return_day(day_):
    '''Asks the user for a day and returns the specified day.

    Args:
        day_ - string - should data be filtered by day
    Returns:
        (str) Day information.
    '''
    if day_ == 'day_of_week':
        day = input('\Kindly choose a day of the week? Please type a day M, Tu, W, Th, F, Sa, Su. \n')
        while day.lower().strip() not in ['m', 'tu', 'w', 'th', 'f', 'sa', 'su']:
            day = input('\nPlease choose a day from M, Tu, W, Th, F, Sa, Su. \n')
        return day.lower().strip()
    else:
        return 'none'


def load_data(city):
    """
    Reads the city file name and loads it to a dataframe
    INPUT:
    city - path to the file as a string
    OUTPUT:

    df - dataframe to be used to calculate relevant statistics

    """
    print('\nLoading the data...\n')
    df = pd.read_csv(city)

    #add datetime format to aid filtering
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #add columns to aid filtering

    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df["day_of_month"] = df["Start Time"].dt.day

    return df

def apply_time_filters(df, time_period, month, dayOfWeek, monthAndDay):
    '''
    Filters the data according to the criteria specified by the user.
    INPUT:
    df           - city dataframe
    time_period  - this string tells us the specific time period (either "month", "day_of_month", or "day_of_week")
    month        - this string tells us the specific month used to filter the data
    dayOfWeek    - this string tells us the specific week day used to filter the data
    dayOfMonth   - this list tells us the month (at index [0]) used to filter the data
                    and the day number (at index [1])

    OUTPUT:
    df - dataframe to be used to calculate all aggregates that is filtered according to
         the specified time period
    '''


    print('Data loaded. Now computing statistics... \n')
    #Filter by Month if required
    if time_period == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #Filter by day of week if required
    if time_period == 'day_of_week':
        days = ['Monday', 'Tuesday',
        'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday']
        for d in days:
            if dayOfWeek.capitalize() in d:
                day_of_week = d
        df = df[df['day_of_week'] == day_of_week]

    if time_period == "day_of_month":
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = monthAndDay[0]
        month = months.index(month) + 1
        df = df[df['month']==month]
        day = monthAndDay[1]
        df = df[df['day_of_month'] == day]

    return df

    #Filter by most popular month of the year

def popular_month(df):
    '''What is the most popular month for start time?
    INPUT:
        df - dataframe returned from apply_time_filters

    OUTPUT:
        most_popular_month - string of most frequent month

    '''
    print('\n * What is the most popular month for bike traveling?')
    mnth = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_popular_month = months[mnth - 1].capitalize()
    return most_popular_month


    #Get the most popular day of the the week

def popular_day(df):
    '''What is the most popular day of week for start time?
    INPUT:
        df - dataframe returned from apply_time_filters
    OUTPUT:
        popular_day - string with name of day with most rides

    '''
    print('\n * What is the most popular day of the week (Monday to Sunday) for bike traveling?')

    return df['day_of_week'].value_counts().reset_index()['index'][0]

    #Get the most popular hour of the the week


def popular_hour(df):
    '''What is the most popular hour of day for start time?
    INPUT:
        df - dataframe returned from apply_time_filters
    OUTPUT:
        popular_hour - int of the most popular hour

    '''
    print('\n * What is the most popular hour of the day for bike traveling?')
    df['hour'] = df['Start Time'].dt.hour
    return df.hour.mode()[0]

    #Get the total trip duration and average trip duration

def trip_duration(df):
    '''What is the total trip duration and average trip duration?
    INPUT:
        df - dataframe returned from apply_time_filters
    OUTPUT:
        tuple = total trip duration, average trip durations

        each is a pandas._libs.tslib.Timedelta objects

    '''
    print('\n * What was the total traveling done for 2017 through June, and what was the average time spent on each trip?')
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']

    #Find sum for total trip time, mean for avg trip time

    total_travel_time = np.sum(df['Travel Time'])

    totalDays = str(total_travel_time).split()[0]

    print ("\nThe total travel time on 2017 through June was " + totalDays + " days \n")

    average_travel_time = np.mean(df['Travel Time'])

    averageDays = str(average_travel_time).split()[0]

    print("The average travel time on 2017 through June was " + averageDays + " days \n")

    return total_travel_time, average_travel_time

    #Get the most popular start station

def popular_stations(df):
    '''What is the most popular start station and most popular end station?
    INPUT:
        df - dataframe returned from apply_time_filters
    OUTPUT:
        tuple - indicating most popular start and end stations
    '''
    print("\n* What is the most popular start station?\n")
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]
    print (start_station)
    print("\n* What is the most popular end station?\n")
    end_station = df['End Station'].value_counts().reset_index()['index'][0]
    print(end_station)
    return start_station, end_station

#Find the most popular trip

def popular_trip(df):
    '''What is the most popular trip?
    INPUT:
        df - dataframe returned from apply_time_filters
    OUTPUT:
        result - pandas.core.frame.DataFrame - with start, end, and number of trips for most popular trip
    '''
    result = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\n* What was the most popular trip from start to end?')
    return result

#Find number of each user type

def users(df):
    '''What are the counts of each user type?
    INPUT:
        df - dataframe returned from apply_time_filters
    OUTPUT:
        users - pandas series with counts for each user type

    '''
    print('\n* Are users subscribers, customers, or dependents?\n')

    return df['User Type'].value_counts()

#What are the birth years

def birth_years(df):
    '''Get the earliest, latest, and most frequent birth year?
    INPUT:
        df - dataframe returned from apply_time_filters
    OUTPUT:
        tuple of earliest, latest, and most frequent year of birth

    '''
    try:
        print('\n* What is the earliest, latest, and most frequent year of birth, respectively?')
        earliest = np.min(df['Birth Year'])
        print ("\nThe earliest year of birth is " + str(earliest) + "\n")
        latest = np.max(df['Birth Year'])
        print ("The latest year of birth is " + str(latest) + "\n")
        most_frequent= df['Birth Year'].mode()[0]
        print ("The most frequent year of birth is " + str(most_frequent) + "\n")
        return earliest, latest, most_frequent
    except:
        print('No available birth date data for this period.')

def compute_stat(f, df):
    """
    Calculates the time it will takes to calculate relevant statistics
    INPUT:
      f  - the applied statistics function
      df - the dataframe with all the data

    OUTPUT:
        prints to console, doesn't return a value
    """

    start_time = time.time()
    statToCompute = f(df)
    print(statToCompute)
    print("Computing this stat took %s seconds." % (time.time() - start_time))

def return_max_day_of_month(df, month):
    """
    returns the max day of the month
    INPUT:

      df - the city dataframe

      month - string of the selected month

    OUTPUT:

       maxDay - integer with the max day of the month
    """
    months = {"january": 1, "february": 2, "march": 3, "april":4, "may": 5, "june":6}
    df = df[df["month"] == months[month]]

    maxDay = max(df["day_of_month"])
    return maxDay

def display_raw_data(df):
    """
    Displays the data used to compute the statistics

    Input:
        the dataframe with all the bikeshare data

    Returns:
       none
    """

    #omit auxiliary columns from visualization
    df = df.drop(['month', 'day_of_month'], axis = 1)

    rowIndex = 0

    seeData = input("\n Can i show you data used to compute the statistics? Please write 'yes' or 'no' \n").lower()

    while True:

        if seeData == 'no':
            return

        if seeData == 'yes':
            print(df[rowIndex: rowIndex + 5])
            rowIndex = rowIndex + 5


        seeData = input("\n Can i show you five more rows of the data used to calculate the statistics? Please write 'yes' or 'no' \n").lower()

def statistics():
    '''Calculates and prints out the descriptive statistics about a city

    and time period specified by the user via raw input.

    Args:
        none.
    Returns:
        none.
    '''
    city = return_city()

    df = load_data(city)

    time_period = return_time_period()

    month = return_month(time_period)
    day = return_day(time_period)
    monthAndDay = return_day_of_month(df, time_period)

    df = apply_time_filters(df, time_period, month, day, monthAndDay)

    display_raw_data(df)

    stat_function_list = [popular_month,
     popular_day, popular_hour,
     trip_duration, popular_trip,
     popular_stations, users, birth_years, gender]

    for fun in stat_function_list:
        compute_stat(fun, df)

    # Restart?
    restart = input('\nCan i restart? Type \'yes\' or \'no\'.\n')
    while restart.lower() not in ['yes', 'no']:
        print("Invalid input. Type 'yes' or 'no'.")
        restart = input('\nCan i restart? Type \'yes\' or \'no\'.\n')
    if restart.lower() == 'yes':
        statistics()


if __name__ == "__main__":
	statistics()
