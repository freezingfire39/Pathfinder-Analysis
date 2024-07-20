import json
import os
import csv
import argparse
import pandas as pd

def main(input_dir, output_dir, section_percent=0.6):
    industry_set = set()
    category_set = set()
    industry_fund_map = dict()
    industry_fund_agg_details = dict()
    industry_fund_agg = dict()
    for subdir in os.listdir(input_dir):
        sub = os.path.join(input_dir, subdir)
        # checking if it is a file
        ticker = subdir

        f = os.path.join(sub, "Background.csv")
        with open(f, encoding="utf8") as file:
            csvreader = csv.reader(file)
            header =next(csvreader)
            value = next(csvreader)
            category = value[4]
            category_set.add(category)

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
            if percentage_float > section_percent:
                industry_fund_map[ticker] = industry

            for row in csvreader:
                i = row[1]
                industry_set.add(i)

        f = os.path.join(sub, "sample_feature.csv")
        if not os.path.exists(f):
            continue
        df = pd.read_csv(f)
        latest_return = df['return'].iloc[-1]
        if industry_fund_agg_details.get(industry) == None:
            industry_fund_agg_details[industry] = {}

        industry_fund_agg_details[industry][ticker]= latest_return

    for k in industry_fund_agg_details.keys():
        returns = industry_fund_agg_details[k]
        avg = sum(returns.values())/len(returns)
        industry_fund_agg[k] = avg

    with open(f'{output_dir}/fund_agg_details.json', 'w',  encoding='utf-8') as json_file:
        json.dump(industry_fund_map, json_file, ensure_ascii=False)

    with open(f'{output_dir}/fund_agg.json', 'w',  encoding='utf-8') as json_file:
        json.dump(industry_fund_agg, json_file, ensure_ascii=False)

    with open(f'{output_dir}/fund_industry.json', 'w',  encoding='utf-8') as json_file:
        json.dump(industry_fund_map, json_file,ensure_ascii=False)

    industry_list = list(industry_set)
    with open(f'{output_dir}/industry_list.json', 'w',  encoding='utf-8') as json_file:
        json.dump(industry_list, json_file, ensure_ascii=False)

    category_list = list(category_set)
    with open(f'{output_dir}/category_list.json', 'w', encoding='utf-8') as json_file:
        json.dump(category_list, json_file, ensure_ascii=False)


if __name__ == '__main__':
    import argparse

    # Create the parser
    parser = argparse.ArgumentParser(description="Read an input file and write to an output file.")

    # Add arguments
    parser.add_argument('--input', type=str, help='The input file path')
    parser.add_argument('--output', type=str, help='The output file path')

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    input = args.input
    output = args.output
    main(input, output)
