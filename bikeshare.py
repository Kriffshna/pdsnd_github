import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}
months = ('january', 'february', 'march', 'april', 'may', 'june')
days = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')

def selection(prompt, selections=('yes', 'no')):

    """Takes in and processes user inputs to handle requests and allows them to confirm or deny certain prompts and exit at any time."""

    while True:
        selection = input(prompt).lower().strip()
        if selection == 'exit':
            raise SystemExit('Exited program.')
        elif ',' in selection:
            selection = [i.lower().strip() for i in selection.split(',')]
            if list(filter(lambda x: x in selections, selection)) == selection:
                break
        elif ',' not in selection:
            if selection in selections:
                break

    return selection

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    if selection:
        city = selection("\nWhich city or cities would you like information about? Choose New York City, Chicago, Washington, or any combination of them with commas in between. ", CITY_DATA.keys())
        month = selection("\nBy which months would you like to filter the data? Choose january, february, march, april, may, june, or any combination with commas in between. ", months)
        day = selection("\nBy which days of the week would you like to filter the data? Choose any day or any combination with commas in between. ", days)

    else:
        print("The information you entered returned an error. Please make sure you entered the information into the fields correctly.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    start_time = time.time()

    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city),
                       sort=True)
    else:
        df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour

    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] == (month.title)], month))
    else:
        df = df[df['Month'] == (months.index(month)+1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Day'] == (day.title())], day))
    else:
        df = df[df['Day'] == day.title()]

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    most_common_month = df['Month'].mode()[0]
    print('The month number with most frequent traveling was: ' + str(most_common_month))


    most_common_day = df['Day'].mode()[0]
    print('The day of the week with most frequent traveling was: ' + str(most_common_day))


    most_common_hour = df['Start Hour'].mode()[0]
    print('The most common travel start hour was: ' + str(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    most_common_start_station = df['Start Station'].mode()[0]
    print("The most common start station was: " + str(most_common_start_station))


    most_common_end_station = df['End Station'].mode()[0]
    print("The most common end station was: " + str(most_common_end_station))


    df['Start-End Combination'] = df['Start Station'] + ' to ' + df['End Station']
    most_common_station_combo = str(df['Start-End Combination'].mode()[0])
    print("The most common starting and ending station combo was: " + most_common_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    """ Taking the travel time in seconds and convering into days, months, minutes, and seconds """
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time//86400)) + 'd ' + str(int((total_travel_time % 86400)//3600)) + 'h ' + str(int(((total_travel_time % 86400) % 3600)//60)) + 'm ' + str(int(((total_travel_time % 86400) % 3600) % 60)) + 's')

    print('The total travel time was: ' + total_travel_time)


    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time//60)) + 'm ' + str(int(mean_travel_time % 60)) + 's')
    print('The average travel time was: ' + mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    user_types = df['User Type'].value_counts().to_string()
    print('Here are some stats about the users: \n' + user_types)


    try:
        gender_counts = df['Gender'].value_counts().to_string()
        print('Here are the available gender stats for the users: \n' + gender_counts)

    except:
        print('Unfortunately, the gender stats could not be provided for this instance.')


    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print('The oldest person to ride a bike here was born in: ' + earliest_birth_year)

        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print('The youngest person to ride a bike here was born in: ' + most_recent_birth_year)

        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print('The most common birth year for riders here was: ' + most_common_birth_year)

    except:
        print('Unfortunately, age information could not be found for this instance.')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def raw(df, location):
    """Displays raw data for user upon request and iterates by five rows per confirmation."""

    print('You are viewing raw data.')

    while True:
        for i in range(location, len(df.index)):
            print(df.iloc[location:location+5].to_string())
            location += 5

            if selection("\nWould you like to print 5 more rows? Enter yes or no.\n") == 'yes':
                continue
            else:
                break
        break

    return location

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        location = 0

        while True:
            raw_option = selection("\nWould like to view raw data? Enter yes or no.\n")
            if raw_option == 'yes':
                location = raw(df, location)
            elif raw_option == 'no':
                break

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = selection('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
