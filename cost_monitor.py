import boto3
import datetime
import smtplib
from email.mime.text import MIMEText
import os

# AWS Cost Explorer Client
client = boto3.client('ce', region_name='us-east-1')

# Email Configuration (environment variables)
SENDER_EMAIL = os.environ.get('mulappsrk@gmail.com')  #updated these files already
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL')
COST_THRESHOLD = float(os.environ.get('COST_THRESHOLD', '1.0'))

# Get current month AWS cost
today = datetime.date.today()
start = today.replace(day=1).strftime('%Y-%m-%d')
end = today.strftime('%Y-%m-%d')

response = client.get_cost_and_usage(
    TimePeriod={'Start': start, 'End': end},
    Granularity='MONTHLY',
    Metrics=['UnblendedCost']
)

cost = float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
print(f"Current AWS spend: ${cost:.2f}")

# Send alert if cost exceeds threshold
if cost > COST_THRESHOLD:
    msg = MIMEText(f"🚨 AWS Cost Alert: Your current spend is ${cost:.2f}")
    msg['Subject'] = 'AWS Cost Alert'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

    print("Alert email sent!")
else:
    print("Cost is within threshold.")
