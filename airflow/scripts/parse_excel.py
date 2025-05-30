import pandas as pd
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

def parse_excel(input_path, output_path):
    logging.debug("Reading Excel file: %s", input_path)
    df = pd.read_excel(input_path)
    logging.debug("Successfully read %d rows", len(df))
    output_path = Path(output_path)
    logging.debug("Writing JSON output to: %s", output_path)
    output_path.write_text(df.to_json(orient="records"), encoding="utf-8")
    logging.debug("JSON writing complete")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: parse_excel.py <input.xlsx> <output.json>")
        sys.exit(1)
    parse_excel(sys.argv[1], sys.argv[2])
