AWS Cost Monitor with Email Alerts

Overview

A lightweight Python script that checks current AWS cost and sends an alert email if the cost exceeds a predefined threshold.

Tech Stack

Python 3

AWS Boto3 (Cost Explorer)

Amazon SES (Email Service)

Docker

Cron (Scheduled Execution)

Setup Instructions

Clone the repository:git clone https://github.com/Yusufshaik19/aws_costmanagement_alerts.git


Environment Variables:
Export the following variables inside your EC2 instance or Docker container:

export SENDER_PASSWORD='your_app_password'
export RECEIVER_EMAIL='receiver_email@example.com'
export COST_THRESHOLD='1.0'

Run Locally (Direct Python):
python3 cost_monitor.py



Run via Docker:
docker build -t aws-cost-monitor-app .
docker run --rm aws-cost-monitor-app




Email Configuration

Use Amazon SES to verify email addresses.

Generate an App Password for secure login if using Gmail.

Automating with Cron

1.Create Shell Script: run_cost_monitor.sh
#!/bin/bash
cd /home/ec2-user/aws_costmanagement_alerts
docker stop cost-monitor 2>/dev/null || true
docker rm cost-monitor 2>/dev/null || true
docker build -t aws-cost-monitor-app .
docker run --rm aws-cost-monitor-app



Make it executable
chmod +x run_cost_monitor.sh

Set Cron Job:
crontab -e

logs
cat /home/ec2-user/aws_costmanagement_alerts/cron_log.txt
