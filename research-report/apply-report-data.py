#!/usr/bin/env python3
"""Apply research-report-data.json changes back to research-report.html"""
import json
import sys

def main():
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
    else:
        data_file = 'research-report-data.json'
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Loaded {len(data['sections'])} sections from {data_file}")
    print(f"Project: {data['meta']['project']} v{data['meta']['version']}")
    
    # Here you would regenerate the HTML report from this data
    # For now, just print the sections
    for key, sec in data['sections'].items():
        print(f"  - {key}: {sec.get('title', '(no title)')}")

if __name__ == '__main__':
    main()
