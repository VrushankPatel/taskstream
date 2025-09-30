#!/usr/bin/env python3
"""
Update TaskStream files on Hugging Face
"""

from huggingface_hub import HfApi
import sys

def update_hf_files(username, dataset_name="taskstream"):
    """Update specific files on HF"""
    
    api = HfApi()
    repo_id = f"{username}/{dataset_name}"
    
    print(f"Updating files in: {repo_id}")
    
    try:
        # Upload README_HF.md as README.md
        print("\n📤 Uploading README.md with dataset config...")
        api.upload_file(
            path_or_fileobj="README_HF.md",
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type="dataset",
            commit_message="fix: add dataset config to resolve FileFormatMismatchError"
        )
        
        # Upload dataset loader script
        print("📤 Uploading taskstream.py loader script...")
        api.upload_file(
            path_or_fileobj="taskstream.py",
            path_in_repo="taskstream.py",
            repo_id=repo_id,
            repo_type="dataset",
            commit_message="add: dataset loading script for HF datasets library"
        )
        
        print("\n✅ Files updated successfully!")
        print(f"\n🎉 Check your dataset: https://huggingface.co/datasets/{repo_id}")
        print("\nThe error should be resolved within a few minutes as HF rebuilds the dataset.")
        return True
        
    except Exception as e:
        print(f"\n❌ Error updating files: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 update_hf_files.py YOUR_HF_USERNAME")
        sys.exit(1)
    
    username = sys.argv[1]
    update_hf_files(username)
