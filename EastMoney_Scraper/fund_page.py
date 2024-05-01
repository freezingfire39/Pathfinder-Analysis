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
from requests.adapters import HTTPAdapter # HTTPAdapter for retrying requests

# Define a function to parse dates in various formats
def parse_date(date_str):
   formats = ['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', '%d-%b-%Y']  # Add more formats as needed
   for fmt in formats:
      try:
         return datetime.strptime(date_str, fmt)
      except ValueError:
         pass
   raise ValueError(f"Could not parse date: {date_str}")

def make_request_with_retries(url, payload, headers, querystring, retries=100, retry_delay=5):
   """
   Make a request to the specified URL with retry logic.

   Args:
   - url (str): The URL to make the request to.
   - payload (dict): The payload to be sent with the request.
   - headers (dict): The headers to be sent with the request.
   - querystring (dict): The query string parameters for the request.
   - retries (int): Number of retries in case of failure. Default is 3.
   - retry_delay (int): Number of seconds to wait before each retry. Default is 5.

   Returns:
   - response (requests.Response or None): The response object if the request was successful, otherwise None.
   """
   session = requests.Session()

   for _ in range(retries):
      try:
         response = session.get(url, data=payload, headers=headers, params=querystring)
         response.raise_for_status()  # Check if the request was successful
         return response
      except requests.exceptions.RequestException as e:
         print("Request failed:", e)
         print(f"Retrying in {retry_delay} seconds...")
         sleep(retry_delay)

   # print("Request failed after retries.")
   return None

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

# Define a function to read data from the Fund_1.csv and Fund_2.csv files in the specified folders
def read_folder_data(folder_names):
   folder_data = {}
   
   for folder_name in folder_names:
      folder_path = os.path.join(os.getcwd(), folder_name)  # Assuming the folders are in the current working directory
      
      # Check if the folder exists
      if os.path.isdir(folder_path):
         fund_1_path = os.path.join(folder_path, 'Fund_1.csv')
         fund_2_path = os.path.join(folder_path, 'Fund_2.csv')
         
         # Check if fund_1.csv exists in the folder
         if os.path.exists(fund_1_path):
            with open(fund_1_path, 'r', newline='', encoding='utf-8-sig') as fund_1_file:
               fund_1_reader = csv.reader(fund_1_file)
               next(fund_1_reader)  # Skip header
               date = next(fund_1_reader)[0]  # Read date from the second row
            folder_data[folder_name] = date
            
         # Check if fund_2.csv exists in the folder
         elif os.path.exists(fund_2_path):
            with open(fund_2_path, 'r', newline='', encoding='utf-8-sig') as fund_2_file:
               fund_2_reader = csv.reader(fund_2_file)
               next(fund_2_reader)  # Skip header
               date = next(fund_2_reader)[0]  # Read date from the second row
            folder_data[folder_name] = date
            
   return folder_data

# Define a method to save data to CSV files based on the record and data provided 
def save_data(record, data, csv_name, first_time=False, date=""):
   # Save data into folder named after the record
   folder_name = os.path.join(os.path.dirname(__file__), record)

   # Save data to Fund_1.csv
   if csv_name == "Fund_1":
      if date == "":
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
      if date == "":
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

# Call the function scrape_records() to retrieve records
records = scrape_records()
# records = records[:1]  # Limiting the number of records to 5 for testing purposes

# Call the function create_folders() with the retrieved records and scrape_fund variable as arguments
create_folders(records)

# Example usage:
folder_names = records
fund_dates = read_folder_data(folder_names)
# print(fund_dates)

# Initialize a set to store processed records
processed_records = set()

try:
   # def scrape_records(record):
   for record in records:
      # Define URL for fund data API
      fund_url = "http://api.fund.eastmoney.com/f10/lsjz"

      payload = ""
      
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

      
      # response = requests.request("GET", fund_url, data=payload, headers=fund_headers, params=fund_querystring)

      # Make the request with retry logic
      response = make_request_with_retries(fund_url, payload, fund_headers, fund_querystring)

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
         
         break_loop = False

         # Loop through each page of data
         for current_page in range(1, total_pages + 1):
            print("> Scraping page", current_page, "for record", record)

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

            # response = requests.request("GET", fund_url, data=payload, headers=fund_headers, params=fund_querystring)

            # Make the request with retry logic
            response = make_request_with_retries(fund_url, payload, fund_headers, fund_querystring)

            # Get the date for the record from the fund_dates dictionary 
            try:
               date = fund_dates[record]
            except:
               date = ""

            # Check if save_data has been called for this record before
            if record not in processed_records:
               first_time = True
               # Add the record to the set
               processed_records.add(record)
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
            
            # Initialize list to store fund data
            fund_data = []
            
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

                  if date:
                     try:
                        date1_obj = datetime.strptime(净值日期, '%Y-%m-%d')
                        date2_obj = parse_date(date)

                        if date1_obj <= date2_obj:
                           break_loop = True
                           break
                     except Exception as e:
                        pass
                  else:
                     pass

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

               if fund_data:
                  save_data(record, fund_data, "Fund_1", first_time=first_time, date=date)

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

                  if date:
                     try:
                        date1_obj = datetime.strptime(净值日期, '%Y-%m-%d')
                        date2_obj = parse_date(date)
                        
                        if date1_obj <= date2_obj:
                           break_loop = True
                           break
                     except ValueError:
                        pass
                  else:
                     pass

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

               if fund_data:
                  save_data(record, fund_data, "Fund_2", first_time=first_time, date=date)

            if break_loop:
               break_loop = False
               # return
               break
            
      except KeyError as e:
         # logging.error(f"KeyError: {e}")
         continue
except Exception as e:
   pass
   # logging.error(f"Error: {e}")
   # input("Press Enter to continue...")


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

               try:
                  # Sort the data by the first column (assuming it's a date)
                  data = sorted(rows[1:], key=lambda x: parse_date(x[0]), reverse=True)
               except Exception as e:
                  data
                  # print(f"Error: {e}")

               # print(data)
               
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
print("\n\n> Data Scraping completed successfully!\n\n")