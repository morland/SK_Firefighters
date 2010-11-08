#!/usr/bin/python

import datetime
import random

final_schedule = {}
start_date = datetime.datetime(2010, 11, 01)
end_date = datetime.datetime(2010, 12, 31)
default_duty_date = datetime.datetime(2010, 01, 01)
stint_length = 4

A = 0
B = 1


people = {
          1: {'name': 'MP', 'team': 'growth', 'unavailable': [], 'last_duty': default_duty_date, 'count': 0},
          2: {'name': 'MJ', 'team': 'growth', 'unavailable': [], 'last_duty': default_duty_date, 'count': 0},
          3: {'name': 'JW', 'team': 'growth', 'unavailable': [], 'last_duty': default_duty_date, 'count': 0},
          4: {'name': 'NF', 'team': 'data', 'unavailable': [], 'last_duty': default_duty_date, 'count': 0},
          5: {'name': 'RT', 'team': 'data', 'unavailable': [], 'last_duty': default_duty_date, 'count': 0},
          6: {'name': 'SL', 'team': 'platform', 'unavailable': [], 'last_duty': default_duty_date, 'count': 0},
          7: {'name': 'JC', 'team': 'platform', 'unavailable': [], 'last_duty': default_duty_date, 'count': 0},
          8: {'name': 'DL', 'team': 'platform', 'unavailable': [], 'last_duty': default_duty_date, 'count': 0}
          }

##### Company holidays here #####
company_holidays = []
#####

def date_range(start, end, just_dates=False):
  r = (end+datetime.timedelta(days=1)-start).days
  date_list = [start+datetime.timedelta(days=i) for i in range(r) \
              if (start+datetime.timedelta(days=i)).weekday() <= 4 \
              if (start+datetime.timedelta(days=i)) not in company_holidays]
  if just_dates == True: 
    return date_list
  else:
    return [(i + 1, date) for i, date in enumerate(date_list)]

def stint_dates(date):
  return [date+datetime.timedelta(days=i) for i in range(stint_length + 1)]

def person_picker(date, pair):
  available = [p for p in people \
               if len(set(stint_dates(date)).intersection(set(people[p]['unavailable']))) == 0] # get a list of people who are available within the stint
  different_team = [(p, people[p]['last_duty']) for p in available \
                    if people[p]['team'] != people[pair]['team']]   # narrow down the availability list to those not on the team of the other firefighter... assumption for now: there will always be at least one available dev outside the current firefighter's team
  longest_free = [i[0] for i in different_team \
                  if i[1] == min([p[1] for p in different_team])]  # narrow down the list to those who have been off firefighting the longest
  winner = longest_free[random.randrange(0, len(longest_free), 1)]  # choose one of the longest-free devs at random
  people[winner]['last_duty'] = date
  people[winner]['count'] = people[winner]['count'] + 1
  return winner

##### Put people's unavailable dates here #####
## example: ## people[1]['unavailable'].extend(date_range(datetime.datetime(2010, 11, 6), datetime.datetime(2010, 11, 18), just_dates=True))
#####

fire_range = date_range(start_date, end_date)
for day in fire_range:
  day_count = day[0]
  date = day[1]
  final_schedule[day_count] = {}
  final_schedule[day_count]['date'] = date
  if (day_count - 1) % 4 == 0: A = person_picker(date, B)
  if day_count == 1: B = person_picker(date, A)
  if (day_count + 1) % 4 == 0: B = person_picker(date, A)
  final_schedule[day_count]['A'] = people[A]['name']
  final_schedule[day_count]['B'] = people[B]['name']

print
if company_holidays:
  print 'Company holidays:', ' '.join([i.strftime('%a %d-%b') for i in company_holidays])
  print

print '\t'.join(['Person','count','unavailable_dates'])
for row in people:
  print '\t'.join([people[row]['name'], \
                  str(people[row]['count']), \
                  ' '.join([i.strftime('%a %d-%b') for i in people[row]['unavailable']])])

print
print '\t'.join(['day_count','date','A','B'])
for day_count in final_schedule:
  print '\t'.join([str(day_count), \
                  final_schedule[day_count]['date'].strftime('%a %d-%b'),\
                  final_schedule[day_count]['A'],\
                  final_schedule[day_count]['B']])