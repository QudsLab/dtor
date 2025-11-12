# PyPI Upload Checklist for dtor

## ✅ What's Already Done

- [x] `setup.py` configured with all metadata
- [x] `requirements.txt` created with dependencies
- [x] `setup.py` reads from `requirements.txt`
- [x] LICENSE file (MIT)
- [x] `MANIFEST.in` for including necessary files
- [x] PyPI classifiers added
- [x] GitHub Actions test workflow (`.github/workflows/test.yml`)
- [x] GitHub Actions publish workflow (`.github/workflows/publish.yml`)
- [x] Python version requirement set to >=3.8
- [x] Repository URL updated to QudsLab/dtor

## ⚠️ What You Need to Do Before Publishing

### 1. **Update README.md** (Required)
Your README is currently empty. Add:
- Project description
- Installation instructions
- Usage examples
- Features list
- Basic documentation
- Links to documentation/issues

**Example structure:**
```markdown
# dtor - Tor Process Management Library

A comprehensive Python library for managing Tor processes...

## Installation
```bash
pip install dtor
```

## Quick Start
```python
from dtor import TorHandler

handler = TorHandler()
handler.download_and_install_tor_binaries()
handler.start_tor_service()
```

## Features
- Automatic Tor binary download
- Hidden service management
- ...
```

### 2. **Create PyPI Account & API Token**
1. Sign up at https://pypi.org/account/register/
2. Verify your email
3. Go to https://pypi.org/manage/account/token/
4. Create API token with name "dtor-upload"
5. Copy the token (starts with `pyp-`)

### 3. **Add PyPI Token to GitHub Secrets**
1. Go to https://github.com/QudsLab/dtor/settings/secrets/actions
2. Click "New repository secret"
3. Name: `PYPI_API_TOKEN`
4. Value: Your PyPI API token
5. Click "Add secret"

### 4. **Test Locally First**
```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check the build
twine check dist/*

# Test upload to TestPyPI (optional)
twine upload --repository testpypi dist/*
```

### 5. **Manual Upload to PyPI**
```bash
# Upload to real PyPI
twine upload dist/*
# Username: __token__
# Password: your-pypi-token
```

### 6. **OR Automatic Upload via GitHub Release**
1. Push all changes to GitHub
2. Create a new release:
   - Go to https://github.com/QudsLab/dtor/releases/new
   - Tag: `v0.1.0`
   - Title: `v0.1.0 - Initial Release`
   - Description: Release notes
   - Click "Publish release"
3. GitHub Actions will automatically build and publish to PyPI

## 📝 Current Package Info

- **Name:** dtor
- **Version:** 0.1.0
- **Python:** >=3.8
- **Dependencies:** psutil, requests
- **License:** MIT
- **Author:** Ahmad Yousuf
- **Repository:** https://github.com/QudsLab/dtor

## 🔄 For Future Updates

1. Update version in `setup.py` and `dtor/__init__.py`
2. Update CHANGELOG (if you create one)
3. Commit changes
4. Create new GitHub release with new version tag
5. Automatic publish via GitHub Actions

## ⚡ Quick Command Reference

```bash
# Build
python -m build

# Check
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Clean build artifacts
rm -rf build/ dist/ *.egg-info/
```
