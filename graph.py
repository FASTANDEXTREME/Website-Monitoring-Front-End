import gspread
from datetime import timedelta, datetime
import plotly.graph_objects as go
import schedule
import os
import time

gc = gspread.service_account(filename="credentials.json")

def update_graph():
    total_downtime = timedelta()  
    spreadsheet = gc.open("Website Monitoring")
    worksheet = spreadsheet.sheet1  

    ## CALCULATE TOTAL TIME OF MONITORING #
    dates = worksheet.col_values(4) 
    times = worksheet.col_values(5)  
    timestamps = [datetime.strptime(f"{date} {time}", "%d/%m/%Y %I:%M:%S %p") for date, time in zip(dates[1:], times[1:])]
    first_log = timestamps[0] 
    last_log = timestamps[-1]   
    total_monitoring_time = last_log - first_log
    ########################################################

    ## CODE TO CALCULATE DOWNTIME ##
    downtime_column = worksheet.col_values(6)  
    for downtime in downtime_column[1:]:  
        if downtime:  
            h, m, s = map(int, downtime.split(":"))  
            total_downtime += timedelta(hours=h, minutes=m, seconds=s)

    # Calculating uptime and making chart ##
    total_uptime = total_monitoring_time - total_downtime

    labels = ['Uptime', 'Downtime']
    times = [total_uptime.total_seconds(), total_downtime.total_seconds()]  
    fig = go.Figure(data=[go.Pie(labels=labels, values=times, hole=.3)])
    fig.update_traces(marker=dict(colors=['#1f77b4', '#ff7f0e']),
                      hoverinfo='label+percent',  # Show percent on hover
                      textinfo='percent',         # Show percent in text
                      textfont_size=15)
    
    fig.update_layout(title="Website Monitoring: Uptime vs Downtime", title_x=0.5)
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fig.add_annotation(
        x=0.5,
        y=-0.1,
        text=f"Last Updated: {last_updated}",
        showarrow=False,
        font=dict(size=12),
        xref="paper", yref="paper"
    )

    relative_path = os.path.join("static", "images", "graph.png")
    fig.write_image(relative_path, format="png") 

schedule.every(15).seconds.do(update_graph)
while True:
    schedule.run_pending()
    time.sleep(1)


