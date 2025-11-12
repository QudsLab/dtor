# PyPI Publishing Guide for dtor

## Prerequisites

1. Install build tools:
```bash
pip install --upgrade build twine
```

2. Create PyPI account at https://pypi.org/account/register/

3. Create API token at https://pypi.org/manage/account/token/

## Build the Package

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build the package
python -m build
```

This creates:
- `dist/dtor-0.1.0.tar.gz` (source distribution)
- `dist/dtor-0.1.0-py3-none-any.whl` (wheel distribution)

## Test on TestPyPI (Optional but Recommended)

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ dtor
```

## Upload to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*
```

You'll be prompted for:
- Username: `__token__`
- Password: Your PyPI API token (starts with `pyp-`)

## Verify Installation

```bash
pip install dtor
```

## Version Updates

For new versions:
1. Update version in `setup.py` and `dtor/__init__.py`
2. Update `README.md` with changelog
3. Create a git tag: `git tag v0.1.1`
4. Push tag: `git push origin v0.1.1`
5. Rebuild and upload

## Automated Publishing (Optional)

Create `.github/workflows/publish.yml` for automatic PyPI publishing on release.
