import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import os
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime

def get_mobile_device_presets():
    """
    Device presets seperti di Chrome DevTools Mobile Simulator
    """
    return {
        "galaxy_s20": {
            "name": "Samsung Galaxy S20",
            "width": 412,
            "height": 915,
            "pixelRatio": 3.0,
            "userAgent": "Mozilla/5.0 (Linux; Android 12; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        },
        "iphone_14": {
            "name": "iPhone 14",
            "width": 390,
            "height": 844,
            "pixelRatio": 3.0,
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        },
        "iphone_14_pro_max": {
            "name": "iPhone 14 Pro Max",
            "width": 428,
            "height": 926,
            "pixelRatio": 3.0,
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        },
        "galaxy_s23_ultra": {
            "name": "Samsung Galaxy S23 Ultra",
            "width": 412,
            "height": 915,
            "pixelRatio": 3.0,
            "userAgent": "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        },
        "pixel_7": {
            "name": "Google Pixel 7",
            "width": 412,
            "height": 915,
            "pixelRatio": 2.75,
            "userAgent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        },
        "xiaomi_13": {
            "name": "Xiaomi 13",
            "width": 412,
            "height": 915,
            "pixelRatio": 3.0,
            "userAgent": "Mozilla/5.0 (Linux; Android 13; 2210132C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        }
    }

def get_driver_ultra_fast(device="galaxy_s20"):
    """
    Ultra fast ChromeDriver - minimal setup for maximum speed
    """
    options = Options()
    
    devices = get_mobile_device_presets()
    device_config = devices[device]
    
    # Mobile emulation
    mobile_emulation = {
        "deviceMetrics": {
            "width": device_config["width"],
            "height": device_config["height"],
            "pixelRatio": device_config["pixelRatio"]
        },
        "userAgent": device_config["userAgent"]
    }
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    # Add headless mode
    
    # Ultra speed optimizations
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-images")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-features=TranslateUI,BlinkGenPropertyTrees")
    options.add_argument("--disable-ipc-flooding-protection")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--disable-default-apps")
    options.add_argument("--no-first-run")
    options.add_argument("--fast-start")
    options.add_argument("--disable-web-security")
    
    # Ultra fast prefs
    prefs = {
        "profile.default_content_setting_values": {
            "notifications": 2,
            "images": 2,
            "plugins": 2,
            "popups": 2,
            "geolocation": 2,
            "media_stream": 2
        }
    }
    options.add_experimental_option("prefs", prefs)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Ultra fast timeouts - NO IMPLICIT WAIT
    driver.set_page_load_timeout(8)
    # Remove implicit wait - use only explicit waits for better performance
    # driver.implicitly_wait(2)  # REMOVED
    
    print(f"⚡ ULTRA FAST browser started ({device_config['name']}) - HEADLESS MODE")
    return driver

def fast_login(driver, username, password):
    """
    Ultra fast login - explicit waits only
    """
    print("🚀 FAST LOGIN...")
    
    driver.get("https://account.xiaomi.com/pass/serviceLogin")
    
    wait = WebDriverWait(driver, 8)
    
    # Quick cookie handle with explicit wait
    try:
        cookie_btn = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mi-cookie-banner__button"))
        )
        if cookie_btn.is_displayed():
            driver.execute_script("arguments[0].click();", cookie_btn)
    except:
        pass
    
    # Fast form fill with explicit waits
    account_field = wait.until(EC.presence_of_element_located((By.NAME, "account")))
    account_field.clear()
    account_field.send_keys(username)
    
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.clear()
    password_field.send_keys(password)
    
    # Submit with explicit wait
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    driver.execute_script("arguments[0].click();", submit_button)
    
    time.sleep(2)  # Minimal wait
    
    current_url = driver.current_url
    if "serviceLogin" not in current_url:
        print("✅ Login SUCCESS!")
        return True
    
    print("❌ Login failed")
    return False

def fast_click_button(driver, selector, description):
    """
    Ultra fast button clicking with explicit waits only
    """
    print(f"🎯 {description}...")
    
    # Enhanced checkout handling with comprehensive selectors
    if "Checkout" in description:
        print("   🔍 DEBUG: Searching for checkout button...")
        
        # First, scroll to bottom to ensure checkout button is visible
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        except:
            pass
        
        # Wait for page to be stable before proceeding
        try:
            print("   ⏳ Waiting for page to be stable...")
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(2)  # Additional buffer for dynamic content
        except:
            print("   ⚠️ Page readiness check failed, continuing...")
        
        # Debug: Show all buttons on the page
        try:
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            print(f"   📊 Total buttons found: {len(all_buttons)}")
            for idx, btn in enumerate(all_buttons[:15]):  # Show first 15 buttons
                try:
                    btn_text = btn.text.strip()
                    btn_class = btn.get_attribute('class') or ''
                    btn_visible = btn.is_displayed()
                    btn_enabled = btn.is_enabled()
                    if btn_text or 'checkout' in btn_class.lower() or 'cart' in btn_class.lower():
                        print(f"   📋 Button {idx+1}: '{btn_text}' | Class: '{btn_class[:60]}...' | Visible: {btn_visible} | Enabled: {btn_enabled}")
                except:
                    continue
        except:
            pass
        
        # Comprehensive checkout selectors
        checkout_selectors = [
            # Original selector
            ".cart-footer__submit",
            # Alternative specific selectors
            "button.cart-footer__submit",
            ".cart-footer .mi-btn",
            ".checkout-btn",
            ".cart-checkout-btn",
            "button[data-testid='checkout']",
            ".mi-btn.mi-btn--primary",
            # Generic button selectors in cart area
            ".cart-footer button",
            ".cart-actions button",
            ".footer__submit",
            ".cart-bottom button",
            ".checkout-section button",
            ".cart-summary button",
            # Mobile-specific selectors
            ".mobile-checkout-btn",
            ".cart-footer__btn",
            ".cart-submit-btn",
            # Additional patterns
            "button[class*='checkout']",
            "button[class*='cart-footer']",
            "button[class*='submit']",
            # Very generic fallbacks
            ".cart-container button",
            ".footer button",
            "button.mi-btn"
        ]
        
        for i, checkout_selector in enumerate(checkout_selectors, 1):
            try:
                print(f"   🔄 Checkout Method {i}: {checkout_selector}")
                
                # Find elements fresh each time to avoid stale references
                elements = driver.find_elements(By.CSS_SELECTOR, checkout_selector)
                
                if not elements:
                    print(f"   ❌ No elements found")
                    continue
                
                for idx, element in enumerate(elements):
                    try:
                        print(f"   📍 Trying element {idx+1}/{len(elements)}")
                        
                        # Re-check element freshness before each operation
                        try:
                            # Test if element is still valid
                            element.tag_name  # This will throw if stale
                        except:
                            print(f"   ⚠️ Element became stale, re-finding...")
                            # Re-find elements
                            fresh_elements = driver.find_elements(By.CSS_SELECTOR, checkout_selector)
                            if idx < len(fresh_elements):
                                element = fresh_elements[idx]
                            else:
                                continue
                        
                        # Check if element is visible and enabled
                        try:
                            if not element.is_displayed():
                                print(f"   ⏭️ Element not visible")
                                continue
                                
                            if not element.is_enabled():
                                print(f"   ⏭️ Element not enabled")
                                continue
                        except:
                            print(f"   ⚠️ Cannot check element state, skipping...")
                            continue
                        
                        # Get element info
                        try:
                            element_text = element.text.strip()
                            element_class = element.get_attribute('class') or ''
                            print(f"   📝 Element text: '{element_text}' | Class: '{element_class[:50]}...'")
                        except:
                            print(f"   ⚠️ Cannot get element info")
                        
                        # Scroll to element with retry
                        try:
                            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                            time.sleep(0.8)
                        except:
                            print(f"   ⚠️ Scroll failed, continuing...")
                        
                        # Multiple click methods with stale element handling
                        click_methods = [
                            ("JavaScript click", lambda el: driver.execute_script("arguments[0].click();", el)),
                            ("Event dispatch", lambda el: driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));", el)),
                            ("Standard click", lambda el: el.click()),
                            ("ActionChains", lambda el: ActionChains(driver).move_to_element(el).click().perform())
                        ]
                        
                        for method_name, method in click_methods:
                            try:
                                print(f"   🔄 Trying {method_name}...")
                                
                                # Re-find element right before click to avoid stale reference
                                fresh_elements = driver.find_elements(By.CSS_SELECTOR, checkout_selector)
                                if idx >= len(fresh_elements):
                                    print(f"   ⚠️ Element disappeared, skipping method...")
                                    break
                                    
                                fresh_element = fresh_elements[idx]
                                
                                # Verify element is still clickable
                                if not fresh_element.is_displayed() or not fresh_element.is_enabled():
                                    print(f"   ⚠️ Element no longer clickable, skipping method...")
                                    continue
                                
                                # Attempt click
                                method(fresh_element)
                                print(f"   ✅ Checkout Method {i}.{idx+1} SUCCESS with {method_name}!")
                                
                                # Wait for page response
                                time.sleep(2)
                                
                                # Check if page changed
                                try:
                                    current_url = driver.current_url
                                    print(f"   📍 URL after click: {current_url}")
                                    
                                    # Check for checkout page indicators
                                    if any(indicator in current_url for indicator in ['checkout', 'order', 'payment']):
                                        print(f"   ✅ Page navigation detected!")
                                        return True
                                    
                                    # Also check if we're still on cart page but something changed
                                    if 'cart' in current_url:
                                        print(f"   ⚠️ Still on cart page, but click registered")
                                        return True
                                        
                                except Exception as e:
                                    print(f"   ⚠️ URL check failed: {str(e)[:30]}...")
                                
                                return True
                                
                            except Exception as e:
                                error_msg = str(e)
                                if "stale element" in error_msg.lower():
                                    print(f"   ⚠️ {method_name} - stale element, retrying...")
                                    # Wait a bit for page to stabilize
                                    time.sleep(1)
                                    continue
                                else:
                                    print(f"   ❌ {method_name} failed: {error_msg[:40]}...")
                                    continue
                                
                    except Exception as e:
                        print(f"   ❌ Element processing failed: {str(e)[:40]}...")
                        continue
                        
            except Exception as e:
                print(f"   ❌ Checkout Method {i} failed: {str(e)[:40]}...")
                continue
        
        # Final XPath fallback for checkout with stale element handling
        print("   🔄 Final checkout fallback: XPath text search...")
        try:
            xpath_selectors = [
                "//button[contains(text(), 'Checkout')]",
                "//button[contains(text(), 'checkout')]",
                "//button[contains(text(), 'Check out')]",
                "//div[contains(text(), 'Checkout')]",
                "//*[contains(text(), 'Checkout')]",
                "//button[contains(@class, 'checkout')]",
                "//button[contains(@class, 'cart-footer')]"
            ]
            
            for xpath in xpath_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, xpath)
                    for element in elements:
                        try:
                            if element.is_displayed() and element.is_enabled():
                                print(f"   📝 XPath element: '{element.text}' | Tag: '{element.tag_name}'")
                                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                                time.sleep(0.5)
                                
                                # Try JavaScript click first (most reliable for dynamic pages)
                                driver.execute_script("arguments[0].click();", element)
                                print(f"   ✅ XPath checkout SUCCESS!")
                                time.sleep(2)
                                return True
                        except Exception as e:
                            if "stale element" not in str(e).lower():
                                print(f"   ❌ XPath element failed: {str(e)[:30]}...")
                            continue
                except:
                    continue
        except:
            pass
        
        print(f"   ❌ All checkout methods failed")
        return False
    
    # Original logic for non-checkout buttons
    try:
        # Method 1: Direct selector with explicit wait
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.execute_script("arguments[0].click();", element)
        print(f"   ✅ {description} SUCCESS!")
        return True
    except Exception as e:
        print(f"   ❌ Direct selector failed: {str(e)}")
    
    try:
        # Method 2: By text content with explicit wait
        if "Beli Sekarang" in description:
            wait = WebDriverWait(driver, 3)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Beli Sekarang')]")))
        elif "Bayar sekarang" in description:
            wait = WebDriverWait(driver, 3)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Bayar sekarang')]")))
        else:
            return False
            
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.execute_script("arguments[0].click();", element)
        print(f"   ✅ {description} SUCCESS!")
        return True
    except Exception as e:
        print(f"   ❌ Text search failed: {str(e)}")
    
    print(f"   ❌ {description} FAILED")
    return False

