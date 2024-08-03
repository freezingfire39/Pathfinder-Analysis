import json
import os
import csv
import argparse
import pandas as pd

import warnings

warnings.filterwarnings('ignore')

def asset_calc(input_dir, output_dir, year, quarter, section_percent=0.6):
    quarter = f'{year}Q{quarter}'
    industry_set = set()
    category_set = set()
    asset_fund_map = dict()
    asset_fund_agg_details = dict()
    asset_fund_agg = dict()
    for subdir in os.listdir(input_dir):
        sub = os.path.join(input_dir, subdir)
        # checking if it is a file
        ticker = subdir

        f = os.path.join(sub, "Industry.csv")
        if not os.path.exists(f):
            continue
        with open(f, encoding="utf8") as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            top = next(csvreader)
            industry = top[1]
            percentage_str = top[3]
            percentage_float = float(percentage_str.strip('%'))/100
            industry_set.add(industry)

            for row in csvreader:
                i = row[1]
                industry_set.add(i)

            if percentage_float > section_percent:
                asset_fund_map[ticker] = industry
            else:
                continue

        f = os.path.join(sub, 'Asset.csv')
        if not os.path.exists(f):
            continue
        df = pd.read_csv(f)
        df = df[~df['日期'].str.contains('说明')]
        df['日期'] = pd.to_datetime(df['日期'])

        # Extract the year and quarter from the date
        df['Year'] = df['日期'].dt.year
        df['Quarter'] = df['日期'].dt.to_period('Q')

        # Filter the data for the specified year
        df_year = df[df['Year'] == int(year)]
        df_year["asset"] = df_year['期末净资产（亿元）'].astype(float)
        # Group by quarter and calculate the average of the net assets
        quarterly_avg = df_year.groupby('Quarter')['asset'].mean().reset_index()
        df = quarterly_avg.set_index("Quarter")
        if quarter in df.index:
            asset = df.loc[quarter, 'asset']

            if asset_fund_agg_details.get(industry) == None:
                asset_fund_agg_details[industry] = {}

            asset_fund_agg_details[industry][ticker]= asset

    for k in asset_fund_agg_details.keys():
        assets = asset_fund_agg_details[k]
        sum_ = sum(assets.values())
        asset_fund_agg[k] = sum_

    output_dir = output_dir + '/' + ''.join(quarter)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(f'{output_dir}/asset_sum.json', 'w',  encoding='utf-8') as json_file:
        json.dump(asset_fund_agg, json_file, ensure_ascii=False)


if __name__ == '__main__':
    import argparse

    # Create the parser
    parser = argparse.ArgumentParser(description="Read an input file and write to an output file.")

    # Add arguments
    parser.add_argument('--input', type=str, help='The input file path')
    parser.add_argument('--output', type=str, help='The output file path')
    parser.add_argument('--year', type=str, help='start year')
    parser.add_argument('--quarter', type=str, help='quarter')
    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    input = args.input
    output = args.output
    year = args.year
    quarter = args.quarter
    asset_calc(input, output, year, quarter)
