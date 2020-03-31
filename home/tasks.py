from background_task import background
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import sched, time
from datetime import datetime, timedelta

global sent
sent = False
s = sched.scheduler(time.time, time.sleep)


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
    with open('time.txt', 'r') as f:
        date = f.read()

    time = datetime.strptime(date, '%b %d %Y %I:%M:%S')
    print("ping: ", time)
    print("now: ", datetime.now())
    delta = datetime.now() - time - timedelta(hours=12, minutes=0)
    print('delta is: ', delta.seconds)
    if delta.seconds > 60:
        print('sending mail +++++++++++++++++++++++=')
        # if sent == False:
        #     sendgrid_mail()
            # sent = True


# https://django-background-tasks.readthedocs.io/en/latest/
@background(schedule=10)
def notify_user():
    print('notifiy user function')
    check_time()