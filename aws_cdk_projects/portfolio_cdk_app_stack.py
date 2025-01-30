from aws_cdk import (
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    RemovalPolicy,
    Stack, CfnOutput
)
from constructs import Construct

class PortfolioCdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        try:
            # Create an S3 bucket for hosting the portfolio
            portfolio_bucket = s3.Bucket(
                self,
                "PortfolioBucket",
                website_index_document="index.html",  # Set index.html as the entry point
                public_read_access=True,             # Enable public read access
                block_public_access=s3.BlockPublicAccess.BLOCK_ACLS,  # Allow public access
                removal_policy=RemovalPolicy.DESTROY,  # Allow CDK to delete the bucket
                auto_delete_objects=True  # Ensures objects are removed before deletion
            )
            
            # Output the bucket name
            CfnOutput(
                self, "BucketName",
                value=portfolio_bucket.bucket_name,
                description="The name of the S3 bucket"
            )

        except Exception as e:
            print(f"Error creating S3 bucket: {e}")
            return

        try:
            # Deploy static asset files to the S3 bucket
            deployment = s3_deployment.BucketDeployment(
                self,
                "DeployPortfolioAssets",
                sources=[s3_deployment.Source.asset("./portfolio_files")],  # Path to your static files
                destination_bucket=portfolio_bucket,
            )
            # Output the bucket website URL
            CfnOutput(
                self, "WebsiteURL",
                value=portfolio_bucket.bucket_website_url,
                description="The URL of the S3 bucket hosting the portfolio website"
            )

        except Exception as e:
            print(f"Error deploying static files to S3 bucket: {e}")
            return

