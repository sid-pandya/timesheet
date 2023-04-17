# from flask import Flask, render_template, request, redirect, url_for

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("home.html")

# @app.route("/hours", methods=["POST"])
# def calculate_hours():
#     week_start = request.form["week-start"]
#     hours = [
#         float(request.form["hours-mon"]),
#         float(request.form["hours-tue"]),
#         float(request.form["hours-wed"]),
#         float(request.form["hours-thu"]),
#         float(request.form["hours-fri"])
#     ]
#     total_hours = sum(hours)
#     return redirect(url_for("hours_view", week_start=week_start, total_hours=total_hours))


# @app.route("/hours/<week_start>/<total_hours>")
# def hours_view(week_start, total_hours):
#     return render_template("hours_view.html", week_start=week_start, total_hours=total_hours)


# # Define routes and view functions here
# @app.route("/month/<month>")
# def view_month(month):
#     # Convert month string to integer
#     month_int = int(month)

#     # Calculate start and end dates for the selected month
#     start_date = f"2023-{month_int:02d}-01"
#     end_date = f"2023-{month_int:02d}-31"

#     # TODO: Query database to retrieve working hours for selected month
#     # Example query: SELECT * FROM hours WHERE date >= start_date AND date <= end_date

#     # Render template with working hours data
#     return render_template("month.html", month=month_int, start_date=start_date, end_date=end_date)

# from flask import Flask, render_template, request

# app = Flask(__name__)

# # Dummy data for demonstration purposes
# days = [
#     {'id': 1, 'date': '2022-01-01', 'time_in': '09:00', 'time_out': '17:00', 'break_time': 1},
#     {'id': 2, 'date': '2022-01-02', 'time_in': '08:30', 'time_out': '16:30', 'break_time': 0},
#     {'id': 3, 'date': '2022-01-03', 'time_in': '09:15', 'time_out': '17:15', 'break_time': 1.5},
#     {'id': 4, 'date': '2022-01-04', 'time_in': '09:30', 'time_out': '17:30', 'break_time': 1},
#     {'id': 5, 'date': '2022-01-05', 'time_in': '08:45', 'time_out': '16:45', 'break_time': 0},
# ]

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         # Update the dummy data with the submitted form values
#         for day in days:
#             day['time_in'] = request.form[f"{day['id']}-time_in"]
#             day['time_out'] = request.form[f"{day['id']}-time_out"]
#             day['break_time'] = request.form[f"{day['id']}-break_time"]
        
#         # Calculate the total working hours
#         total_hours = sum((float(day['time_out'].replace(':', '.')) - float(day['time_in'].replace(':', '.')) - float(day['break_time'])) for day in days)
#         total_hours = f"{int(total_hours)}:{int((total_hours - int(total_hours)) * 60):02d}"
        
#         return render_template('home.html', days=days, total_hours=total_hours)
#     else:
#         # Calculate the total working hours
#         total_hours = sum((float(day['time_out'].replace(':', '.')) - float(day['time_in'].replace(':', '.')) - float(day['break_time'])) for day in days)
#         total_hours = f"{int(total_hours)}:{int((total_hours - int(total_hours)) * 60):02d}"
        
#         return render_template('home.html', days=days, total_hours=total_hours)

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request
from datetime import datetime, timedelta
from db import Database
import json

app = Flask(__name__)

@app.route('/')
def timesheet():
    # Get the week offset from the request args
    week_offset = int(request.args.get('week_offset', '0'))

    # Create a list of dates for the current week
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    dates = [start_of_week + timedelta(days=i) for i in range(7)]
    
    # Create a list of rows for the time sheet
    rows = []
    for date in dates:
        row = {'date': date.strftime('%m/%d/%Y (%a)'),'day':  date.strftime('%Y:%m:%d'), 'time_in': '', 'time_out': ''}
        rows.append(row)

    # Render the template with the rows and week offset
    return render_template('timesheet.html', rows=rows, week_offset=week_offset)

@app.route('/submithours',methods=['POST'])
def write_hours():
    db = Database("database.db")
    timesheet_data = json.loads(request.get_json())
    year, month, day = timesheet_data[0][:10].split("-")
    finalString = year+'-'+month+'-'+day
    ifExist = db.read_timesheet(finalString);
    if(len(ifExist) > 0):
        print(json.dumps(timesheet_data[1]))
        db.update_timesheet((json.dumps(timesheet_data[1]),timesheet_data[0]))
    else:
        db.write_timesheet((timesheet_data[0],json.dumps(timesheet_data[1]),timesheet_data[2]))
    # Close the database connection
    db.close()
    return 'true';

@app.route('/gethours')
def get_hours():
    db = Database("database.db")
    data = db.read_timesheet(request.args['week'])
    # Close the database connection
    db.close()
    return data;

if __name__ == '__main__':
    app.run(debug=True)