def fast_click_radio(driver, selector, description):
    """
    Fast radio button clicking with enhanced BCA support
    """
    print(f"📡 {description}...")
    
    try:
        # Method 1: Direct selector
        element = driver.find_element(By.CSS_SELECTOR, selector)
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.execute_script("arguments[0].click();", element)
        print(f"   ✅ {description} SUCCESS!")
        return True
    except:
        pass
    
    try:
        # Method 2: Enhanced BCA specific selectors
        if "BCA" in description:
            bca_selectors = [
                # Radio icon with BCA context
                '.checkout-pay__item .radio__icon[data-id="pay-method-radio"]',
                # BCA payment item wrapper
                '.checkout-pay__item.pay-item .radio__wrapper',
                # BCA title element
                '.pay-item__title:contains("BCA")',
                # Radio icon in BCA payment section
                '.pay-item .radio__icon',
                # Article with BCA content
                'article .pay-item__right',
                # Image alt BCA
                'img[alt="bca"]',
                # Any element containing BCA text
                '*:contains("BCA")'
            ]
            
            for bca_selector in bca_selectors:
                try:
                    if ':contains(' in bca_selector:
                        # Use XPath for text content
                        element = driver.find_element(By.XPATH, f"//*[contains(text(), 'BCA')]")
                    else:
                        element = driver.find_element(By.CSS_SELECTOR, bca_selector)
                    
                    # Multiple click methods for BCA
                    click_methods = [
                        lambda: element.click(),
                        lambda: driver.execute_script("arguments[0].click();", element),
                        lambda: driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", element),
                        lambda: ActionChains(driver).move_to_element(element).click().perform()
                    ]
                    
                    for method in click_methods:
                        try:
                            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                            time.sleep(0.3)
                            method()
                            print(f"   ✅ {description} SUCCESS with {bca_selector}!")
                            return True
                        except:
                            continue
                            
                except:
                    continue
        
        # Method 3: Pengiriman standar fallback
        elif "Pengiriman standar" in description:
            shipping_selectors = [
                # Radio input with delivery-item name
                'input[name="delivery-item"][value="normal"]',
                # Radio icon with aria-label
                'i[aria-label="Pengiriman standar"]',
                # Radio icon with micon classes
                'i.radio__icon.micon.micon-radio-unchecked',
                # Generic radio input
                'input.radio__input[name="delivery-item"]',
                # Text-based selectors
                "//div[contains(text(), 'Pengiriman standar')]",
                "//span[contains(text(), 'Pengiriman standar')]",
                ".radio-wrapper .radio__icon",
                ".item-title:contains('Pengiriman standar')"
            ]
            
            for shipping_selector in shipping_selectors:
                try:
                    if shipping_selector.startswith('//'):
                        element = driver.find_element(By.XPATH, shipping_selector)
                    else:
                        element = driver.find_element(By.CSS_SELECTOR, shipping_selector)
                    
                    # Multiple click methods for shipping
                    click_methods = [
                        lambda: element.click(),
                        lambda: driver.execute_script("arguments[0].click();", element),
                        lambda: driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", element),
                        lambda: ActionChains(driver).move_to_element(element).click().perform()
                    ]
                    
                    for method in click_methods:
                        try:
                            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                            time.sleep(0.2)
                            method()
                            print(f"   ✅ {description} SUCCESS with {shipping_selector}!")
                            return True
                        except:
                            continue
                            
                except:
                    continue
        
        print(f"   ❌ {description} FAILED")
        return False
        
    except Exception as e:
        print(f"   ❌ {description} FAILED: {e}")
        return False

