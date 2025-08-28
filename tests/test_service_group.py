"""Test cases for Service Group functionality with data-driven testing."""

import pytest
import json
from pages.login_page import LoginPage
from pages.service_group_page import ServiceGroupPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load test data from JSON file
with open("data/service_group_data.json", "r", encoding="utf-8") as file:
    test_data = json.load(file)["test_cases"]

@pytest.mark.parametrize("test_case", test_data, ids=lambda x: f"test_id_{x['test_id']}")
def test_add_edit_delete_service_group(driver, test_case):
    """Test the full lifecycle of adding, editing, and deleting a service group."""
    test_id = test_case["test_id"]
    group_name = test_case["group_name"]
    description = test_case["description"]
    new_group_name = test_case["new_group_name"]
    new_description = test_case["new_description"]

    wait = WebDriverWait(driver, 30)
    login_page = LoginPage(driver)
    service_group = ServiceGroupPage(driver)

    # Login
    login_page.login()
    wait.until(lambda d: d.current_url.startswith("https://clinic-local.amaz.com.vn/"))

    # Navigate to service group page
    service_group.navigate()

    # Add group
    service_group.add_group(group_name, description)
    assert service_group.verify_add_success(), f"Test {test_id}: Add failed"
    assert service_group.verify_group_in_table(group_name), f"Test {test_id}: Group not found after add"

    # Edit group
    service_group.edit_group(group_name, new_group_name, new_description)
    assert service_group.verify_edit_success(new_group_name), f"Test {test_id}: Edit failed"
    assert service_group.verify_group_in_table(new_group_name), f"Test {test_id}: Group not found after edit"

    # Delete group
    service_group.delete_group(new_group_name)
    assert service_group.verify_delete_success(new_group_name), f"Test {test_id}: Delete failed"