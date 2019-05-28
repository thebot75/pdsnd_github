import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    valid_cities = ['chicago', 'new york city', 'washington']
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    #these are the valid options for the three variables that allow us to continue with the rest of the code
    #anything else will cause us to loop round until we have one valid variable in each field

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    city_names = { 'ch': 'chicago',
                  'ny': 'new york city',
                  'wa': 'washington' }
    #note: different to valid list - used dictionary so that user has to type less to continue (and
    #less chance of mistakes by doing it this way)

    while city not in valid_cities:
        city_short = input("Please enter a city (For Chicago enter 'ch' / New York City enter 'ny'/ Washington enter 'wa': ").lower()
        if city_short not in city_names:
            print("Entry is not valid, please try again (please use ch / ny / wa)")
        else:
            city = city_names[city_short]
        #this just loops around until we get a valid input - city_names dictionary used to derive 'proper' name
        #from shorter user input

    # get user input for month (all, january, february, ... , june)
    month = ""
    month_names = { 'jan': 'january',
                  'feb': 'february',
                  'mar': 'march',
                  'apr': 'april',
                  'may': 'may',
                  'jun': 'june',
                  'all': 'all'}
    #note: different to valid list - used dictionary so that user has to type less to continue (and
    #less chance of mistakes by doing it this way)

    while month not in valid_months:
        month_short = input("Please enter a month (jan / feb / mar / apr / may/ jun), or enter 'all' to see all data: ").lower()
        if month_short not in month_names:
            print("Not a valid entry, please try again (please use short versions of months above).")
        else:
            month = month_names[month_short]
        #this just loops around until we get a valid input - month_names dictionary used to derive 'proper' name
        #from shorter user input

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    day_names = { 'mon': 'monday',
                 'tue': 'tuesday',
                 'wed': 'wednesday',
                 'thu': 'thursday',
                 'fri': 'friday',
                 'sat': 'saturday',
                 'sun': 'sunday',
                 'all': 'all'}
    #note: different to valid list - used dictionary so that user has to type less to continue (and
    #less chance of mistakes by doing it this way)

    while day not in valid_days:
        day_short = input("Please enter a day (mon / tue / wed / thu / fri / sat / sun), or enter 'all' to see all data: ").lower()
        if day_short not in day_names:
            print("Not a valid entry, please try again (please use short versions of days above).")
        else:
            day = day_names[day_short]
        #this just loops around until we get a valid input - day_names dictionary used to derive 'proper' name
        #from shorter user input


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    #uses the CITY_DATA dictionary to define the path for the city data we're uploading

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['weekday'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = months[popular_month - 1]
    print('The most common start month for a journey is ' + str(month).title() + ".")

    # display the most common day of week
    popular_day = df['weekday'].mode()[0]

    print('The most common weekday for a journey is ' + str(popular_day) + ".")

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    if popular_hour < 13:
        print('The most common hour for starting a journey is {}AM.'.format(popular_hour))
    else:
        pm_hour = popular_hour - 12
        print('The most common hour for starting a journey is {}PM.'.format(pm_hour))

    #this section just converts the raw hour format into something a bit more readable for the user

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    df['total_trip'] = df['Start Station'] + " to " + df['End Station']
    #this sets up a new column for total trip, which is a combination of start and end station

    total_rows = len(df['Start Station'])

    # display most commonly used start station
    most_starts = df['Start Station'].mode()
    maxstarts = df['Start Station'].value_counts().max()
    #these two lines derive the most commonly used start station using mode, and the number of times that
    #station was used using value_counts

    print("The most common start station was " + most_starts[0] + ", which was the start station \n" +                 str(maxstarts) + " times out of " + str(total_rows) + " total journeys.\n")

    # display most commonly used end station
    most_ends = df['End Station'].mode()
    maxends = df['End Station'].value_counts().max()

    #these two lines derive the most commonly used end station using mode, and the number of times that
    #station was used using value_counts

    print("The most common end station was " + most_ends[0] + ", which was the final station \n" + str(maxends) +
    " times out of " + str(total_rows) + " total journeys.\n")

    # display most frequent combination of start station and end station trip
    most_trips = df['total_trip'].mode()
    maxtotal = df['total_trip'].value_counts().max()
   #these two lines use the 'total_trip' series we created above, and use this to derive the most common
   #trip using mode, and the number of times that trip was taken using value_counts

    print("The most common trip is from " + most_trips[0] + ", which\nwas travelled "
    + str(maxtotal) + " times out of " + str(total_rows) + " total journeys.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print("The total time spent travelling across all customers was " + str(int(round(total_duration/360)))
    + " hours.")

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print("The average travel time was " + str(int(round(mean_duration/60))) + " minutes.")

    #the above use sum and mean to get the stats for the travel time in seconds, convert that to
    #hours for total / minutes for mean, then uses round & int to get to the nearest integer (& str
    #so it prints)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # Display counts of user types
    print("We had the following types of users in our customer base over this period: \n")
    userdf = df['User Type'].value_counts().reset_index()
    print(userdf.to_string(header=None, index=None))
    print("\n")
    #this convert to another df, then from that df to_string, is a neat method of getting rid of
    #the additional info (dtype etc) that you get using value_counts


    if city == 'washington':
        print("We have no gender or year of birth data for our Washington customer base, sorry.")
        #this makes sure the code doesn't fall over if the city is Washington, using city from get_filters()
    else:
        # Display counts of gender
        print("This is the gender split in our customers across the period (where known): \n")
        genderdf = df['Gender'].value_counts().reset_index()
        print(genderdf.to_string(header=None, index=None))
        print("\n")
        #this convert to another df, then from that df to_string, is a neat method of getting rid of
        #the additional info (dtype etc) that you get using value_counts

        # Display earliest, most recent, and most common year of birth
        print("The earliest year of birth for a passenger was " + str(int(df['Birth Year'].min())) + ".")
        print("The most recent year of birth for a passenger was " + str(int(df['Birth Year'].max())) + ".")
        print("The most common year of birth for our passengers was " + str(int(df['Birth Year'].mode()[0])) + ".")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Asks if users want to see the raw dataframe data, then lets them see it 5 rows at a time"""

    display_data = input("\nWould you like to see the raw data? (yes to see data, no to continue): ").lower()
    if display_data == 'yes':
        start_data = 0
        end_data = min(5, len(df['Start Station']))
        #this line just makes sure the data is still displayed if the data set is less than 5
        cont_data = 'yes'
        while cont_data == 'yes':
            print("\n")
            print(df.iloc[start_data:end_data])
            if end_data == len(df['Start Station']):
                print("\nEnd of data reached.\n")
                cont_data = 'no'
            else:
                start_data +=5
                end_data = min(end_data + 5, len(df['Start Station']))
                cont_data = input("\nDo you want to see another 5 rows? (enter yes to continue, no to quit:                         ").lower()
        #this while loop keeps going until user enters 'not yes', or until we reach the end of the data
        #on each run round the loop start data is increased by 5, as is end data UNLESS that would take it past
        #the final piece of data - in which case it's limited to the final index

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
