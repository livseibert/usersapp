from flask import Flask, render_template, request, session
from datetime import datetime, date, timedelta
import csv, codecs
import matplotlib.pyplot as plt
import numpy as np
import os, os.path, sys

app = Flask(__name__)
app.secret_key = 'sec_key'

app.config.update(dict(
    DATA_PATH="/Users/liviaseibert/usersapp/data",
    STATIC_PATH="/Users/liviaseibert/usersapp/static"
))

@app.route('/')
def index():
    url=os.path.join(app.config['STATIC_PATH'], 'graph.png')
    if os.path.isfile(url):
        os.remove(url)
    return render_template('form.html')

@app.route('/results', methods = ['POST'])
def index_res():
    dates=[]
    start_date=request.form['start']
    end_date=request.form['end']
    start_date=datetime.strptime(start_date, "%Y-%m-%d")
    end_date=datetime.strptime(end_date, "%Y-%m-%d")
    step = timedelta(days=1)
    while start_date <= end_date:
        dates.append(start_date)
        start_date += step
    counts=[]
    names=[]
    e_dates=[]
    show_li=[]
    rows=len(dates)
    for date in dates:
        count=0
        csv_name=os.path.join(app.config['DATA_PATH'], date.strftime('%Y-%m-%d')+'-cavatica_users.csv')
        names.append(date.strftime('%Y-%m-%d'))
        if os.path.isfile(csv_name):
            f = open(csv_name)
            csv_f = csv.reader(f)
            for row in csv_f:
                count += 1
            counts.append(count)
            show_li.append(True)
        else:
            counts.append("no data")
            e_dates.append(date)
            show_li.append(False)
    if len(dates)==len(e_dates):
        yes=False
    else:
        yes=True
        update_plot(dates, counts, e_dates)
    timestr = datetime.now().strftime("%H%M%S")
    return render_template('index.html', dates=dates, counts=counts, rows=rows, names=names, today=timestr, yes=yes, show_li=show_li)

def update_plot(da, c, e):
    background_color = '#2f3f4f'
    text_color = '#ffffff'
    graph_color = '#7fffd4'
    new_dates=[]
    nums=list(c)
    while "no data" in nums:
        nums.remove("no data")
    new_dates=[elem for elem in da if elem not in e]
    for i in nums:
        print i
    for i in new_dates:
        print i
    d=np.array(new_dates)
    u=np.array(nums)
    plt.plot(d, u, marker='o', color=graph_color)
    plt.xticks(rotation=45)
    plt.gcf().subplots_adjust(bottom=0.25) #Add margin on the bottom
    plt.xlabel('Date', color=text_color)
    plt.ylabel('# of Users', color=text_color)
    plt.yticks(np.arange(min(u)-5, max(u)+5, 1)) #Make ticks only integers (can't have fractions of users)
    plt.title('# Users over Time', color=text_color)
    ax = plt.gca()
    ax.set_facecolor(background_color)
    ax.tick_params(colors=text_color)
    for spine in ax.spines.values():
        spine.set_edgecolor(text_color)

    plt.savefig(os.path.join(app.config['STATIC_PATH'], 'graph.png'), facecolor=background_color)
    plt.close()

@app.route('/more_info/<date>/<sort>/<switch>')
def more_info(date, sort, switch):
    csv_name=os.path.join(app.config['DATA_PATH'], date+'-cavatica_users.csv')
    f = codecs.open(csv_name, encoding='ascii', errors='ignore')
    csv_f = csv.reader(f)
    rows=list(csv_f)
    numrows=len(rows)
    unswitch=1-int(switch)
    if sort=='username':
        rows=sortli(rows, 0, unswitch)
    elif sort=='affiliation':
        rows=sortli(rows, 1, unswitch)
    elif sort=='timecr' and unswitch==1:
        for i in range(1,numrows):
            index=i;
            for j in range (i+1,numrows):
                if datetime.strptime(rows[j][2], "%Y-%m-%d %H:%M:%S")<datetime.strptime(rows[index][2], "%Y-%m-%d %H:%M:%S"):
                    index=j
            smallerNum=rows[index]
            rows[index]=rows[i]
            rows[i]=smallerNum
    elif sort=='timecr' and unswitch==0:
        for i in range(1,numrows):
            index=i;
            for j in range (i+1,numrows):
                if datetime.strptime(rows[j][2], "%Y-%m-%d %H:%M:%S")>datetime.strptime(rows[index][2], "%Y-%m-%d %H:%M:%S"):
                    index=j
            smallerNum=rows[index]
            rows[index]=rows[i]
            rows[i]=smallerNum
    elif sort=='email':
        rows=sortli(rows, 3, unswitch)
    elif sort=='first':
        rows=sortli(rows, 4, unswitch)
    elif sort=='last':
        rows=sortli(rows, 5, unswitch)
    return render_template('more_info.html', rows=rows, numrows=numrows, date=date, sort=sort, switch=unswitch)

def sortli(li, pos, num):
    if num==1:
        for i in range(1,len(li)):
            index=i;
            for j in range (i+1,len(li)):
                if li[j][pos].lower()<li[index][pos].lower():
                    index=j
            smallerNum=li[index]
            li[index]=li[i]
            li[i]=smallerNum
    else:
        for i in range(1,len(li)):
            index=i;
            for j in range (i+1,len(li)):
                if li[j][pos].lower()>li[index][pos].lower():
                    index=j
            smallerNum=li[index]
            li[index]=li[i]
            li[i]=smallerNum
    return li

if __name__ == '__main__':
    db.create_all()
    app.run()
