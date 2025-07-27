from collections import defaultdict, Counter
from typing import List, Dict, Any

monday_visitors = {"user1", "user2", "user3", "user4", "user5"}
tuesday_visitors = {"user2", "user4", "user6", "user7", "user8"}
wednesday_visitors = {"user1", "user3", "user6", "user9", "user10"}

# Unique Visitors Across All Days
# Find the total number of unique visitors who visited on any of the three days.
def unique_visitors(monday_visitors:set,tuesday_visitors:set,wednesday_visitors:set):
    all_visitors = monday_visitors.union(tuesday_visitors,wednesday_visitors   )
    print(len(all_visitors))

unique_visitors(monday_visitors, tuesday_visitors, wednesday_visitors)

# Returning Visitors on Tuesday
# Identify users who visited on both Monday and Tuesday.
def returning_visitors(monday_visitors:set, tuesday_visitors:set):
    print( monday_visitors.intersection(tuesday_visitors))

returning_visitors(monday_visitors, tuesday_visitors)



# New Visitors Each Day
# Determine which users visited for the first time each day (i.e., not seen on previous days).
def new_visitors(monday_visitors:set,tuesday_visitors:set,wednesday_visitors:set):
    new_on_tuesday = tuesday_visitors - monday_visitors
    new_on_wednesday = wednesday_visitors - (monday_visitors.union(tuesday_visitors))
    print("New visitors on Tuesday:", new_on_tuesday)
    print("New visitors on Wednesday:", new_on_wednesday)

new_visitors(monday_visitors, tuesday_visitors, wednesday_visitors)


# Loyal Visitors
# Find users who visited the site on all three days.
def loyal_visitors(monday_visitors:set, tuesday_visitors:set, wednesday_visitors:set):
    loyal = monday_visitors.intersection(tuesday_visitors, wednesday_visitors)
    print("Loyal visitors:", loyal)

loyal_visitors(monday_visitors, tuesday_visitors, wednesday_visitors)


# Daily Visitor Overlap Analysis
# Compare and print overlaps between each pair of days (e.g., Monday-Tuesday, Tuesday-Wednesday, etc.).
def daily_overlap_analysis(monday_visitors:set, tuesday_visitors:set, wednesday_visitors:set):
    overlap_monday_tuesday = monday_visitors.intersection(tuesday_visitors)
    overlap_tuesday_wednesday = tuesday_visitors.intersection(wednesday_visitors)
    overlap_monday_wednesday = monday_visitors.intersection(wednesday_visitors)
    
    print("Overlap between Monday and Tuesday:", overlap_monday_tuesday)
    print("Overlap between Tuesday and Wednesday:", overlap_tuesday_wednesday)
    print("Overlap between Monday and Wednesday:", overlap_monday_wednesday)

daily_overlap_analysis(monday_visitors, tuesday_visitors, wednesday_visitors)

