from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnOutput,
)
from constructs import Construct

vpcID = "vpc-0a5d901e206e8e488"
region="eu-west-1"
amiID="ami-03fd334507439f4d1"


class MyJenkinsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Import the existing VPC
        vpc = ec2.Vpc.from_lookup(self, "MyVpc",
            vpc_id=vpcID  
        )

        # Create a security group for the EC2 instance
        security_group = ec2.SecurityGroup(self, "MySecurityGroup",
            vpc=vpc,
            description="Allow SSH and HTTP access",
            allow_all_outbound=True
        )

        # Allow SSH access on port 22
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="Allow SSH access"
        )

        # Allow HTTP access on port 80
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow HTTP access"
        )

        # Allow access on port 8080 for Jenkins
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),  # Allows access from any IP
            connection=ec2.Port.tcp(8080),  # Opens TCP port 8080
            description="Allow Jenkins access on port 8080"
        )

        # Allow access on port 3000 for frontend web app
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),  # Allows access from any IP
            connection=ec2.Port.tcp(3000),  # Opens TCP port 3000
            description="Allow Jenkins access on port 3000"
        )


        # User data script to run on instance launch
        user_data_script = """#!/bin/bash
        sudo apt update -y && sudo apt upgrade -y

        # install docker
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh ./get-docker.sh

        # install java
        sudo apt install fontconfig openjdk-17-jre -y

        # install jenkins
        sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
        https://pkg.jenkins.io/debian/jenkins.io-2023.key
        echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
        https://pkg.jenkins.io/debian binary/ | sudo tee \
        /etc/apt/sources.list.d/jenkins.list > /dev/null
        sudo apt-get update
        sudo apt-get install jenkins -y
        """

        # Create the EC2 instance in the existing public subnet
        keypair=ec2.KeyPair.from_key_pair_name(self, "MyKeyPair", "todoLab")
        instance = ec2.Instance(self, "webServer",
            instance_type=ec2.InstanceType("t3.small"),
            machine_image=ec2.MachineImage.generic_linux({
                region: amiID 
            }),
            vpc=vpc,
            security_group=security_group,
            key_pair=keypair,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC  # Ensure the subnet is public
        ),
            associate_public_ip_address=True,  # ✅ Explicitly enable public IP
            user_data=ec2.UserData.custom(user_data_script)  # ✅ Runs script on launch
        )

        # Output the public IP of the instance
        CfnOutput(self, "InstancePublicIp",
            value=instance.instance_public_ip,
            description="Public IP of the EC2 instance"
        )

        # Output the instance ID for EC2 Instance Connect
        CfnOutput(self, "InstanceId",
            value=instance.instance_id,
            description="Instance ID for EC2 Instance Connect"
        )