def check_stock_api(product_url):
    """
    Check stock availability via API - Loop until available
    """
    print('📊 Checking stock availability...')
    
    try:
        # Extract product tag from URL
        # URL format: https://www.mi.co.id/id/product/redmi-13x/?skupanel=1&gid=4223716725
        # Extract tag from path: /product/redmi-13x/
        if '/product/' not in product_url:
            print('❌ Invalid product URL format')
            return False
            
        # Extract tag between /product/ and /
        url_parts = product_url.split('/product/')
        if len(url_parts) < 2:
            print('❌ Cannot extract product tag from URL')
            return False
            
        tag = url_parts[1].split('/')[0].split('?')[0]
        
        # Xiaomi stock API endpoint (correct one from user)
        stock_api_url = f"https://go.buy.mi.co.id/id/misc/getgoodsinformation?from=mobile&tag={tag}"
        
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.mi.co.id',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.mi.co.id/id/product/redmi-13x/',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36'
        }
        
        print(f'   🔍 Checking product tag: {tag}')
        print('   🔄 Continuous stock monitoring started...')
        
        check_count = 0
        while True:
            check_count += 1
            print(f'   📡 Stock check #{check_count}...', end=' ')
            
            try:
                response = requests.get(stock_api_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    try:
                        stock_data = response.json()
                        
                        # Parse JSON directly without .get() - access nested structure
                        is_cos = str(stock_data['data']['goodsinformation'][0]['is_cos'])
                        
                        if is_cos == "False":
                            print('✅ AVAILABLE! (is_cos: False)')
                            print(f'   🎉 Stock became available after {check_count} checks!')
                            return True
                        else:
                            print(f'❌ OUT OF STOCK (is_cos: {is_cos})')
                        
                    except (json.JSONDecodeError, KeyError, IndexError) as e:
                        print(f'❌ JSON parsing error: {str(e)[:30]}...')
                else:
                    print(f'❌ HTTP {response.status_code}')
                    
            except requests.exceptions.RequestException as e:
                print(f'❌ Request failed - {str(e)[:30]}...')
            
            # Wait before next check
            print(f'   ⏰ Waiting 2 seconds before next check...')
            time.sleep(2)
            
    except Exception as e:
        print(f'   ❌ Unexpected error during stock check: {e}')
        return False

def accept_cookies_early(driver):
    """
    Enhanced cookie acceptance - Direct to method 6
    """
    print('🍪 Accepting cookies...')
    
    # Wait a bit for page to load
    time.sleep(2)
    
    # Direct to Method 6: #truste-consent-button
    try:
        print('   🔄 Cookie Method 6: #truste-consent-button')
        
        wait = WebDriverWait(driver, 3)
        cookie_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#truste-consent-button')))
        
        # Multiple click methods
        click_methods = [
            lambda: cookie_btn.click(),
            lambda: driver.execute_script("arguments[0].click();", cookie_btn),
            lambda: driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", cookie_btn),
            lambda: ActionChains(driver).move_to_element(cookie_btn).click().perform()
        ]
        
        for j, method in enumerate(click_methods, 1):
            try:
                # Scroll into view first
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", cookie_btn)
                time.sleep(0.3)
                
                method()
                print(f'   ✅ Cookie Method 6.{j} SUCCESS!')
                time.sleep(1)  # Wait for cookie banner to disappear
                return True
            except Exception as e:
                print(f'   ❌ Click method {j} failed: {str(e)[:30]}...')
                continue
                
    except (TimeoutException, NoSuchElementException):
        print(f'   ❌ Cookie Method 6 not found')
    except Exception as e:
        print(f'   ❌ Cookie Method 6 failed: {str(e)[:30]}...')
        
    print('   ✅ Cookie method 6 completed!')
    time.sleep(1)
    return True

def ultra_fast_purchase(username, password, product_url):
    driver = None
    try:
        print("🚀 ULTRA FAST PURCHASE STARTING...")
        
        # Get ultra fast driver
        driver = get_driver_ultra_fast()
        
        # Step 1: Login
        print("🔐 Step 1: Ultra fast login...")
        if not fast_login(driver, username, password):
            print("❌ Login failed!")
            return False
        
        print("✅ Login SUCCESS!")
        time.sleep(1)
        
        # Step 2: Navigate to product URL
        print("🛒 Step 2: Navigating to product...")
        success = False
        for attempt in range(5):  # Increase attempts to 5
            try:
                print(f"   📡 Attempt {attempt + 1}/5...")
                
                # Clear any existing cookies/cache before navigation
                if attempt > 0:
                    print(f"   🧹 Clearing cache before attempt {attempt + 1}...")
                    driver.delete_all_cookies()
                    driver.execute_script("window.localStorage.clear();")
                    driver.execute_script("window.sessionStorage.clear();")
                
                # Set longer timeout for navigation
                driver.set_page_load_timeout(15)
                driver.get(product_url)
                
                # Wait for page to be ready
                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                
                print("   ✅ Product page loaded!")
                success = True
                break
                
            except Exception as e:
                error_msg = str(e)
                print(f"   ❌ Attempt {attempt + 1} failed: {error_msg[:50]}...")
                
                if attempt < 4:  # Not the last attempt
                    wait_time = (attempt + 1) * 2  # Progressive wait: 2, 4, 6, 8 seconds
                    print(f"   ⏰ Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    
                    # Try to recover by refreshing
                    try:
                        print(f"   🔄 Attempting recovery...")
                        driver.refresh()
                        time.sleep(2)
                    except:
                        pass
                else:
                    print("   ❌ All navigation attempts failed!")
                    return False
        
        if not success:
            return False
        
        time.sleep(1)
        
        # Step 3: Accept cookies early
        print("🍪 Step 3: Accepting cookies...")
        accept_cookies_early(driver)
        time.sleep(0.5)
        
        # Step 4: Check stock via API
        print("📊 Step 4: Checking stock availability...")
        if not check_stock_api(product_url):
            print("❌ Product out of stock! Stopping purchase flow.")
            return False
        
        print("✅ Stock available! Continuing with purchase...")
        time.sleep(1)
        
        # Step 5: Click "Beli Sekarang"
        print("🎯 Step 5: Clicking Beli Sekarang...")
        if not fast_click_button(driver, ".footer__btn.footer__submit.footer__submit--main", "Beli Sekarang"):
            print("❌ Beli Sekarang failed!")
            return False
        
        time.sleep(1)
            
        # Step 6: Click "Checkout"
        print("🛒 Step 6: Clicking Checkout...")
        if not fast_click_button(driver, ".cart-footer__submit", "Checkout"):
            print("❌ Checkout failed!")
            return False
        
        time.sleep(1)
        
        # Step 7: Select shipping with loading wait
        print("📦 Step 7: Waiting for shipping options to load...")
        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="delivery-item"], .radio__icon, .delivery-option')))
            time.sleep(1)  # Additional buffer
            print("   ✅ Shipping options loaded!")
        except TimeoutException:
            print("   ⚠️ Shipping options may still be loading, continuing...")
        
        shipping_success = enhanced_click_shipping(driver)
        if not shipping_success:
            print("   ❌ All shipping methods failed, trying alternative...")
            try:
                time.sleep(5)
                alternative_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Pengiriman standar')]")
                if alternative_elements:
                    alternative_elements[0].click()
                    print("   ✅ Pengiriman standar SUCCESS (alternative)!")
                else:
                    print("   ❌ Pengiriman standar FAILED completely")
            except Exception as e:
                print("   ❌ Pengiriman standar FAILED completely")
        
        time.sleep(0.5)
        
        # Step 8: Select BCA payment with loading wait
        print("💳 Step 8: Waiting for payment options to load...")
        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.checkout-pay__item, .pay-item, img[alt="bca"]')))
            time.sleep(1)  # Additional buffer
            print("   ✅ Payment options loaded!")
        except TimeoutException:
            print("   ⚠️ Payment options may still be loading, continuing...")
        
        bca_success = enhanced_click_bca(driver)
        if not bca_success:
            print("❌ All BCA methods failed, but continuing...")
        
        time.sleep(0.5)
        
        # Step 9: Click agreement checkbox
        print("☑️ Step 9: Clicking agreement checkbox...")
        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.checkbox__icon, i[role="checkbox"], i[aria-labelledby="a11y-agree"]')))
            time.sleep(0.5)
            print("   ✅ Checkbox found!")
        except TimeoutException:
            print("   ⚠️ Checkbox may not be present, continuing...")
        
        checkbox_success = enhanced_click_checkbox(driver)
        if not checkbox_success:
            print("⚠️ Checkbox click failed, but continuing...")
        
        time.sleep(0.5)
        
        # Step 10: Click "Bayar sekarang"
        print("💰 Step 10: Waiting for payment button to be ready...")
        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.checkout-footer__submit--pay, button[aria-disabled="false"]')))
            time.sleep(1)
            print("   ✅ Payment button ready!")
        except TimeoutException:
            print("   ⚠️ Payment button may still be loading, continuing...")
        
        bayar_success = enhanced_click_bayar_sekarang(driver)
        if not bayar_success:
            print("❌ All Bayar sekarang methods failed!")
            return False
        
        print("🎉 ULTRA FAST PURCHASE COMPLETED!")
        print("💳 Payment page should be loading...")
        
        # Extract payment information
        payment_info = extract_payment_info(driver)
        
        # Keep running for a bit to ensure extraction
        print("\n⏸️  Payment info extracted. Process will complete in 10 seconds...")
        time.sleep(10)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        try:
            driver.quit()
        except:
            pass

def enhanced_click_shipping(driver):
    """
    Enhanced shipping selection with multiple methods and proper waits
    """
    print("📦 Selecting Pengiriman standar...")
    
    # Multiple shipping selectors in priority order
    shipping_selectors = [
        # Most specific first
        'input[name="delivery-item"][value="normal"]',
        'i[aria-label="Pengiriman standar"]',
        'i.radio__icon.micon.micon-radio-unchecked',
        'input.radio__input[name="delivery-item"]',
        '.radio__icon[role="radio"]',
        '.delivery-option input[type="radio"]',
        # Fallback selectors
        'input[type="radio"][name="delivery-item"]',
        '.radio-wrapper .radio__icon',
        '.shipping-option .radio__icon'
    ]
    
    for i, selector in enumerate(shipping_selectors, 1):
        try:
            print(f"   🔄 Shipping Method {i}: {selector}")
            
            # Wait for element to be present
            element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            
            # Scroll into view first
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(0.3)
            
            # Multiple click methods
            click_methods = [
                # Method 1: Standard Selenium click
                lambda: element.click(),
                # Method 2: JavaScript click
                lambda: driver.execute_script("arguments[0].click();", element),
                # Method 3: JavaScript with event dispatch
                lambda: driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));", element),
                # Method 4: ActionChains click
                lambda: ActionChains(driver).move_to_element(element).click().perform(),
                # Method 5: Force click with JavaScript
                lambda: driver.execute_script("arguments[0].checked = true; arguments[0].dispatchEvent(new Event('change', {bubbles: true}));", element)
            ]
            
            for j, method in enumerate(click_methods, 1):
                try:
                    method()
                    print(f"   ✅ Shipping Method {i}.{j} SUCCESS!")
                    
                    # Verify selection worked
                    time.sleep(0.5)
                    try:
                        if element.get_attribute('checked') or element.get_attribute('aria-checked') == 'true':
                            print(f"   ✅ Shipping selection verified!")
                            return True
                    except:
                        pass
                    
                    return True
                    
                except Exception as e:
                    print(f"   ❌ Click method {j} failed: {str(e)[:30]}...")
                    continue
                    
        except Exception as e:
            print(f"   ❌ Shipping Method {i} failed: {str(e)[:50]}...")
            continue
    
    # Final fallback with XPath text search
    try:
        print("   🔄 Final shipping fallback: text search...")
        xpath_selectors = [
            "//div[contains(text(), 'Pengiriman standar')]",
            "//span[contains(text(), 'Pengiriman standar')]",
            "//label[contains(text(), 'Pengiriman standar')]",
            "//*[contains(text(), 'standar')]"
        ]
        
        for xpath in xpath_selectors:
            try:
                element = driver.find_element(By.XPATH, xpath)
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                driver.execute_script("arguments[0].click();", element)
                print(f"   ✅ Final shipping fallback SUCCESS!")
                return True
            except:
                continue
        
    except:
        pass
        
    print("   ❌ All shipping methods failed!")
    return False

