import csv
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

def parse_excel(input_path, output_path):
    logging.debug("Reading CSV file: %s", input_path)
    input_path = Path(input_path)
    with input_path.open(newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        if not rows:
            logging.error("CSV file is empty")
            sys.exit(1)
        data = rows[0]  # Assuming single row CSV as per example

    logging.debug("Successfully read CSV with keys: %s", list(data.keys()))

    output_path = Path(output_path)
    logging.debug("Writing INI config output to: %s", output_path)

    # Ensure parent directories exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open('w', encoding='utf-8') as cfgfile:
        cfgfile.write("[Collection]\n")
        for key, value in data.items():
            # Remove any surrounding quotes from value if present
            if value is None:
                value = ""
            else:
                value = value.strip('"')
            cfgfile.write(f"{key}={value}\n")

    logging.debug("INI config writing complete")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: parse_excel.py <input.csv> <output.cfg>")
        sys.exit(1)
    parse_excel(sys.argv[1], sys.argv[2])
