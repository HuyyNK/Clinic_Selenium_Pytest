"""Pytest configuration and fixtures."""

import pytest
import logging
import os
from selenium.webdriver.support.ui import WebDriverWait
from utils.driver_factory import get_driver
import config.config as cfg

# Cấu hình logging
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
log_file = os.path.join(log_directory, "test_log.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def driver():
    """Fixture to initialize and teardown WebDriver."""
    logger.info("Setting up test environment...")
    driver = get_driver(cfg.BROWSER)
    driver.implicitly_wait(cfg.IMPLICIT_WAIT)
    driver.get(cfg.BASE_URL)
    yield driver
    logger.info("Tearing down test environment...")
    driver.quit()