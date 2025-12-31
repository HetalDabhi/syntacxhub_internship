import pandas as pd
import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def convert_csv_to_excel(input_file, output_file):
    try:
        logging.info("Reading CSV file...")
        df = pd.read_csv(input_file)

        
        logging.info("Handling missing values...")
        df.fillna("N/A", inplace=True)

        
        for col in df.columns:
            if "date" in col.lower():
                df[col] = pd.to_datetime(df[col], errors="coerce")

    
        rename_map = {
            "fname": "First Name",
            "lname": "Last Name"
        }
        df.rename(columns=rename_map, inplace=True)

        
        logging.info("Exporting to Excel...")
        df.to_excel(output_file, index=False, engine="openpyxl")

        logging.info("Conversion completed successfully!")
        logging.info(f"File saved at: {output_file}")

    except FileNotFoundError:
        logging.error("Input CSV file not found.")
        sys.exit(1)

    except pd.errors.EmptyDataError:
        logging.error("CSV file is empty or invalid.")
        sys.exit(1)

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)



def main():
    parser = argparse.ArgumentParser(
        description="CSV to Excel Converter using Pandas"
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to input CSV file"
    )

    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Path to output Excel file (.xlsx)"
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    convert_csv_to_excel(input_path, output_path)

if __name__ == "__main__":
    main()
