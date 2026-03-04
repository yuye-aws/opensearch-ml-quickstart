# Before and After Examples

This document shows concrete examples of the changes made to fix issues #2, #3, and #5.

## Issue #2: sys.path.append Everywhere

### Before

Every example file had this boilerplate:

```python
# examples/dense_hnsw_search.py
import os
import sys

import cmd_line_interface

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client import OsMlClientWrapper, get_client
from configs.configuration_manager import get_client_configs
```

Library files also had it:

```python
# client/helper.py
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configs.configuration_manager import get_opensearch_config
```

### After

Example files are clean:

```python
# examples/dense_hnsw_search.py
import os
import sys

import cmd_line_interface

from client import OsMlClientWrapper, get_client
from configs.configuration_manager import get_client_configs
```

Library files use proper relative imports:

```python
# client/helper.py
import os

from configs.configuration_manager import get_opensearch_config
```

### Setup Required

Users set PYTHONPATH once:

```bash
# In shell or .bashrc/.zshrc
export PYTHONPATH="/path/to/opensearch-ml-quickstart:$PYTHONPATH"

# Or when running:
PYTHONPATH=/path/to/opensearch-ml-quickstart python examples/dense_hnsw_search.py
```

## Issue #3: Interactive input() Calls in Library Code

### Before

Library code forced interactive prompts:

```python
# models/ml_model.py
def _undeploy_and_delete_model(self, model_id):
    user_input = (
        input(f"Do you want to undeploy and delete the model {model_id}? (y/n): ")
        .strip()
        .lower()
    )

    if user_input != "y":
        logging.info("Undeploy and delete model canceled.")
        return

    # ... deletion code ...
```

