# 🚀 READY TO UPLOAD TO PYPI!

## ✅ What I Did For You:

1. ✅ Created comprehensive README.md with examples
2. ✅ Built the package (dist/dtor-0.1.0.tar.gz and .whl)
3. ✅ Verified package is valid (twine check passed)
4. ✅ Created upload script (upload_to_pypi.py)

## 📦 Package Files Ready:
- `dist/dtor-0.1.0.tar.gz` (source distribution)
- `dist/dtor-0.1.0-py3-none-any.whl` (wheel)

---

## 🔑 WHAT YOU NEED TO DO:

### Step 1: Get PyPI Token (5 minutes)

1. **Create PyPI account** (if you don't have one):
   - Go to: https://pypi.org/account/register/
   - Verify your email

2. **Create API Token**:
   - Login to PyPI
   - Go to: https://pypi.org/manage/account/token/
   - Click "Add API token"
   - Token name: `dtor-upload`
   - Scope: "Entire account" (you can limit it later)
   - Click "Add token"
   - **COPY THE TOKEN** (starts with `pyp-...`)
   - ⚠️ You won't see it again!

---

### Step 2: Upload to PyPI (2 methods)

#### **Method A: Using Upload Script (EASIEST)**

```powershell
# Set your token as environment variable
$env:TWINE_PASSWORD = "pyp-your-token-here"

# Run upload script
python upload_to_pypi.py
```

The script will:
- Optionally test on TestPyPI first
- Upload to real PyPI
- Give you confirmation

---

#### **Method B: Manual Upload**

```powershell
# Set environment variables
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pyp-your-token-here"

# Upload
twine upload dist/*
```

---

### Step 3: Verify It Worked

After upload, check:
- **PyPI page**: https://pypi.org/project/dtor/
- **Test install**: `pip install dtor`

---

## 🔄 For Future Updates:

1. Update version in `setup.py` and `dtor/__init__.py`
2. Rebuild: `python -m build`
3. Upload: `python upload_to_pypi.py`

OR use GitHub releases (automatic via `.github/workflows/publish.yml`)

---

## 🛡️ GitHub Secrets (For Automatic Publishing)

To use automatic GitHub Actions publishing:

1. Go to: https://github.com/QudsLab/dtor/settings/secrets/actions
2. Click "New repository secret"
3. Name: `PYPI_API_TOKEN`
4. Value: Your PyPI token
5. Click "Add secret"

Then create a GitHub release and it auto-publishes!

---

## 📋 Quick Checklist:

- [ ] Have PyPI account
- [ ] Created API token
- [ ] Copied token somewhere safe
- [ ] Set `$env:TWINE_PASSWORD`
- [ ] Run `python upload_to_pypi.py`
- [ ] Verify on PyPI
- [ ] Test: `pip install dtor`
- [ ] (Optional) Add token to GitHub secrets

---

## 🆘 Troubleshooting:

**"Package already exists"**
- Version 0.1.0 is already uploaded
- Update version in setup.py to 0.1.1
- Rebuild: `python -m build`
- Upload again

**"Invalid token"**
- Make sure token starts with `pyp-`
- Username should be `__token__` (with double underscores)
- Token scope should include upload permissions

**"403 Forbidden"**
- Package name might be taken
- Try different name in setup.py
- Or contact PyPI to claim the name

---

## 📞 Need Help?

- PyPI Help: https://pypi.org/help/
- Packaging Guide: https://packaging.python.org/
- Twine Docs: https://twine.readthedocs.io/

---

**The package is 100% ready to upload. You just need your PyPI token!**
