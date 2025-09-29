#!/usr/bin/env python3
"""
CSV to SQLite converter
Usage: python csv_to_sqlite.py <database_name> <csv_file>
"""

import csv
import sqlite3
import sys
import os

def main():
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python csv_to_sqlite.py <database_name> <csv_file>")
        sys.exit(1)
    
    db_name = sys.argv[1]
    csv_file = sys.argv[2]
    
    # Check if CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found.")
        sys.exit(1)
    
    try:
        # Read CSV file
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            # Use csv.Sniffer to detect delimiter
            sample = file.read(1024)
            file.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            
            reader = csv.reader(file, delimiter=delimiter)
            
            # Get header row (column names)
            headers = next(reader)
            
            # Read all data rows
            rows = list(reader)
        
        # Connect to SQLite database (creates if doesn't exist)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Create table name from CSV filename (remove extension)
        table_name = os.path.splitext(os.path.basename(csv_file))[0]
        
        # Drop table if it exists (to handle re-runs)
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        
        # Create table schema - assuming all columns are TEXT type
        columns_def = ", ".join([f"{col} TEXT" for col in headers])
        create_table_sql = f"CREATE TABLE {table_name} ({columns_def})"
        cursor.execute(create_table_sql)
        
        # Insert data
        placeholders = ", ".join(["?" for _ in headers])
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        
        cursor.executemany(insert_sql, rows)
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        print(f"Successfully converted '{csv_file}' to SQLite database '{db_name}'")
        print(f"Table '{table_name}' created with {len(rows)} rows")
        
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()