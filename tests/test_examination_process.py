"""Test cases for patient appointment workflow with data-driven testing."""
import pytest
import json
import os
from pages.login_page import LoginPage
from pages.patient_page import PatientPage
from pages.examination_page import ExaminationPage
from pages.payment_page import PaymentPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, "data", "test_data.json"), "r", encoding="utf-8") as file:
    test_data = json.load(file)["test_cases"]

@pytest.mark.parametrize("test_case", test_data)
def test_appointment_workflow(driver, test_case):
    """Test the complete appointment, examination, and payment workflow."""
    test_id = test_case["test_id"]
    patient_index = test_case["patient_index"]
    symptom = test_case["symptom"]
    diagnosis = test_case["diagnosis"]
    treatment = test_case["treatment"]
    doctor_advice = test_case["doctor_advice"]

    water_morning = test_case["water_morning"]
    water_afternoon = test_case["water_afternoon"]
    water_evening = test_case["water_evening"]
    water_night = test_case["water_night"]
    water_duration = test_case["water_duration"]
    water_quantity = test_case["water_quantity"]
    water_note = test_case["water_note"]

    spray_morning = test_case["spray_morning"]
    spray_afternoon = test_case["spray_afternoon"]
    spray_evening = test_case["spray_evening"]
    spray_night = test_case["spray_night"]
    spray_duration = test_case["spray_duration"]
    spray_quantity = test_case["spray_quantity"]
    spray_note = test_case["spray_note"]

    expected_exam_status = test_case["expected_exam_status"]
    expected_payment_status = test_case["expected_payment_status"]

    extra_data = {k: v for k, v in test_case.items() if k not in [
        "test_id", "patient_index", "symptom", "diagnosis", "treatment", "doctor_advice",
        "water_morning", "water_afternoon", "water_evening", "water_night", "water_duration", "water_quantity", "water_note",
        "spray_morning", "spray_afternoon", "spray_evening", "spray_night", "spray_duration", "spray_quantity", "spray_note",
        "expected_exam_status", "expected_payment_status"
    ]}

    wait = WebDriverWait(driver, 50)

    login_page = LoginPage(driver)
    patient_page = PatientPage(driver)
    exam_page = ExaminationPage(driver)
    payment_page = PaymentPage(driver)

    login_page.login()
    wait.until(lambda d: d.current_url.startswith("https://clinic-local.amaz.com.vn/"))

    patient_page.go_to_patient_tab()
    patient_page.select_patient(patient_index)
    patient_page.click_appointment_button()

    image_path = os.path.join(BASE_DIR, "data", "images", "image_1.png")
    patient_page.fill_appointment_modal(symptom, [image_path])

    wait.until(EC.url_contains("/examination/detail/"))
    assert "/examination/detail/" in driver.current_url, f"Test {test_id}: Failed to reach exam page"

    exam_page.enter_vital_signs(extra_data.get("vital_signs", {}))
    exam_page.enter_medical_history(extra_data.get("medical_history", {}))
    exam_page.enter_physical_examination(extra_data.get("physical_exam", {}))
    exam_page.enter_regional_examination(extra_data.get("regional_exam", {}).get("other_organs", ""))
    exam_page.enter_paraclinical(extra_data.get("paraclinical", {}).get("result", ""))
    exam_page.enter_diagnosis(diagnosis)
    exam_page.enter_treatment(treatment)
    exam_page.set_follow_up(5)

    exam_page.assign_prescription()
    exam_page.configure_prescription({
        "doctor_advice": doctor_advice,
        "water_morning": water_morning, "water_afternoon": water_afternoon, "water_evening": water_evening,
        "water_night": water_night, "water_duration": water_duration, "water_quantity": water_quantity,
        "water_note": water_note,
        "spray_morning": spray_morning, "spray_afternoon": spray_afternoon, "spray_evening": spray_evening,
        "spray_night": spray_night, "spray_duration": spray_duration, "spray_quantity": spray_quantity,
        "spray_note": spray_note
    })

    exam_page.save_exam()
    exam_page.finish_exam()
    exam_page.confirm_exam()
    assert exam_page.is_exam_completed(), f"Test {test_id}: Exam not completed"

    exam_page.proceed_to_payment()
    wait.until(EC.url_contains("/booking/payment/"))
    payment_page.clickCompleteButton()
    payment_page.clickConfirmButton()
    assert payment_page.isPaymentCompleted(), f"Test {test_id}: Payment not completed"
