import sys
import csv
import time
import calendar
import matplotlib.pyplot as plt
from collections import OrderedDict
from datetime import date, timedelta as td

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'Please insert processed twitdata.csv'
        exit()

    twitReader = csv.DictReader(open(sys.argv[1], 'rb'), delimiter = ',', fieldnames=['uid','lat','lon','province','province_abbr','province_abbr_index','epoch','date','time'])

    hourFreq = [0 for x in range(24)]
    # TODO
    hourFreqDays = [[0 for x in range(24)] for y in range(7)]
    dayFreq = [0 for x in range(7)]
    everyDayFreq = {}
    twitReader.next()
    for twit in twitReader:
        tTime = time.strptime(twit['time'],'%H:%M:%S')
        hourFreq[tTime.tm_hour] += 1

        tDay = time.strptime(twit['date'], '%Y-%m-%d')
        dayFreq[calendar.weekday(tDay.tm_year, tDay.tm_mon, tDay.tm_mday)] += 1

        tDayTuple = str(tDay.tm_year)+'-'+str(tDay.tm_mon)+'-'+str(tDay.tm_mday)
        if tDayTuple not in everyDayFreq:
            everyDayFreq[tDayTuple] = 1
        else:
            everyDayFreq[tDayTuple] += 1

    everyDayFreq = OrderedDict(sorted(everyDayFreq.items()))
    dStart = time.strptime(everyDayFreq.keys()[0], '%Y-%m-%d')
    dStart = date(dStart.tm_year, dStart.tm_mon, dStart.tm_mday)
    dEnd = time.strptime(everyDayFreq.keys()[-1], '%Y-%m-%d')
    dEnd = date(dEnd.tm_year, dEnd.tm_mon, dEnd.tm_mday)
    delta = dEnd - dStart
    fullEveryDayFreq = OrderedDict()
    weekDayCount = OrderedDict()
    for i in range(7):
        weekDayCount[i] = []
    for i in range(delta.days+1):
        tempDay = time.strptime(str(dStart + td(days=i)), '%Y-%m-%d')
        dayStr = str(tempDay.tm_year)+'-'+str(tempDay.tm_mon)+'-'+str(tempDay.tm_mday)
        fullEveryDayFreq[dayStr] = 0
        weekDay = calendar.weekday(tempDay.tm_year, tempDay.tm_mon, tempDay.tm_mday)
        if dayStr not in weekDayCount[weekDay]:
            weekDayCount[weekDay].append(dayStr)

    for day in everyDayFreq.items():
        fullEveryDayFreq[day[0]] = day[1]

    for i in range(7):
        try:
            dayFreq[i] /= len(weekDayCount[i])
        except:
            pass

    # Plot tweet freq by day hour
    plt.plot(hourFreq, 'ro', hourFreq, 'b-')
    plt.xticks(range(24))
    plt.xlabel('Hour during the day')
    plt.ylabel('Number of tweet')
    plt.title('Tweet frequency during the day')
    plt.show()

    exit()
    # Plot tweet freq by day in week
    plt.plot(dayFreq, 'ro', dayFreq, 'b-')
    plt.xticks(range(7), ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
    plt.xlabel('Day')
    plt.ylabel('Mean number of tweet')
    plt.title('Tweet frequency by day in week')
    plt.show()

    # Plot tweet freq in every day of collected data
    plt.plot(fullEveryDayFreq.values(), 'ro', fullEveryDayFreq.values(), 'b-')
    plt.xticks(range(len(fullEveryDayFreq.values())), fullEveryDayFreq.keys(), rotation = 'vertical')
    plt.xlabel('Date')
    plt.ylabel('Number of tweet')
    plt.title('Tweet frequency of overall collected data')
    plt.show()