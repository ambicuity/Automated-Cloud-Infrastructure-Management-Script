# Automated Cloud Infrastructure Management Script

A comprehensive Python script that automates the management of cloud infrastructure across multiple cloud providers (AWS, Azure, GCP). This tool streamlines day-to-day infrastructure tasks and ensures adherence to security best practices.

## Features

### 🚀 Multi-Cloud Support
- **AWS**: EC2, EBS, S3, VPC, Security Groups, IAM
- **Azure**: Virtual Machines, Storage Accounts, VNet, NSG
- **GCP**: Compute Engine, Persistent Disks, Cloud Storage, VPC

### 🛠️ Infrastructure Automation
- **Virtual Machine Provisioning**: Automated VM creation with customizable configurations
- **Storage Management**: Automated setup of disks, buckets, and storage accounts
- **Network Configuration**: VPC/VNet creation, subnets, security groups, and firewall rules
- **Security Best Practices**: Automated application of security policies and compliance standards

### 📊 Management Features
- Configuration validation
- Deployment reporting
- Comprehensive logging
- Error handling and rollback capabilities

## Installation

### Prerequisites
- Python 3.7 or higher
- Cloud provider CLI tools (optional but recommended):
  - AWS CLI
  - Azure CLI
  - Google Cloud SDK

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ambicuity/Automated-Cloud-Infrastructure-Management-Script.git
   cd Automated-Cloud-Infrastructure-Management-Script
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install cloud provider SDKs (optional):**
   ```bash
   # For AWS
   pip install boto3 botocore
   
   # For Azure
   pip install azure-mgmt-compute azure-mgmt-network azure-mgmt-storage azure-identity
   
   # For GCP
   pip install google-cloud-compute google-cloud-storage google-auth
   ```

4. **Configure cloud provider credentials:**
   
   **AWS:**
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   # Or use AWS CLI: aws configure
   ```
   
   **Azure:**
   ```bash
   export AZURE_SUBSCRIPTION_ID=your_subscription_id
   # Or use Azure CLI: az login
   ```
   
   **GCP:**
   ```bash
   export GCP_PROJECT_ID=your_project_id
   # Or use gcloud CLI: gcloud auth application-default login
   ```

## Usage

### Basic Usage

1. **Create a configuration file** (see examples in `config/` directory):
   ```yaml
   providers:
     AWS:
       region: us-east-1
   
   infrastructure:
     AWS:
       virtual_machines:
         - name: web-server
           instance_type: t2.micro
           ami_id: ami-0c02fb55956c7d316
   ```

2. **Run the script:**
   ```bash
   python cloud_infrastructure_manager.py config/your-config.yaml
   ```

### Advanced Usage

**Validate configuration only:**
```bash
python cloud_infrastructure_manager.py config/aws-simple-example.yaml --validate-only
```

**Generate deployment report:**
```bash
python cloud_infrastructure_manager.py config/multi-cloud-example.yaml --report
```

**Set custom log level:**
```bash
python cloud_infrastructure_manager.py config/your-config.yaml --log-level DEBUG
```

**Help:**
```bash
python cloud_infrastructure_manager.py --help
```

## Configuration

### Configuration File Structure

The script uses YAML configuration files to define infrastructure. Here's the basic structure:

```yaml
providers:
  PROVIDER_NAME:
    # Provider-specific configuration
    region: region-name
    # credentials and other settings

infrastructure:
  PROVIDER_NAME:
    virtual_machines:
      - name: vm-name
        # VM-specific configuration
    
    storage:
      # Storage configuration
    
    network:
      # Network configuration
    
    security:
      # Security configuration
