
# Import necessary modules
import scrapy  # Scrapy is a web crawling and web scraping framework
from scrapy.crawler import CrawlerProcess  # CrawlerProcess is a class to control the crawling process
import requests  # Requests module is used to send HTTP requests
from scrapy import Selector  # Selector is used to extract data from HTML/XML documents
import csv  # CSV module for handling CSV files
import os  # OS module provides functions for interacting with the operating system
import re  # Regular expression module for pattern matching
# from urllib import response # urllib module provides a high-level interface for fetching data across the World Wide Web
from selenium import webdriver # Selenium is a web testing library used to automate web browser interaction
from time import sleep # Time module for adding delays 
from selenium.webdriver.chrome.options import Options # Options class to configure Chrome
from selenium.webdriver.common.by import By # By class to locate elements by different strategies
from selenium.webdriver.support.ui import WebDriverWait # WebDriverWait class to wait for a certain condition to occur before proceeding
from selenium.webdriver.support import expected_conditions as EC # EC provides a set of predefined conditions to wait until satisfied
from selenium.webdriver.chrome.service import Service # Service class to manage the ChromeDriver server 
from webdriver_manager.chrome import ChromeDriverManager # ChromeDriverManager class to install the ChromeDriver
from selenium.webdriver.chrome.service import Service

# # Record the starting time of the program
# start_time = time.time()

# Function to scrape_records function to scrape records e.g. 000001, 000002, 000003, etc.
def scrape_records():
   print("\n> Scraping records (e.g. 000001, 000002, 000003, etc.)...")

   # URL of the webpage to scrape
   url = "https://fund.eastmoney.com/allfund.html"

   payload = ""  # No payload required for this GET request

   # Headers to mimic a request from a web browser
   headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
   }

   # Sending a GET request to the URL with provided payload and headers
   response = requests.request("GET", url, data=payload, headers=headers)

   # Creating a Selector object from the HTML content of the response
   response = Selector(text=response.text)

   # Extracting records from the HTML using XPath
   # The XPath selects text within div tags of class "num_box", under ul and li tags, inside an a tag which is the first child of div
   records = response.xpath('//div[@class="num_box"]/ul/li/div/a[1]/text()').extract()

   # Processing extracted records to remove unwanted characters and extract desired information
   # Splitting each record by "£¨" (left parenthesis) and taking the second part, then splitting by "£©" (right parenthesis) and taking the first part
   records = [record.split("£¨")[1].split("£©")[0] for record in records]

   # Returning the list of extracted and processed records
   return records

# Function to create_folders function to create folders with the provided records as names
def create_folders(records):
   print("> Creating folders for records...\n")
   sleep(2)

   # Looping through each record in the provided list
   for record in records:
      # Converting the record to a string to use as folder name
      folder_name = str(record)
      
      # Checking if the folder already exists
      if not os.path.exists(folder_name):
         # Creating a folder with the folder_name, since it doesn't exist
         os.makedirs(folder_name)
         
         # Printing a message indicating the folder creation
         print(f"> Created folder {folder_name}")
      else:
         print(f"> Folder {folder_name} already exists, skipping creation.")

   # Printing a message indicating the completion of folder creation
   # print("\n> Folders created successfully.")
   sleep(3) # Pause for 3 seconds

   # Print a message indicating the start of the scraping process
   print("\n> Starting scraping process...\n")
   sleep(2) # Pause for 2 seconds


# Call the function scrape_records() to retrieve records
records = scrape_records()

print("\n> Excluding records that do not have desired data table...\n\n")
sleep(2) # Pause for 2 seconds

# Initialize a list to store those records that has desired data table
table_records = []

