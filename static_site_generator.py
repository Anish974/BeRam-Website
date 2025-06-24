import os
import sys
import shutil
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time
import re

# Configuration
BASE_URL = "http://127.0.0.1:5000"  # Your Flask app URL when running locally
OUTPUT_DIR = "beram_static_site"     # Output directory for static files
IGNORED_URLS = [
    "mailto:",                       # Ignore email links
    "#",                             # Ignore anchor links
    "javascript:",                   # Ignore javascript links
]
STATIC_DIRS = ["css", "js", "img", "assets"]  # Static directories to copy

# Create output directory
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR)

# Create directories for static files
for static_dir in STATIC_DIRS:
    os.makedirs(os.path.join(OUTPUT_DIR, static_dir), exist_ok=True)

# Track processed URLs to avoid duplicates
processed_urls = set()
urls_to_process = [BASE_URL]

def clean_url(url):
    """Clean URL by removing fragments and query parameters"""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

def is_valid_url(url):
    """Check if URL should be processed"""
    if not url:
        return False

    # Skip ignored URL patterns
    for pattern in IGNORED_URLS:
        if url.startswith(pattern):
            return False

    # Only process URLs from the same domain
    parsed_url = urlparse(url)
    parsed_base = urlparse(BASE_URL)
    return parsed_url.netloc == parsed_base.netloc or not parsed_url.netloc

def get_output_path(url):
    """Convert URL to local file path"""
    parsed = urlparse(url)
    path = parsed.path.strip("/")

    # Handle root URL
    if not path:
        return os.path.join(OUTPUT_DIR, "index.html")

    # Handle paths without extensions (add .html)
    if not os.path.splitext(path)[1]:
        if path.endswith('/'):
            path = os.path.join(path, "index.html")
        else:
            path = f"{path}.html"

    return os.path.join(OUTPUT_DIR, path)

def save_static_file(url, content):
    """Save static file (CSS, JS, images)"""
    parsed = urlparse(url)
    path = parsed.path.lstrip("/")
    output_path = os.path.join(OUTPUT_DIR, path)

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(content)

    return output_path

def process_html(url, content):
    """Process HTML content, extract links, and fix paths"""
    soup = BeautifulSoup(content, "html.parser")

    # Ensure viewport meta tag exists for responsive design
    head = soup.find('head')
    if head:
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if not viewport:
            viewport = soup.new_tag('meta')
            viewport['name'] = 'viewport'
            viewport['content'] = 'width=device-width, initial-scale=1.0'
            if head.contents:
                head.contents[0].insert_before(viewport)
            else:
                head.append(viewport)

    # Find all links
    for tag in soup.find_all(["a", "link", "script", "img", "source", "video"]):
        # Process different tag types
        if tag.name == "a" and tag.has_attr("href"):
            attr = "href"
        elif tag.name == "link" and tag.has_attr("href"):
            attr = "href"
        elif tag.name in ["script", "img", "source"] and tag.has_attr("src"):
            attr = "src"
        elif tag.name == "video" and tag.has_attr("poster"):
            attr = "poster"
        else:
            continue

        # Get the link URL
        link_url = tag[attr]

        # Skip if it's an ignored URL
        if not is_valid_url(link_url):
            continue

        # Convert relative URLs to absolute
        if not urlparse(link_url).netloc:
            absolute_url = urljoin(url, link_url)
            link_url = absolute_url

        # Fix URL for static site
        if link_url.startswith(BASE_URL):
            # For internal links, add to processing queue
            if tag.name == "a":
                clean_link = clean_url(link_url)
                if clean_link not in processed_urls:
                    urls_to_process.append(clean_link)

            # Update the link to be relative
            relative_path = urlparse(link_url).path
            if tag.name == "a":
                # For anchor tags, make them relative to the current page
                current_path = urlparse(url).path
                if not current_path or current_path == "/":
                    # If we're at the root, just use the relative path
                    if not relative_path or relative_path == "/":
                        tag[attr] = "index.html"
                    else:
                        # Remove leading slash and add .html if needed
                        rel_path = relative_path.lstrip("/")
                        if not os.path.splitext(rel_path)[1]:
                            if rel_path.endswith('/'):
                                rel_path = f"{rel_path}index.html"
                            else:
                                rel_path = f"{rel_path}.html"
                        tag[attr] = rel_path
                else:
                    # Calculate relative path from current page
                    # This is a simplified approach - might need refinement for complex sites
                    if not relative_path or relative_path == "/":
                        # Link to home from subpage
                        depth = len([p for p in current_path.split("/") if p]) - 1
                        prefix = "../" * depth if depth > 0 else ""
                        tag[attr] = f"{prefix}index.html"
                    else:
                        # Link to another page
                        depth = len([p for p in current_path.split("/") if p])
                        prefix = "../" * depth if depth > 0 else ""
                        rel_path = relative_path.lstrip("/")
                        if not os.path.splitext(rel_path)[1]:
                            if rel_path.endswith('/'):
                                rel_path = f"{rel_path}index.html"
                            else:
                                rel_path = f"{rel_path}.html"
                        tag[attr] = f"{prefix}{rel_path}"
            else:
                # For other tags (CSS, JS, images), use a simpler approach
                tag[attr] = relative_path.lstrip("/")

    # Fix Flask-specific URL patterns
    html_content = str(soup)
    # Replace url_for patterns
    html_content = re.sub(r'url_for\([\'"]static[\'"]\s*,\s*filename=[\'"]([^\'"]+)[\'"]\)', r'\1', html_content)

    return html_content, soup.find_all("a", href=True)

