import datetime
import logging

#pip install azure-functions
import azure.functions as func

# CRON {0 */30 23-2 * * *} -> A cada Meia Hora a partir das 23 p.m. até 2 a.m. o sistema verificará a request
# CRON -> {{second}{minute}{hour}{day}{month}{day-of-week}} - https://crontab.guru/

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
