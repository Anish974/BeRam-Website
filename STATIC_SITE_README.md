# BeRAM Website - Shareable Static Version

This guide explains how to create a shareable version of the BeRAM website that can be viewed without any installation or technical skills.

## What This Does

The included scripts will:

1. Create a static HTML version of your BeRAM website
2. Package everything into a ZIP file
3. Generate helper files to make viewing easy for non-technical users

The result is a completely self-contained website that can be shared with investors or stakeholders who can view it on their local computer without needing to install anything or access your source code.

## How to Generate the Shareable Website

### Prerequisites

- Python 3.6 or higher
- Your BeRAM Flask application

### Steps

1. **Run the batch file**:
   - Simply double-click on `generate_shareable_site.bat`
   - This will install required packages, start your Flask app, and generate the static site
   - When prompted, press Enter to continue the process

2. **Wait for completion**:
   - The process will take a few minutes depending on the size of your website
   - When complete, you'll see a success message

3. **Find the output**:
   - `beram_static_site` folder: Contains the static website
   - `BeRAM_Website_Shareable.zip`: Compressed version ready to share

## Sharing with Investors

1. Send them the `BeRAM_Website_Shareable.zip` file
2. Provide these simple instructions:
   - Extract the ZIP file to a folder on your computer
   - Open the extracted folder
   - Double-click on `index.html` or `Open_BeRAM_Website.bat` to view the website
   - No installation or technical skills required

## What's Included in the Shareable Version

The static website includes:

- All HTML pages from your BeRAM website
- All CSS, JavaScript, and images
- A README.html file with viewing instructions
- A batch file for easy opening on Windows

## Limitations

- Forms that submit data won't work (like contact forms)
- Any server-side functionality won't be available
- External links will still require an internet connection

## Troubleshooting

If you encounter issues:

1. Make sure your Flask application is running before generating the static site
2. Check that all static files (CSS, JS, images) are in the correct locations
3. If links don't work in the static version, the generator might need adjustments for your specific site structure
