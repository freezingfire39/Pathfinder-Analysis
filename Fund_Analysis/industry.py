import json
import os
import csv
import argparse

def main(input_dir, output_dir, section_percent=0.6):
    industry_set = set()
    category_set = set()
    industry_fund_map = dict()
    for subdir in os.listdir(input_dir):
        sub = os.path.join(input_dir, subdir)
        # checking if it is a file
        for filename in os.listdir(sub):
            f = os.path.join(sub, filename)
            ticker = filename
            if (filename=="Background.csv"):
                with open(f, encoding="utf8") as file:
                    csvreader = csv.reader(file)
                    header =next(csvreader)
                    value = next(csvreader)
                    category = value[4]
                    category_set.add(category)

            if (filename=="Industry.csv"):
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
                        industry = row[1]
                        industry_set.add(industry)

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
    parser.add_argument('input', type=str, help='The input file path')
    parser.add_argument('output', type=str, help='The output file path')

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    input = args.input
    output = args.output
    main(input, output)
