# 🛡️ Sentinel CLI
Self-healing DevOps agent for the GitHub Copilot CLI Challenge.

## Overview
Sentinel CLI monitors AWS EC2 instances and detects stopped instances that may require attention. It includes a placeholder for future integration with GitHub Copilot CLI to enable automated self-healing capabilities.

## Features
- 🔍 Monitors EC2 instances in the `us-east-1` region
- 🚨 Bold terminal alerts for stopped instances
- 🔧 Placeholder `trigger_healing()` function for future Copilot CLI integration
- ⚡ Simple, single-execution design
- 🛡️ Robust error handling for AWS API calls

## Prerequisites
- Python 3.7 or higher
- AWS CLI configured with valid credentials
- AWS IAM permissions to describe EC2 instances

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd sentinel-cli
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure AWS CLI is configured:
```bash
aws configure
# Or verify existing configuration
aws sts get-caller-identity
```

## Usage

Run the sentinel watcher script:
```bash
python sentinel_watcher.py
```

The script will:
1. Connect to AWS using your default credentials
2. Query all EC2 instances in `us-east-1`
3. Display bold alerts for any stopped instances
4. Show a summary of instances checked

### Example Output
```
🛡️  Sentinel Watcher - EC2 Monitoring
==================================================
Checking EC2 instances in us-east-1...
🚨 ALERT: Instance i-1234567890abcdef0 is STOPPED!
[HEALING] Placeholder: Would trigger healing for i-1234567890abcdef0

Summary: 5 instances checked, 1 stopped

⚠️  Found 1 stopped instance(s) requiring attention.
```

## Future Enhancements
- Integration with GitHub Copilot CLI for automated diagnosis and healing
- Support for multiple AWS regions
- Configuration file for customizable settings
- Continuous monitoring mode with configurable intervals
- Notification integrations (email, Slack, etc.)

## License
MIT
