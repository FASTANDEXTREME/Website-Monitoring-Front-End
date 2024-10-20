import gspread
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
import asyncio

gc = gspread.service_account(filename="credentials.json")

async def update_graph():
    total_downtime = timedelta()  

    spreadsheet = gc.open("Website Monitoring")
    worksheet = spreadsheet.sheet1  

    ## CALCULATE TOTAL TIME OF MONITORING ##
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
    plt.figure(figsize=(10, 10))
    plt.pie(times, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#1f77b4', '#ff7f0e'])
    plt.axis('equal')  
    plt.title("Website Monitoring: Uptime vs Downtime")
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    plt.figtext(0.5, 0.01, f"Last Updated: {last_updated}", ha='center', fontsize=12)
    absolute_path = "static\images\graph.png"
    plt.savefig(absolute_path, bbox_inches='tight')
    plt.close()

async def scheduler():
    while True:
        await update_graph()
        await asyncio.sleep(15)  

async def main():
    await scheduler()

asyncio.run(main())