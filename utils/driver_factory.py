"""Utility to create WebDriver instances based on browser type."""

from selenium import webdriver

def get_driver(browser="chrome"):
    """Create and return a WebDriver instance for the specified browser.

    Args:
        browser (str): The browser type (default: "chrome", supported: "chrome", "firefox").

    Returns:
        webdriver: The WebDriver instance.

    Raises:
        ValueError: If an unsupported browser is specified.
    """
    try:
        if browser.lower() == "chrome":
            driver = webdriver.Chrome()
        elif browser.lower() == "firefox":
            driver = webdriver.Firefox()
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        driver.maximize_window()
        return driver
    except Exception as e:
        raise