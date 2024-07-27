import pandas as pd
import os


def merge_return_columns(folder_path, output_folder):
    # Initialize an empty DataFrame for merging
    merged_df = None

    # Iterate through each sub-folder
    count = 0
    for sub_folder in os.listdir(folder_path):
        count +=1
        sub_folder_path = os.path.join(folder_path, sub_folder)

        # Check if it is a directory
        if os.path.isdir(sub_folder_path):
            file_path = os.path.join(sub_folder_path, 'sample_feature.csv')

            # Check if the CSV file exists
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                df['timestamp'] = pd.to_datetime(df['净值日期'])
                # Extract only the 'timestamp' and 'return' columns
                df = df[['timestamp', 'return']]

                # Rename the 'return' column to include the sub-folder name
                df.rename(columns={'return': f'return_{sub_folder}'}, inplace=True)

                # Merge the DataFrame
                if merged_df is None:
                    merged_df = df
                else:
                    merged_df = pd.merge(merged_df, df, on='timestamp', how='outer')
        if count % 100 == 0:
            print(f'Processed {count} files')

    merged_df.to_csv(os.path.join(output_folder, 'merged_returns.csv'), index=False)


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