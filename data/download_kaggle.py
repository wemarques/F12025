import os
import subprocess
import zipfile

DATA_DIR = os.path.join(os.path.dirname(__file__), 'raw')
DATASET_NAME = "rohanrao/formula-1-world-championship-1950-2020" # Update if needed

def download_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    print(f"Downloading {DATASET_NAME} to {DATA_DIR}...")
    try:
        subprocess.run(["kaggle", "datasets", "download", "-d", DATASET_NAME, "-p", DATA_DIR], check=True)
        print("Download complete.")
        
        # Unzip
        for file in os.listdir(DATA_DIR):
            if file.endswith(".zip"):
                with zipfile.ZipFile(os.path.join(DATA_DIR, file), 'r') as zip_ref:
                    zip_ref.extractall(DATA_DIR)
                print(f"Unzipped {file}")
                
    except Exception as e:
        print(f"Error downloading data: {e}")
        print("Ensure you have kaggle.json in your .kaggle directory or env vars set.")

if __name__ == "__main__":
    download_data()
