#!/usr/bin/env python3
"""
Simple Hugging Face login script
"""
from huggingface_hub import login
import getpass

print("="*60)
print("Hugging Face Login")
print("="*60)
print("\nGet your token from: https://huggingface.co/settings/tokens")
print("(You need 'Write' access)")
print()

token = getpass.getpass("Enter your HF token: ")

if token:
    try:
        login(token=token)
        print("\n✅ Successfully logged in to Hugging Face!")
    except Exception as e:
        print(f"\n❌ Login failed: {e}")
else:
    print("\n❌ No token provided")
