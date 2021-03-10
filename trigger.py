from subprocess import call
import time
from apscheduler.schedulers.background import BackgroundScheduler
import os
from UpdateDB import load_cases_covid_from_date


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(load_cases_covid_from_date, 'interval', minutes=60)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()