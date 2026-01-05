from abc import ABC, abstractmethod
from typing import Dict, Any
import datetime

class ReportGenerator(ABC):
    def generate_file(self, data: Dict[str, Any], date: datetime.date) -> str:
        """Template method for generating an HTML report file."""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WMS Report - {date}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', Arial, sans-serif;
            background: #f5f5f5;
            padding: 2rem;
            color: #333;
        }}
        
        .report-container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 3rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
        }}
        
        .print-btn {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #007bff;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            transition: background 0.2s;
        }}
        
        .print-btn:hover {{
            background: #0056b3;
        }}
        
        h1 {{
            color: #1a1a1a;
            font-size: 28px;
            margin-bottom: 0.5rem;
        }}
        
        h2 {{
            color: #555;
            font-size: 20px;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        
        .doc-header {{
            border-bottom: 3px solid #007bff;
            padding-bottom: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .doc-title {{
            font-size: 14px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }}
        
        .doc-info {{
            display: flex;
            justify-content: space-between;
            margin-top: 1rem;
            font-size: 14px;
            color: #666;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }}
        
        thead {{
            background: #f8f9fa;
        }}
        
        th {{
            text-align: left;
            padding: 1rem;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #dee2e6;
        }}
        
        td {{
            padding: 0.85rem 1rem;
            border-bottom: 1px solid #e9ecef;
        }}
        
        tbody tr:hover {{
            background: #f8f9fa;
        }}
        
        .total-row {{
            background: #e9ecef;
            font-weight: 700;
            font-size: 18px;
        }}
        
        .total-row td {{
            padding: 1.25rem 1rem;
            border-top: 2px solid #dee2e6;
            border-bottom: 2px solid #dee2e6;
        }}
        
        .footer {{
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #dee2e6;
        }}
        
        .signature {{
            margin-top: 3rem;
            padding-top: 1rem;
        }}
        
        .signature-line {{
            border-top: 2px solid #333;
            width: 250px;
            margin-top: 3rem;
        }}
        
        .text-right {{
            text-align: right;
        }}
        
        .text-center {{
            text-align: center;
        }}
        
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: #28a745;
            color: white;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .report-container {{
                box-shadow: none;
                padding: 0;
            }}
            
            .print-btn {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <button class="print-btn" onclick="window.print()">🖨️ Print Report</button>
    <div class="report-container">
        {self.header(data, date)}
        {self.body(data)}
        {self.footer(data)}
    </div>
</body>
</html>
"""

    @abstractmethod
    def header(self, data: Dict[str, Any], date: datetime.date) -> str:
        pass

    @abstractmethod
    def body(self, data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def footer(self, data: Dict[str, Any]) -> str:
        pass
