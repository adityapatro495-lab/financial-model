from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

TOTAL_TESTS = 30

passed = 0
failed = 0

# ---------------------------------------------------
# TEST LOOP
# ---------------------------------------------------

for test_number in range(1, TOTAL_TESTS + 1):

    print(f"\nRunning Test #{test_number}")

    try:

        driver = webdriver.Chrome()

        driver.get("http://127.0.0.1:5000")

        driver.maximize_window()

        time.sleep(1)

        # ---------------------------------------------------
        # RANDOM INPUTS
        # ---------------------------------------------------

        equity_opening = random.randint(10000, 1000000)
        equity_monthly = random.randint(1000, 50000)
        equity_cagr = random.randint(8, 18)

        fd_opening = random.randint(10000, 500000)
        fd_monthly = random.randint(1000, 25000)
        fd_cagr = random.randint(5, 9)

        bonds_opening = random.randint(10000, 300000)
        bonds_monthly = random.randint(1000, 20000)
        bonds_cagr = random.randint(6, 12)

        gold_opening = random.randint(10000, 300000)
        gold_monthly = random.randint(1000, 20000)
        gold_cagr = random.randint(5, 11)

        years = random.randint(5, 35)

        withdrawal = random.randint(100000, 1000000)
        withdrawal_increase = random.randint(3, 8)
        growth_rate = random.randint(7, 14)

        tax_rate = random.randint(0, 20)

        # ---------------------------------------------------
        # EQUITY
        # ---------------------------------------------------

        driver.find_element(By.ID, "equity_opening_number").clear()
        driver.find_element(By.ID, "equity_opening_number").send_keys(str(equity_opening))

        driver.find_element(By.ID, "equity_monthly_number").clear()
        driver.find_element(By.ID, "equity_monthly_number").send_keys(str(equity_monthly))

        driver.find_element(By.ID, "equity_cagr_number").clear()
        driver.find_element(By.ID, "equity_cagr_number").send_keys(str(equity_cagr))

        # ---------------------------------------------------
        # FD
        # ---------------------------------------------------

        driver.find_element(By.ID, "fd_opening_number").clear()
        driver.find_element(By.ID, "fd_opening_number").send_keys(str(fd_opening))

        driver.find_element(By.ID, "fd_monthly_number").clear()
        driver.find_element(By.ID, "fd_monthly_number").send_keys(str(fd_monthly))

        driver.find_element(By.ID, "fd_cagr_number").clear()
        driver.find_element(By.ID, "fd_cagr_number").send_keys(str(fd_cagr))

        # ---------------------------------------------------
        # BONDS
        # ---------------------------------------------------

        driver.find_element(By.ID, "bonds_opening_number").clear()
        driver.find_element(By.ID, "bonds_opening_number").send_keys(str(bonds_opening))

        driver.find_element(By.ID, "bonds_monthly_number").clear()
        driver.find_element(By.ID, "bonds_monthly_number").send_keys(str(bonds_monthly))

        driver.find_element(By.ID, "bonds_cagr_number").clear()
        driver.find_element(By.ID, "bonds_cagr_number").send_keys(str(bonds_cagr))

        # ---------------------------------------------------
        # GOLD
        # ---------------------------------------------------

        driver.find_element(By.ID, "gold_opening_number").clear()
        driver.find_element(By.ID, "gold_opening_number").send_keys(str(gold_opening))

        driver.find_element(By.ID, "gold_monthly_number").clear()
        driver.find_element(By.ID, "gold_monthly_number").send_keys(str(gold_monthly))

        driver.find_element(By.ID, "gold_cagr_number").clear()
        driver.find_element(By.ID, "gold_cagr_number").send_keys(str(gold_cagr))

        # ---------------------------------------------------
        # YEARS
        # ---------------------------------------------------

        driver.find_element(By.ID, "years_number").clear()
        driver.find_element(By.ID, "years_number").send_keys(str(years))

        # ---------------------------------------------------
        # SWP
        # ---------------------------------------------------

        driver.find_element(By.ID, "tax_rate_number").clear()
        driver.find_element(By.ID, "tax_rate_number").send_keys(str(tax_rate))

        driver.find_element(By.ID, "withdraw_amount_number").clear()
        driver.find_element(By.ID, "withdraw_amount_number").send_keys(str(withdrawal))

        driver.find_element(By.ID, "withdraw_increase_number").clear()
        driver.find_element(By.ID, "withdraw_increase_number").send_keys(str(withdrawal_increase))

        driver.find_element(By.ID, "growth_rate_number").clear()
        driver.find_element(By.ID, "growth_rate_number").send_keys(str(growth_rate))

        # ---------------------------------------------------
        # SUBMIT
        # ---------------------------------------------------

        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        submit_button.click()

        time.sleep(3)

        # ---------------------------------------------------
        # VALIDATION
        # ---------------------------------------------------

        results = driver.find_element(By.ID, "results").text

        assert "Equity Forecast" in results
        assert "FD Forecast" in results
        assert "Bonds Forecast" in results
        assert "Gold Forecast" in results
        assert "SWP Forecast" in results

        print(f"Test #{test_number} PASSED")

        passed += 1

    except Exception as e:

        print(f"Test #{test_number} FAILED")
        print("Reason:", e)

        failed += 1

    finally:

        driver.quit()

# ---------------------------------------------------
# FINAL REPORT
# ---------------------------------------------------

print("\n-----------------------------------")
print("FINAL TEST REPORT")
print("-----------------------------------")

print(f"Total Tests : {TOTAL_TESTS}")
print(f"Passed      : {passed}")
print(f"Failed      : {failed}")

success_rate = (passed / TOTAL_TESTS) * 100

print(f"Success Rate: {success_rate:.2f}%")