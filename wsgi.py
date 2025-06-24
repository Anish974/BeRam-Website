from beram import create_app
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create production app
app = create_app('production')

if __name__ == '__main__':
    app.run()
