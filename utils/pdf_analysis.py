# pdf_analysis.py
import pdfplumber

def analyze_pdf(pdf_path):
    crime_data = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Example parsing logic: count mentions of locations and crime types
                locations = ["City1", "City2", "City3"]  # Replace with actual locations
                for location in locations:
                    if location in text:
                        crime_data[location] = crime_data.get(location, 0) + 1
    return crime_data
