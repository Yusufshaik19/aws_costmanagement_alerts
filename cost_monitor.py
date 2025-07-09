import boto3
import datetime
import smtplib
from email.mime.text import MIMEText

# AWS setup
client = boto3.client('ce', region_name='us-east-1')  # Keep us-east-1 for Cost Explorer

# Email settings
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"
RECEIVER_EMAIL = "receiver_email@gmail.com"
COST_THRESHOLD = 1.0  # USD

# Get today's cost
today = datetime.date.today()
start = today.replace(day=1).strftime('%Y-%m-%d')
end = today.strftime('%Y-%m-%d')

response = client.get_cost_and_usage(
    TimePeriod={'Start': start, 'End': end},
    Granularity='MONTHLY',
    Metrics=['UnblendedCost']
)

cost = float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])

# Send email if over threshold
if cost > COST_THRESHOLD:
    msg = MIMEText(f"AWS Cost Alert: Your current spend is ${cost:.2f}")
    msg['Subject'] = 'AWS Cost Alert'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

print(f"Current AWS Spend: ${cost:.2f}")
