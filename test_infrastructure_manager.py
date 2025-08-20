#!/usr/bin/env python3
"""
Simple tests for the cloud infrastructure manager
"""

import os
import sys
import tempfile
import yaml
from pathlib import Path

# Add the parent directory to the path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cloud_infrastructure_manager import InfrastructureManager


def test_aws_configuration():
    """Test AWS configuration parsing and validation."""
    config = {
        'providers': {
            'AWS': {
                'region': 'us-east-1',
                'access_key': 'test-key',
                'secret_key': 'test-secret'
            }
        },
        'infrastructure': {
            'AWS': {
                'virtual_machines': [{
                    'name': 'test-vm',
                    'instance_type': 't2.micro',
                    'ami_id': 'ami-12345',
                    'key_pair': 'test-key',
                    'security_groups': ['default']
                }],
                'storage': {
                    'ebs': {
                        'size_gb': 20,
                        'type': 'gp3'
                    }
                },
                'network': {
                    'vpc': {
                        'cidr_block': '10.0.0.0/16'
                    }
                },
                'security': {
                    'security_groups': [{
                        'name': 'test-sg',
                        'rules': [{
                            'protocol': 'tcp',
                            'from_port': 80,
                            'to_port': 80,
                            'cidr_blocks': ['0.0.0.0/0']
                        }]
                    }]
                }
            }
        }
    }
    
    # Create temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config, f)
        temp_config_path = f.name
    
    try:
        # Test configuration loading and validation
        manager = InfrastructureManager(temp_config_path)
        assert manager.validate_configuration(), "AWS configuration validation failed"
        
        # Test provider initialization
        assert 'aws' in manager.providers, "AWS provider not initialized"
        
        print("✓ AWS configuration test passed")
        return True
        
    except Exception as e:
        print(f"✗ AWS configuration test failed: {str(e)}")
        return False
        
    finally:
        # Clean up temporary file
        os.unlink(temp_config_path)


def test_multi_cloud_configuration():
    """Test multi-cloud configuration parsing and validation."""
    config = {
        'providers': {
            'AWS': {
                'region': 'us-east-1'
            },
            'Azure': {
                'subscription_id': 'test-subscription',
                'resource_group': 'test-rg',
                'location': 'East US'
            },
            'GCP': {
                'project_id': 'test-project',
                'zone': 'us-central1-a'
            }
        },
        'infrastructure': {
            'AWS': {
                'virtual_machines': [{
                    'name': 'aws-vm',
                    'instance_type': 't2.micro'
                }]
            },
            'Azure': {
                'virtual_machines': [{
                    'name': 'azure-vm',
                    'size': 'Standard_B1s'
                }]
            },
            'GCP': {
                'virtual_machines': [{
                    'name': 'gcp-vm',
                    'machine_type': 'e2-micro'
                }]
            }
        }
    }
    
    # Create temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config, f)
        temp_config_path = f.name
    
    try:
        # Test configuration loading and validation
        manager = InfrastructureManager(temp_config_path)
        assert manager.validate_configuration(), "Multi-cloud configuration validation failed"
        
        # Test provider initialization
        assert len(manager.providers) == 3, f"Expected 3 providers, got {len(manager.providers)}"
        assert 'aws' in manager.providers, "AWS provider not initialized"
        assert 'azure' in manager.providers, "Azure provider not initialized"
        assert 'gcp' in manager.providers, "GCP provider not initialized"
        
        print("✓ Multi-cloud configuration test passed")
        return True
        
    except Exception as e:
        print(f"✗ Multi-cloud configuration test failed: {str(e)}")
        return False
        
    finally:
        # Clean up temporary file
        os.unlink(temp_config_path)


def test_invalid_configuration():
    """Test handling of invalid configurations."""
    config = {
        'providers': {
            'InvalidProvider': {
                'some_config': 'value'
            }
        },
        # Missing infrastructure section
    }
    
    # Create temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config, f)
        temp_config_path = f.name
    
    try:
        manager = InfrastructureManager(temp_config_path)
        assert not manager.validate_configuration(), "Invalid configuration should fail validation"
        
        print("✓ Invalid configuration test passed")
        return True
        
    except Exception as e:
        print(f"✗ Invalid configuration test failed: {str(e)}")
        return False
        
    finally:
        # Clean up temporary file
        os.unlink(temp_config_path)


def test_configuration_files():
    """Test the provided configuration files."""
    config_dir = Path(__file__).parent / 'config'
    
    if not config_dir.exists():
        print("✗ Config directory not found")
        return False
    
    config_files = list(config_dir.glob('*.yaml'))
    
    if not config_files:
        print("✗ No configuration files found")
        return False
    
    success = True
    for config_file in config_files:
        try:
            manager = InfrastructureManager(str(config_file))
            if manager.validate_configuration():
                print(f"✓ Configuration file {config_file.name} is valid")
            else:
                print(f"✗ Configuration file {config_file.name} is invalid")
                success = False
        except Exception as e:
            print(f"✗ Configuration file {config_file.name} failed: {str(e)}")
            success = False
    
    return success


def main():
    """Run all tests."""
    print("Running Cloud Infrastructure Manager Tests")
    print("=" * 50)
    
    tests = [
        test_aws_configuration,
        test_multi_cloud_configuration,
        test_invalid_configuration,
        test_configuration_files
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())