def fetch_and_process_url(url):
    """Fetch URL content and process it"""
    print(f"Processing: {url}")

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"  Error: HTTP {response.status_code}")
            return

        content_type = response.headers.get("Content-Type", "").lower()

        # Process HTML pages
        if "text/html" in content_type:
            html_content, links = process_html(url, response.text)

            # Save the processed HTML
            output_path = get_output_path(url)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            print(f"  Saved: {output_path}")

        # Save static files directly
        elif any(f"/{static_dir}/" in url for static_dir in STATIC_DIRS):
            output_path = save_static_file(url, response.content)
            print(f"  Saved static: {output_path}")

    except Exception as e:
        print(f"  Error processing {url}: {str(e)}")

def copy_static_files():
    """Copy static files from Flask app to static site"""
    static_dir = os.path.join("beram", "static")
    if os.path.exists(static_dir):
        for root, dirs, files in os.walk(static_dir):
            for file in files:
                src_path = os.path.join(root, file)
                # Get relative path from static directory
                rel_path = os.path.relpath(src_path, static_dir)
                dest_path = os.path.join(OUTPUT_DIR, rel_path)

                # Create destination directory if it doesn't exist
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Copy the file
                shutil.copy2(src_path, dest_path)
                print(f"Copied static file: {rel_path}")

