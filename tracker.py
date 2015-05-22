# coding: utf-8

import ui
import sqlite3
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt

SQL_TABLE = '''
CREATE TABLE tracker (
timestamp DATE,
time_type TEXT,
hours REAL);
'''

def create_pie(info):
    # make a square figure and axes
    print info
    plt.figure(1, figsize=(6,6))
    ax = plt.axes([0.1, 0.1, 0.8, 0.8])

    # The slices will be ordered and plotted counter-clockwise.
    labels = 'Wife', 'Family', 'Friends', 'Solo'
    fracs = [info['Wife'], info['Family'], info['Friends'], info['Solo']]
    explode=(0, 0, 0, 0)

    plt.pie(fracs, explode=explode, labels=labels,
                autopct='%1.1f%%', shadow=True, startangle=90)
                # The default startangle is 0, which would start
                # the Frogs slice on the x-axis.  With startangle=90,
                # everything is rotated counter-clockwise by 90 degrees,
                # so the plotting starts on the positive y-axis.

    plt.title('Time Spent', bbox={'facecolor':'0.8', 'pad':5})

    plt.savefig('test.jpg')
    plt.close()

def query(length=None):
    if length == None:
        date_delta = timedelta(days=100000)
    else:
        date_delta = length
    start_date = datetime.date(datetime.now()) - date_delta
    conn = sqlite3.connect('tracker.db')
    cur = conn.cursor()
    cur.execute('select time_type, hours from tracker where timestamp >= ?', (start_date,))
    output = {'Wife':0, 'Family': 0, 'Friends': 0, 'Solo':0}
    for entry in cur.fetchall():
        if entry[0] == 'Wife':
            output['Wife'] += entry[1]
        elif entry[0] == 'Family':
            output['Family'] += entry[1]
        elif entry[0] == 'Friends':
            output['Friends'] += entry[1]
        elif entry[0] == 'Solo':
            output['Solo'] += entry[1]
    return output
            
def reload():
    year = query(timedelta(days=365))
    month = query(timedelta(weeks=4))
    week = query(timedelta(weeks=1))
    day = query(timedelta(minutes=1))
    create_pie(day)
    

def button_tapped(sender):
    date = datetime.date(datetime.now())
    time_type = v['types'].segments[v['types'].selected_index]
    hours = float(v['tb1'].text)
    print date
    if hours != '':
        conn = sqlite3.connect('tracker.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO tracker VALUES(?, ?, ?)", (date, time_type, hours,))
        conn.commit()
        conn.close()
        v['tb1'].text = ''
        seg_changed(v['sg2'])
        
        
def seg_changed(sender):
    selection =  sender.segments[sender.selected_index]
    if selection == 'Day':
        day = query(timedelta(minutes=1))
        create_pie(day)
    elif selection == 'Week':
        week = query(timedelta(weeks=1))
        create_pie(week)
    elif selection == 'Month':
        month = query(timedelta(weeks=4))
        create_pie(month)
    elif selection == 'All':
        all = query(timedelta(days=1000))
        create_pie(all)
    v['im1'].image = ui.Image.named('test.jpg')


if not os.path.isfile('tracker.db'):
    conn = sqlite3.connect('tracker.db')
    cur = conn.cursor()
    cur.executescript(SQL_TABLE)
    conn.commit()
    

v = ui.load_view()
v['button1'].action = button_tapped
v['sg2'].action = seg_changed

v.present('fullscreen')