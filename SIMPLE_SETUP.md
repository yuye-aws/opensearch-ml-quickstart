# Simple Setup Guide

This project has been cleaned up to remove excessive `sys.path.append` calls. Here's how to use it:

## Quick Start

1. **Clone and install dependencies:**
   ```bash
   git clone <repo-url>
   cd opensearch-ml-quickstart
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set PYTHONPATH (choose one method):**

   **Method A: In your shell session**
   ```bash
   export PYTHONPATH="${PWD}:${PYTHONPATH}"
   ```

   **Method B: In your shell profile (~/.bashrc, ~/.zshrc)**
   ```bash
   export PYTHONPATH="/full/path/to/opensearch-ml-quickstart:${PYTHONPATH}"
   ```

   **Method C: When running scripts**
   ```bash
   PYTHONPATH=/path/to/opensearch-ml-quickstart python examples/dense_hnsw_search.py
   ```

3. **Run examples:**
   ```bash
   python examples/dense_hnsw_search.py --help
   ```

## What Changed?

- ✅ Removed all `sys.path.append(os.path.dirname(...))` calls from 17 files
- ✅ Added `confirm` parameter to cleanup methods (for automation/testing)
- ✅ Removed duplicate functions
- ✅ Cleaner, more maintainable code

## For IDE Users

**VS Code:** Add to `.vscode/settings.json`:
```json
{
  "python.analysis.extraPaths": ["${workspaceFolder}"]
}
```

**PyCharm:** Right-click project root → "Mark Directory as" → "Sources Root"

## That's It!

No complex packaging, no pip install tricks. Just set PYTHONPATH and you're good to go.