This made the code:
- Untestable (tests would hang waiting for input)
- Unusable in automation (scripts would hang)
- Surprising (library code shouldn't prompt users)

### After

Added optional `confirm` parameter:

```python
# models/ml_model.py
def _undeploy_and_delete_model(self, model_id, confirm=True):
    if confirm:
        user_input = (
            input(f"Do you want to undeploy and delete the model {model_id}? (y/n): ")
            .strip()
            .lower()
        )

        if user_input != "y":
            logging.info("Undeploy and delete model canceled.")
            return

    # ... deletion code ...
```

### Usage Examples

**Interactive mode (backward compatible):**
```python
# Still works exactly as before
model._undeploy_and_delete_model(model_id)  # Will prompt
```

**Automated mode (new capability):**
```python
# For tests and automation
model._undeploy_and_delete_model(model_id, confirm=False)  # No prompt

# In test suite
def test_cleanup():
    wrapper.cleanup_kNN(
        ml_model=model,
        index_name="test_index",
        pipeline_name="test_pipeline",
        confirm=False  # No prompts in tests!
    )
```

**In CI/CD pipelines:**
```python
# cleanup_script.py
if os.environ.get('CI'):
    # Non-interactive in CI
    wrapper.cleanup_kNN(model, index, pipeline, confirm=False)
else:
    # Interactive locally
    wrapper.cleanup_kNN(model, index, pipeline)
```

## Issue #5: Duplicated Code

### Example 1: Duplicate Function Definition

**Before:**

```python
# configs/configuration_manager.py (lines 657-660)
def get_pipeline_field_map() -> Dict[str, str]:
    """Get the pipeline field mapping."""
    return get_raw_config_value("PIPELINE_FIELD_MAP", {"chunk": "chunk_embedding"})

# Same function again! (lines 661-664)
def get_pipeline_field_map() -> Dict[str, str]:
    """Get the pipeline field mapping."""
    return get_raw_config_value("PIPELINE_FIELD_MAP", {"chunk": "chunk_embedding"})
```

**After:**

```python
# configs/configuration_manager.py
def get_pipeline_field_map() -> Dict[str, str]:
    """Get the pipeline field mapping."""
    return get_raw_config_value("PIPELINE_FIELD_MAP", {"chunk": "chunk_embedding"})

# Second definition removed!
```

### Example 2: Duplicated Logic

**Before:**

Two identical implementations of the same recursive mapping update logic:

```python
# mapping/helper.py
def mapping_update(base_mapping, settings):
    for key, value in settings.items():
        if (
            key in base_mapping
            and isinstance(base_mapping[key], dict)
            and isinstance(value, dict)
        ):
            mapping_update(base_mapping[key], value)
        else:
            base_mapping[key] = value

# data_process/base_dataset.py
def update_mapping(self, base_mapping: Dict[str, Any], updates: Dict[str, Any]) -> None:
    """Update mapping with additional fields (e.g., vector fields)."""
    for key, value in updates.items():
        if (
            key in base_mapping
            and isinstance(base_mapping[key], dict)
            and isinstance(value, dict)
        ):
            self.update_mapping(base_mapping[key], value)  # Recursive call
        else:
            base_mapping[key] = value
```

**After:**

Single implementation with delegation:

```python
# mapping/helper.py (unchanged)
def mapping_update(base_mapping, settings):
    for key, value in settings.items():
        if (
            key in base_mapping
            and isinstance(base_mapping[key], dict)
            and isinstance(value, dict)
        ):
            mapping_update(base_mapping[key], value)
        else:
            base_mapping[key] = value

# data_process/base_dataset.py (now delegates)
from mapping.helper import mapping_update

class BaseDataset(ABC):
    # ...
    
    def update_mapping(self, base_mapping: Dict[str, Any], updates: Dict[str, Any]) -> None:
        """Update mapping with additional fields (e.g., vector fields).
        
        This is a convenience wrapper around mapping.helper.mapping_update.
        """
        mapping_update(base_mapping, updates)
```

## Benefits Summary

### Issue #2 Benefits
- ✅ No more path manipulation hacks in every file
- ✅ Cleaner, more maintainable code
- ✅ Better IDE support and autocomplete
- ✅ Simple one-time PYTHONPATH setup
- ✅ Follows Python best practices

### Issue #3 Benefits
- ✅ Library code is testable
- ✅ Can be used in automation
- ✅ Backward compatible (defaults to interactive)
- ✅ Clear separation of concerns
- ✅ No surprises for library users

### Issue #5 Benefits
- ✅ Single source of truth
- ✅ Easier maintenance
- ✅ Less code to maintain
- ✅ No risk of implementations diverging
- ✅ Clearer code organization

## Migration Checklist

If you're using this codebase, here's what you need to do:

- [ ] Set PYTHONPATH: `export PYTHONPATH="/path/to/opensearch-ml-quickstart:$PYTHONPATH"`
- [ ] Remove any custom `sys.path` manipulation in your scripts
- [ ] Update test code to use `confirm=False` for cleanup methods
- [ ] Update automation scripts to use `confirm=False` for cleanup methods
- [ ] Run your test suite to verify everything works
- [ ] Update any documentation that references the old sys.path.append pattern

## Verification

Run the test script to verify all fixes:

```bash
python test_fixes.py
```

Expected output:
```
======================================================================
Testing fixes for codebase critique issues #2, #3, and #5
======================================================================
Testing Issue #2: Package imports...
  ✓ All modules imported successfully without sys.path manipulation

Testing Issue #3: Confirm parameters in cleanup methods...
  ✓ models.ml_model.MlModel._undeploy_and_delete_model has confirm parameter (default=True)
  ✓ models.ml_model_group.MlModelGroup._delete_model_group has confirm parameter (default=True)
  ✓ connectors.ml_connector.MlConnector._delete_connector has confirm parameter (default=True)
  ✓ client.os_ml_client_wrapper.OsMlClientWrapper.cleanup_kNN has confirm parameter (default=True)

Testing Issue #5: No duplicate functions...
  ✓ get_pipeline_field_map defined only once in configuration_manager
  ✓ BaseDataset.update_mapping properly delegates to mapping.helper.mapping_update

======================================================================
Summary:
======================================================================
Issue #2 (sys.path.append): ✓ PASSED
Issue #3 (input() calls): ✓ PASSED
Issue #5 (duplicated code): ✓ PASSED
======================================================================

🎉 All tests passed! The fixes are working correctly.
```
