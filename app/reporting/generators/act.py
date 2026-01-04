from .base import ReportGenerator
from typing import Dict, Any
import datetime

class ActGenerator(ReportGenerator):
    def header(self, data: Dict[str, Any]) -> str:
        return f"OFFICIAL ACT - {datetime.date.today()}\nSubject: {data.get('report_type')}\n" + "-"*40

    def body(self, data: Dict[str, Any]) -> str:
        lines = ["\nFINDINGS:"]
        if 'details' in data:
             for item in data['details']:
                lines.append(f" [OK] {item.get('name')} (ID: {item.get('id')}) - Stock: {item.get('quantity')}")
        elif 'summary' in data:
            lines.append(f"Movement Summary: {data['summary']}")
        return "\n".join(lines)

    def footer(self, data: Dict[str, Any]) -> str:
        return f"\n{'-'*40}\nCertified by Warehouse Manager.\nSignature: _______________"
