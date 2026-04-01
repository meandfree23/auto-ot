import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add scripts to path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "scripts"))

import poll_drive_to_tasks as poll

def simulate():
    load_dotenv()
    print(f"--- Google Drive Status Check ---")
    print(f"WATCH_FOLDER_ID: {poll.WATCH_FOLDER_ID}")
    
    try:
        service = poll.build_drive_service()
        print("✅ Credentials: OK")
        
        # 1. Check for files
        query = f"'{poll.WATCH_FOLDER_ID}' in parents and trashed = false"
        results = service.files().list(
            q=query,
            fields="files(id, name, mimeType, parents, webViewLink, modifiedTime)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        
        files = results.get("files", [])
        print(f"Found {len(files)} files in the watched folder.")
        
        for f in files:
            is_target = poll.is_target_file(f)
            status = "✅ Processable" if is_target else "❌ Skipped (MimeType)"
            print(f"- {f.get('name')} ({f.get('mimeType')}): {status}")
            
            if is_target:
                task = poll.create_task_json(f)
                print(f"  [Simulation] Would create Job ID: {task['job_id']}")
                print(f"  [Simulation] Task Metadata: {task['source']['file_name']} -> {task['project_type']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    simulate()
