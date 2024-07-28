import pandas as pd
import os


def split_by_year_and_save(input_folder):
    # Iterate through each sub-folder
    for sub_folder in os.listdir(input_folder):
        sub_folder_path = os.path.join(input_folder, sub_folder)

        if os.path.isdir(sub_folder_path):
            # Path to the sample_features.csv file
            features_path = os.path.join(sub_folder_path, 'sample_feature.csv')

            # Check if the CSV file exists
            if os.path.exists(features_path):
                # Read the sample_features.csv
                df = pd.read_csv(features_path)

                # Ensure the timestamp column is parsed as datetime
                df['timestamp'] = pd.to_datetime(df['净值日期'])

                # Create a new directory to save the split files
                output_dir = os.path.join(sub_folder_path, 'split_by_year')
                os.makedirs(output_dir, exist_ok=True)

                # Split the DataFrame by year and save each year's data to a separate file
                for year, year_df in df.groupby(df['timestamp'].dt.year):
                    year_file_path = os.path.join(output_dir, f'sample_features_{year}.csv')
                    year_df.to_csv(year_file_path, index=False)
                    print(f'Saved {year_file_path}')


# Provide the path to the folder containing the symbol folders
if __name__ == '__main__':
    import argparse

    # Create the parser
    parser = argparse.ArgumentParser(description="Read an input file and write to an output file.")

    # Add arguments
    parser.add_argument('--input', type=str, help='The input file path')
    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    input = args.input

    split_by_year_and_save(input)
