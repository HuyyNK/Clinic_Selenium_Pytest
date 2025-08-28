"""Page object for managing service group operations."""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from utils.retry import retry_on_failure

class ServiceGroupPage:
    """Page object for managing service group operations."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Locators
    LOCATORS = {
        "service_group_image": (By.XPATH, "//img[@class='sc-iOnGvX NPksH group-service']"),
        "add_button": (By.XPATH, "//span[contains(text(), 'Thêm nhóm dịch vụ')]"),
        "specialty_dropdown": (By.XPATH, "//div[contains(@class,'ant-modal')]//label[contains(., 'Chuyên khoa')]/following::div//div[contains(@class,'ant-select-selector')]"),
        "specialty_nhi_khoa": (By.XPATH, "//div[@class='ant-select-item-option-content' and text()='Nhi Khoa']"),
        "group_name_input": (By.XPATH, "//label[contains(., 'Tên nhóm dịch vụ')]/following::input[1]"),
        "description_input": (By.XPATH, "//label[contains(., 'Mô tả')]/following::textarea[1]"),
        "confirm_button": (By.XPATH, "//span[contains(text(), 'Xác nhận')]"),
    }

    # Messages
    MESSAGES = {
        "add_success": "Thêm nhóm dịch vụ thành công",
        "edit_success": "Chỉnh sửa nhóm dịch vụ thành công",
        "delete_success": 'Xoá nhóm dịch vụ "{}" thành công'
    }

    # Helper methods
    def _scroll_to_element(self, element):
        """Scroll the given element into view."""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def _input_text(self, locator, value):
        """Clear and input text into the given locator."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self._scroll_to_element(element)
        element.click()
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(value)

    def _wait_for_toast(self, message, timeout=7):
        """Wait for the latest toast message containing the given text."""
        xpath = f"(//div[contains(@class,'ant-notification-notice-message')][contains(., '{message}')])[last()]"
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)), timeout)

    def _get_row_locator(self, name):
        """Return locator for a row cell with the given name."""
        return (By.XPATH, f"//tbody[@class='ant-table-tbody']//td[normalize-space()='{name}']")

    def _wait_for_row(self, name, present=True, timeout=10):
        """Wait for a row to be present or absent."""
        locator = self._get_row_locator(name)
        condition = EC.presence_of_element_located if present else EC.invisibility_of_element_located
        self.wait.until(condition(locator), timeout)

    def _click_action(self, group_name, action):
        """Click the specified action (edit/delete) for the given group."""
        icon = "ic-edit.svg" if action == "edit" else "ic-delete.svg"
        row_xpath = f"//tbody[@class='ant-table-tbody']//tr[td[normalize-space()='{group_name}']]"
        icon_xpath = f"{row_xpath}//td[last()]//img[@src='/images/{icon}']"
        if action == "delete":
            icon_xpath += "[not(contains(@class,'action-disabled'))]"
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, icon_xpath)))
        self._scroll_to_element(element)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    # Core actions
    @retry_on_failure()
    def navigate(self):
        """Navigate to the service group page."""
        self.wait.until(EC.element_to_be_clickable(self.LOCATORS["service_group_image"])).click()
        self.wait.until(EC.url_contains("clinic-local.amaz.com.vn/#/config/group-service"))

    @retry_on_failure()
    def add_group(self, group_name, description):
        """Add a new service group."""
        self.wait.until(EC.element_to_be_clickable(self.LOCATORS["add_button"])).click()
        self.wait.until(EC.visibility_of_element_located(self.LOCATORS["group_name_input"]))
        self.wait.until(EC.element_to_be_clickable(self.LOCATORS["specialty_dropdown"])).click()
        self.wait.until(EC.element_to_be_clickable(self.LOCATORS["specialty_nhi_khoa"])).click()
        self._input_text(self.LOCATORS["group_name_input"], group_name)
        self._input_text(self.LOCATORS["description_input"], description)
        self.wait.until(EC.element_to_be_clickable(self.LOCATORS["confirm_button"])).click()
        self._wait_for_toast(self.MESSAGES["add_success"])
        self._wait_for_row(group_name)

    @retry_on_failure()
    def edit_group(self, original_name, new_name, new_description):
        """Edit an existing service group."""
        self._click_action(original_name, "edit")
        self.wait.until(EC.visibility_of_element_located(self.LOCATORS["group_name_input"]))
        self._input_text(self.LOCATORS["group_name_input"], new_name)
        self._input_text(self.LOCATORS["description_input"], new_description)
        self.wait.until(EC.element_to_be_clickable(self.LOCATORS["confirm_button"])).click()
        self._wait_for_toast(self.MESSAGES["edit_success"])
        self._wait_for_row(new_name)

    @retry_on_failure()
    def delete_group(self, group_name):
        """Delete a service group."""
        self._click_action(group_name, "delete")
        self.wait.until(EC.element_to_be_clickable(self.LOCATORS["confirm_button"])).click()
        self._wait_for_toast(self.MESSAGES["delete_success"].format(group_name))
        self._wait_for_row(group_name, present=False)

    # Verification methods
    def _verify_operation(self, message, row_name=None, should_exist=True):
        """Verify operation success via toast or row state."""
        try:
            self._wait_for_toast(message, timeout=3)
            return True
        except:
            if row_name:
                try:
                    self._wait_for_row(row_name, should_exist, timeout=5)
                    return True
                except:
                    return False
            return False

    def verify_add_success(self):
        """Verify the success of adding a service group."""
        return self._verify_operation(self.MESSAGES["add_success"])

    def verify_edit_success(self, new_name=None):
        """Verify the success of editing a service group."""
        return self._verify_operation(self.MESSAGES["edit_success"], new_name)

    def verify_delete_success(self, group_name):
        """Verify the success of deleting a service group."""
        return self._verify_operation(self.MESSAGES["delete_success"].format(group_name), group_name, False)

    def verify_group_in_table(self, group_name):
        """Verify if a group exists in the table."""
        try:
            self._wait_for_row(group_name, timeout=5)
            return True
        except:
            return False