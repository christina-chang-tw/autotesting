from pathlib import Path
import csv

from argparse import ArgumentParser
import pandas as pd
import numpy as np

def convert(filepath: Path, sheet_name: str = None):
    if filepath.suffix == ".xlsx":
        # Convert excel to csv and make sure delimiter is ','
        with open(filepath, "rb", encoding="utf-8") as f:
            df = pd.read_excel(f, sheet_name=sheet_name).to_numpy()
        np.savetxt(filepath, df, delimiter=",")
        print("The excel file has been converted to the correct format csv.")
    

def main():
    parser = ArgumentParser(description="Convert excel file to csv file.")
    parser.add_argument("filepath", help="The filepath to convert.")
    parser.add_argument("-s", "--sheet", help="The sheet name to convert.", default=None)
    args = parser.parse_args()

    filepath = Path(args.filepath)
    convert(filepath, sheet_name=args.sheet)

if __name__ == "__main__":
    main()