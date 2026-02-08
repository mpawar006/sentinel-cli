#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sentinel Watcher - EC2 Instance Monitoring Script
Monitors EC2 instances in us-east-1 and alerts on stopped instances.
"""

import sys
import argparse
import subprocess
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def trigger_healing(instance_id):
    """
    Trigger self-healing via GitHub Copilot CLI.
    
    Uses Copilot CLI to suggest an AWS CLI command to restart the stopped instance,
    then prompts user for approval before executing.
    
    Args:
        instance_id (str): The ID of the stopped EC2 instance to heal
    """
    print(f"\n[HEALING] Requesting Copilot CLI suggestion for {instance_id}...")
    
    # Check if gh CLI is available
    try:
        subprocess.run(['gh', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  GitHub CLI (gh) not found. Please install it to use healing functionality.")
        print("   Visit: https://cli.github.com/")
        return
    
    # Prepare prompt for Copilot CLI
    prompt = f"What is the AWS CLI command to start EC2 instance {instance_id} in the us-east-1 region? Reply with ONLY the command, no explanation."
    
    try:
        # Call gh copilot in non-interactive mode with silent output
        result = subprocess.run(
            ['gh', 'copilot', '-p', prompt, '-s'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"⚠️  Copilot CLI error: {result.stderr.strip()}")
            return
        
        # Get the suggested command
        suggested_cmd = result.stdout.strip()
        
        if not suggested_cmd:
            print("⚠️  No suggestion received from Copilot CLI")
            return
        
        # Display the suggestion
        print("\n" + "─" * 50)
        print("💡 Copilot CLI Suggestion:")
        print(suggested_cmd)
        print("─" * 50)
        
        # Prompt for user approval
        response = input("\nExecute this command? (y/n): ").strip().lower()
        
        if response == 'y':
            print("\n[EXECUTING] Running suggested command...")
            # Execute the AWS command directly
            exec_result = subprocess.run(
                ['aws', 'ec2', 'start-instances', '--instance-ids', instance_id, '--region', 'us-east-1'],
                capture_output=True,
                text=True
            )
            
            if exec_result.returncode == 0:
                print(f"✅ Successfully initiated start for {instance_id}")
            else:
                print(f"❌ Failed to start instance: {exec_result.stderr.strip()}")
        else:
            print("⏭️  Skipped healing action.")
            
    except subprocess.TimeoutExpired:
        print("⚠️  Copilot CLI request timed out.")
    except Exception as e:
        print(f"⚠️  Error during healing: {str(e)}")


def print_bold(text):
    """Print text in bold using ANSI escape codes."""
    print(f"\033[1m{text}\033[0m")


def check_ec2_instances(mock_mode=False):
    """
    Check EC2 instances in us-east-1 region and alert on stopped instances.
    
    Args:
        mock_mode (bool): If True, simulate a stopped instance instead of querying AWS
    
    Returns:
        int: Number of stopped instances found
    """
    region = 'us-east-1'
    
    if mock_mode:
        # Mock mode: simulate a stopped instance
        print(f"🧪 Mock mode: Simulating stopped instance check in {region}...")
        instance_id = 'sentinel-test-vm'
        print_bold(f"🚨 ALERT: Instance {instance_id} is STOPPED!")
        trigger_healing(instance_id)
        print(f"\nSummary: 1 instance checked (mock), 1 stopped")
        return 1
    
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
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Sentinel Watcher - EC2 Instance Monitoring'
    )
    parser.add_argument(
        '--mock',
        action='store_true',
        help='Run in mock mode: simulate a stopped instance (sentinel-test-vm) without AWS credentials'
    )
    args = parser.parse_args()
    
    print("🛡️  Sentinel Watcher - EC2 Monitoring")
    print("=" * 50)
    
    stopped_count = check_ec2_instances(mock_mode=args.mock)
    
    if stopped_count == 0:
        print("\n✅ All instances are running normally!")
    else:
        print(f"\n⚠️  Found {stopped_count} stopped instance(s) requiring attention.")


if __name__ == "__main__":
    main()
