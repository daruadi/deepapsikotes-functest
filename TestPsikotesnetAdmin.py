import unittest
from selenium import webdriver
import datetime
from dotenv import load_dotenv
import os

class TestPsikotesnetAdmin(unittest.TestCase):

	def setUp(self):
		load_dotenv()
		self.driver = webdriver.PhantomJS()
		self.driver.get(os.getenv("login_url"))
		self.driver.find_element_by_id("identity").send_keys(os.getenv("USERNAME"))
		self.driver.find_element_by_id("password").send_keys(os.getenv("PASSWORD"))
		self.driver.find_element_by_xpath("/html/body/div/div[2]/form/div[3]/div[2]/button").click()

	def test_login(self):
		message = self.driver.find_element_by_xpath("/html/body/div/div/section[2]/div[1]/p")
		self.assertIn("Logged In Successfully", message.text, "not login")

	def test_create_kode_unik(self):
		self.driver.get(os.getenv("unqcode_list_url"))
		self.driver.find_element_by_xpath("/html/body/div/div/section[2]/div[2]/div/form/div/span/span[1]/span").click()
		self.driver.find_element_by_xpath("/html/body/span/span/span[1]/input").send_keys("Testing")
		self.driver.find_element_by_xpath("/html/body/span/span/span[2]/ul/li").click()

		kolom = self.driver.find_element_by_xpath("/html/body/div/div/section[2]/div[3]/div/table/tbody/tr[2]/td[5]")
		self.assertIn("Testing", kolom.text, "Client Testing tidak ditemukan")

		jumlah_kode_unik_awal = len(self.driver.find_elements_by_xpath("/html/body/div/div/section[2]/div[3]/div/table/tbody/*"))

		self.driver.get(os.getenv("make_unqcode_url"))
		self.driver.find_element_by_xpath("/html/body/div/div/section[2]/form/div[1]/input").send_keys("1")
		self.driver.find_element_by_xpath("/html/body/div/div/section[2]/form/div[3]/span/span[1]/span/span[2]").click()
		self.driver.find_element_by_xpath("/html/body/span/span/span[1]/input").send_keys("Testing")
		self.driver.find_element_by_xpath("/html/body/span/span/span[2]/ul/li").click()
		tomorrow = datetime.date.today() + datetime.timedelta(days=1)
		self.driver.find_element_by_id("datepicker").send_keys(tomorrow.strftime("%d %b %Y"))
		self.driver.find_element_by_xpath("/html/body/div/div/section[2]/form/div[5]/input").click()
		
		jumlah_kode_unik = len(self.driver.find_elements_by_xpath("/html/body/div/div/section[2]/div[3]/div/table/tbody/*"))
		self.assertEquals(jumlah_kode_unik, (jumlah_kode_unik_awal+1))

	def tearDown(self):
		self.driver.find_element_by_xpath("/html/body/div/header/nav/div/ul/li/a").click()
		self.driver.find_element_by_xpath("/html/body/div/header/nav/div/ul/li/ul/li[2]/div[2]/a").click()
		self.driver.quit()

if __name__ == '__main__':
	unittest.main(warnings='ignore')