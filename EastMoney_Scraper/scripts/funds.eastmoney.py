# Import necessary modules
import scrapy  # Scrapy is a web crawling and web scraping framework
from scrapy.crawler import CrawlerProcess  # CrawlerProcess is a class to control the crawling process
import requests  # Requests module is used to send HTTP requests
from scrapy import Selector  # Selector is used to extract data from HTML/XML documents
import csv  # CSV module for handling CSV files
import os  # OS module provides functions for interacting with the operating system
import json  # JSON module for handling JSON data
import concurrent.futures # Concurrent futures module for parallel execution of tasks
from datetime import datetime # Datetime module for handling date and time
import logging # Logging module for logging errors and messages
from time import sleep # Sleep function to pause the execution of the program
from pathlib import Path
home = str(Path.home())
# Record the starting time of the program
# start_time = time.time()

# Function to take input from the user regarding whether to scrape data from a CSV file.
def take_input(csv_name):
   # Loop until valid input is provided by the user.
   while True:
      # Prompt the user to enter 'y' or 'n' to indicate their choice.
      # word = input(f"> Scrape {csv_name}.csv? (y/n): ")
      word = "y"
      # Check if the input is either 'y' or 'n'.
      if word.lower() == "y" or word.lower() == "n":
         # Break the loop if the input is valid.
         break
      else:
         # Inform the user about invalid input and prompt again.
         print("Invalid input. Please enter 'y' or 'n'.")

   # Return the lowercase version of the valid input.
   return word.lower()

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
   print("> Starting scraping process...\n")
   sleep(2) # Pause for 2 seconds

print("\n\n")
# Take user input for whether to scrape fund data
scrape_fund = take_input("Fund")

# Take user input for whether to scrape background data
scrape_background = take_input("Background")

# Take user input for whether to scrape industry data
scrape_industry = take_input("Industry")

# scrape_fund = "y"
# scrape_background = "y"
# scrape_industry = "y"

# Call the function scrape_records() to retrieve records
records = scrape_records()
# records = records[:20]  # Limiting the number of records to 5 for testing purposes

# Call the function create_folders() with the retrieved records and scrape_fund variable as arguments
create_folders(records)

# # Configure logging
# logging.basicConfig(
#    filename='scrapy_errors.log',  # Specify the file to save logs
#    format='%(asctime)s [%(levelname)s] %(message)s',
#    level=logging.ERROR  # Set the logging level to ERROR or higher
# )

