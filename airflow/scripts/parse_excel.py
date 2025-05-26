import pandas as pd
import sys
from pathlib import Path

def parse_excel(input_path, output_path):
    df = pd.read_excel(input_path)
    output_path = Path(output_path)
    output_path.write_text(df.to_json(orient="records"), encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: parse_excel.py <input.xlsx> <output.json>")
        sys.exit(1)
    parse_excel(sys.argv[1], sys.argv[2])
