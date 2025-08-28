"""Page Object for Payment page."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.retry import retry_on_failure

class PaymentPage:
    """Page Object representing the Payment section."""

    def __init__(self, driver):
        """Initialize PaymentPage with WebDriver instance."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 50)
        
        # Locators
        self.completeButton = (By.XPATH, "//span[normalize-space()='Hoàn thành']")
        self.confirmButton = (By.XPATH, "//span[contains(text(), 'Xác nhận')]")
        self.paymentStatus = (By.XPATH, "//div[label[@class='sc-bKhNmF KeDvq' and normalize-space()='Trạng thái thanh toán']]//span[@class='ant-select-selection-item' and @title='Đã thanh toán']")
        self.confirmPopup = (By.XPATH, "//div[@class='sc-iIPllB gIvmZg']")

    @retry_on_failure()
    def clickCompleteButton(self):
        """Click the 'Hoàn thành' button and wait for confirmation popup."""
        button = self.wait.until(EC.element_to_be_clickable(self.completeButton))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        button.click()
        # Chờ popup xác nhận xuất hiện
        self.wait.until(EC.visibility_of_element_located(self.confirmPopup))

    @retry_on_failure()
    def clickConfirmButton(self):
        """Click the 'Xác nhận' button on the confirmation popup."""
        try:
            button = self.wait.until(EC.element_to_be_clickable(self.confirmButton), 20)  # Tăng thời gian chờ
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            button.click()
            # Chờ popup biến mất để xác nhận hành động hoàn tất
            self.wait.until(EC.invisibility_of_element_located(self.confirmPopup))
        except TimeoutException:
            raise Exception("Không thể nhấp vào nút 'Xác nhận' sau khi nhấn 'Hoàn thành'. Vui lòng kiểm tra locator hoặc giao diện.")

    def isPaymentCompleted(self):
        """Check if payment status is 'Đã thanh toán'.
        Returns:
            bool: True if payment is completed, False otherwise.
        """
        try:
            status_element = self.wait.until(EC.presence_of_element_located(self.paymentStatus), 10)
            status_value = status_element.text.strip()
            return status_value == "Đã thanh toán"
        except (TimeoutException, NoSuchElementException):
            return False

    def isConfirmPopupPresent(self):
        """Check if the confirmation popup is present."""
        try:
            self.wait.until(EC.presence_of_element_located(self.confirmPopup), 5)
            return True
        except TimeoutException:
            return False