def create_readme():
    """Create a README.html file with instructions"""
    readme_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BeRAM Website - How to View</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        h1 {
            color: #0B5ED7;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }
        h2 {
            color: #1E3A8A;
            margin-top: 30px;
        }
        .step {
            background-color: #f8f9fa;
            border-left: 4px solid #0B5ED7;
            padding: 15px;
            margin-bottom: 20px;
        }
        .note {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
        }
        code {
            background-color: #f1f1f1;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: Consolas, monospace;
        }
        .button {
            display: inline-block;
            background-color: #0B5ED7;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
        }
        .button:hover {
            background-color: #0a53be;
        }
        /* Responsive adjustments */
        @media (max-width: 768px) {
            body {
                padding: 15px;
            }
            h1 {
                font-size: 1.8rem;
            }
            h2 {
                font-size: 1.5rem;
            }
            .step {
                padding: 10px;
            }
        }
    </style>
</head>
<body>
    <h1>BeRAM Website - Static Version</h1>

    <p>Welcome to the static version of the BeRAM website. This package contains a complete copy of the website that you can view without installing any software or running a web server.</p>

    <div class="note">
        <strong>Note:</strong> This is a static version of the website for demonstration purposes. Some interactive features may not work as they would on the live site.
    </div>

    <h2>How to View the Website</h2>

    <div class="step">
        <h3>Step 1: Extract the Files</h3>
        <p>If you received this as a ZIP file, extract all files to a folder on your computer.</p>
    </div>

    <div class="step">
        <h3>Step 2: Open the Website</h3>
        <p>Simply double-click on the <code>index.html</code> file in the main folder, or right-click and select "Open with" and choose your preferred web browser.</p>
    </div>

    <div class="step">
        <h3>Step 3: Navigate the Website</h3>
        <p>Once opened, you can browse the website just like you would online. Click on links to navigate between pages.</p>
    </div>

    <h2>Viewing on Mobile Devices</h2>

    <div class="step">
        <h3>Option 1: Transfer Files</h3>
        <p>Transfer the entire folder to your mobile device and open the index.html file with any mobile browser.</p>
    </div>

    <div class="step">
        <h3>Option 2: Use a Local Server</h3>
        <p>If you have technical knowledge, you can set up a simple local server on your computer and access it from your mobile device on the same network.</p>
    </div>

    <h2>Troubleshooting</h2>

    <p><strong>If images or styles don't load correctly:</strong> Make sure you've extracted all files and folders from the ZIP file while maintaining the folder structure.</p>

    <p><strong>If links don't work:</strong> Some links might point to external websites or resources that require an internet connection.</p>

    <p><strong>If the site doesn't display properly on mobile:</strong> Try rotating your device or using a different browser.</p>

    <a href="index.html" class="button">Go to BeRAM Homepage</a>

    <p style="margin-top: 50px; color: #6c757d; font-size: 0.9em;">© BeRAM - Bhandarkar Excellences of Research and Management</p>
</body>
</html>
"""

    with open(os.path.join(OUTPUT_DIR, "README.html"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("Created README.html with instructions")

def create_batch_file():
    """Create a batch file to easily open the website on Windows"""
    batch_content = """@echo off
echo Opening BeRAM Website...
start "" "%~dp0index.html"
"""

    with open(os.path.join(OUTPUT_DIR, "Open_BeRAM_Website.bat"), "w") as f:
        f.write(batch_content)
    print("Created Open_BeRAM_Website.bat for easy access")

    # Create a batch file to run the server
    server_batch_content = """@echo off
echo Starting BeRAM Website Server...
cd ..
python run_static_site.py
pause
"""

    with open(os.path.join(OUTPUT_DIR, "Run_Server.bat"), "w") as f:
        f.write(server_batch_content)
    print("Created Run_Server.bat for running the local server")

def copy_server_script():
    """Copy the server script to the parent directory"""
    if os.path.exists("run_static_site.py"):
        print("Copying server script to output directory...")
        with open("run_static_site.py", "r") as f:
            script_content = f.read()

        # Update the static site directory in the script if needed
        script_content = script_content.replace('STATIC_SITE_DIR = "beram_static_site"', f'STATIC_SITE_DIR = "{os.path.basename(OUTPUT_DIR)}"')

        with open(os.path.join(OUTPUT_DIR, ".." , "run_static_site.py"), "w") as f:
            f.write(script_content)
        print("Server script copied successfully")

    # Copy shell script for Unix/Linux/Mac users
    if os.path.exists("run_static_site.sh"):
        print("Copying shell script to output directory...")
        with open("run_static_site.sh", "r") as f:
            shell_content = f.read()

        with open(os.path.join(OUTPUT_DIR, ".." , "run_static_site.sh"), "w") as f:
            f.write(shell_content)

        # Make the shell script executable
        try:
            os.chmod(os.path.join(OUTPUT_DIR, ".." , "run_static_site.sh"), 0o755)
        except Exception as e:
            print(f"Warning: Could not make shell script executable: {e}")

        print("Shell script copied successfully")

def main():
    print("Starting static site generation...")
    print(f"Base URL: {BASE_URL}")
    print(f"Output directory: {OUTPUT_DIR}")

    # First, copy all static files
    copy_static_files()

    # Start the Flask application in a separate process
    print("Please make sure your Flask application is running at", BASE_URL)
    input("Press Enter to continue when the Flask app is running...")

    # Process all URLs
    while urls_to_process:
        url = urls_to_process.pop(0)
        clean_url_str = clean_url(url)

        if clean_url_str in processed_urls:
            continue

        processed_urls.add(clean_url_str)
        fetch_and_process_url(url)

        # Small delay to avoid overwhelming the server
        time.sleep(0.1)

    # Create helper files
    create_readme()
    create_batch_file()
    copy_server_script()

    print("\nStatic site generation complete!")
    print(f"The static website has been created in the '{OUTPUT_DIR}' directory.")
    print("\nTo view the website:")
    print("1. Open index.html directly in your browser")
    print("2. For Windows users, double-click on Open_BeRAM_Website.bat")
    print("\nTo make the website accessible on other devices (phones, tablets):")
    print("1. Run the run_static_site.py script or Run_Server.bat")
    print("2. Access the website from any device on your network using the provided URL")

if __name__ == "__main__":
    main()
