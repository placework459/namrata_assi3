import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=str, help="Path to the input CSV file")
    parser.add_argument("output_path", type=str, help="Path to the output CSV file")
    args = parser.parse_args()

    # Read the input file
    df = pd.read_csv(args.input_path)

    # Save the dataframe to the output file
    df.to_csv(args.output_path, index=False)

if __name__ == "__main__":
    main()
