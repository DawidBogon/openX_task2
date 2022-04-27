import itertools
import glob
import argparse
import ntpath
from datetime import datetime, timedelta
import pandas as pd


def find_avalible_slot(calendars:str, dur_in_mins: int, min_people: int) -> str:
    def path_leaf(path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    cur_time = datetime.now()
    dur_in_mins_dt_object = timedelta(minutes=dur_in_mins)
    # im skipping first element here because its not needed,
    # at least on Windows, im not
    # sure if it will work on linux like this
    # paths to text files
    cal_paths: list = glob.glob(calendars[1:]+r'\*.txt')
    peoples_names: list = [path_leaf(path)[:-4] for path in cal_paths]

    # stores busy times for each person:
    busy_dict: dict = {}
    # stores all timestamps, and times 1 second befeor start
    #  of being busy and 1 second after not being busy.
    timestamps: list = []

    for idx, file in enumerate(cal_paths):
        # name_person = path_leaf(file)[:-4]
        busy_dict[peoples_names[idx]] = []
        with open(file) as fil:
            for line in fil:
                if len(line) == 11:
                    start_date = datetime.strptime(line[0:10], '%Y-%m-%d')
                    end_date = start_date + timedelta(
                                hours=23, minutes=59, seconds=59)
                else:
                    start_date = datetime.strptime(
                                line[:19], '%Y-%m-%d %H:%M:%S')
                    end_date = datetime.strptime(
                                line[22:], '%Y-%m-%d %H:%M:%S')

                timestamps.append(start_date)
                timestamps.append(start_date - timedelta(seconds=1))
                timestamps.append(end_date)
                timestamps.append(end_date+timedelta(seconds=1))

                busy_dict[peoples_names[idx]].append((start_date, end_date))

    timestamps = sorted(set(timestamps))
    # im adding extra elemnt, it will be end time of meeting
    # if any earlier time is not suitable
    timestamps.append(timestamps[-1]+dur_in_mins_dt_object)

    # creating pandas DataFrame with columns dates,
    # and avalibility of each person
    df = pd.DataFrame(timestamps, columns=["dates"])
    for name in peoples_names:
        df[name] = 1

    # setting 0 in timestamps when person is not avalible
    for person in busy_dict.keys():
        for start_date, end_date in busy_dict[person]:
            for idx, _ in enumerate(df[person]):
                if start_date <= df["dates"][idx] <= end_date:
                    df.loc[idx, person] = 0

    # setting meeting time in worst case scenario or
    # returning curent time if its later than
    # last elem in array
    if cur_time > timestamps[-2]:
        return cur_time
    else:
        metting_time = timestamps[-2]

    # iterating over every combination of people looking
    # for earliest time to start meeting

    # this is unnecesary, but if lets say we would like
    # to check avbability
    # for each combination of persons then this would be needed
    # for n_of_people in range(min_people,len(peoples_names)+1):

    for comb in itertools.combinations(peoples_names, min_people):
        # for 'debbuging purposes'
        # df['temp'] = df[list(comb)].all(axis='columns')
        # print(df)
        # creating pd.Series object that stores boolean values
        # if every person is avalible at give time
        s = pd.Series(df[list(comb)].all(axis='columns'))
        for _, x in s[s].groupby((1-s).cumsum()):
            if x.index[0] != x.index[-1]:
                time_avalibe = df["dates"][x.index[-1]]-df["dates"][x.index[0]]
                if time_avalibe >= dur_in_mins_dt_object:
                    if metting_time > df["dates"][x.index[0]] and cur_time < df["dates"][x.index[0]]:
                        metting_time = df["dates"][x.index[0]]
                        break
    return metting_time.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find closest avalible time slot")
    parser.add_argument(
        "--calendars", type=str, required=True,
        help="directory with people's calendars as *.txt files"
    )
    parser.add_argument(
        "--duration-in-minutes", type=int, required=True,
        help="How many minutes people should be available"
    )
    parser.add_argument(
        "--minumum-people", type=int, required=True,
        help="Minimum number of people that must be avalible"
    )
    # for debbuging purposes i have added
    # parser.add_argument("-v",'--verbose',action="store_true",
    # help="print meeting start time and avalible people")
    args = parser.parse_args()

    date = find_avalible_slot(args.calendars, args.duration_in_minutes, args.minumum_people)
    print(date)
