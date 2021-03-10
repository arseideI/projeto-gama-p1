from subprocess import call
import time
from apscheduler.schedulers.background import BackgroundScheduler
import os
#from UpdateBD import load_cases_covid_from_date

def job():
    print("In job")
    # call(['python', 'scheduler/main.py'])

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    # scheduler.configure(timezone=utc)
    scheduler.add_job(job, 'interval', seconds=1)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()