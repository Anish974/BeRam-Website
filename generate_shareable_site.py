#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import shutil
import zipfile

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 50)
    print(text)
    print("=" * 50 + "\n")

def install_requirements():
    """Install required packages"""
    print_header("Step 1: Installing required packages")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4"])

def start_flask_app():
    """Start the Flask application"""
    print_header("Step 2: Starting the Flask application")
    
    # Different command based on OS
    if os.name == 'nt':  # Windows
        flask_process = subprocess.Popen(["start", "cmd", "/k", "python", "run.py"], shell=True)
    else:  # Unix/Linux/Mac
        flask_process = subprocess.Popen(["python", "run.py"], 
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE,
                                         start_new_session=True)
    
    print("Flask application starting...")
    print("Waiting for Flask to initialize...")
    time.sleep(5)  # Give Flask time to start
    
    return flask_process

def generate_static_site():
    """Run the static site generator"""
    print_header("Step 3: Generating static site")
    subprocess.check_call([sys.executable, "static_site_generator.py"])

def create_zip_file():
    """Create a ZIP file of the static site"""
    print_header("Step 4: Creating ZIP file")
    
    output_dir = "beram_static_site"
    zip_filename = "BeRAM_Website_Shareable.zip"
    
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
    
    print(f"Creating {zip_filename}...")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_dir)
                zipf.write(file_path, arcname)
    
    print(f"ZIP file created: {zip_filename}")

def main():
    """Main function to run the entire process"""
    print_header("BeRAM Website - Static Site Generator")
    
    try:
        # Step 1: Install requirements
        install_requirements()
        
        # Step 2: Start Flask app
        flask_process = start_flask_app()
        
        # Step 3: Generate static site
        input("Press Enter when Flask is running to continue with static site generation...")
        generate_static_site()
        
        # Step 4: Create ZIP file
        create_zip_file()
        
        # Final message
        print_header("COMPLETE! The shareable website has been created")
        print("You can find the following files:")
        print("- beram_static_site folder: Contains the static website")
        print("- BeRAM_Website_Shareable.zip: Compressed version ready to share")
        print("\nTo share with investors:")
        print("1. Send them the BeRAM_Website_Shareable.zip file")
        print("2. They can extract it and open index.html in any browser")
        print("3. No installation or technical skills required")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Static site generation failed. Please check the error message above.")
    
    finally:
        # Clean up Flask process if it's still running
        if 'flask_process' in locals():
            try:
                if os.name != 'nt':  # Not Windows
                    os.killpg(os.getpgid(flask_process.pid), signal.SIGTERM)
            except:
                pass
        
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
