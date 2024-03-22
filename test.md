```python
from webdriver_manager.chrome import ChromeDriverManager
driver_executable_path = ChromeDriverManager().install()
print(driver_executable_path)

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


```bash
clear
pip list | grep selenium
```

```bash
pip install -U pip
pip install -r requirements.txt
```
