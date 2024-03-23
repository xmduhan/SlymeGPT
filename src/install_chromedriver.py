from webdriver_manager.chrome import ChromeDriverManager
driver_executable_path = ChromeDriverManager().install()
print(driver_executable_path)
