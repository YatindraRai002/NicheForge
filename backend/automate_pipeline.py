import os
import time
import subprocess
import sys

DATASET_FILE = "dataset.json"
TRAIN_SCRIPT = "fine_tuning/train.py"

def wait_for_dataset():
    print(f"Waiting for {DATASET_FILE} to be populated...")
    initial_size = os.path.getsize(DATASET_FILE)
    
    while True:
        if not os.path.exists(DATASET_FILE):
             time.sleep(5)
             continue
             
        current_size = os.path.getsize(DATASET_FILE)
        # If size changed significantly (more than just empty list [])
        if current_size > 100 and current_size != initial_size:
            print(f"Dataset detected! Size: {current_size} bytes")
            # Wait a few seconds to ensure write is complete
            time.sleep(5)
            return
        
        # Check if generator is still running? 
        # For simplicity, we just poll file size.
        # If the generator crashes, this might wait forever. 
        # But for now, we assume success.
        
        print(f"Still waiting... (Current size: {current_size})")
        time.sleep(10)

def run_fine_tuning():
    print("Starting fine-tuning...")
    try:
        subprocess.check_call([sys.executable, TRAIN_SCRIPT])
        print("Fine-tuning complete!")
    except subprocess.CalledProcessError as e:
        print(f"Fine-tuning failed with error: {e}")
        print("Please check the terminal output for details.")

if __name__ == "__main__":
    wait_for_dataset()
    run_fine_tuning()
