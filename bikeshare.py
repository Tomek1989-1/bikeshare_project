import pandas as pd
import numpy as np
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def inputs():
    #city input
    while True:
        city = str(input('Please choose a city (Chicago/New York City/Washington):'))
        city_lowercase = city.lower()
        cities_list = ['chicago','new york city','washington']
        if city_lowercase in cities_list:
            break
        else:
            print('invalid city name')
    #month input
    while True:
        month = str(input('Please choose a month (january/february/march/april/may/june) or put "all" to apply no month filter:'))
        month_lowercase = month.lower()
        month_list = ['all','january','february','march','april','may','june']
        if month_lowercase in month_list:
            break
        else:
            print('invalid month name')
    #weekday input
    while True:
        weekday = str(input('Please choose a weekday or put "all" to apply no weekday filter:'))
        weekday_lowercase = weekday.lower()
        weekday_list = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        if weekday_lowercase in weekday_list:
            break
        else:
            print('invalid weekday name')
            
    print('-'*40)        
    return city_lowercase,month_lowercase,weekday_lowercase

def load_data(city,month,weekday):
    df = pd.read_csv(CITY_DATA[city])
    while True:
        raw_data = str(input("do you want to see raw data(yes/no)?:"))
        raw_data_lowercase = raw_data.lower()
        if raw_data_lowercase == 'yes':
            i = 5
            while True:
                print(df.head(i))
                question = str(input("do you want to see 5 addtional raw rows(yes/no)?:"))
                question_lowercase = question.lower()
                if question_lowercase == 'yes':
                    i = i+5
                elif question_lowercase == 'no':
                    break
                else:
                    print("wrong input")
        else:
            break
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['weekday'] = pd.to_datetime(df['Start Time']).dt.weekday
    #filtering by day and month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month)+1
        df = df[df['month'] == month_index]
    if weekday != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day_index = days.index(weekday)
        df = df[df['weekday'] == day_index]
    return df
    
def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\npopular hour: {}'.format(popular_hour))
    
    popular_weekday = df['weekday'].mode()[0]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print('\npopular weekday: {}'.format(days[popular_weekday]))
    
    popular_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('\npopular month: {}'.format(months[popular_month-1]))
    
    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)
            
def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print('\npopular start station: {}'.format(popular_start_station))

    popular_end_station = df['End Station'].mode()[0]
    print('\npopular end station: {}'.format(popular_end_station))

    df['start-end stations'] = df['Start Station']+' - '+df['End Station']
    popular_combination = df['start-end stations'].mode()[0]
    print('\npopular start-end combination: {}'.format(popular_combination))

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print('\nTotal travel time: {}'.format(total_travel_time))

    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean travel time: {}'.format(mean_travel_time))

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)
    
def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    #creating dataframe for user/gender calculation
    df_user_gender_type = df.copy()
    df_user_gender_type.fillna('no data',inplace=True)
    user_types_count = df_user_gender_type.groupby(['User Type'])['User Type'].count()
    print('\nUser types count:\n {}'.format(user_types_count))
    try:
        gender_count = df_user_gender_type.groupby(['Gender'])['Gender'].count()
        print('\nGender count:\n {}'.format(gender_count))
    except:
        print('\nNo gender data')
    
    #creating dateframe for birth year calculation
    try:
        df_birth_year = df.copy()
        df_birth_year.dropna(subset = ['Birth Year'], inplace=True) #removing empty 'birth year' rows
        earliest_year_of_birth = df_birth_year['Birth Year'].min()
        most_recent_year_of_birth = df_birth_year['Birth Year'].max()
        most_common_year_of_birth = df_birth_year['Birth Year'].mode()[0]
        print('\nEarliest year of birth: {}'.format(earliest_year_of_birth))
        print('\nMost recent year of birth: {}'.format(most_recent_year_of_birth))
        print('\nMost common year of birth: {}'.format(most_common_year_of_birth))
        print("\nThis took {} seconds.".format((time.time() - start_time)))
        print('-'*40)
    except:
        print('\nNo birth date data')
    
def main():
    while True:
        city, month, weekday = inputs()
        df = load_data(city, month, weekday)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

main()