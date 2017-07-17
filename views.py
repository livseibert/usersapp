from flask import Flask, render_template, request, session
from datetime import datetime, date, timedelta
import csv, codecs
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)
app.secret_key = 'sec_key'

@app.route('/')
def index():
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
    rows=len(dates)
    for date in dates:
        count=0
        csv_name='/Users/liviaseibert/usersapp/data/' + date.strftime('%Y-%m-%d')+'-cavatica_users.csv'
        names.append(date.strftime('%Y-%m-%d'))
        f = open(csv_name)
        csv_f = csv.reader(f)
        for row in csv_f:
            count += 1
        counts.append(count)
    d=np.array(dates)
    u=np.array(counts)
    plt.plot(d,u)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.xlabel('dates')
    plt.ylabel('users')
    plt.title('Date vs. Users')
    timestr = datetime.now().strftime("%H%M%S")
    plt.savefig('/Users/liviaseibert/usersapp/static/graph.png')
    return render_template('index.html', dates=dates, counts=counts, rows=rows, names=names, today=timestr)

@app.route('/more_info/<date>/<sort>/<switch>')
def more_info(date, sort, switch):
    csv_name='/Users/liviaseibert/usersapp/data/' + date +'-cavatica_users.csv'
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
