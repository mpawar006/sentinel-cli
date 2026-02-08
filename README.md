# 🛡️ Sentinel CLI
Self-healing DevOps agent for the GitHub Copilot CLI Challenge.

## Overview
Sentinel CLI monitors AWS EC2 instances and detects stopped instances that may require attention. It includes a placeholder for future integration with GitHub Copilot CLI to enable automated self-healing capabilities.

## Features
- 🔍 Monitors EC2 instances in the `us-east-1` region
- 🚨 Bold terminal alerts for stopped instances
- 🤖 Self-healing via GitHub Copilot CLI integration
- 🧪 Mock mode for testing without AWS credentials
- 💬 Interactive approval workflow for healing actions
- ⚡ Simple, single-execution design
- 🛡️ Robust error handling for AWS API calls

## Prerequisites
- Python 3.7 or higher
- AWS CLI configured with valid credentials (not required for `--mock` mode)
- GitHub CLI (`gh`) installed for self-healing functionality
- AWS IAM permissions to describe and start EC2 instances

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

### Mock Mode
Test the healing functionality without AWS credentials:
```bash
python sentinel_watcher.py --mock
```

Mock mode simulates a stopped instance called `sentinel-test-vm` and demonstrates the self-healing workflow using GitHub Copilot CLI.

The script will:
1. Connect to AWS using your default credentials (or simulate in mock mode)
2. Query all EC2 instances in `us-east-1` (or use mock data)
3. Display bold alerts for any stopped instances
4. Trigger self-healing via GitHub Copilot CLI
5. Request AWS CLI command suggestions from Copilot
6. Prompt for user approval before executing healing actions
7. Show a summary of instances checked

### Example Output
```
🛡️  Sentinel Watcher - EC2 Monitoring
==================================================
Checking EC2 instances in us-east-1...
🚨 ALERT: Instance i-1234567890abcdef0 is STOPPED!

[HEALING] Requesting Copilot CLI suggestion for i-1234567890abcdef0...

──────────────────────────────────────────────────
💡 Copilot CLI Suggestion:
aws ec2 start-instances --instance-ids i-1234567890abcdef0 --region us-east-1
──────────────────────────────────────────────────

Execute this command? (y/n): y

[EXECUTING] Running suggested command...
✅ Successfully initiated start for i-1234567890abcdef0

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