def enhanced_click_bca(driver):
    """
    Enhanced BCA payment selection with comprehensive selectors and explicit waits
    """
    print("💳 Selecting BCA payment...")
    
    # First, debug what payment options are available
    try:
        print("   🔍 DEBUG: Payment options available:")
        payment_items = driver.find_elements(By.CSS_SELECTOR, ".checkout-pay__item, .pay-item, .payment-method")
        for idx, item in enumerate(payment_items):
            try:
                item_text = item.text.strip()
                item_class = item.get_attribute('class') or ''
                print(f"   📋 Payment {idx+1}: '{item_text[:50]}...' | Class: '{item_class[:50]}...'")
            except:
                continue
    except:
        pass
    
    # Comprehensive BCA selectors in priority order
    bca_selectors = [
        # Most specific BCA selectors first - target the radio button or clickable area
        'img[alt="bca"]',
        'img[alt="BCA"]',
        'img[src*="bca"]',
        'img[src*="BCA"]',
        # BCA payment item containers
        '.checkout-pay__item:has(img[alt="bca"])',
        '.pay-item:has(img[alt="bca"])',
        # Radio buttons in BCA context
        '.checkout-pay__item .radio__icon[data-id="pay-method-radio"]',
        '.checkout-pay__item.pay-item .radio-wrapper',
        '.checkout-pay__item .radio__wrapper',
        '.pay-item .radio__icon',
        '.pay-item .radio__wrapper',
        # Input radio buttons
        '.checkout-pay__item input[type="radio"]',
        '.pay-item input[type="radio"]',
        'input[name*="payment"][value*="bca"]',
        'input[name*="payment"][value*="BCA"]',
        # Container elements that might be clickable
        '.checkout-pay__item.pay-item',
        '.pay-item__right',
        'article .pay-item__right',
        # Generic radio selectors (will be filtered)
        '.checkout-pay__item .radio__icon',
        '.pay-method-radio'
    ]
    
    for i, selector in enumerate(bca_selectors, 1):
        try:
            print(f"   🔄 BCA Method {i}: {selector}")
            
            # Use explicit wait for element presence
            try:
                wait = WebDriverWait(driver, 3)
                if ':has(' in selector:
                    # For :has() pseudo-selector, use XPath equivalent
                    if 'img[alt="bca"]' in selector:
                        elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'checkout-pay__item') and .//img[@alt='bca']] | //div[contains(@class, 'pay-item') and .//img[@alt='bca']]")
                    else:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector.replace(':has(img[alt="bca"])', ''))
                else:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                if not elements:
                    print(f"   ❌ No elements found")
                    continue
                    
            except Exception as e:
                print(f"   ❌ Element search failed: {str(e)[:30]}...")
                continue
            
            # Try each element found
            for elem_idx, element in enumerate(elements):
                try:
                    print(f"   📍 Trying element {elem_idx+1}/{len(elements)}")
                    
                    # Check if this element is related to BCA
                    element_context = ""
                    try:
                        # Get element attributes and text
                        element_alt = element.get_attribute('alt') or ""
                        element_src = element.get_attribute('src') or ""
                        element_text = element.text or ""
                        element_value = element.get_attribute('value') or ""
                        
                        # Get parent context
                        parent = element.find_element(By.XPATH, "./..")
                        parent_text = parent.text or ""
                        
                        # Get siblings context
                        siblings = parent.find_elements(By.XPATH, ".//*")
                        sibling_texts = []
                        for sibling in siblings[:5]:  # Check first 5 siblings
                            try:
                                sibling_alt = sibling.get_attribute('alt') or ""
                                sibling_text = sibling.text or ""
                                if sibling_alt or sibling_text:
                                    sibling_texts.append(f"{sibling_alt} {sibling_text}".strip())
                            except:
                                continue
                        
                        element_context = f"{element_alt} {element_src} {element_text} {element_value} {parent_text} {' '.join(sibling_texts)}".lower()
                        print(f"   📝 Element context: '{element_context[:100]}...'")
                        
                    except Exception as e:
                        print(f"   ⚠️ Context check failed: {str(e)[:30]}...")
                    
                    # Skip if not BCA related (for generic selectors)
                    if i > 15 and "bca" not in element_context:
                        print(f"   ⏭️ Skipping non-BCA element")
                        continue
                    
                    # Check if element is visible and interactable
                    if not element.is_displayed():
                        print(f"   ⏭️ Element not visible")
                        continue
                    
                    # Scroll into view first
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                    time.sleep(0.5)
                    
                    # Multiple click methods with enhanced debugging
                    click_methods = [
                        # Method 1: Standard Selenium click
                        ("Standard click", lambda: element.click()),
                        # Method 2: JavaScript click
                        ("JavaScript click", lambda: driver.execute_script("arguments[0].click();", element)),
                        # Method 3: JavaScript with event dispatch
                        ("Event dispatch", lambda: driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));", element)),
                        # Method 4: ActionChains click
                        ("ActionChains", lambda: ActionChains(driver).move_to_element(element).click().perform()),
                        # Method 5: Parent element click (for radio icons)
                        ("Parent click", lambda: driver.execute_script("arguments[0].parentElement.click();", element)),
                        # Method 6: Force selection for radio inputs
                        ("Force radio", lambda: driver.execute_script("if(arguments[0].type === 'radio') { arguments[0].checked = true; arguments[0].dispatchEvent(new Event('change', {bubbles: true})); } else { arguments[0].click(); }", element)),
                        # Method 7: Click container if this is an image
                        ("Container click", lambda: driver.execute_script("var container = arguments[0].closest('.checkout-pay__item, .pay-item'); if(container) container.click(); else arguments[0].click();", element))
                    ]
                    
                    for method_name, method in click_methods:
                        try:
                            print(f"   🔄 Trying {method_name}...")
                            method()
                            print(f"   ✅ BCA Method {i}.{elem_idx+1} SUCCESS with {method_name}!")
                            
                            # Verify selection worked
                            time.sleep(0.8)
                            try:
                                # Check various indicators of selection
                                is_selected = (
                                    element.get_attribute('checked') == 'true' or
                                    element.get_attribute('aria-checked') == 'true' or
                                    'selected' in (element.get_attribute('class') or '') or
                                    'checked' in (element.get_attribute('class') or '')
                                )
                                
                                # Also check parent for selection indicators
                                try:
                                    parent = element.find_element(By.XPATH, "./..")
                                    parent_selected = (
                                        'selected' in (parent.get_attribute('class') or '') or
                                        'checked' in (parent.get_attribute('class') or '') or
                                        'active' in (parent.get_attribute('class') or '')
                                    )
                                    is_selected = is_selected or parent_selected
                                except:
                                    pass
                                
                                if is_selected:
                                    print(f"   ✅ BCA selection verified!")
                                else:
                                    print(f"   ⚠️ Selection not verified, but continuing...")
                                    
                            except Exception as e:
                                print(f"   ⚠️ Verification failed: {str(e)[:30]}...")
                            
                            return True
                            
                        except Exception as e:
                            print(f"   ❌ {method_name} failed: {str(e)[:40]}...")
                            continue
                            
                except Exception as e:
                    print(f"   ❌ Element {elem_idx+1} processing failed: {str(e)[:50]}...")
                    continue
                    
        except Exception as e:
            print(f"   ❌ BCA Method {i} failed: {str(e)[:50]}...")
            continue
    
    # Final fallback with XPath text search and explicit waits
    try:
        print("   🔄 Final BCA fallback: comprehensive text search...")
        xpath_selectors = [
            "//img[@alt='bca' or @alt='BCA']",
            "//img[contains(@src, 'bca') or contains(@src, 'BCA')]",
            "//div[contains(text(), 'BCA')]",
            "//span[contains(text(), 'BCA')]",
            "//label[contains(text(), 'BCA')]",
            "//*[contains(text(), 'BCA')]",
            "//*[@aria-label='BCA' or @aria-label='bca']",
            "//div[contains(@class, 'pay-item') and contains(., 'BCA')]",
            "//div[contains(@class, 'checkout-pay__item') and contains(., 'BCA')]"
        ]
        
        for xpath in xpath_selectors:
            try:
                wait = WebDriverWait(driver, 2)
                elements = driver.find_elements(By.XPATH, xpath)
                
                for element in elements:
                    if not element.is_displayed():
                        continue
                        
                    print(f"   📝 XPath element found: '{element.get_attribute('alt') or element.text or 'no text'}' with tag '{element.tag_name}'")
                    
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                    time.sleep(0.3)
                    
                    # Try multiple click approaches for XPath elements
                    try:
                        # Try clicking the element itself
                        driver.execute_script("arguments[0].click();", element)
                        print(f"   ✅ Final BCA fallback SUCCESS (direct)!")
                        return True
                    except:
                        try:
                            # Try clicking parent container
                            driver.execute_script("var container = arguments[0].closest('.checkout-pay__item, .pay-item'); if(container) container.click();", element)
                            print(f"   ✅ Final BCA fallback SUCCESS (container)!")
                            return True
                        except:
                            try:
                                # Try standard click
                                element.click()
                                print(f"   ✅ Final BCA fallback SUCCESS (standard)!")
                                return True
                            except:
                                continue
                        
            except:
                continue
                
    except:
        pass
    
    print("   ❌ All BCA methods failed!")
    return False