```

### Example Configurations

The `config/` directory contains several example configurations:

- **`aws-simple-example.yaml`**: Basic AWS infrastructure setup
- **`multi-cloud-example.yaml`**: Comprehensive multi-cloud deployment

### Security Best Practices

The script implements several security best practices:

- **Encryption**: Storage encryption at rest and in transit
- **Network Security**: Proper security group/firewall configurations
- **Access Control**: Principle of least privilege
- **Monitoring**: Comprehensive logging and audit trails
- **Compliance**: Support for SOC2, ISO27001, PCI-DSS frameworks

## Architecture

### Project Structure

```
Automated-Cloud-Infrastructure-Management-Script/
├── cloud_infrastructure_manager.py    # Main script
├── requirements.txt                    # Python dependencies
├── config/                            # Configuration examples
│   ├── aws-simple-example.yaml
│   └── multi-cloud-example.yaml
├── README.md                          # This file
└── LICENSE                           # Apache 2.0 License
```

### Core Components

1. **CloudProvider**: Base class for cloud provider implementations
2. **AWSProvider**: AWS-specific infrastructure management
3. **AzureProvider**: Azure-specific infrastructure management
4. **GCPProvider**: GCP-specific infrastructure management
5. **InfrastructureManager**: Main orchestrator class

### Key Features

- **Modular Design**: Easy to extend with new cloud providers
- **Configuration-Driven**: All infrastructure defined in YAML files
- **Error Handling**: Comprehensive error handling and logging
- **Validation**: Configuration validation before deployment
- **Reporting**: Detailed deployment reports and logs

## Examples

### Provision a Simple Web Server on AWS

```yaml
providers:
  AWS:
    region: us-east-1

infrastructure:
  AWS:
    virtual_machines:
      - name: web-server
        instance_type: t2.micro
        ami_id: ami-0c02fb55956c7d316
        key_pair: my-keypair
        security_groups: [web-sg]
    
    security:
      security_groups:
        - name: web-sg
          rules:
            - protocol: tcp
              from_port: 80
              to_port: 80
              cidr_blocks: [0.0.0.0/0]
            - protocol: tcp
              from_port: 443
              to_port: 443
              cidr_blocks: [0.0.0.0/0]
```

### Multi-Cloud Deployment

```yaml
providers:
  AWS:
    region: us-east-1
  Azure:
    resource_group: my-rg
    location: East US
  GCP:
    project_id: my-project
    zone: us-central1-a

infrastructure:
  AWS:
    virtual_machines:
      - name: aws-web-server
        instance_type: t2.micro
  
  Azure:
    virtual_machines:
      - name: azure-web-vm
        size: Standard_B1s
  
  GCP:
    virtual_machines:
      - name: gcp-web-instance
        machine_type: e2-micro
```

## Logging and Monitoring

The script provides comprehensive logging:

- **Console Output**: Real-time progress and status updates
- **Log Files**: Detailed logs saved to `infrastructure.log`
- **Deployment Reports**: Summary reports with resource counts and status

### Log Levels

- **DEBUG**: Detailed debugging information
- **INFO**: General information about script execution
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failed operations

## Error Handling

The script includes robust error handling:

- **Configuration Validation**: Validates configuration before deployment
- **Provider Validation**: Checks if required cloud providers are available
- **Resource Validation**: Validates resource configurations
- **Deployment Rollback**: Ability to rollback failed deployments (provider-dependent)

## Security Considerations

### Credential Management

- Use environment variables for sensitive information
- Never commit credentials to version control
- Use cloud provider IAM roles when possible
- Implement credential rotation policies

### Network Security

- Follow principle of least privilege for security groups
- Use private subnets for sensitive resources
- Implement network segmentation
- Enable encryption in transit and at rest

### Compliance

The script supports various compliance frameworks:
- SOC 2 Type II
- ISO 27001
- PCI DSS
- NIST Cybersecurity Framework

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes and add tests
4. Commit your changes: `git commit -am 'Add new feature'`
5. Push to the branch: `git push origin feature/new-feature`
6. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# Run tests
pytest

# Format code
black cloud_infrastructure_manager.py

# Lint code
flake8 cloud_infrastructure_manager.py

# Type checking
mypy cloud_infrastructure_manager.py
```

## Troubleshooting

### Common Issues

1. **Configuration Validation Errors**:
   - Check YAML syntax
   - Verify required fields are present
   - Ensure cloud provider credentials are configured

2. **Provider Authentication Errors**:
   - Verify cloud provider credentials
   - Check IAM permissions
   - Ensure required APIs are enabled

3. **Resource Creation Failures**:
   - Check resource quotas and limits
   - Verify resource naming conventions
   - Review cloud provider-specific requirements

### Getting Help

- Check the logs in `infrastructure.log`
- Use `--log-level DEBUG` for detailed information
- Validate configuration with `--validate-only`
- Review cloud provider documentation

## Roadmap

- [ ] Terraform integration
- [ ] Infrastructure drift detection
- [ ] Cost optimization recommendations
- [ ] Auto-scaling configurations
- [ ] Disaster recovery automation
- [ ] Integration with monitoring tools
- [ ] Infrastructure testing framework

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by Infrastructure as Code best practices
- Built with security and compliance in mind
- Designed for enterprise-scale deployments