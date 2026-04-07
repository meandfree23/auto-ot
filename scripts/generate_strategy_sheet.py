import sys
import os
import json
import re
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def parse_md_tables(content):
    """
    Extract content from markdown tables.
    Matches | Col1 | Col2 |
            |------|------|
            | Cell | Cell |
    """
    tables = []
    # Identify table blocks
    table_regex = re.compile(r'(\|.*\|)\n(\|[- |:]+\|)\n((\|.*\|\n)+)', re.MULTILINE)
    matches = table_regex.finditer(content)
    
    for match in matches:
        header_row = match.group(1).strip('|').split('|')
        data_rows = match.group(3).strip().split('\n')
        
        table_data = []
        table_data.append([c.strip() for c in header_row])
        for row in data_rows:
            table_data.append([c.strip() for c in row.strip('|').split('|')])
        tables.append(table_data)
    
    return tables

def create_strategic_sheet(job_id):
    """
    Reconstruct the Strategic Sheets board generation script.
    """
    ROOT = Path(__file__).resolve().parents[1]
    input_file = ROOT / "outputs" / "02_deep_analysis" / f"{job_id}_deep_report.md"
    token_path = ROOT / "token.json"

    if not input_file.exists():
        print(f"Error: Input file {input_file} not found.")
        return False

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    tables = parse_md_tables(content)
    if not tables:
        print("No tables found in markdown.")
        # Create a dummy table if none found
        tables = [[["Strategic Proposal", "Priority", "Owner"], ["Action 1", "HIGH", "PM"]]]

    # Auth
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path))
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("Error: No valid credentials found. Run setup_auth.py first.")
            return False

    service = build("sheets", "v4", credentials=creds)
    
    # Create new sheet
    spreadsheet_body = {
        'properties': {
            'title': f"[STRATEGY BOARD] {job_id}"
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet_body, fields='spreadsheetId').execute()
    spreadsheet_id = spreadsheet.get('spreadsheetId')
    print(f"Created Strategic Sheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")

    # Populate with tables
    range_name = 'Sheet1!A1'
    # Combine tables for import
    all_data = []
    for t in tables:
        all_data.extend(t)
        all_data.append([]) # Spacer

    value_range_body = {
        'values': all_data
    }
    
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=value_range_body
    ).execute()

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_strategy_sheet.py <job_id>")
        sys.exit(1)
    create_strategic_sheet(sys.argv[1])