def enhanced_click_bayar_sekarang(driver):
    """
    Enhanced "Bayar sekarang" button clicking with multiple methods
    """
    print("💰 Clicking Bayar sekarang...")
    
    # Multiple selectors for "Bayar sekarang" button in priority order
    bayar_selectors = [
        # Most specific selector based on the actual button
        'button.mi-btn.mi-btn--primary.mi-btn--normal.mi-btn--light.checkout-footer__submit--pay',
        # Alternative specific selectors
        '.checkout-footer__submit--pay',
        'button.checkout-footer__submit--pay',
        '.mi-btn.checkout-footer__submit--pay',
        # Generic selectors with aria-disabled check
        'button[aria-disabled="false"].checkout-footer__submit--pay',
        'button.mi-btn.mi-btn--primary[aria-disabled="false"]',
        # Fallback selectors
        '.checkout-footer__submit',
        'button.mi-btn--primary',
        '.payment-submit-btn',
        'button[tabindex="0"][aria-disabled="false"]'
    ]
    
    for i, selector in enumerate(bayar_selectors, 1):
        try:
            print(f"   🔄 Bayar Method {i}: {selector}")
            
            # Wait for element to be present and clickable
            element = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            
            # Check if button is enabled
            aria_disabled = element.get_attribute('aria-disabled')
            if aria_disabled == 'true':
                print(f"   ⏭️ Button is disabled, skipping...")
                continue
            
            # Check if this is the correct button by text content
            button_text = element.text.strip().lower()
            if i > 5 and 'bayar' not in button_text and 'sekarang' not in button_text and 'pay' not in button_text:
                print(f"   ⏭️ Not payment button: '{button_text}', skipping...")
                continue
            
            # Scroll into view first
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(0.5)
            
            # Multiple click methods
            click_methods = [
                # Method 1: Standard Selenium click
                lambda: element.click(),
                # Method 2: JavaScript click
                lambda: driver.execute_script("arguments[0].click();", element),
                # Method 3: JavaScript with event dispatch
                lambda: driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));", element),
                # Method 4: ActionChains click
                lambda: ActionChains(driver).move_to_element(element).click().perform(),
                # Method 5: Force click with focus
                lambda: driver.execute_script("arguments[0].focus(); arguments[0].click();", element),
                # Method 6: Submit form if it's a submit button
                lambda: driver.execute_script("if(arguments[0].form) arguments[0].form.submit(); else arguments[0].click();", element)
            ]
            
            for j, method in enumerate(click_methods, 1):
                try:
                    method()
                    print(f"   ✅ Bayar Method {i}.{j} SUCCESS!")
                    
                    # Check if page changed or loading started
                    time.sleep(1)
                    current_url = driver.current_url
                    if 'payment' in current_url or 'bayar' in current_url or 'checkout' not in current_url:
                        print(f"   ✅ Payment page navigation detected!")
                        return True
                    
                    return True
                    
                except Exception as e:
                    print(f"   ❌ Bayar click method {j} failed: {str(e)[:30]}...")
                    continue
                    
        except Exception as e:
            print(f"   ❌ Bayar Method {i} failed: {str(e)[:50]}...")
            continue
    
    # Final fallback with XPath text search
    try:
        print("   🔄 Final Bayar fallback: text search...")
        xpath_selectors = [
            "//button[contains(text(), 'Bayar sekarang')]",
            "//button[contains(text(), 'Bayar')]",
            "//button[contains(text(), 'sekarang')]",
            "//*[contains(text(), 'Bayar sekarang')]",
            "//button[@aria-disabled='false' and contains(text(), 'Bayar')]"
        ]
        
        for xpath in xpath_selectors:
            try:
                element = driver.find_element(By.XPATH, xpath)
                
                # Check if button is enabled
                if element.get_attribute('aria-disabled') == 'true':
                    continue
                
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.3)
                
                # Try multiple click methods
                try:
                    driver.execute_script("arguments[0].click();", element)
                    print(f"   ✅ Final Bayar fallback SUCCESS (JS click)!")
                    return True
                except:
                    try:
                        element.click()
                        print(f"   ✅ Final Bayar fallback SUCCESS (direct click)!")
                        return True
                    except:
                        continue
                        
            except:
                continue
                
    except:
        pass
    
    print("   ❌ All Bayar sekarang methods failed!")
    return False

