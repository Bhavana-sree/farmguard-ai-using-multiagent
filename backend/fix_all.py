"""
Run all database fixes
"""

import subprocess
import os

print("=" * 60)
print("🔧 FARMGUARD AI - DATABASE FIXES")
print("=" * 60)

# Run farmers fix
print("\n📋 Running farmers table fix...")
subprocess.run(["python", "fix_farmers.py"])

# Run companies fix
print("\n📋 Running companies table fix...")
subprocess.run(["python", "fix_companies.py"])

print("\n" + "=" * 60)
print("✅ ALL FIXES COMPLETE!")
print("=" * 60)
print("\n🚀 Next steps:")
print("1. Restart your backend: python -m uvicorn app.main:app --reload")
print("2. Run tests: python test_api.py")