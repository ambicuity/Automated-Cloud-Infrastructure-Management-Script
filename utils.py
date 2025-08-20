#!/usr/bin/env python3
"""
Utility script for common cloud infrastructure management operations
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
import subprocess

def create_aws_config():
    """Create a basic AWS configuration file."""
    config_content = """# Basic AWS Infrastructure Configuration
providers:
  AWS:
    region: us-east-1
    # Use environment variables for credentials in production
    access_key: ${AWS_ACCESS_KEY_ID}
    secret_key: ${AWS_SECRET_ACCESS_KEY}

infrastructure:
  AWS:
    virtual_machines:
      - name: web-server
        instance_type: t2.micro
        ami_id: ami-0c02fb55956c7d316  # Amazon Linux 2
        key_pair: my-keypair
        security_groups: [web-sg]
        tags:
          Name: WebServer
          Environment: development
          Project: my-project
    
    storage:
      ebs:
        size_gb: 20
        type: gp3
        encrypted: true
      
      s3:
        bucket_name: my-project-bucket
        versioning: false
        encryption: AES256
    
    network:
      vpc:
        cidr_block: 10.0.0.0/16
      
      subnets:
        - cidr_block: 10.0.1.0/24
          availability_zone: us-east-1a
          public: true
    
    security:
      security_groups:
        - name: web-sg
          description: Security group for web server
          rules:
            - protocol: tcp
              from_port: 80
              to_port: 80
              cidr_blocks: [0.0.0.0/0]
            - protocol: tcp
              from_port: 443
              to_port: 443
              cidr_blocks: [0.0.0.0/0]
            - protocol: tcp
              from_port: 22
              to_port: 22
              cidr_blocks: [10.0.0.0/16]  # SSH only from VPC
"""
    
    filename = "my-aws-config.yaml"
    with open(filename, 'w') as f:
        f.write(config_content)
    
    print(f"✓ AWS configuration created: {filename}")
    print("  Edit the file to customize your infrastructure")
    print("  Then run: python cloud_infrastructure_manager.py my-aws-config.yaml")


def validate_config(config_file):
    """Validate a configuration file."""
    if not os.path.exists(config_file):
        print(f"✗ Configuration file not found: {config_file}")
        return False
    
    cmd = [
        sys.executable, 
        "cloud_infrastructure_manager.py", 
        config_file, 
        "--validate-only"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Configuration {config_file} is valid")
            return True
        else:
            print(f"✗ Configuration {config_file} is invalid:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"✗ Error validating configuration: {str(e)}")
        return False


def deploy_infrastructure(config_file, generate_report=False):
    """Deploy infrastructure from configuration file."""
    if not os.path.exists(config_file):
        print(f"✗ Configuration file not found: {config_file}")
        return False
    
    cmd = [sys.executable, "cloud_infrastructure_manager.py", config_file]
    
    if generate_report:
        cmd.append("--report")
    
    try:
        result = subprocess.run(cmd, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"✗ Error deploying infrastructure: {str(e)}")
        return False


def setup_development_environment():
    """Setup development environment with required tools."""
    print("Setting up development environment...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 7):
        print("✗ Python 3.7 or higher is required")
        return False
    
    print(f"✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Install required packages
    requirements = ["PyYAML"]
    
    for package in requirements:
        try:
            __import__(package.lower().replace('-', '_'))
            print(f"✓ {package} is already installed")
        except ImportError:
            print(f"Installing {package}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ {package} installed successfully")
            else:
                print(f"✗ Failed to install {package}")
                print(result.stderr)
                return False
    
    print("\n🎉 Development environment setup complete!")
    print("\nNext steps:")
    print("1. Configure cloud provider credentials")
    print("2. Create a configuration file (run: python utils.py create-aws-config)")
    print("3. Validate your configuration (run: python utils.py validate config-file.yaml)")
    print("4. Deploy infrastructure (run: python utils.py deploy config-file.yaml)")
    
    return True


def show_examples():
    """Show usage examples."""
    examples = """
Cloud Infrastructure Management Examples
========================================

1. Create a basic AWS configuration:
   python utils.py create-aws-config

2. Validate a configuration file:
   python utils.py validate my-config.yaml

3. Deploy infrastructure:
   python utils.py deploy my-config.yaml

4. Deploy infrastructure with report:
   python utils.py deploy my-config.yaml --report

5. Setup development environment:
   python utils.py setup-dev

6. Validate directly with main script:
   python cloud_infrastructure_manager.py config.yaml --validate-only

7. Deploy with debug logging:
   python cloud_infrastructure_manager.py config.yaml --log-level DEBUG

Configuration File Examples:
- config/aws-simple-example.yaml - Simple AWS setup
- config/multi-cloud-example.yaml - Multi-cloud deployment

Cloud Provider Credentials:
- AWS: Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
- Azure: Set AZURE_SUBSCRIPTION_ID
- GCP: Set GCP_PROJECT_ID

For more information, see README.md
"""
    print(examples)


def main():
    parser = argparse.ArgumentParser(
        description="Utility script for cloud infrastructure management"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create AWS config command
    subparsers.add_parser('create-aws-config', help='Create basic AWS configuration file')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate configuration file')
    validate_parser.add_argument('config', help='Path to configuration file')
    
    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy infrastructure')
    deploy_parser.add_argument('config', help='Path to configuration file')
    deploy_parser.add_argument('--report', action='store_true', help='Generate deployment report')
    
    # Setup development environment
    subparsers.add_parser('setup-dev', help='Setup development environment')
    
    # Show examples
    subparsers.add_parser('examples', help='Show usage examples')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == 'create-aws-config':
        create_aws_config()
        return 0
    
    elif args.command == 'validate':
        success = validate_config(args.config)
        return 0 if success else 1
    
    elif args.command == 'deploy':
        success = deploy_infrastructure(args.config, args.report)
        return 0 if success else 1
    
    elif args.command == 'setup-dev':
        success = setup_development_environment()
        return 0 if success else 1
    
    elif args.command == 'examples':
        show_examples()
        return 0
    
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())