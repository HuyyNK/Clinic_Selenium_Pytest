import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from utils.retry import retry_on_failure

class ExaminationPage:
    """Manages interactions with the examination page of the EMR system."""

    def __init__(self, driver):
        """Initialize the ExaminationPage with a WebDriver instance."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 50)
        self.action_chain = ActionChains(driver)

        # Centralized locator dictionary
        self.locators = {
            "vital_signs": {
                "temperature": (By.ID, "hypothermia"),
                "height": (By.ID, "height"),
                "weight": (By.ID, "weight"),
                "systolic": (By.ID, "systolic"),
                "diastolic": (By.ID, "diastolic"),
                "heartbeat": (By.ID, "heartbeat"),
                "blood_group": (By.XPATH, "//label[normalize-space()='Nhóm máu']/following::div[contains(@class, 'ant-select-selector')][1]"),
                "spo2": (By.ID, "spo2"),
                "blood_sugar": (By.ID, "blood_sugar")
            },
            "medical_history": {
                "admission_reason": (By.XPATH, "//label[normalize-space()='Lý do vào viện']/following::textarea[1]"),
                "allergy": (By.XPATH, "//label[normalize-space()='Dị ứng']/following::textarea[1]"),
                "personal_history": (By.XPATH, "//label[normalize-space()='Tiền căn bản thân']/following::textarea[1]"),
                "family_history": (By.XPATH, "//label[normalize-space()='Tiền căn gia đình']/following::textarea[1]"),
                "medical_history": (By.XPATH, "//label[normalize-space()='Bệnh sử']/following::textarea[1]")
            },
            "physical_exam": {
                "tab": (By.XPATH, "//div[@class='sc-eItTMj gTopxD'][normalize-space()='Khám toàn thân']"),
                "respiratory": (By.XPATH, "//label[normalize-space()='Hô hấp']/following::div[contains(@class, 'ant-select-selector')][1]"),
                "digestion": (By.XPATH, "//label[normalize-space()='Tiêu hóa']/following::div[contains(@class, 'ant-select-selector')][1]"),
                "renal": (By.XPATH, "//label[normalize-space()='Thận tiết niệu']/following::div[contains(@class, 'ant-select-selector')][1]"),
                "neurology": (By.XPATH, "//label[normalize-space()='Thần kinh']/following::textarea[1]"),
                "dermatology": (By.XPATH, "//label[normalize-space()='Da liễu']/following::textarea[1]"),
                "physical_state": (By.XPATH, "//label[normalize-space()='Thể trạng']/following::div[contains(@class, 'ant-select-selector')][1]"),
                "lymph_node": (By.XPATH, "//label[normalize-space()='Hạch Ngoại Vi']/following::div[contains(@class, 'ant-select-selector')][1]")
            },
            "regional_exam": {
                "tab": (By.XPATH, "//div[@class='sc-eItTMj gTopxD'][contains(text(), 'Khám bộ phận')]"),
                "cardiovascular": (By.XPATH, "//label[normalize-space()='Tim Mạch']/following::div[contains(@class, 'ant-select-selector')][1]"),
                "other_organs": (By.XPATH, "//label[normalize-space()='Các cơ quan khác']/following::textarea[1]")
            },
            "clinical_follow_up": {
                "paraclinical_result": (By.XPATH, "//label[normalize-space()='Kết quả cận lâm sàng']/following::textarea[1]"),
                "follow_up_days": (By.XPATH, "//input[@class='ant-input sc-bWXABl OWVOl']"),
                "follow_up_time": (By.XPATH, "//input[@placeholder='Vui lòng chọn thời gian']"),
                "now_option": (By.XPATH, "//h4[contains(text(), 'Bây giờ')]"),
                "ok_button": (By.XPATH, "//span[normalize-space()='OK']")
            },
            "diagnosis_treatment": {
                "diagnosis": (By.XPATH, "//div[@class='ant-form-item-control-input-content'][./label[contains(text(), 'Chẩn đoán')]]//textarea"),
                "treatment": (By.XPATH, "//div[@class='ant-form-item-control-input-content'][./label[contains(text(), 'Hướng điều trị')]]//textarea")
            },
            "prescription": {
                "chi_dinh_tab": (By.XPATH, "//li[contains(text(), 'Chỉ định')]"),
                "nhi_khoa_b_group": (By.XPATH, "//span[normalize-space()='Nhi Khoa B Group']"),
                "nhi_khoa_b2_service": (By.XPATH, "//span[normalize-space()='Nhi Khoa B2 Service']"),
                "don_thuoc_tab": (By.XPATH, "//li[contains(text(), 'Đơn thuốc')]"),
                "doctor_advice": (By.XPATH, "//div[@class='ant-form-item-control-input-content'][./label[contains(text(), 'Lời Dặn')]]//input[@type='text']"),
                "medicine_search": (By.XPATH, "//div[contains(@class, 'ant-select sc-fCdBJp byMnNB ant-select-single ant-select-show-arrow ant-select-show-search')]"),
                "water_injection": (By.XPATH, "//span[contains(text(), 'Nước cất tiêm 2ml (AM100007-N/A)')]"),
                "nasal_spray": (By.XPATH, "//span[contains(text(), 'Thuốc xịt mũi Thái Dương (AM100008-N/A)')]"),
                "row_inputs": {
                    "morning": "//tr[@data-row-key='{row_key}']//td[3]//div[1]//input[1]",
                    "afternoon": "//tr[@data-row-key='{row_key}']//td[4]//div[1]//input[1]",
                    "evening": "//tr[@data-row-key='{row_key}']//td[5]//div[1]//input[1]",
                    "night": "//tr[@data-row-key='{row_key}']//td[6]//div[1]//input[1]",
                    "duration": "//tr[@data-row-key='{row_key}']//td[10]//div[1]//input[1]",
                    "quantity": "//tr[@data-row-key='{row_key}']//td[11]//div[1]//input[1]",
                    "note": "//tr[@data-row-key='{row_key}']//td[15]//input[contains(@class, 'non-border')]"
                }
            },
            "actions": {
                "save": (By.XPATH, "//span[contains(text(), 'Lưu')]"),
                "finish_exam": (By.XPATH, "//span[normalize-space()='Khám xong']"),
                "confirm": (By.XPATH, "//span[contains(text(), 'Xác nhận')]"),
                "payment": (By.XPATH, "//span[normalize-space()='Thanh toán']"),
                "toast_message": (By.XPATH, "//div[contains(@class, 'ant-notification-notice-message')]"),
                "exam_status": (By.XPATH, "//div[contains(@class, 'ant-col-12')]//input[@value='Khám xong']"),
            }
        }

    def _scroll_to(self, element):
        """Scroll to the specified element."""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.5)

    @retry_on_failure()
    def _input_field(self, locator, value, clear=True):
        """Input value into a field with optional clearing."""
        by_type, locator_value = locator if isinstance(locator, tuple) else (By.XPATH, locator)
        field = self.wait.until(EC.element_to_be_clickable((by_type, locator_value)))
        self._scroll_to(field)
        if clear:
            field.send_keys(Keys.CONTROL + "a", Keys.DELETE)
        for char in str(value or ""):
            field.send_keys(char)
            time.sleep(0.1)
        field.send_keys(Keys.TAB)
        time.sleep(0.5)

    @retry_on_failure()
    def _input_textarea(self, locator, value):
        """Input text into a textarea."""
        textarea = self.wait.until(EC.element_to_be_clickable(locator))
        self._scroll_to(textarea)
        textarea.clear()
        textarea.send_keys(value or "")
        time.sleep(0.5)

    @retry_on_failure()
    def _select_option(self, dropdown_locator, option_text):
        """Select an option from a dropdown menu."""
        dropdown = self.wait.until(EC.element_to_be_clickable(dropdown_locator))
        self._scroll_to(dropdown)
        dropdown.click()
        option_xpath = (
            f"//div[contains(@class, 'ant-select-dropdown')]//div[contains(@class, 'ant-select-item')]"
            f"[.//div[@class='ant-select-item-option-content' and normalize-space()='{option_text}']]"
        )
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        self._scroll_to(option)
        option.click()
        time.sleep(0.2)

    @retry_on_failure()
    def enter_vital_signs(self, data):
        """Enter vital signs data with default blood group 'O-'.
        Args:
            data (dict): Dictionary containing vital sign values.
        """
        for key, value in data.items():
            if key in self.locators["vital_signs"] and value is not None:
                self._input_field(self.locators["vital_signs"][key], value)
        self._select_option(self.locators["vital_signs"]["blood_group"], "O-")

    @retry_on_failure()
    def enter_medical_history(self, data):
        """Enter medical history details.
        Args:
            data (dict): Dictionary containing medical history fields.
        """
        for key, value in data.items():
            if key in self.locators["medical_history"] and value is not None:
                self._input_textarea(self.locators["medical_history"][key], value)

    @retry_on_failure()
    def enter_physical_examination(self, data):
        """Enter physical examination details with default selections.
        Args:
            data (dict): Dictionary containing neurology and dermatology text.
        """
        tab = self.wait.until(EC.element_to_be_clickable(self.locators["physical_exam"]["tab"]))
        self._scroll_to(tab)
        tab.click()
        self._select_option(self.locators["physical_exam"]["respiratory"], "Phổi trong")
        self._select_option(self.locators["physical_exam"]["digestion"], "Bụng mềm")
        self._select_option(self.locators["physical_exam"]["renal"], "Âm tính")
        self._input_textarea(self.locators["physical_exam"]["neurology"], data.get("neurology", ""))
        self._input_textarea(self.locators["physical_exam"]["dermatology"], data.get("dermatology", ""))
        self._select_option(self.locators["physical_exam"]["physical_state"], "Bình thường")
        self._select_option(self.locators["physical_exam"]["lymph_node"], "Không sờ chạm")

    @retry_on_failure()
    def enter_regional_examination(self, other_organs):
        """Enter regional examination details.
        Args:
            other_organs (str): Text for other organs field.
        """
        tab = self.wait.until(EC.element_to_be_clickable(self.locators["regional_exam"]["tab"]))
        self._scroll_to(tab)
        tab.click()
        self._select_option(self.locators["regional_exam"]["cardiovascular"], "T2 rõ")
        self._input_textarea(self.locators["regional_exam"]["other_organs"], other_organs or "")

    @retry_on_failure()
    def enter_paraclinical(self, result):
        """Enter paraclinical results.
        Args:
            result (str): Paraclinical result text.
        """
        self._input_textarea(self.locators["clinical_follow_up"]["paraclinical_result"], result or "")

    @retry_on_failure()
    def set_follow_up(self, days):
        """Set follow-up date and select 'Bây giờ' time.
        Args:
            days (int): Number of days for follow-up.
        """
        self._input_field(self.locators["clinical_follow_up"]["follow_up_days"], days)
        time_field = self.wait.until(EC.element_to_be_clickable(self.locators["clinical_follow_up"]["follow_up_time"]))
        self._scroll_to(time_field)
        time_field.click()
        now_option = self.wait.until(EC.element_to_be_clickable(self.locators["clinical_follow_up"]["now_option"]))
        self._scroll_to(now_option)
        now_option.click()
        ok_button = self.wait.until(EC.element_to_be_clickable(self.locators["clinical_follow_up"]["ok_button"]))
        self._scroll_to(ok_button)
        ok_button.click()
        time.sleep(0.5)

    @retry_on_failure()
    def enter_diagnosis(self, text):
        """Enter diagnosis text.
        Args:
            text (str): Diagnosis text to input.
        """
        textarea = self.wait.until(EC.element_to_be_clickable(self.locators["diagnosis_treatment"]["diagnosis"]))
        self._scroll_to(textarea)
        if textarea.get_attribute("disabled") or textarea.get_attribute("readonly"):
            raise TimeoutException("Diagnosis field is disabled")
        textarea.clear()
        textarea.send_keys(text or "")
        time.sleep(0.5)

    @retry_on_failure()
    def enter_treatment(self, text):
        """Enter treatment text.
        Args:
            text (str): Treatment text to input.
        """
        textarea = self.wait.until(EC.element_to_be_clickable(self.locators["diagnosis_treatment"]["treatment"]))
        self._scroll_to(textarea)
        if textarea.get_attribute("disabled") or textarea.get_attribute("readonly"):
            raise TimeoutException("Treatment field is disabled")
        textarea.clear()
        textarea.send_keys(text or "")
        time.sleep(0.5)

    @retry_on_failure()
    def assign_prescription(self):
        """Assign prescription services (Nhi Khoa B Group)."""
        tab = self.wait.until(EC.element_to_be_clickable(self.locators["prescription"]["chi_dinh_tab"]))
        self._scroll_to(tab)
        self.driver.execute_script("arguments[0].click();", tab)
        group = self.wait.until(EC.element_to_be_clickable(self.locators["prescription"]["nhi_khoa_b_group"]))
        group.click()
        service = self.wait.until(EC.element_to_be_clickable(self.locators["prescription"]["nhi_khoa_b2_service"]))
        self.action_chain.double_click(service).perform()

    def _get_row_locator(self, field_name, row_key):
        """Return formatted locator for a specific row key."""
        return self.locators["prescription"]["row_inputs"][field_name].format(row_key=row_key)

    @retry_on_failure()
    def _fill_row_data(self, row_key, data_dict):
        """
        Fill row data for a specific prescription row.
        Args:
            row_key (str): The data-row-key identifier for the row.
            data_dict (dict): Dictionary with keys matching row_inputs (e.g., {"morning": "10", "duration": "5"}).
        """
        for field, value in data_dict.items():
            locator = (By.XPATH, self._get_row_locator(field, row_key))
            if field in ["morning", "afternoon", "evening", "night", "duration", "quantity", "note"]:
                self._input_field(locator, value)
            time.sleep(0.2)

    @retry_on_failure()
    def configure_prescription(self, data):
        """
        Configure prescription details for multiple rows of medicines.
        Args:
            data (dict): Dictionary containing prescription details for each medicine.
        """
        tab = self.wait.until(EC.element_to_be_clickable(self.locators["prescription"]["don_thuoc_tab"]))
        self._scroll_to(tab)
        self.driver.execute_script("arguments[0].click();", tab)
        self._input_field(self.locators["prescription"]["doctor_advice"], data.get("doctor_advice", ""))

        medicines = {
            "water_injection": {
                "locator": self.locators["prescription"]["water_injection"],
                "row_key": "4319",
                "prefix": "water"
            },
            "nasal_spray": {
                "locator": self.locators["prescription"]["nasal_spray"],
                "row_key": "4320",
                "prefix": "spray"
            }
        }

        for med_name, med_config in medicines.items():
            search = self.wait.until(EC.element_to_be_clickable(self.locators["prescription"]["medicine_search"]))
            search.click()
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'ant-select-dropdown')]")))
            medicine = self.wait.until(EC.element_to_be_clickable(med_config["locator"]))
            medicine.click()

            row_data = {
                "morning": data.get(f"{med_config['prefix']}_morning", 0),
                "afternoon": data.get(f"{med_config['prefix']}_afternoon", 0),
                "evening": data.get(f"{med_config['prefix']}_evening", 0),
                "night": data.get(f"{med_config['prefix']}_night", 0),
                "duration": data.get(f"{med_config['prefix']}_duration", 0),
                "quantity": data.get(f"{med_config['prefix']}_quantity", 0),
                "note": data.get(f"{med_config['prefix']}_note", "")
            }
            self._fill_row_data(med_config["row_key"], row_data)
            time.sleep(0.5)

    @retry_on_failure()
    def save_exam(self):
        """Save the current examination."""
        button = self.wait.until(EC.element_to_be_clickable(self.locators["actions"]["save"]))
        self._scroll_to(button)
        self.driver.execute_script("arguments[0].click();", button)

    @retry_on_failure()
    def finish_exam(self):
        """Mark the examination as complete."""
        button = self.wait.until(EC.element_to_be_clickable(self.locators["actions"]["finish_exam"]))
        self._scroll_to(button)
        self.driver.execute_script("arguments[0].click();", button)

    @retry_on_failure()
    def confirm_exam(self):
        """Confirm the examination completion."""
        button = self.wait.until(EC.element_to_be_clickable(self.locators["actions"]["confirm"]))
        self._scroll_to(button)
        button.click()
        self.wait.until(EC.visibility_of_element_located(self.locators["actions"]["toast_message"]))

    @retry_on_failure()
    def proceed_to_payment(self):
        """Navigate to the payment page."""
        button = self.wait.until(EC.element_to_be_clickable(self.locators["actions"]["payment"]))
        self._scroll_to(button)
        self.driver.execute_script("arguments[0].click();", button)

    def verify_toast(self, expected_text):
        """Verify the toast message content.
        Args:
            expected_text (str): Expected text in the toast message.
        """
        toast = self.wait.until(EC.visibility_of_element_located(self.locators["actions"]["toast_message"]))
        assert expected_text in toast.text, f"Expected: {expected_text}, Got: {toast.text}"

    def is_exam_completed(self):
        """Check if the examination status is 'Khám xong'.
        Returns:
            bool: True if examination is completed, False otherwise.
        """
        try:
            status = self.wait.until(EC.presence_of_element_located(self.locators["actions"]["exam_status"]), 10)
            return status.get_attribute("value") == "Khám xong"
        except TimeoutException:
            return False