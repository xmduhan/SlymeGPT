
from webdriver_manager.chrome import ChromeDriverManager
driver_executable_path = ChromeDriverManager().install()
browser_executable_path = '/opt/google/chrome/google-chrome'

import undetected_chromedriver as uc
driver = uc.Chrome(
    driver_executable_path=driver_executable_path,
    browser_executable_path=browser_executable_path,
    use_subprocess=False,
)
input("Press Enter to continue...")
