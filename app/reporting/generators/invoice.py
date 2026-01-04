from .base import ReportGenerator
from typing import Dict, Any
import datetime

class InvoiceGenerator(ReportGenerator):
    def header(self, data: Dict[str, Any]) -> str:
        return f"INVOICE REPORT - {datetime.date.today()}\nType: {data.get('report_type')}\n" + "="*40

    def body(self, data: Dict[str, Any]) -> str:
        lines = ["\nDETAILS:"]
        if 'details' in data:
            for item in data['details']:
                lines.append(f" - Item: {item.get('name', 'Unknown')}, Qty: {item.get('quantity', 0)}, Val: ${item.get('value', 0):.2f}")
        elif 'summary' in data: # Handle historical if requested as invoice
            lines.append(f"Summary: {data['summary']}")
        return "\n".join(lines)

    def footer(self, data: Dict[str, Any]) -> str:
        total = data.get('total_value', 'N/A')
        return f"\n{'='*40}\nTOTAL DUE: ${total}\nEND OF INVOICE"
