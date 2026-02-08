#!/usr/bin/env python3
"""
Sentinel Watcher - EC2 Instance Monitoring Script
Monitors EC2 instances in us-east-1 and alerts on stopped instances.
"""

import sys
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def trigger_healing(instance_id):
    """
    Placeholder function for triggering self-healing via GitHub Copilot CLI.
    
    This function will be used to invoke the Copilot CLI to automatically
    diagnose and fix issues with stopped EC2 instances.
    
    Args:
        instance_id (str): The ID of the stopped EC2 instance to heal
        
    Future implementation will:
    - Call GitHub Copilot CLI with appropriate context
    - Request automated diagnosis and fix recommendations
    - Execute healing actions based on Copilot's suggestions
    """
    print(f"[HEALING] Placeholder: Would trigger healing for {instance_id}")


def print_bold(text):
    """Print text in bold using ANSI escape codes."""
    print(f"\033[1m{text}\033[0m")


def check_ec2_instances():
    """
    Check EC2 instances in us-east-1 region and alert on stopped instances.
    
    Returns:
        int: Number of stopped instances found
    """
    region = 'us-east-1'
    
    try:
        # Create EC2 client for us-east-1
        ec2_client = boto3.client('ec2', region_name=region)
        
        print(f"Checking EC2 instances in {region}...")
        
        # Describe all instances
        response = ec2_client.describe_instances()
        
        stopped_count = 0
        total_count = 0
        
        # Iterate through reservations and instances
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                total_count += 1
                instance_id = instance['InstanceId']
                state = instance['State']['Name']
                
                # Check if instance is stopped
                if state == 'stopped':
                    stopped_count += 1
                    print_bold(f"🚨 ALERT: Instance {instance_id} is STOPPED!")
                    trigger_healing(instance_id)
        
        print(f"\nSummary: {total_count} instances checked, {stopped_count} stopped")
        return stopped_count
        
    except NoCredentialsError:
        print("ERROR: AWS credentials not found. Please configure AWS CLI or set environment variables.", file=sys.stderr)
        sys.exit(1)
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'UnauthorizedOperation':
            print(f"ERROR: Not authorized to describe EC2 instances in {region}.", file=sys.stderr)
        else:
            print(f"ERROR: AWS API error - {e.response['Error']['Message']}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected error - {str(e)}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the script."""
    print("🛡️  Sentinel Watcher - EC2 Monitoring")
    print("=" * 50)
    
    stopped_count = check_ec2_instances()
    
    if stopped_count == 0:
        print("\n✅ All instances are running normally!")
    else:
        print(f"\n⚠️  Found {stopped_count} stopped instance(s) requiring attention.")


if __name__ == "__main__":
    main()
