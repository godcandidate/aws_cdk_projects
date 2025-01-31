#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws_cdk_projects.portfolio_cdk_app_stack import PortfolioCdkAppStack
from aws_cdk_projects.ec2_setup_stack import MyEc2Stack
from dotenv import load_dotenv 

# Load environment variables from .env file
load_dotenv()

# Get AWS account, region, and VPC ID from environment variables
env = cdk.Environment(
    account=os.getenv("AWS_ACCOUNT"),
    region=os.getenv("AWS_REGION")
)
app = cdk.App()

# Define and add stacks
portfolio_stack = PortfolioCdkAppStack(app, "PortfolioCdkAppStack")
ec2_stack = MyEc2Stack(app, "MyEc2Stack", env=env)

app.synth()