# Define a class named scrapySpider which inherits from scrapy.Spider
class scrapySpider(scrapy.Spider):
   # Define the name of the spider 
   name = "scrapySpider"

   # Define custom settings for the spider
   custom_settings = {
      "DUPEFILTER_CLASS": "scrapy.dupefilters.BaseDupeFilter",  # Disable default duplicate filter
      "RETRY_TIMES": 50,  # Retry failed requests 50 times
      "CONCURRENT_REQUESTS": 100,  # Limit concurrent requests to 100
   }

   # Initialize an empty set to keep track of records for which save_data has been called
   processed_records = set()

   # Define a method to initiate requests to scrape fund data
   def start_requests(self):
      # Iterate over records
      for record in records:
         # Define URL for holdings data API
         holdings_url = "https://fundf10.eastmoney.com/FundArchivesDatas.aspx"

         # Define query parameters for holdings data API
         holdings_querystring = {
            "type":"jjcc", # Set the type to jjcc
            "code":f"{record}", # Use the current record as the fund code
            "topline":"10", # Set the topline to 10
            "year":"","month":"" # Set year and month to empty string
         }

         # Define headers for the HTTP request to holdings data API
         headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9,so;q=0.8",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
         }

         # Construct full URL for the holdings data API request
         full_holdings_url = f"{holdings_url}?{'&'.join(f'{k}={v}' for k, v in holdings_querystring.items())}"

         # Initiate a request to the holdings data API
         yield scrapy.Request(
            url = full_holdings_url, # Use the full URL
            method = "GET", # Use the GET method
            headers = headers, # Use the defined headers
            dont_filter = True,  # Disable default duplicate filter
            meta={"record": record}, # Pass the record as metadata
            callback=self.parse_holdings, # Call the parse_holdings method to parse the response
         ) 
      
   # Define a method to parse the response from the holdings data API
   def parse_holdings(self, response):
      # Extracting the record from meta data
      record = response.meta['record']

      # Extracting HTML content from the response string using regular expressions
      html_content_match = re.search(r'content:\"(.*)\",arryear', response.text)
      if html_content_match:
         html_content = html_content_match.group(1)

      # Parsing the HTML content using Scrapy Selector
      response = Selector(text=html_content)

      # Initialize data_table to None 
      data_table = None 
      
      # Extracting tables from the response using XPath
      tables = response.xpath('//table/tbody')
      for table in tables:
         # Checking if the table has 9 columns
         tds = table.xpath('.//tr[1]/td')
         if len(tds) == 9:
            data_table = table
            break

      # If a suitable data table is found, record it
      if data_table:
         table_records.append(record)

      # # If only one table record is found, close the spider as crawling is completed
      # if len(table_records) == 1:
      #    self.crawler.engine.close_spider(self, "Crawling completed successfully")

      # Log the parsing of holdings for a specific record
      self.logger.info(f"Parsing holdings for record: {record}")


process = CrawlerProcess() # Create a CrawlerProcess object
process.crawl(scrapySpider) # Pass the scrapySpider class to the crawl method
process.start() # Start the crawling process

print("\n\n\n> Records with desired data table extracted successfully.")

# # Define a function to initialize the bot, by setting up the Chrome driver
# def botInitialization():
#    # Initialize the Bot
#    chromeOptions = Options()
#    chromeOptions.add_argument("start-maximized")
#    chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
#    chromeOptions.add_experimental_option("excludeSwitches", ["enable-logging"])
#    chromeOptions.add_experimental_option('useAutomationExtension', False)
#    chromeOptions.add_argument('--disable-blink-features=AutomationControlled')
   
#    # Disable images loading    
#    prefs = {"profile.managed_default_content_settings.images": 2}
#    chromeOptions.add_experimental_option("prefs", prefs)
   
#    chromePath = "chromedriver.exe" # Path to the Chrome driver executable
#    driver = webdriver.Chrome(executable_path=chromePath, options=chromeOptions) # Initialize the Chrome driver
#    driver.maximize_window() # Maximize the window
#    return driver # Return the driver object

# Define a function to initialize the bot, by setting up the Chrome driver
def botInitialization():
   options = Options()
   # options.add_argument('--headless')
   # options.add_argument('--no-sandbox')
   options.add_argument('--disable-dev-shm-usage')
   service=Service(ChromeDriverManager().install())
   driver = webdriver.Chrome(service=service, options=options)
   return driver

# Define a function to save data to a CSV file
def save_data(record, data):
   # Save data into folder named after the record
   folder_name = os.path.join(os.path.dirname(__file__), record)

   # Open or create a Holdings.csv file inside the folder
   holdings_csv = open(f'{folder_name}/Holdings.csv', 'w', newline='', encoding="utf-8-sig")

   # Define field names for Holdings.csv
   holdings_field_names = ['序号', '股票代码', '股票名称', '最新价', '涨跌幅', '相关资讯', '占净值\n 比例', '持股数\n（万股）', '持仓市值\n（万元）']

   # Create a CSV writer object for Holdings.csv
   holdings_writer = csv.DictWriter(holdings_csv, fieldnames=holdings_field_names)

   # Write header row to Holdings.csv
   holdings_writer.writeheader()

   # Write data rows to Holdings.csv
   for data_row in data:
      holdings_writer.writerow(data_row)

   # Close Holdings.csv file
   holdings_csv.close()

# table_records = table_records[0:1] # Limiting the number of records to 100 for testing purposes

# Call the function create_folders() with the retrieved records and scrape_fund variable as arguments
create_folders(table_records)
records_scraped = 0 # Initialize a variable to keep track of the number of records scraped

