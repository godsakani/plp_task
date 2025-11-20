"""
Automated Testing with AI - Login Page Test
Framework: Selenium WebDriver with AI-enhanced test patterns
Task: Automate login page testing with valid/invalid credentials
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from datetime import datetime
import json


class AIEnhancedLoginTest:
    """
    AI-Enhanced Login Test Suite
    Demonstrates how AI improves test coverage through:
    - Self-healing locators (multiple fallback strategies)
    - Intelligent wait mechanisms
    - Automatic error detection and reporting
    - Pattern-based test generation
    """
    
    def __init__(self, base_url="https://practicetestautomation.com/practice-test-login/"):
        self.base_url = base_url
        self.driver = None
        self.test_results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "test_cases": []
        }
    
    def setup(self):
        """Initialize WebDriver with options"""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        print("✓ Browser initialized successfully")
    
    def teardown(self):
        """Close browser and cleanup"""
        if self.driver:
            self.driver.quit()
            print("✓ Browser closed")
    
    def ai_find_element(self, locator_strategies):
        """
        AI-Enhanced Element Locator with Self-Healing
        Tries multiple locator strategies (mimics AI self-healing)
        """
        for strategy_name, (by, value) in locator_strategies.items():
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((by, value))
                )
                print(f"  → Element found using: {strategy_name}")
                return element
            except TimeoutException:
                continue
        raise NoSuchElementException("Element not found with any strategy")
    
    def test_valid_login(self):
        """Test Case 1: Valid Login Credentials"""
        test_name = "Valid Login Test"
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print(f"{'='*60}")
        
        try:
            self.driver.get(self.base_url)
            print(f"✓ Navigated to: {self.base_url}")
            
            # AI-enhanced element location with multiple strategies
            username_locators = {
                "id": (By.ID, "username"),
                "name": (By.NAME, "username"),
                "xpath": (By.XPATH, "//input[@type='text']")
            }
            
            password_locators = {
                "id": (By.ID, "password"),
                "name": (By.NAME, "password"),
                "xpath": (By.XPATH, "//input[@type='password']")
            }
            
            submit_locators = {
                "id": (By.ID, "submit"),
                "xpath": (By.XPATH, "//button[@type='submit']"),
                "css": (By.CSS_SELECTOR, "button.btn")
            }
            
            # Enter valid credentials
            username_field = self.ai_find_element(username_locators)
            username_field.clear()
            username_field.send_keys("student")
            print("✓ Username entered: student")
            
            password_field = self.ai_find_element(password_locators)
            password_field.clear()
            password_field.send_keys("Password123")
            print("✓ Password entered: Password123")
            
            # Click submit
            submit_button = self.ai_find_element(submit_locators)
            submit_button.click()
            print("✓ Submit button clicked")
            
            # Wait for successful login
            time.sleep(2)
            
            # Verify successful login
            success_indicators = {
                "url_change": self.driver.current_url != self.base_url,
                "success_message": self._check_success_message(),
                "logout_button": self._check_logout_button()
            }
            
            if any(success_indicators.values()):
                print(f"✓ Login successful! Current URL: {self.driver.current_url}")
                self._record_result(test_name, "PASSED", "Login successful with valid credentials")
            else:
                raise Exception("Login success indicators not found")
                
        except Exception as e:
            print(f"✗ Test failed: {str(e)}")
            self._record_result(test_name, "FAILED", str(e))
    
    def test_invalid_username(self):
        """Test Case 2: Invalid Username"""
        test_name = "Invalid Username Test"
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print(f"{'='*60}")
        
        try:
            self.driver.get(self.base_url)
            print(f"✓ Navigated to: {self.base_url}")
            
            # Enter invalid username
            username = self.driver.find_element(By.ID, "username")
            username.clear()
            username.send_keys("invaliduser")
            print("✓ Username entered: invaliduser")
            
            password = self.driver.find_element(By.ID, "password")
            password.clear()
            password.send_keys("Password123")
            print("✓ Password entered: Password123")
            
            submit = self.driver.find_element(By.ID, "submit")
            submit.click()
            print("✓ Submit button clicked")
            
            time.sleep(2)
            
            # Verify error message appears
            if self._check_error_message():
                print("✓ Error message displayed as expected")
                self._record_result(test_name, "PASSED", "Invalid username correctly rejected")
            else:
                raise Exception("Error message not displayed")
                
        except Exception as e:
            print(f"✗ Test failed: {str(e)}")
            self._record_result(test_name, "FAILED", str(e))
    
    def test_invalid_password(self):
        """Test Case 3: Invalid Password"""
        test_name = "Invalid Password Test"
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print(f"{'='*60}")
        
        try:
            self.driver.get(self.base_url)
            print(f"✓ Navigated to: {self.base_url}")
            
            # Enter valid username but invalid password
            username = self.driver.find_element(By.ID, "username")
            username.clear()
            username.send_keys("student")
            print("✓ Username entered: student")
            
            password = self.driver.find_element(By.ID, "password")
            password.clear()
            password.send_keys("wrongpassword")
            print("✓ Password entered: wrongpassword")
            
            submit = self.driver.find_element(By.ID, "submit")
            submit.click()
            print("✓ Submit button clicked")
            
            time.sleep(2)
            
            # Verify error message appears
            if self._check_error_message():
                print("✓ Error message displayed as expected")
                self._record_result(test_name, "PASSED", "Invalid password correctly rejected")
            else:
                raise Exception("Error message not displayed")
                
        except Exception as e:
            print(f"✗ Test failed: {str(e)}")
            self._record_result(test_name, "FAILED", str(e))
    
    def _check_success_message(self):
        """Check for success message or indicator"""
        try:
            success_element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Logged In Successfully') or contains(text(), 'successfully')]")
            return True
        except NoSuchElementException:
            return False
    
    def _check_logout_button(self):
        """Check for logout button presence"""
        try:
            self.driver.find_element(By.LINK_TEXT, "Log out")
            return True
        except NoSuchElementException:
            return False
    
    def _check_error_message(self):
        """Check for error message"""
        try:
            error_element = self.driver.find_element(By.ID, "error")
            return error_element.is_displayed()
        except NoSuchElementException:
            return False
    
    def _record_result(self, test_name, status, message):
        """Record test result"""
        self.test_results["total_tests"] += 1
        if status == "PASSED":
            self.test_results["passed"] += 1
        else:
            self.test_results["failed"] += 1
        
        self.test_results["test_cases"].append({
            "test_name": test_name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def generate_report(self):
        """Generate test report"""
        print(f"\n{'='*60}")
        print("TEST EXECUTION SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {self.test_results['total_tests']}")
        print(f"Passed: {self.test_results['passed']}")
        print(f"Failed: {self.test_results['failed']}")
        print(f"Success Rate: {(self.test_results['passed']/self.test_results['total_tests']*100):.1f}%")
        print(f"{'='*60}\n")
        
        # Save to JSON
        with open('test_results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print("✓ Test results saved to test_results.json")
    
    def run_all_tests(self):
        """Execute all test cases"""
        print("\n" + "="*60)
        print("AI-ENHANCED LOGIN TEST SUITE")
        print("="*60)
        
        self.setup()
        
        try:
            self.test_valid_login()
            self.test_invalid_username()
            self.test_invalid_password()
        finally:
            self.teardown()
            self.generate_report()


if __name__ == "__main__":
    # Run the test suite
    test_suite = AIEnhancedLoginTest()
    test_suite.run_all_tests()