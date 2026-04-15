from selenium import webdriver

import time


driver = webdriver.Chrome()
driver.maximize_window()  # 最大化浏览器
driver.implicitly_wait(8)  # 设置隐式时间等待

driver.get("https://inv-veri.chinatax.gov.cn/")
time.sleep(1) # 延迟1秒
# 1.1、点击高级，
driver.find_element_by_id("details-button").click()
time.sleep(1) # 延迟1秒
# 1.2、继续前往（不安全）
driver.find_element_by_id("proceed-link").click()
time.sleep(1) # 延迟1秒
# 2.1、输入发票代码，
driver.find_element_by_id("fpdm").send_keys("3200211130")
time.sleep(1) # 延迟1秒
# 2.2、输入发票号码
driver.find_element_by_id("fphm").send_keys("80996614")
#913207001389999296
# 2.3、开票日期
driver.find_element_by_id("kprq").send_keys("20220210")
time.sleep(1) # 20220120
# 2.4、开票日期
driver.find_element_by_id("kjje").send_keys("2088.5")


# 2.5、验证码
# driver.find_element_by_id("yzm").send_keys("6406.21")
# driver.quit()
