# Deploy Infrastructure with AWS CDK: Portfolio and EC2 Continuous Deployment

This project uses **AWS CDK** to deploy two distinct stacks for different purposes:
1. **Portfolio Stack**: Creates an S3 bucket and hosts static files for a portfolio website.
2. **EC2 Continuous Deployment Stack**: Sets up an EC2 instance configured for continuous deployment.

The architecture is simple, cost-effective, and scalable. Each stack can be deployed independently, allowing you to manage infrastructure for different projects within the same repository.

---

## Prerequisites

Before you begin, ensure the following are installed and configured:

- **Node.js** (LTS version or later)
- **Python 3.7+** with `pip`
- **AWS CLI** configured with credentials
- **AWS CDK** installed globally:
  ```bash
  npm install -g aws-cdk
  ```
- Virtual environment setup for Python:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate.bat
  pip install -r requirements.txt
  ```

---

## Project Structure

```
.
├── app.py
├── assets
├── cdk.json
├── cdk.out
├── aws_cdk_projects 
│   └── (stacks for various project)
├── portfolio_files 
│   └── (Static files for portfolio, e.g., index.html, css, js, images)
├── system_monitor_gui
│   └── (Files for EC2 continuous deployment setup)
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── source.bat
└── tests
```

---

## AWS Architecture for Projects

### 1. Portfolio Stack: S3 Bucket for Static Website Hosting
![Portfolio Stack Architecture](assets/cdk-s3-upload.png)

### 2. EC2 Continuous Deployment Stack: EC2 Instance for Continuous Deployment
![EC2 Stack Architecture](assets/cdk-ec2-cd.png)

---

## Steps to Deploy

### 1. Clone the Project

Clone the repository and navigate to the project directory.

```bash
git clone <repo-url>
cd <project-name>
```

### 2. Deploy the Portfolio Stack

#### Add Your Static Files
Place all portfolio static files (e.g., `index.html`, `css`, `images`, etc.) into the `portfolio_files` directory.

#### Synthesize the CDK Stack
Run the following command to generate the CloudFormation template for the Portfolio Stack:

```bash
cdk synth PortfolioStack
```

#### Deploy the S3 Bucket and Upload Files
Deploy the stack to your AWS account and region:

```bash
cdk deploy PortfolioStack
```

This will create:
- An S3 bucket for hosting the portfolio.
- Static files from the `portfolio_files` folder automatically uploaded to the S3 bucket.

#### Access Your Portfolio
Once the deployment is complete:
1. The S3 bucket's **Website URL** will be displayed in the terminal.
2. Open the URL in your browser to view the portfolio.

---

### 3. Deploy the EC2 Continuous Deployment Stack

#### Synthesize the CDK Stack
Run the following command to generate the CloudFormation template for the EC2 Stack:

```bash
cdk synth EC2CDStack
```

#### Deploy the EC2 Instance
Deploy the stack to your AWS account and region:

```bash
cdk deploy EC2CDStack
```

This will create:
- An EC2 instance configured for continuous deployment.
- Necessary security groups and IAM roles.

#### Access the EC2 Instance
Once the deployment is complete:
1. The **EC2 Instance ID** and **Public IP** will be displayed in the terminal.
2. Use SSH to connect to the instance and configure your deployment pipeline.

---

## Useful Commands

| Command                | Description                                      |
|------------------------|--------------------------------------------------|
| `cdk synth <StackName>`| Generates the CloudFormation template for a specific stack. |
| `cdk deploy <StackName>`| Deploys the specified stack to your AWS account. |
| `cdk destroy <StackName>`| Destroys the deployed stack.                     |
| `cdk diff <StackName>` | Compares the deployed stack with local changes.  |
| `cdk ls`               | Lists all stacks in the project.                 |

---

## Example Code

The core implementation is in the `app.py` file. Below are examples of the stacks:

### Portfolio Stack: S3 Bucket and File Upload
![Portfolio Stack Code](assets/code.png)

### EC2 Continuous Deployment Stack: EC2 Instance Setup
![EC2 Stack Code](assets/ec2-code.png)

---

## Cleanup

To delete the resources created by a specific stack:

```bash
cdk destroy <StackName>
```

For example:
- To delete the Portfolio Stack:
  ```bash
  cdk destroy PortfolioStack
  ```
- To delete the EC2 Continuous Deployment Stack:
  ```bash
  cdk destroy EC2CDStack
  ```

This will remove the resources associated with the specified stack.

---

### Notes:
- Ensure your static files include an `index.html` for proper website hosting in the Portfolio Stack.
- Use `.gitignore` to exclude sensitive or large files from version control.
- Each stack is independent and can be deployed