# Record the starting time of the program
# start_time = time.time()

# Calling the botInitialization function to initialize the bot and storing the driver object in the driver variable
driver = botInitialization() 

# Loop through each record in table_records
for record in table_records:
   
   while True:
      # Construct the link for the current record
      link = f"https://fundf10.eastmoney.com/ccmx_{record}.html"
      
      # Open the link in the driver
      driver.get(link)

      # Wait for the table element to be present on the page
      try:
         # Find the table element by XPath
         WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//table/tbody//tr[1]')))
         break
      except:
         # If the table is not found, continue the loop
         continue

   # Continue looping until the table data is loaded on the page
   while True:
      # Extract the HTML content from the page using Scrapy Selector
      response = Selector(text=driver.page_source)
      
      # Check if the table data is loaded by checking if the first cell of the first row exists
      if response.xpath('//table/tbody//tr[1]/td[1]/text()').extract_first():
         # If table data is loaded, break the loop
         break
      else:
         # If table data is not loaded, continue the loop
         continue

   # sleep(1) # Waiting for 1 second
   # response = Selector(text=driver.page_source) # Converting the page source to a response object

   # Initialize variables to store data
   序号 = ""
   股票代码 = ""
   股票名称 = ""
   最新价 = ""
   涨跌幅 = ""
   相关资讯 = ""
   占净值比例 = ""
   持股数 = ""
   持仓市值 = ""

   # Initialize holdings_data list
   holdings_data = []

   # Initialize data_table as None
   data_table = None

   # Extracting all tables from the response
   tables = response.xpath('//table/tbody')

   # Iterate over each table
   for table in tables:
      # Extract the first row of the table
      tds = table.xpath('.//tr[1]/td')
      
      # Check if the table has 9 columns (td elements)
      if len(tds) == 9:
         # If the condition is met, assign the table to data_table and break the loop
         data_table = table
         break

   # Check if a suitable data_table is found
   if data_table:
      # Extract all rows from the data_table
      data_rows = data_table.xpath('.//tr')

      # Iterate over each row
      for row in data_rows:
         # Extracting data from each column of the row
         序号 = row.xpath('.//td[1]/text()').extract_first()
         股票代码 = row.xpath('.//td[2]/a/text()').extract_first()
         股票名称 = row.xpath('.//td[3]/a/text()').extract_first()
         最新价 = row.xpath('.//td[4]/span/text()').extract_first()
         涨跌幅 = row.xpath('.//td[5]/span/text()').extract_first()
         
         # Extract and join related news from the column
         相关资讯 = row.xpath('.//td[6]/a/text()').extract()
         相关资讯 = " ".join(相关资讯)
         
         占净值比例 = row.xpath('.//td[7]/text()').extract_first()
         持股数 = row.xpath('.//td[8]/text()').extract_first()
         持仓市值 = row.xpath('.//td[9]/text()').extract_first()

         # Print the extracted data 
         # print("--------------------------------------------")
         # print("序号:", 序号)
         # print("股票代码:", 股票代码)
         # print("股票名称:", 股票名称)
         # print("最新价:", 最新价)
         # print("涨跌幅:", 涨跌幅)
         # print("相关资讯:", 相关资讯)
         # print("占净值 比例:", 占净值比例)
         # print("持股数（万股）", 持股数)   
         # print("持仓市值（万元）", 持仓市值)
         # print("--------------------------------------------")
            
        # Create a dictionary to store data for a single row
         holdings_data_row = {
            "序号": 序号,
            "股票代码": 股票代码,
            "股票名称": 股票名称,
            "最新价": 最新价,
            "涨跌幅": 涨跌幅,
            "相关资讯": 相关资讯,
            "占净值\n 比例": 占净值比例,
            "持股数\n（万股）": 持股数,
            "持仓市值\n（万元）": 持仓市值
         }

         # Append the row data to holdings_data list
         holdings_data.append(holdings_data_row)

      # Save the holding data for the current record
      save_data(record, holdings_data)

   # Incrementing the records_scraped variable
   records_scraped += 1
   
   # if records are 25 then close the browser and save the data and again open the browser
   if records_scraped == 100:
      # Closing the driver 
      driver.quit()

      sleep(5) # Waiting for 5 seconds
      
      # Calling the botInitialization function to initialize the bot and storing the driver object in the driver variable
      driver = botInitialization()
      
      # Resetting the records_scraped variable
      records_scraped = 0

driver.quit() # Closing the driver

print("\n> Data saved successfully.\n")

# time in minutes
# print(f"Time Taken: {round((time.time() - start_time) / 60, 2)} minutes")
