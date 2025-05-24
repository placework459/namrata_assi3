import argparse
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
import yaml

def main():
    # Setup argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=str, help="Path to the input CSV file")
    parser.add_argument("output_path", type=str, help="Path to the output model file")
    parser.add_argument("metrics_path", type=str, help="Path to the metrics file")
    args = parser.parse_args()

    # Load parameters from params.yml
    with open("params.yml", "r") as f:
        params = yaml.safe_load(f)

    # Load the dataset
    df = pd.read_csv(args.input_path)

    # Extract features and target from params
    feature = params["train"]["features"]
    target = params["train"]["target"]  # Fixed the typo here, changed "tarin" to "train"

    # Split the dataset into features (X) and target (y)
    x = df[feature]
    y = df[target]

    # Initialize and train the model
    model = LinearRegression()
    model.fit(x, y)

    # Save the trained model to the output path
    with open(args.output_path, "wb") as f:
        pickle.dump(model, f)

    # Save the R-squared score to the metrics path
    with open(args.metrics_path, "w") as f:
        f.write(f"R-squared: {model.score(x, y)}")

if __name__ == "__main__":
    main()
