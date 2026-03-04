# Installation Guide

## Quick Start

```bash
# Clone the repository
gh repo clone Jon-AtAWS/opensearch-ml-quickstart
cd opensearch-ml-quickstart

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the project (this is the key step!)
pip install -e .
```

## What does `pip install -e .` do?

The `-e` flag means "editable install". This command:

1. **Installs all dependencies** from `requirements.txt` automatically
2. **Makes the project importable** - Python now knows where to find `client`, `configs`, `models`, etc.
3. **Keeps your code editable** - Any changes you make are immediately available
4. **Eliminates import issues** - No need for `sys.path.append` anywhere

## How it works

The `pyproject.toml` file tells Python:
- This is a package called `opensearch-ml-quickstart`
- These are the folders that contain code: `client`, `configs`, `connectors`, `data_process`, `mapping`, `models`
- These are the dependencies it needs

Once installed, Python can find these modules from anywhere in your project.

## Before vs After

**Before (without pyproject.toml):**
```python
# Every file needed this ugly hack
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client import helper  # Now it works
```

**After (with pyproject.toml and pip install -e .):**
```python
# Clean imports, no path manipulation needed!
from client import helper  # Just works!
```

## Verifying Installation

After running `pip install -e .`, you can verify it worked:

```bash
# Test imports work
python -c "from client import helper; from configs import configuration_manager; print('✓ Imports work!')"

# Run the test suite
python test_fixes.py

# Run an example
python examples/dense_hnsw_search.py --help
```

## FAQ

**Q: Do I need to run `pip install -e .` every time I change code?**
A: No! That's what "editable" means - your changes are immediately available.

**Q: What if I add a new dependency?**
A: Add it to `pyproject.toml` under `dependencies`, then run `pip install -e .` again.

**Q: Can I still use `pip install -r requirements.txt`?**
A: Yes, but `pip install -e .` is better because it also sets up the package structure.

**Q: What if I don't want to install it?**
A: You'd need to add `sys.path.append` back to every file, which is messy. The editable install is the clean solution.

## Troubleshooting

**Import errors after installation:**
```bash
# Make sure you're in the virtual environment
source .venv/bin/activate

# Reinstall
pip install -e .
```

**"No module named 'client'" error:**
```bash
# You probably forgot to run pip install -e .
pip install -e .
```

## Summary

The `pyproject.toml` + `pip install -e .` approach is:
- ✅ The modern Python standard
- ✅ Cleaner than `sys.path.append` everywhere
- ✅ Better for development (editable mode)
- ✅ Better for IDEs (they understand the structure)
- ✅ One command to set everything up

Just run `pip install -e .` once after cloning, and you're good to go!
