"""Page Object for Patient and Appointment pages."""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.retry import retry_on_failure

class PatientPage:
    def __init__(self, driver):
        """Initialize PatientPage with WebDriver instance."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)

        # Locators
        self.patient_tab_button = (By.XPATH, "//div[@class='ant-collapse-item ant-collapse-item-active sc-coCPJf eqFRNs']//div[@class='ant-collapse-content ant-collapse-content-active']//div[2]//div[1]//div[1]//div[1]//div[1]//div[2]//div[1]")
        self.appointment_button = (By.XPATH, "//td[@class='ant-table-cell ant-table-cell-fix-right ant-table-cell-fix-right-first ant-table-cell-row-hover']//span[contains(text(),'Lịch hẹn')]")
        self.room_dropdown = (By.XPATH, "//label[normalize-space()='Chỉ định phòng khám']/following-sibling::div[contains(@class, 'ant-select')]")
        self.room_option_phong_1 = (By.XPATH, "//div[normalize-space()='Phòng 1']")
        self.symptom_textarea = (By.XPATH, "//div[contains(@class, 'ant-modal')]//textarea")
        self.service_group_nhi_khoa_a = (By.XPATH, "//span[normalize-space()='Nhi Khoa A Group']")
        self.service_option_nhi_khoa_a1 = (By.XPATH, "//span[normalize-space()='Nhi Khoa A1 Service']")
        self.examine_now_button = (By.XPATH, "//span[normalize-space()='Khám ngay']")
        self.upload_input = (By.XPATH, "//input[@type='file' and contains(@accept, '.png, .jpg, .jpeg')]")
        self.examination_type_dropdown = (By.XPATH, "//label[normalize-space()='Loại khám']/following-sibling::div[contains(@class, 'ant-select')]")
        self.examination_type_new = (By.XPATH, "//div[@title='Khám mới']//div[1]")
        self.priority_dropdown = (By.XPATH, "//label[normalize-space()='Ưu tiên']/following-sibling::div[contains(@class, 'ant-select')]")
        self.priority_normal = (By.XPATH, "//div[@title='Bình thường']//div[1]")
        self.service_group_nhi_khoa_d = (By.XPATH, "//span[normalize-space()='Nhi Khoa D Group']")
        self.service_option_nhi_khoa_d2 = (By.XPATH, "//span[normalize-space()='Nhi Khoa D2 Service']")
        self.toast_message = (By.XPATH, "//div[@class='ant-notification-notice-message']") 

    @property
    def is_patient_tab_visible(self):
        """Check if patient tab is visible."""
        return self.wait.until(EC.visibility_of_element_located(self.patient_tab_button)).is_displayed()

    def go_to_patient_tab(self):
        """Navigate to the Patient tab."""
        self.wait.until(EC.element_to_be_clickable(self.patient_tab_button)).click()

    def select_patient(self, patient_index):
        """Select a patient by index from the table."""
        if patient_index < 1:
            raise ValueError("Patient index must be positive.")
        patient_row = (By.XPATH, f"(//tr[contains(@class, 'ant-table-row')])[{patient_index}]")
        self.wait.until(EC.element_to_be_clickable(patient_row)).click()

    @retry_on_failure()
    def click_appointment_button(self):
        """Click the Appointment button with retry logic."""
        button = self.wait.until(EC.visibility_of_element_located(self.appointment_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        self.driver.execute_script("arguments[0].click();", button)
        self.wait.until(EC.visibility_of_element_located(self.symptom_textarea))

    def _select_examination_type(self):
        """Select 'Khám mới' from the examination type dropdown."""
        dropdown_el = self.wait.until(EC.element_to_be_clickable(self.examination_type_dropdown))
        dropdown_el.click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'ant-select-dropdown')]")))
        option_el = self.wait.until(EC.element_to_be_clickable(self.examination_type_new))
        option_el.click()

    def _select_priority(self):
        """Select 'Bình thường' from the priority dropdown."""
        dropdown_el = self.wait.until(EC.element_to_be_clickable(self.priority_dropdown))
        dropdown_el.click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'ant-select-dropdown')]")))
        option_el = self.wait.until(EC.element_to_be_clickable(self.priority_normal))
        option_el.click()

    def _upload_images(self, image_paths):
        """Upload one or multiple images using the file input element."""
        input_el = self.wait.until(EC.presence_of_element_located(self.upload_input))
        for path in image_paths:
            input_el.send_keys(path)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'ant-upload-list')]")))

    def _select_service_nhi_khoa_d(self):
        """Select 'Nhi Khoa D Group' and double-click 'Nhi Khoa D2 Service'."""
        modal = self.driver.find_element(By.XPATH, "//div[contains(@class, 'ant-modal')]")
        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", modal)
        service_group_el = self.wait.until(EC.element_to_be_clickable(self.service_group_nhi_khoa_d))
        service_group_el.click()
        service_option_el = self.wait.until(EC.element_to_be_clickable(self.service_option_nhi_khoa_d2))
        self.actions.double_click(service_option_el).perform()

    def _select_room(self):
        """Select room 'Phòng 1' from dropdown."""
        room_dropdown_el = self.wait.until(EC.element_to_be_clickable(self.room_dropdown))
        room_dropdown_el.click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'ant-select-dropdown')]")))
        room_option_el = self.wait.until(EC.element_to_be_clickable(self.room_option_phong_1))
        room_option_el.click()

    def _enter_symptom(self, symptom_text):
        """Enter symptom text into textarea."""
        symptom_el = self.wait.until(EC.visibility_of_element_located(self.symptom_textarea))
        symptom_el.clear()
        symptom_el.send_keys(symptom_text)

    def _select_service(self):
        """Select service group and option for Nhi Khoa A."""
        modal = self.driver.find_element(By.XPATH, "//div[contains(@class, 'ant-modal')]")
        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", modal)
        service_group_el = self.wait.until(EC.element_to_be_clickable(self.service_group_nhi_khoa_a))
        service_group_el.click()
        service_option_el = self.wait.until(EC.element_to_be_clickable(self.service_option_nhi_khoa_a1))
        self.actions.double_click(service_option_el).perform()

    @retry_on_failure(max_attempts=3)
    def _click_examine_now(self):
        """Click the 'Khám ngay' button with retry logic based on page navigation."""
        button = self.wait.until(EC.element_to_be_clickable(self.examine_now_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        self.driver.execute_script("arguments[0].click();", button)

        # Chờ chuyển trang để xác nhận hành động thành công
        self.wait.until(EC.url_contains("/examination/detail/"))

    @retry_on_failure()
    def fill_appointment_modal(self, symptom_text, image_paths):
        """Fill and submit the appointment modal with new behavior."""
        self._select_priority()
        self._select_room()
        self._enter_symptom(symptom_text)
        self._upload_images(image_paths)
        self._select_service()
        self._select_service_nhi_khoa_d()
        time.sleep(2)
        self._click_examine_now()

    def submit_appointment(self):
        """Submit the appointment (legacy method)."""
        self._click_examine_now()