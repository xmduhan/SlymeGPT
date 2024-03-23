```python
from webdriver_manager.chrome import ChromeDriverManager
driver_executable_path = ChromeDriverManager().install()
print(driver_executable_path)
```

```python
from selenium import webdriver
driver_executable_path = '/home/duhan/.wdm/drivers/chromedriver/linux64/123.0.6312.58/chromedriver-linux64/chromedriver'
driver = webdriver.Chrome(driver_executable_path)
input("Press Enter to continue...")
```

```python
import undetected_chromedriver as uc
driver_executable_path = '/home/duhan/.wdm/drivers/chromedriver/linux64/123.0.6312.58/chromedriver-linux64/chromedriver'
browser_executable_path = '/opt/google/chrome/google-chrome'
driver = uc.Chrome(
    driver_executable_path=driver_executable_path,
    browser_executable_path=browser_executable_path,
    use_subprocess=False,
)
input("Press Enter to continue...")
```

```python
from selenium import webdriver

options = webdriver.ChromeOptions()
# options.add_argument(f"--user-data-dir=~/.config/google-chrome/selenium-standalone-chrome")
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options
)

driver.get("https://www.nowsecure.nl")
input("Press Enter to continue...")

driver.quit()
```


```bash
clear
pip list | grep selenium
```

```bash
pip install -U pip
pip install -r requirements.txt
```
