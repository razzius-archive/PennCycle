# Allows a description in a certain format to decide if a station is open or not.

import datetime

days = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}

strings = dict([v, k] for k, v in days.items())


def decimal(time):
    if len(time) <= 2:
        return int(time)
    else:
        hours, minutes = time.split(":")
        return int(hours) + float(minutes) / 60


def hour(time):
    return decimal(time[0]) if (time[1] == "am" or time[0] == "12") else decimal(time[0])+12


def enter_hours(interval, info, day):
    start_time = hour(info[0:2])
    end_time = hour(info[3:5])
    if day in interval:
        interval[day].append((start_time, end_time))
    else:
        interval[day] = [(start_time, end_time)]


def get_hours(description):
    intervals = {}
    day = 0
    if not description:  # empty station
        return {}
    for line in description.split("\n"):  # assumes to be in order
        if line.split()[1] == "-":  # there is a range of days
            # print("range of days")
            start = days[line.split()[0]]
            end = days[line.split()[2][:-1]]
            for i in range(end-start+1):
                that_day = strings[day]
                if "and" in line:  # multiple ranges
                    enter_hours(intervals, line.split()[3:8], that_day)
                    enter_hours(intervals, line.split()[9:14], that_day)
                else:
                    enter_hours(intervals, line.split()[3:8], that_day)
                day += 1
        elif line.split()[0][-1] == ":":
            # print("matched :")
            that_day = strings[day]
            if "and" in line:  # multiple ranges
                enter_hours(intervals, line.split()[1:6], that_day)
                enter_hours(intervals, line.split()[7:12], that_day)
            else:
                enter_hours(intervals, line.split()[1:6], that_day)
                day += 1
        else:  # 7 days a week.
            for day in range(7):
                enter_hours(intervals, line.split()[2:7], strings[day])
    return intervals


def is_open(description):
    ranges = get_hours(description)
    today = datetime.datetime.today().weekday()
    this_hour = datetime.datetime.today().hour
    if strings[today] in ranges:
        hours = ranges[strings[today]]
        for opening in hours:
            if this_hour > opening[0] and this_hour < opening[1]:
                return True
    return False