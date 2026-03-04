#!/usr/bin/env python
"""
Test script to verify the fixes for issues #2, #3, and #5.

This script demonstrates that:
1. Modules can be imported without sys.path manipulation (Issue #2)
2. Cleanup methods accept a confirm parameter (Issue #3)
3. No duplicate functions exist (Issue #5)
"""

import sys
import inspect


def test_issue_2_imports():
    """Test that modules can be imported without sys.path manipulation."""
    print("Testing Issue #2: Package imports...")
    try:
        from configs import configuration_manager
        from mapping import helper
        from data_process import base_dataset
        from client import helper as client_helper
        from models import ml_model
        from connectors import ml_connector
        print("  ✓ All modules imported successfully without sys.path manipulation")
        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False


def test_issue_3_confirm_parameters():
    """Test that cleanup methods have confirm parameters."""
    print("\nTesting Issue #3: Confirm parameters in cleanup methods...")
    
    tests = [
        ("models.ml_model.MlModel._undeploy_and_delete_model", "models.ml_model", "MlModel", "_undeploy_and_delete_model"),
        ("models.ml_model_group.MlModelGroup._delete_model_group", "models.ml_model_group", "MlModelGroup", "_delete_model_group"),
        ("connectors.ml_connector.MlConnector._delete_connector", "connectors.ml_connector", "MlConnector", "_delete_connector"),
        ("client.os_ml_client_wrapper.OsMlClientWrapper.cleanup_kNN", "client.os_ml_client_wrapper", "OsMlClientWrapper", "cleanup_kNN"),
    ]
    
    all_passed = True
    for full_name, module_name, class_name, method_name in tests:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            method = getattr(cls, method_name)
            sig = inspect.signature(method)
            
            if 'confirm' in sig.parameters:
                param = sig.parameters['confirm']
                if param.default is True:
                    print(f"  ✓ {full_name} has confirm parameter (default=True)")
                else:
                    print(f"  ⚠ {full_name} has confirm parameter but default is {param.default}")
                    all_passed = False
            else:
                print(f"  ✗ {full_name} missing confirm parameter")
                all_passed = False
        except Exception as e:
            print(f"  ✗ Error checking {full_name}: {e}")
            all_passed = False
    
    return all_passed


def test_issue_5_no_duplicates():
    """Test that duplicate functions have been removed."""
    print("\nTesting Issue #5: No duplicate functions...")
    
    # Test get_pipeline_field_map is only defined once
    try:
        from configs import configuration_manager
        import inspect
        
        source = inspect.getsource(configuration_manager)
        count = source.count("def get_pipeline_field_map")
        
        if count == 1:
            print(f"  ✓ get_pipeline_field_map defined only once in configuration_manager")
        else:
            print(f"  ✗ get_pipeline_field_map defined {count} times (expected 1)")
            return False
    except Exception as e:
        print(f"  ✗ Error checking get_pipeline_field_map: {e}")
        return False
    
    # Test that BaseDataset.update_mapping uses mapping.helper.mapping_update
    try:
        from data_process import base_dataset
        from mapping import helper
        
        # Check that both exist
        assert hasattr(base_dataset.BaseDataset, 'update_mapping')
        assert hasattr(helper, 'mapping_update')
        
        # Check that BaseDataset.update_mapping is documented as a wrapper
        source = inspect.getsource(base_dataset.BaseDataset.update_mapping)
        if 'mapping_update' in source and 'wrapper' in source.lower():
            print(f"  ✓ BaseDataset.update_mapping properly delegates to mapping.helper.mapping_update")
        else:
            print(f"  ⚠ BaseDataset.update_mapping may not be properly delegating")
            
        return True
    except Exception as e:
        print(f"  ✗ Error checking mapping functions: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("Testing fixes for codebase critique issues #2, #3, and #5")
    print("=" * 70)
    
    results = []
    results.append(("Issue #2 (sys.path.append)", test_issue_2_imports()))
    results.append(("Issue #3 (input() calls)", test_issue_3_confirm_parameters()))
    results.append(("Issue #5 (duplicated code)", test_issue_5_no_duplicates()))
    
    print("\n" + "=" * 70)
    print("Summary:")
    print("=" * 70)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name}: {status}")
        all_passed = all_passed and passed
    
    print("=" * 70)
    
    if all_passed:
        print("\n🎉 All tests passed! The fixes are working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
