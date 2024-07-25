from fastapi import FastAPI, HTTPException
from typing import List
import csv
import re

app = FastAPI()


def search_in_csv(file_path: str, search_term: str) -> List[str]:
    results = []
    pattern = re.compile(search_term, re.IGNORECASE)
    try:
        with open(file_path, mode='r', newline='') as file:
            csv_reader = csv.reader(file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            header = next(csv_reader)
            for row in csv_reader:
                if any(pattern.search(field) for field in row):
                    results.append(row[0])  # Append only the first column
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found")
    return results


@app.get("/search", response_model=List[str])
def search_csv(search_term: str):
    file_path = 'data/quotes.csv'
    results = search_in_csv(file_path, search_term)
    if not results:
        raise HTTPException(status_code=404, detail="No matching rows found")
    return results