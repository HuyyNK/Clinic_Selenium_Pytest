"""Configuration file for EMR test framework."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base URL and credentials
BASE_URL = os.getenv("BASE_URL", "https://clinic-local.amaz.com.vn/login#/login")
USERNAME = os.getenv("USERNAME", "huynk.software@gmail.com")
PASSWORD = os.getenv("PASSWORD", "111111a@A")

# Browser configuration
BROWSER = os.getenv("BROWSER", "chrome")

# Timeout settings (seconds)
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", 5))
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", 10))

# Retry settings
MAX_RETRY_ATTEMPTS = 3

# Notes:
# - Add .env file with variables (BASE_URL, USERNAME, PASSWORD, etc.)
# - Use environment-specific configs (dev/staging/prod) if needed