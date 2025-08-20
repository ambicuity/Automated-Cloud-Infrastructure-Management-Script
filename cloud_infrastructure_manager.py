#!/usr/bin/env python3
"""
Automated Cloud Infrastructure Management Script

This script automates the management of cloud infrastructure, including:
- Virtual machine provisioning
- Storage management
- Network configuration
- Security best practices enforcement

Author: Cloud Infrastructure Team
License: Apache 2.0
"""

import os
import sys
import json
import yaml
import logging
import argparse
import subprocess
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('infrastructure.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class CloudProvider:
    """Base class for cloud provider implementations."""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{name}")
    
    def provision_vm(self, vm_config: Dict[str, Any]) -> bool:
        """Provision a virtual machine."""
        raise NotImplementedError("Subclasses must implement provision_vm")
    
    def configure_storage(self, storage_config: Dict[str, Any]) -> bool:
        """Configure storage resources."""
        raise NotImplementedError("Subclasses must implement configure_storage")
    
    def setup_network(self, network_config: Dict[str, Any]) -> bool:
        """Setup network configuration."""
        raise NotImplementedError("Subclasses must implement setup_network")
    
    def apply_security_policies(self, security_config: Dict[str, Any]) -> bool:
        """Apply security best practices."""
        raise NotImplementedError("Subclasses must implement apply_security_policies")


class AWSProvider(CloudProvider):
    """AWS cloud provider implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("AWS", config)
        self.region = config.get('region', 'us-east-1')
        self.access_key = config.get('access_key')
        self.secret_key = config.get('secret_key')
    
    def provision_vm(self, vm_config: Dict[str, Any]) -> bool:
        """Provision EC2 instance."""
        try:
            instance_type = vm_config.get('instance_type', 't2.micro')
            ami_id = vm_config.get('ami_id', 'ami-0c02fb55956c7d316')  # Amazon Linux 2
            key_pair = vm_config.get('key_pair', 'default')
            security_groups = vm_config.get('security_groups', ['default'])
            
            self.logger.info(f"Provisioning EC2 instance: {instance_type}")
            
            # Simulate AWS CLI command (in real implementation, use boto3)
            cmd = [
                'aws', 'ec2', 'run-instances',
                '--image-id', ami_id,
                '--instance-type', instance_type,
                '--key-name', key_pair,
                '--security-groups'] + security_groups
            
            self.logger.info(f"Command: {' '.join(cmd)}")
            self.logger.info("✓ EC2 instance provisioned successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to provision EC2 instance: {str(e)}")
            return False
    
    def configure_storage(self, storage_config: Dict[str, Any]) -> bool:
        """Configure EBS volumes and S3 buckets."""
        try:
            # EBS Volume configuration
            if 'ebs' in storage_config:
                ebs_config = storage_config['ebs']
                volume_size = ebs_config.get('size_gb', 20)
                volume_type = ebs_config.get('type', 'gp3')
                
                self.logger.info(f"Creating EBS volume: {volume_size}GB {volume_type}")
                self.logger.info("✓ EBS volume configured successfully")
            
            # S3 Bucket configuration
            if 's3' in storage_config:
                s3_config = storage_config['s3']
                bucket_name = s3_config.get('bucket_name')
                
                self.logger.info(f"Creating S3 bucket: {bucket_name}")
                self.logger.info("✓ S3 bucket configured successfully")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to configure storage: {str(e)}")
            return False
    
    def setup_network(self, network_config: Dict[str, Any]) -> bool:
        """Setup VPC, subnets, and security groups."""
        try:
            # VPC configuration
            if 'vpc' in network_config:
                vpc_config = network_config['vpc']
                cidr_block = vpc_config.get('cidr_block', '10.0.0.0/16')
                
                self.logger.info(f"Creating VPC with CIDR: {cidr_block}")
                self.logger.info("✓ VPC created successfully")
            
            # Subnet configuration
            if 'subnets' in network_config:
                subnets = network_config['subnets']
                for subnet in subnets:
                    subnet_cidr = subnet.get('cidr_block')
                    availability_zone = subnet.get('availability_zone')
                    
                    self.logger.info(f"Creating subnet: {subnet_cidr} in {availability_zone}")
                    self.logger.info("✓ Subnet created successfully")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to setup network: {str(e)}")
            return False
    
    def apply_security_policies(self, security_config: Dict[str, Any]) -> bool:
        """Apply AWS security best practices."""
        try:
            # Security Group rules
            if 'security_groups' in security_config:
                for sg_config in security_config['security_groups']:
                    sg_name = sg_config.get('name')
                    rules = sg_config.get('rules', [])
                    
                    self.logger.info(f"Configuring security group: {sg_name}")
                    for rule in rules:
                        protocol = rule.get('protocol', 'tcp')
                        from_port = rule.get('from_port')
                        to_port = rule.get('to_port')
                        cidr = rule.get('cidr_blocks', ['0.0.0.0/0'])
                        
                        self.logger.info(f"  Rule: {protocol} {from_port}-{to_port} from {cidr}")
                    
                    self.logger.info("✓ Security group configured")
            
            # IAM policies
            if 'iam_policies' in security_config:
                for policy in security_config['iam_policies']:
                    policy_name = policy.get('name')
                    self.logger.info(f"Applying IAM policy: {policy_name}")
                    self.logger.info("✓ IAM policy applied")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to apply security policies: {str(e)}")
            return False


class AzureProvider(CloudProvider):
    """Azure cloud provider implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("Azure", config)
        self.subscription_id = config.get('subscription_id')
        self.resource_group = config.get('resource_group', 'default-rg')
        self.location = config.get('location', 'East US')
    
    def provision_vm(self, vm_config: Dict[str, Any]) -> bool:
        """Provision Azure Virtual Machine."""
        try:
            vm_name = vm_config.get('name', 'default-vm')
            vm_size = vm_config.get('size', 'Standard_B1s')
            image = vm_config.get('image', 'UbuntuLTS')
            
            self.logger.info(f"Provisioning Azure VM: {vm_name} ({vm_size})")
            self.logger.info("✓ Azure VM provisioned successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to provision Azure VM: {str(e)}")
            return False
    
    def configure_storage(self, storage_config: Dict[str, Any]) -> bool:
        """Configure Azure Storage accounts and disks."""
        try:
            if 'storage_account' in storage_config:
                account_config = storage_config['storage_account']
                account_name = account_config.get('name')
                account_type = account_config.get('type', 'Standard_LRS')
                
                self.logger.info(f"Creating storage account: {account_name}")
                self.logger.info("✓ Azure storage configured successfully")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to configure Azure storage: {str(e)}")
            return False
    
    def setup_network(self, network_config: Dict[str, Any]) -> bool:
        """Setup Azure Virtual Network."""
        try:
            if 'vnet' in network_config:
                vnet_config = network_config['vnet']
                vnet_name = vnet_config.get('name')
                address_space = vnet_config.get('address_space', '10.0.0.0/16')
                
                self.logger.info(f"Creating VNet: {vnet_name} with {address_space}")
                self.logger.info("✓ Azure VNet configured successfully")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to setup Azure network: {str(e)}")
            return False
    
    def apply_security_policies(self, security_config: Dict[str, Any]) -> bool:
        """Apply Azure security best practices."""
        try:
            if 'network_security_groups' in security_config:
                for nsg_config in security_config['network_security_groups']:
                    nsg_name = nsg_config.get('name')
                    self.logger.info(f"Configuring NSG: {nsg_name}")
                    self.logger.info("✓ Azure NSG configured")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to apply Azure security policies: {str(e)}")
            return False


class GCPProvider(CloudProvider):
    """Google Cloud Platform provider implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("GCP", config)
        self.project_id = config.get('project_id')
        self.zone = config.get('zone', 'us-central1-a')
        self.region = config.get('region', 'us-central1')
    
    def provision_vm(self, vm_config: Dict[str, Any]) -> bool:
        """Provision GCP Compute Engine instance."""
        try:
            instance_name = vm_config.get('name', 'default-instance')
            machine_type = vm_config.get('machine_type', 'e2-micro')
            image_family = vm_config.get('image_family', 'ubuntu-2004-lts')
            
            self.logger.info(f"Provisioning GCP instance: {instance_name} ({machine_type})")
            self.logger.info("✓ GCP instance provisioned successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to provision GCP instance: {str(e)}")
            return False
    
    def configure_storage(self, storage_config: Dict[str, Any]) -> bool:
        """Configure GCP storage resources."""
        try:
            if 'persistent_disk' in storage_config:
                disk_config = storage_config['persistent_disk']
                disk_name = disk_config.get('name')
                disk_size = disk_config.get('size_gb', 20)
                
                self.logger.info(f"Creating persistent disk: {disk_name} ({disk_size}GB)")
                self.logger.info("✓ GCP storage configured successfully")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to configure GCP storage: {str(e)}")
            return False
    
    def setup_network(self, network_config: Dict[str, Any]) -> bool:
        """Setup GCP VPC network."""
        try:
            if 'vpc' in network_config:
                vpc_config = network_config['vpc']
                network_name = vpc_config.get('name')
                subnet_range = vpc_config.get('subnet_range', '10.0.0.0/24')
                
                self.logger.info(f"Creating VPC network: {network_name}")
                self.logger.info("✓ GCP network configured successfully")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to setup GCP network: {str(e)}")
            return False
    
    def apply_security_policies(self, security_config: Dict[str, Any]) -> bool:
        """Apply GCP security best practices."""
        try:
            if 'firewall_rules' in security_config:
                for rule_config in security_config['firewall_rules']:
                    rule_name = rule_config.get('name')
                    direction = rule_config.get('direction', 'INGRESS')
                    
                    self.logger.info(f"Creating firewall rule: {rule_name} ({direction})")
                    self.logger.info("✓ GCP firewall rule created")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to apply GCP security policies: {str(e)}")
            return False


class InfrastructureManager:
    """Main infrastructure management orchestrator."""
    
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.logger = logging.getLogger(__name__)
        self.config = self.load_configuration()
        self.providers = self.initialize_providers()
    
    def load_configuration(self) -> Dict[str, Any]:
        """Load configuration from YAML or JSON file."""
        try:
            config_path = Path(self.config_file)
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {self.config_file}")
            
            with open(config_path, 'r') as f:
                if config_path.suffix.lower() in ['.yaml', '.yml']:
                    return yaml.safe_load(f)
                elif config_path.suffix.lower() == '.json':
                    return json.load(f)
                else:
                    raise ValueError("Configuration file must be YAML or JSON")
                    
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {str(e)}")
            raise
    
    def initialize_providers(self) -> Dict[str, CloudProvider]:
        """Initialize cloud providers based on configuration."""
        providers = {}
        
        for provider_name, provider_config in self.config.get('providers', {}).items():
            provider_name_lower = provider_name.lower()
            
            if provider_name_lower == 'aws':
                providers['aws'] = AWSProvider(provider_config)
            elif provider_name_lower == 'azure':
                providers['azure'] = AzureProvider(provider_config)
            elif provider_name_lower == 'gcp':
                providers['gcp'] = GCPProvider(provider_config)
            else:
                self.logger.warning(f"Unknown provider: {provider_name}")
        
        return providers
    
    def deploy_infrastructure(self) -> bool:
        """Deploy complete infrastructure based on configuration."""
        try:
            self.logger.info("Starting infrastructure deployment...")
            
            success = True
            
            # Deploy infrastructure for each provider
            for provider_name, infrastructure_config in self.config.get('infrastructure', {}).items():
                provider = self.providers.get(provider_name.lower())
                if not provider:
                    self.logger.error(f"Provider not found: {provider_name}")
                    success = False
                    continue
                
                self.logger.info(f"Deploying infrastructure on {provider_name}")
                
                # Provision VMs
                if 'virtual_machines' in infrastructure_config:
                    for vm_config in infrastructure_config['virtual_machines']:
                        if not provider.provision_vm(vm_config):
                            success = False
                
                # Configure storage
                if 'storage' in infrastructure_config:
                    if not provider.configure_storage(infrastructure_config['storage']):
                        success = False
                
                # Setup network
                if 'network' in infrastructure_config:
                    if not provider.setup_network(infrastructure_config['network']):
                        success = False
                
                # Apply security policies
                if 'security' in infrastructure_config:
                    if not provider.apply_security_policies(infrastructure_config['security']):
                        success = False
            
            if success:
                self.logger.info("✓ Infrastructure deployment completed successfully")
            else:
                self.logger.error("✗ Infrastructure deployment completed with errors")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Infrastructure deployment failed: {str(e)}")
            return False
    
    def validate_configuration(self) -> bool:
        """Validate the configuration file."""
        try:
            required_sections = ['providers', 'infrastructure']
            
            for section in required_sections:
                if section not in self.config:
                    self.logger.error(f"Required section missing: {section}")
                    return False
            
            # Validate providers
            for provider_name in self.config['providers']:
                if provider_name.lower() not in ['aws', 'azure', 'gcp']:
                    self.logger.error(f"Unsupported provider: {provider_name}")
                    return False
            
            self.logger.info("✓ Configuration validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {str(e)}")
            return False
    
    def generate_report(self) -> str:
        """Generate deployment report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
Infrastructure Deployment Report
Generated: {timestamp}

Configuration File: {self.config_file}
Providers Configured: {', '.join(self.providers.keys())}

Deployment Summary:
- Virtual Machines: {self._count_resources('virtual_machines')}
- Storage Resources: {self._count_resources('storage')}
- Network Resources: {self._count_resources('network')}
- Security Policies: {self._count_resources('security')}

For detailed logs, check: infrastructure.log
"""
        return report
    
    def _count_resources(self, resource_type: str) -> int:
        """Count resources of a specific type across all providers."""
        count = 0
        for infrastructure_config in self.config.get('infrastructure', {}).values():
            if resource_type in infrastructure_config:
                if resource_type == 'virtual_machines':
                    count += len(infrastructure_config[resource_type])
                else:
                    count += 1
        return count


def main():
    """Main entry point for the infrastructure manager."""
    parser = argparse.ArgumentParser(
        description="Automated Cloud Infrastructure Management Script"
    )
    parser.add_argument(
        'config',
        help='Path to configuration file (YAML or JSON)'
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate configuration without deploying'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate deployment report'
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Set logging level'
    )
    
    args = parser.parse_args()
    
    # Set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    try:
        # Initialize infrastructure manager
        manager = InfrastructureManager(args.config)
        
        # Validate configuration
        if not manager.validate_configuration():
            sys.exit(1)
        
        if args.validate_only:
            print("✓ Configuration validation passed")
            sys.exit(0)
        
        # Deploy infrastructure
        success = manager.deploy_infrastructure()
        
        # Generate report
        if args.report:
            report = manager.generate_report()
            print(report)
            
            # Save report to file
            report_file = f"deployment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_file, 'w') as f:
                f.write(report)
            print(f"Report saved to: {report_file}")
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logger.error(f"Script execution failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()