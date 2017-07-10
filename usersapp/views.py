from flask import Flask, render_template
from datetime import datetime, date, timedelta
import csv, codecs

app = Flask(__name__)

@app.route('/')
def index():
    dates=[]
    start_date = datetime(2017,06,8)
    end_date = datetime(2017,06,27)
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
    return render_template('index.html', dates=dates, counts=counts, rows=rows, names=names)

@app.route('/more_info/<date>')
def more_info(date):
    csv_name='/Users/liviaseibert/usersapp/data/' + date +'-cavatica_users.csv'
    f = codecs.open(csv_name, encoding='ascii', errors='ignore')
    csv_f = csv.reader(f)
    usernames=[]
    affiliations=[]
    times_created=[]
    emails=[]
    first_names=[]
    last_names=[]
    rows=0
    for row in csv_f:
        usernames.append(row[0])
        affiliations.append(row[1])
        times_created.append(row[2])
        emails.append(row[3])
        first_names.append(row[4])
        last_names.append(row[5])
        rows+=1
    return render_template('more_info.html', usernames=usernames, affiliations=affiliations, times_created=times_created, emails=emails, first_names=first_names, last_names=last_names, rows=rows)

if __name__ == '__main__':
    db.create_all()
    app.run()
