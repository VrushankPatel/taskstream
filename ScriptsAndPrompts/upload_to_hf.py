#!/usr/bin/env python3
"""
Upload TaskStream dataset to Hugging Face
"""

from huggingface_hub import HfApi, create_repo
from pathlib import Path
import sys

def upload_to_hf(username, dataset_name="taskstream", private=False):
    """
    Upload TaskStream dataset to Hugging Face
    
    Args:
        username: Your Hugging Face username
        dataset_name: Name for the dataset (default: taskstream)
        private: Whether to make the dataset private (default: False)
    """
    
    api = HfApi()
    repo_id = f"{username}/{dataset_name}"
    
    print(f"Preparing to upload to: {repo_id}")
    print(f"Private: {private}")
    
    # Create repository
    try:
        print(f"\nCreating repository: {repo_id}")
        create_repo(
            repo_id=repo_id,
            repo_type="dataset",
            private=private,
            exist_ok=True
        )
        print("✅ Repository created/verified")
    except Exception as e:
        print(f"❌ Error creating repository: {e}")
        return False
    
    # Upload files
    directories = [
        "workflows",
        "decisions", 
        "communications",
        "org_structures",
        "metrics",
        "policies"
    ]
    
    files_to_upload = [
        "SPECIFICATION.md",
        "CHANGES.md",
        "pending_items.md",
        "taskstream.py"
    ]
    
    # Use README_HF.md as README.md if it exists
    if Path("README_HF.md").exists():
        print("\n📄 Using README_HF.md as dataset card...")
        files_to_upload.append("README_HF.md")
    elif Path("README.md").exists():
        files_to_upload.append("README.md")
    
    try:
        # Upload individual files
        print("\n📤 Uploading core files...")
        for file in files_to_upload:
            if Path(file).exists():
                target_name = "README.md" if file == "README_HF.md" else file
                print(f"  Uploading {file} -> {target_name}")
                api.upload_file(
                    path_or_fileobj=file,
                    path_in_repo=target_name,
                    repo_id=repo_id,
                    repo_type="dataset"
                )
        
        # Upload directories
        print("\n📤 Uploading content directories...")
        for directory in directories:
            if Path(directory).exists():
                file_count = len(list(Path(directory).glob("*")))
                print(f"  Uploading {directory}/ ({file_count} files)")
                api.upload_folder(
                    folder_path=directory,
                    path_in_repo=directory,
                    repo_id=repo_id,
                    repo_type="dataset"
                )
        
        print("\n✅ Upload complete!")
        print(f"\n🎉 Your dataset is live at: https://huggingface.co/datasets/{repo_id}")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during upload: {e}")
        return False

def main():
    print("="*60)
    print("TaskStream → Hugging Face Upload Tool")
    print("="*60)
    
    # Get username
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = input("\nEnter your Hugging Face username: ").strip()
    
    if not username:
        print("❌ Username is required")
        sys.exit(1)
    
    # Get dataset name
    dataset_name = input("Dataset name (default: taskstream): ").strip() or "taskstream"
    
    # Ask about privacy
    private_input = input("Make dataset private? (y/N): ").strip().lower()
    private = private_input == 'y'
    
    # Confirm
    print("\n" + "="*60)
    print("Upload Configuration:")
    print(f"  Repository: {username}/{dataset_name}")
    print(f"  Private: {private}")
    print("="*60)
    
    confirm = input("\nProceed with upload? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Upload cancelled")
        sys.exit(0)
    
    # Upload
    success = upload_to_hf(username, dataset_name, private)
    
    if success:
        print("\n" + "="*60)
        print("Next Steps:")
        print("="*60)
        print(f"1. Visit: https://huggingface.co/datasets/{username}/{dataset_name}")
        print("2. Review the dataset card (README.md)")
        print("3. Add tags and update metadata if needed")
        print("4. Share with the community!")
        sys.exit(0)
    else:
        print("\n❌ Upload failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
