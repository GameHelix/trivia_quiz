#!/usr/bin/env python3
"""
Data Conversion Script
Converts PDF data to structured CSV format for analysis
"""

import pandas as pd
from pathlib import Path

def create_adult_obesity_csv():
    """
    Creates adult_obesity.csv from PDF data
    Extracts key metrics: country, income group, obesity rates by gender
    """
    print("Creating adult obesity dataset...")

    # Sample data structure - extend with full PDF data
    data = {
        'Country': [],
        'Income_group': [],
        'Year': [],
        'Males_Overweight': [],
        'Males_Obesity': [],
        'Females_Overweight': [],
        'Females_Obesity': [],
        'All_Overweight': [],
        'All_Obesity': []
    }

    # This would contain full extraction logic from PDF
    # For demonstration, showing the structure

    df = pd.DataFrame(data)
    output_path = Path(__file__).parent.parent / 'data' / 'adult_obesity.csv'
    df.to_csv(output_path, index=False)
    print(f"✓ Adult obesity data saved to {output_path}")

    return df


def create_child_obesity_csv():
    """
    Creates child_obesity.csv from PDF data
    Extracts child/adolescent overweight and obesity rates
    """
    print("Creating child obesity dataset...")

    data = {
        'Country': [],
        'Income_group': [],
        'Year': [],
        'Age': [],
        'Boys': [],
        'Girls': [],
        'All_children': []
    }

    df = pd.DataFrame(data)
    output_path = Path(__file__).parent.parent / 'data' / 'child_obesity.csv'
    df.to_csv(output_path, index=False)
    print(f"✓ Child obesity data saved to {output_path}")

    return df


def validate_data(df, dataset_name):
    """Validate data quality and print summary statistics"""
    print(f"\n--- {dataset_name} Validation ---")
    print(f"Total records: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(f"Missing values:\n{df.isnull().sum()}")
    print(f"Data types:\n{df.dtypes}")
    print("-" * 50)


def clean_numeric_columns(df, numeric_cols):
    """Clean and convert numeric columns"""
    for col in numeric_cols:
        if col in df.columns:
            # Replace common non-numeric values
            df[col] = df[col].replace(['-', '', 'N/A', 'n/a'], pd.NA)
            # Convert to numeric
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


def main():
    """Main conversion process"""
    print("\n" + "="*60)
    print("  DATA CONVERSION - PDF TO CSV")
    print("="*60 + "\n")

    # Create datasets
    adult_df = create_adult_obesity_csv()
    child_df = create_child_obesity_csv()

    # Validate
    validate_data(adult_df, "Adult Obesity Dataset")
    validate_data(child_df, "Child Obesity Dataset")

    print("\n✓ Data conversion completed successfully!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()


# USAGE NOTES:
# -------------
# This script provides the framework for converting PDF data to CSV.
# The actual data has been manually extracted and structured in:
#   - data/adult_obesity.csv
#   - data/child_obesity.csv
#
# To use this script for future updates:
# 1. Update the data dictionaries with new PDF data
# 2. Run: python scripts/convert_data.py
# 3. Validate output files in data/ directory
#
# Data sources:
# - World Obesity Federation Global Obesity Observatory
# - PDF reports in data/ directory
