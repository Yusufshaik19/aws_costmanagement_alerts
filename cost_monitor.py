import boto3
import datetime
import os

# AWS Cost Explorer Client (Always use us-east-1 for billing)
ce_client = boto3.client('ce', region_name='us-east-1')

# AWS SES Client (Same region as your SES setup)
ses_client = boto3.client('ses', region_name='eu-north-1')  # Change if needed

# Configuration: Set these as environment variables in your deployment
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')        # e.g. mullapsrk@gmail.com (SES Verified)
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL')    # e.g. mullapsrk@gmail.com (SES Verified)
COST_THRESHOLD = float(os.environ.get('COST_THRESHOLD', '1.0'))

# Get current month AWS cost
today = datetime.date.today()
start = today.replace(day=1).strftime('%Y-%m-%d')
end = today.strftime('%Y-%m-%d')

response = ce_client.get_cost_and_usage(
    TimePeriod={'Start': start, 'End': end},
    Granularity='MONTHLY',
    Metrics=['UnblendedCost']
)

cost = float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
print(f"Current AWS spend: ${cost:.2f}")

# Send email alert using SES if cost exceeds threshold
if cost > COST_THRESHOLD:
    subject = "🚨 AWS Cost Alert"
    body_text = f"Your current AWS spend is ${cost:.2f}, which exceeds your threshold of ${COST_THRESHOLD:.2f}."

    response = ses_client.send_email(
        Source=SENDER_EMAIL,
        Destination={'ToAddresses': [RECEIVER_EMAIL]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body_text}}
        }
    )

    print("✅ Alert email sent via SES!")
else:
    print("✅ Cost is within threshold.")