# Define a class named scrapySpider which inherits from scrapy.Spider
class scrapySpider(scrapy.Spider):
   # Define the name of the spider 
   name = "scrapySpider"

   # Define custom settings for the spider
   custom_settings = {
      "DUPEFILTER_CLASS": "scrapy.dupefilters.BaseDupeFilter",  # Disable default duplicate filter
      "RETRY_TIMES": 50,  # Retry failed requests 20 times
   }

   # Initialize an empty set to keep track of records for which save_data has been called
   processed_records = set()

   # Define a method to initiate requests to scrape fund data
   def start_requests(self):
      try:
         # Iterate over records
         for record in records:
            # Check if user has chosen to scrape fund data, if yes, proceed with scraping
            if scrape_fund == "y":
                  # Define URL for fund data API
                  fund_url = "http://api.fund.eastmoney.com/f10/lsjz"
                  
                  # Define query parameters for fund data API
                  fund_querystring = {
                     "fundCode": f"{record}", # Use the current record as the fund code
                     "pageIndex": "1", # Start from page 1
                     "pageSize": "20" # Set the page size to 20
                  }
                  
                  # Define headers for the HTTP request to fund data API
                  fund_headers = {
                     "Accept": "*/*",
                     "Accept-Language": "en-US,en;q=0.9,so;q=0.8",
                     "Connection": "keep-alive",
                     "Referer": "http://fundf10.eastmoney.com/",
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                  }
                  
                  # Construct full URL for the fund data API request
                  fund_full_url = f"{fund_url}?{'&'.join(f'{k}={v}' for k, v in fund_querystring.items())}"
                  
                  # Yield a Scrapy Request object
                  yield scrapy.Request(
                     url = fund_full_url, # Set the URL for the request
                     method = "GET", # Use the GET method, as we are retrieving data from the API
                     headers = fund_headers, # Pass the headers to the request
                     meta = {"record": record},  # Pass record metadata to the callback function
                     callback = self.parse_fund_TotalCount, # Set the callback function to parse_fund_TotalCount method
                  )

            # Check if user has chosen to scrape background, if yes, proceed with scraping
            if scrape_background == "y":
               # Define URL for background data API
               background_url = f"http://fundf10.eastmoney.com/jbgk_{record}.html"

               # Define headers for the HTTP request to background data API
               background_headers = {
                  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                  "Accept-Language": "en-US,en;q=0.9,so;q=0.8",
                  "Cache-Control": "max-age=0",
                  "Connection": "keep-alive",
                  "Upgrade-Insecure-Requests": "1",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
               }
               
               # Yield a Scrapy Request object
               yield scrapy.Request(
                  url = background_url, # Set the URL for the request
                  method = "GET", # Use the GET method, as we are retrieving data from the API
                  headers = background_headers, # Pass the headers to the request
                  meta = {"record": record}, # Pass record metadata to the callback function
                  callback = self.parse_background # Set the callback function to parse_background method
               )

            # Check if user has chosen to scrape industry, if yes, proceed with scraping
            if scrape_industry == "y":
               # Define URL for industry data API
               industry_url = "http://api.fund.eastmoney.com/f10/HYPZ"

               # Define query parameters for industry data API
               industry_querystring = {
                  "fundCode":f"{record}", # Use the current record as the fund code
                  "year":"", # Set year to empty string
                  "callback":"", # Set callback to empty string
                  "_":"" # Set _ to empty string
               }

               # Define headers for the HTTP request to industry data API
               headers = {
                  "Accept": "*/*",
                  "Accept-Language": "en-US,en;q=0.9,so;q=0.8",
                  "Connection": "keep-alive",
                  "Referer": "http://fundf10.eastmoney.com/",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
               }

               # Construct full URL for the industry data API request
               full_industry_url = f"{industry_url}?{'&'.join(f'{k}={v}' for k, v in industry_querystring.items())}"
               
               # Yield a Scrapy Request object
               yield scrapy.Request(
                  url = full_industry_url, # Set the URL for the request
                  method = "GET", # Use the GET method, as we are retrieving data from the API
                  headers = headers, # Pass the headers to the request
                  dont_filter = True, # Disable default duplicate filter
                  meta={"record": record}, # Pass record metadata to the callback function
                  callback=self.parse_industry, # Set the callback function to parse_industry method
               )
      except Exception as e:
         logging.error(f"An error occurred: {e}")

   # Define a method to determine the number of pages
   def parse_fund_TotalCount(self, response):
      # Extract metadata from the response object
      record = response.meta['record']

      # Parse the JSON string
      data = json.loads(response.text)

      # Table check
      first_table = True
      second_table = False
      
      try:
         jzzzl_values = [] # Initialize list to store JZZZL values
         data_rows = data["Data"]["LSJZList"] # Extract data rows from the JSON data
         
         # Extract JZZZL values from the data rows
         for row in data_rows:
            jzzzl_value = row["JZZZL"]
            jzzzl_values.append(jzzzl_value)

         # Check if all values in jzzzl_values are "0.00" to determine the table to parse
         if all(value == "0.00" for value in jzzzl_values):
            # print("Second Table for this record:", record)
            first_table = False
            second_table = True
         else:
            # print("First Table for this record:", record)
            first_table = True
            second_table = False
      
         # Extract the TotalCount value
         total_count = data["TotalCount"]

         # Divide TotalCount by the page size and round up to get the number of pages
         total_pages = -(-total_count // data["PageSize"])
         
         # Loop through each page of data
         for current_page in range(1, total_pages + 1):
            # Define the base URL for the fund data
            fund_url = "http://api.fund.eastmoney.com/f10/lsjz"

            # Construct the query string parameters for the request
            fund_querystring = {"fundCode": f"{record}", "pageIndex": f"{current_page}", "pageSize": "20"}

            # Define the headers for the request
            fund_headers = {
               "Accept": "*/*",
               "Accept-Language": "en-US,en;q=0.9,so;q=0.8",
               "Connection": "keep-alive",
               "Referer": "http://fundf10.eastmoney.com/",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            }

            # Construct the full URL with query string parameters
            fund_full_url = f"{fund_url}?{'&'.join(f'{k}={v}' for k, v in fund_querystring.items())}"

            # Send a request to fetch fund data for the current page
            yield scrapy.Request(
               url = fund_full_url, # Set the URL for the request
               method = "GET", # Use the GET method, as we are retrieving data from the API
               headers = fund_headers, # Pass the headers
               meta = {"record": record, "total_pages": total_pages, "current_page": current_page, "first_table": first_table, "second_table": second_table}, # Pass metadata to the callback function
               callback=self.parse_fund, # Set the callback function to parse_fund method
            )
      except:
         pass

   # Define a method to parse fund data for a specific record and save it to a CSV file
   def parse_fund(self, response):
      # Extract metadata from the response object
      record = response.meta['record']
      # total_pages = response.meta['total_pages']
      # current_page = response.meta['current_page']

      # Extract first_table and second_table from the response metadata
      first_table = response.meta['first_table'] 
      second_table = response.meta['second_table'] 

      # Check if save_data has been called for this record before
      if record not in self.processed_records:
         first_time = True
         # Add the record to the set
         self.processed_records.add(record)
      else:
         first_time = False

      # Initialize variables to store fund data
      净值日期 = ""
      单位净值 = ""
      累计净值 = ""
      日增长率 = ""
      申购状态 = ""
      赎回状态 = ""
      分红送配 = ""
      
      fund_data = [] # Initialize list to store fund data
      # Check if first_table exists
      if first_table:
         # Parse JSON data from the response
         data = json.loads(response.text)
         
         # Extract data rows from the JSON data
         data_rows = data["Data"]["LSJZList"]
         
         # Loop through each row in the data
         for row in data_rows:
            # Extract relevant information from the row
            净值日期 = row["FSRQ"]
            单位净值 = row["DWJZ"]
            累计净值 = row["LJJZ"]
            日增长率 = row["JZZZL"]
            
            # Check if 日增长率 exists and format it
            if 日增长率:
                  日增长率 = 日增长率 + "%"
            
            申购状态 = row["SGZT"]
            赎回状态 = row["SHZT"]
            分红送配 = row["FHSP"]

            # Print the values
            # print("-----------------------------------")
            # print("净值日期:", 净值日期)
            # print("单位净值:", 单位净值)
            # print("累计净值:", 累计净值)
            # print("日增长率:", 日增长率)
            # print("申购状态:", 申购状态)
            # print("赎回状态:", 赎回状态)
            # print("分红送配:", 分红送配)
            # print("-----------------------------------")

            # Create a dictionary to store fund data for a single row
            fund_data_row = {
               "净值日期": 净值日期,
               "单位净值": 单位净值,
               "累计净值": 累计净值,
               "日增长率": 日增长率,
               "申购状态": 申购状态,
               "赎回状态": 赎回状态,
               "分红送配": 分红送配
            }

            # Append the fund data row to the fund_data list
            fund_data.append(fund_data_row)

         # Log the parsing of fund_1 table for a specific record
         self.logger.info(f"Parsing fund_1 table for record: {response.meta['record']}")
         
         if fund_data:
            # Save fund data
            self.save_data(record, fund_data, csv_name="Fund_1", first_time=first_time)


      # Initialize variables to store fund data
      净值日期 = ""
      每万份收益 = ""
      日年化收益率 = ""
      申购状态 = ""
      赎回状态 = ""
      分红送配 = ""

      fund_data = [] # Initialize list to store fund data
      # Check if second_table exists
      if second_table:
         # Parse JSON data from the response
         data = json.loads(response.text)
         
         # Extract data rows from the JSON data
         data_rows = data["Data"]["LSJZList"]
         
         # Loop through each row in the data
         for row in data_rows:
            # Extract relevant information from the row
            净值日期 = row["FSRQ"]
            每万份收益 = row["DWJZ"]
            日年化收益率 = row["LJJZ"]
            
            # Check if 日年化收益率 exists and format it
            if 日年化收益率:
               日年化收益率 = 日年化收益率 + "%"
            
            申购状态 = row["SGZT"]
            赎回状态 = row["SHZT"]
            分红送配 = row["FHSP"]


            # print("-----------------------------------")
            # print("净值日期:", 净值日期)
            # print("每万份收益:", 每万份收益)
            # print("日年化收益率:", 日年化收益率)
            # print("申购状态:", 申购状态)
            # print("赎回状态:", 赎回状态)
            # print("分红送配:", 分红送配)
            # print("-----------------------------------")

            # Create a dictionary to store fund data for a single row
            fund_data_row = {
               "净值日期": 净值日期,
               "每万份收益": 每万份收益,
               "7日年化收益率（%）": 日年化收益率,
               "申购状态": 申购状态,
               "赎回状态": 赎回状态,
               "分红送配": 分红送配
            }

            # Append the fund data row to the fund_data list
            fund_data.append(fund_data_row)

         # Log the parsing of fund_2 table for a specific record
         self.logger.info(f"Parsing fund_2 table for record: {response.meta['record']}")

         # Check if fund data exists
         if fund_data:
            # Save fund data
            self.save_data(record, fund_data, csv_name="Fund_2", first_time=first_time)

   # Define a method to parse background data for a specific record and save it to a CSV file
   def parse_background(self, response):
      # Extract the record from the response metadata
      record = response.meta['record']

      # Initialize variables to store background data
      基金简称 = ""
      基金代码 = ""
      管理费率 = ""
      托管费率 = ""
      基金类型 = ""
      发行日期 = ""
      资产规模 = ""
      基金管理人 = ""
      基金经理人 = ""
      基金托管人 = ""

      # Extracting data rows from the HTML response
      data_rows = response.xpath('//div[@class="detail"]/div/div/div[@class="box"]/table/tr')

      # Loop through each row to extract data
      for row in data_rows:
         # Extract headings from th elements in the row
         headings = row.xpath('.//th/text()').extract()
         headings = [heading.strip() for heading in headings]

         # Extract values from td elements in the row
         values = row.xpath('.//td/text() | .//td/a/text()').extract()
         values = [value.strip() for value in values]

         # Assign values to variables based on headings
         for heading, value in zip(headings, values):
            if heading == "基金简称":
               基金简称 = value
            if heading == "基金代码":
               基金代码 = value
            if heading == "管理费率":
               管理费率 = value
            if heading == "托管费率":
               托管费率 = value
            if heading == "基金类型":
               基金类型 = value
            if heading == "发行日期":
               发行日期 = value
            if heading == "资产规模":
               资产规模 = value
            if heading == "基金管理人":
               基金管理人 = value
            if heading == "基金经理人":
               基金经理人 = value
            if heading == "基金托管人":
               基金托管人 = value
      
      # Print the values
      # print("--------------------------------------------")
      # print("基金简称:", 基金简称)
      # print("基金代码:", 基金代码)
      # print("管理费率:", 管理费率)
      # print("托管费率:", 托管费率)
      # print("基金类型:", 基金类型)
      # print("发行日期:", 发行日期)
      # print("资产规模:", 资产规模)
      # print("基金管理人:", 基金管理人)
      # print("基金经理人:", 基金经理人)
      # print("基金托管人:", 基金托管人)
      # print("--------------------------------------------")

      # Create a dictionary to store background data
      background_data = {
         "基金简称": 基金简称,
         "基金代码": 基金代码,
         "管理费率": 管理费率,
         "托管费率": 托管费率,
         "基金类型": 基金类型,
         "发行日期": 发行日期,
         "资产规模": 资产规模,
         "基金管理人": 基金管理人,
         "基金经理人": 基金经理人,
         "基金托管人": 基金托管人
      }

      # Log the parsing of background data for a specific record
      self.logger.info(f"Parsing background for record: {response.meta['record']}")

      # Check if background data exists
      if background_data:
         # Save background data
         self.save_data(record, background_data, csv_name="Background")
   
   # Define a method to parse industry data for a specific record and save it to a CSV file
   def parse_industry(self, response):
      # Extract the record from the response metadata
      record = response.meta['record']
      
      # Initialize variables to store industry data
      序号 = ""
      行业类别 = ""
      行业变动详情 = "变动详情"
      占净值比例 = ""
      市值 = ""
      行业市盈率 = ""

      # Parse the JSON string
      data = json.loads(response.text)

      first_quarter_info = ""
      try:
         # Access the first object in QuarterInfos
         first_quarter_info = data["Data"]["QuarterInfos"][0]
      except:
         # print("No data found for this record:", record)
         pass

      count = 1 # Initialize count for serial number
      industry_data = [] # Initialize list to store industry data
      if first_quarter_info:
         # Iterate over HYPZInfo objects and get SZDesc
         for hypz_info in first_quarter_info["HYPZInfo"]:
            # Assign values to variables
            序号 = count
            行业类别 = hypz_info["HYMC"]
            占净值比例 = hypz_info["ZJZBLDesc"]
            市值 = hypz_info["SZDesc"]

            # Print the values
            # print("--------------------------------------------")
            # print("序号:", 序号)
            # print("行业类别:", 行业类别)
            # print("行业变动详情:", 行业变动详情)
            # print("占净值比例:", 占净值比例)
            # print("市值（万元）:", 市值)
            # print("行业市盈率:", 行业市盈率)
            # print("--------------------------------------------")

            # Create a dictionary to store industry data for a single row
            industry_data_row = {
               "序号": 序号,
               "行业类别": 行业类别,
               "行业变动详情": 行业变动详情,  # Assuming this variable is defined elsewhere
               "占净值比例": 占净值比例,
               "市值（万元）": 市值,
               "行业市盈率": 行业市盈率  # Assuming this variable is defined elsewhere
            }

            # Append the industry data row to the industry_data list
            industry_data.append(industry_data_row)

            # Increment count for the next iteration
            count += 1
 
      # Log the parsing of industry for a specific record
      self.logger.info(f"Parsing industry for record: {response.meta['record']}")

      # Check if there is industry data available
      if industry_data:
         # Save industry data
         self.save_data(record, industry_data, csv_name="Industry")


   # Define a method to save data to CSV files based on the record and data provided 
   def save_data(self, record, data, csv_name, first_time=False):
      # Save data into folder named after the record
      # outputPath = home + "/Desktop/output_china"
      folder_name = os.path.join(os.path.dirname(__file__), record)
      # folder_name = os.path.join(outputPath, record)

      # Save data to Fund_1.csv
      if csv_name == "Fund_1":
         if first_time:
            # Create and open Fund_1.csv for writing with UTF-8 encoding 
            fund_1_csv = open(f'{folder_name}/Fund_1.csv', 'w', newline='', encoding="utf-8-sig")
            
            # Define field names for Fund_1.csv
            fund_1_fields = ['净值日期', '单位净值', '累计净值', '日增长率', '申购状态', '赎回状态', '分红送配']
            
            # Create a CSV writer object for Fund_1.csv
            fund_1_writer = csv.DictWriter(fund_1_csv, fieldnames=fund_1_fields)
            
            # Write header row to Fund_1.csv
            fund_1_writer.writeheader()
            
            # Close Fund_1.csv file
            fund_1_csv.close()

         # Open Fund_1.csv for appending data with UTF-8 encoding
         fund_1_csv = open(f'{folder_name}/{csv_name}.csv', 'a', newline='', encoding="utf-8-sig")

         # Create a CSV writer object for Fund_1.csv
         fund_1_writer = csv.DictWriter(fund_1_csv, fieldnames=data[0].keys())

         # Write data to Fund_1.csv
         for data_row in data:
            fund_1_writer.writerow(data_row)

         # Close Fund_1.csv file
         fund_1_csv.close()

      # Save data to Fund_2.csv
      if csv_name == "Fund_2":
         if first_time:
            # Create and open Fund_2.csv for writing with UTF-8 encoding
            fund_2_csv = open(f'{folder_name}/Fund_2.csv', 'w', newline='', encoding="utf-8-sig")
            
            # Define field names for Fund_2.csv
            fund_2_fields = ['净值日期', '每万份收益', '7日年化收益率（%）', '申购状态', '赎回状态', '分红送配']
            
            # Create a CSV writer object for Fund_2.csv
            fund_2_writer = csv.DictWriter(fund_2_csv, fieldnames=fund_2_fields)
            
            # Write header row to Fund_2.csv
            fund_2_writer.writeheader()
            
            # Close Fund_2.csv file
            fund_2_csv.close()
            
         # Open Fund_2.csv for appending data with UTF-8 encoding
         fund_2_csv = open(f'{folder_name}/{csv_name}.csv', 'a', newline='', encoding="utf-8-sig")

         # Create a CSV writer object for Fund_2.csv
         fund_2_writer = csv.DictWriter(fund_2_csv, fieldnames=data[0].keys())

         # Write data to Fund_2.csv
         for data_row in data:
            fund_2_writer.writerow(data_row)
         
         # Close Fund_2.csv file
         fund_2_csv.close()

      # Save data to Background.csv
      if csv_name == "Background":
         background_csv = open(f'{folder_name}/{csv_name}.csv', 'w', newline='', encoding="utf-8-sig")
         background_field_names = ['基金简称', '基金代码', '管理费率', '托管费率', '基金类型', '发行日期', '资产规模', '基金管理人', '基金经理人', '基金托管人']
         background_writer = csv.DictWriter(background_csv, fieldnames=background_field_names)
         
         # Write header row to Background.csv
         background_writer.writeheader()

         # Write data to Background.csv
         background_writer.writerow(data)
         
         # Close Background.csv file
         background_csv.close()

      # Save data to Industry.csv
      if csv_name == "Industry":
         industry_csv = open(f'{folder_name}/{csv_name}.csv', 'w', newline='', encoding="utf-8-sig")
         industry_field_names = ['序号', '行业类别', '行业变动详情', '占净值比例', '市值（万元）', '行业市盈率']
         industry_writer = csv.DictWriter(industry_csv, fieldnames=industry_field_names)
         
         # Write header row to Industry.csv
         industry_writer.writeheader()

         # Write data to Industry.csv
         for data_row in data:
            industry_writer.writerow(data_row)
         
         # Close Industry.csv file
         industry_csv.close()

process = CrawlerProcess() # Create a CrawlerProcess object
process.crawl(scrapySpider) # Pass the scrapySpider class to the crawl method
process.start() # Start the crawling process

# process_csv_time = time.time() # Get the current time

# Define a function to process each folder
def process_folder(folder):
   """
   Process each folder by iterating through its contents and performing
   operations on 'Fund_1.csv' and 'Fund_2.csv' files.
   
   Parameters:
      folder (str): Path of the folder to be processed.
   """
   for file_name in os.listdir(folder):
      # Check if the file is either 'Fund_1.csv' or 'Fund_2.csv'
      if file_name == 'Fund_1.csv' or file_name == 'Fund_2.csv':
         # Construct the full path of the CSV file
         file_path = os.path.join(folder, file_name)
         
         # Open the CSV file
         with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file) # Create a CSV reader object
            rows = list(reader) # Read all rows from the CSV file
            
            # Check if there is data in the CSV file
            if len(rows) > 1:
               # Extract the header row
               header = rows[0]
               
               # Sort the data by the first column (assuming it's a date)
               data = sorted(rows[1:], key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'), reverse=True)
               
               # Write the sorted data back to the CSV file
               with open(file_path, 'w', newline='', encoding='utf-8-sig') as new_file:
                  writer = csv.writer(new_file) # Create a CSV writer object
                  writer.writerow(header) # Write the header row
                  writer.writerows(data) # Write the sorted data

# Define the main function
def main():
   # Get a list of all folders in the current directory
   folders = [folder for folder in os.listdir() if os.path.isdir(folder)]
   
   # Process folders concurrently using ThreadPoolExecutor
   with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
      executor.map(process_folder, folders)

# Call the main function
if __name__ == "__main__":
   main()

# Print a message indicating the completion of the data processing
print("\n\n > Data Scraping completed successfully!\n\n")

# time in minutes
# print(f"Time Taken: {round((time.time() - start_time) / 60, 2)} minutes")
# print(f"Time Taken to process CSV files: {round((time.time() - process_csv_time) / 60, 2)} minutes")