def enhanced_click_checkbox(driver):
    """
    Enhanced checkbox clicking for agreement checkbox
    """
    print("☑️ Clicking agreement checkbox...")
    
    # Multiple selectors for checkbox in priority order
    checkbox_selectors = [
        # Most specific selector based on the actual checkbox
        'i[aria-labelledby="a11y-agree"][role="checkbox"]',
        'i.checkbox__icon.micon.micon-checkbox-unchecked',
        'i[role="checkbox"][aria-checked="false"]',
        # Alternative selectors
        '.checkbox__icon[role="checkbox"]',
        'i[role="checkbox"]',
        '.checkbox__icon',
        'i.micon-checkbox-unchecked',
        # Generic checkbox selectors
        'input[type="checkbox"]',
        '.checkbox-wrapper',
        '[role="checkbox"]'
    ]
    
    for i, selector in enumerate(checkbox_selectors, 1):
        try:
            print(f"   🔄 Checkbox Method {i}: {selector}")
            
            # Wait for element to be present
            element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            
            # Check if checkbox is already checked
            aria_checked = element.get_attribute('aria-checked')
            if aria_checked == 'true':
                print(f"   ✅ Checkbox already checked!")
                return True
            
            # Scroll into view first
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(0.3)
            
            # Multiple click methods for checkbox
            click_methods = [
                # Method 1: Standard Selenium click
                lambda: element.click(),
                # Method 2: JavaScript click
                lambda: driver.execute_script("arguments[0].click();", element),
                # Method 3: JavaScript with event dispatch
                lambda: driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));", element),
                # Method 4: ActionChains click
                lambda: ActionChains(driver).move_to_element(element).click().perform(),
                # Method 5: Force check with aria-checked
                lambda: driver.execute_script("arguments[0].setAttribute('aria-checked', 'true'); arguments[0].click();", element),
                # Method 6: Change class for visual feedback
                lambda: driver.execute_script("arguments[0].className = arguments[0].className.replace('unchecked', 'checked'); arguments[0].setAttribute('aria-checked', 'true'); arguments[0].click();", element)
            ]
            
            for j, method in enumerate(click_methods, 1):
                try:
                    method()
                    print(f"   ✅ Checkbox Method {i}.{j} SUCCESS!")
                    
                    # Verify checkbox is now checked
                    time.sleep(0.3)
                    try:
                        new_aria_checked = element.get_attribute('aria-checked')
                        class_name = element.get_attribute('class') or ''
                        if new_aria_checked == 'true' or 'checked' in class_name:
                            print(f"   ✅ Checkbox verification SUCCESS!")
                            return True
                    except:
                        pass
                    
                    return True
                    
                except Exception as e:
                    print(f"   ❌ Checkbox click method {j} failed: {str(e)[:30]}...")
                    continue
                    
        except Exception as e:
            print(f"   ❌ Checkbox Method {i} failed: {str(e)[:50]}...")
            continue
    
    # Final fallback with XPath and label search
    try:
        print("   🔄 Final checkbox fallback: text/label search...")
        fallback_selectors = [
            # XPath for agreement related text
            "//i[contains(@aria-labelledby, 'agree')]",
            "//i[contains(@class, 'checkbox')]",
            "//*[@role='checkbox']",
            "//label[contains(text(), 'setuju')]//i",
            "//label[contains(text(), 'agree')]//i",
            # CSS selectors for common checkbox patterns
            "label input[type='checkbox']",
            ".agreement-checkbox",
            ".terms-checkbox"
        ]
        
        for selector in fallback_selectors:
            try:
                if selector.startswith('//'):
                    element = driver.find_element(By.XPATH, selector)
                else:
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.2)
                
                # Try both JS and direct click
                try:
                    driver.execute_script("arguments[0].click();", element)
                    print(f"   ✅ Final checkbox fallback SUCCESS (JS)!")
                    return True
                except:
                    try:
                        element.click()
                        print(f"   ✅ Final checkbox fallback SUCCESS (direct)!")
                        return True
                    except:
                        continue
                        
            except:
                continue
                
    except:
        pass
    
    print("   ❌ All checkbox methods failed!")
    return False

