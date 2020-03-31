from apscheduler.schedulers.blocking import BlockingScheduler
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import sched, time
from datetime import datetime, timedelta
from django.conf import settings
settings.configure()
import os
from django.core.cache import cache
global sent
sent = False


def sendgrid_mail():
    message = Mail(
            from_email='from_email@example.com',
            to_emails='aviadm24@gmail.com',
            subject='Server stopped working',
            html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        # sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


def check_time():
    print("function check")
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(base)
    file = os.path.join(base, 'time.txt')
    with open(file, 'r') as f:
        date = f.read()
    time = datetime.strptime(date, '%b %d %Y %I:%M:%S')
    print("ping: ", time)
    print("now: ", datetime.now())
    delta = datetime.now() - time
    print('delta is: ', delta.seconds)
    if delta.seconds > 60:
        print('sending mail +++++++++++++++++++++++=')
        # if sent == False:
        #     sendgrid_mail()

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=10)
def timed_job():
    check_time()
    # print('Time is: ', time)


sched.start()
# baseurl = settings.__dict__
# print(baseurl)
# base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(base)
# f = os.path.join(base, 'time.txt')
# with open(f, 'r') as fle:
#     print(fle.read())