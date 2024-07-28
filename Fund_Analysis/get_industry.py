import pandas as pd
import os
import csv

def merge_return_columns(folder_path, output_folder, section_percent=0.6):
    # Initialize an empty DataFrame for merging
    combined_df = pd.DataFrame(columns=["symbol", "industry"])

    # Iterate through each sub-folder
    rows = []
    for sub_folder in os.listdir(folder_path):
        sub_folder_path = os.path.join(folder_path, sub_folder)

        # Check if it is a directory
        if os.path.isdir(sub_folder_path):
            # Path to the industry information file (assuming it's named industry_info.csv)
            industry_info_path = os.path.join(sub_folder_path, 'Industry.csv')
            symbol = sub_folder
            # Check if both CSV files exist
            if os.path.exists(industry_info_path):
                with open(industry_info_path, encoding="utf8") as file:
                    csvreader = csv.reader(file)
                    _ = next(csvreader)
                    top = next(csvreader)
                    industry = top[1]
                    percentage_str = top[3]
                    percentage_float = float(percentage_str.strip('%')) / 100
                    if percentage_float > section_percent:
                        row = {"ticker":symbol,"industry": industry }
                        rows.append(row)

    combined_df =pd.DataFrame( rows)
    combined_df.to_csv(os.path.join(output_folder, 'all_industry.csv'), index=False)


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
    merge_return_columns(input, output)