def load_config_simple(filename="data.txt"):
    """
    Simple config loader
    """
    if not os.path.exists(filename):
        print(f"File {filename} not found!")
        return None
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line and '|' in line and not line.startswith('#'):
                parts = line.split('|')
                if len(parts) >= 3:
                    return {
                        'username': parts[0].strip(),
                        'password': parts[1].strip(),
                        'product_url': parts[2].strip()
                    }
    return None

def extract_payment_info(driver):
    """
    Extract payment information from BCA payment page
    """
    print("💰 Extracting payment information...")
    
    try:
        # Wait for payment page to load
        time.sleep(3)
        
        payment_info = {
            "virtualAccount": None,
            "totalPayment": None,
            "invoiceNumber": None,
            "timeRemaining": None
        }
        
        # Extract Virtual Account Number
        va_selectors = [
            ".payment-code .code",
            ".bca__topuserinfo .code",
            "[class*='code']",
            ".virtual-account-number",
            ".va-number"
        ]
        
        for selector in va_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                text = element.text.strip()
                if re.match(r'^\d{20,}$', text):
                    payment_info["virtualAccount"] = text
                    break
            except:
                continue
        
        # Extract Total Payment
        total_selectors = [
            ".right-amount",
            ".container-amount .right-amount",
            ".total-payment",
            "[class*='amount']"
        ]
        
        for selector in total_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                text = element.text.strip()
                if "IDR" in text:
                    payment_info["totalPayment"] = text
                    break
            except:
                continue
        
        # Extract Invoice Number
        invoice_selectors = [
            ".right-invoice",
            ".container-invoice .right-invoice", 
            ".invoice-number",
            "[class*='invoice']"
        ]
        
        for selector in invoice_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                text = element.text.strip()
                if re.match(r'^\d{19,}$', text):
                    payment_info["invoiceNumber"] = text
                    break
            except:
                continue
        
        # Extract Time Remaining
        time_selectors = [
            ".countDown__J_timeRemaining",
            ".countdown-time",
            "[class*='timeRemaining']",
            "[class*='countdown']"
        ]
        
        for selector in time_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                text = element.text.strip()
                if re.match(r'\d{2}\s*:\s*\d{2}\s*:\s*\d{2}', text):
                    payment_info["timeRemaining"] = text
                break
            except:
                continue
        
        # Display extracted information
        print('\n🎉 PAYMENT INFORMATION EXTRACTED:')
        print('=' * 50)
        
        if payment_info["virtualAccount"]:
            print(f"💳 No. Virtual Account: {payment_info['virtualAccount']}")
        else:
            print("❌ Virtual Account: Not found")
        
        if payment_info["totalPayment"]:
            print(f"💰 Total Pembayaran: {payment_info['totalPayment']}")
        else:
            print("❌ Total Payment: Not found")
        
        if payment_info["invoiceNumber"]:
            print(f"📄 No. Tagihan: {payment_info['invoiceNumber']}")
        else:
            print("❌ Invoice Number: Not found")
        
        if payment_info["timeRemaining"]:
            print(f"⏰ Waktu Tersisa: {payment_info['timeRemaining']}")
        else:
            print("❌ Time Remaining: Not found")
        
        print('=' * 50)
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"payment_info_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(payment_info, f, indent=2)
        
        print(f"💾 Payment info saved to: {filename}")
        
        return payment_info
        
    except Exception as e:
        print(f"❌ Error extracting payment info: {str(e)}")
        return None

if __name__ == "__main__":
    print("🚀 XIAOMI ULTRA FAST PURCHASE BOT")
    print("⚡ Optimized for maximum speed")
    print("=" * 40)
    
    config = load_config_simple("data.txt")
    if not config:
        print("❌ Configuration not found!")
        exit()
    
    print(f"📧 Username: {config['username']}")
    print(f"🔗 Product URL: {config['product_url']}")
    print("\n🚀 Starting ultra fast purchase...")
    
    success = ultra_fast_purchase(
        config['username'],
        config['password'],
        config['product_url']
        )
    
    if success:
        print("✅ Process completed!")
    else:
        print("❌ Process failed!") 
