from .base import ReportGenerator
from typing import Dict, Any
import datetime

class InvoiceGenerator(ReportGenerator):
    def header(self, data: Dict[str, Any], date: datetime.date) -> str:
        report_type = data.get('report_type', 'Inventory Report')
        return f"""
        <div class="doc-header">
            <div class="doc-title">Warehouse Management System</div>
            <h1>Invoice Report</h1>
            <div class="doc-info">
                <span><strong>Report Type:</strong> {report_type}</span>
                <span><strong>Date of Issue:</strong> {date}</span>
            </div>
        </div>
        """

    def body(self, data: Dict[str, Any]) -> str:
        html = '<h2>Details</h2>'
        
        if 'details' in data:
            html += """
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Product Name</th>
                        <th class="text-right">Quantity</th>
                        <th class="text-right">Unit Price</th>
                        <th class="text-right">Total Value</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for item in data['details']:
                item_id = item.get('id', '-')
                name = item.get('name', 'Unknown')
                quantity = item.get('quantity', 0)
                price = item.get('price', 0.0)
                value = item.get('value', 0.0)
                
                html += f"""
                    <tr>
                        <td>{item_id}</td>
                        <td>{name}</td>
                        <td class="text-right">{quantity}</td>
                        <td class="text-right">${price:.2f}</td>
                        <td class="text-right">${value:.2f}</td>
                    </tr>
                """
            
            html += '</tbody></table>'
            
        elif 'summary' in data:
            # Handle historical movement summary
            html += '<div style="padding: 1.5rem; background: #f8f9fa; border-radius: 6px; margin: 1rem 0;">'
            html += '<strong>Movement Summary:</strong><br><br>'
            summary = data['summary']
            for movement_type, count in summary.items():
                html += f'<div style="margin: 0.5rem 0;"><span class="badge">{movement_type}</span> {count} units</div>'
            html += '</div>'
        
        return html

    def footer(self, data: Dict[str, Any]) -> str:
        total_value = data.get('total_value', 0)
        total_qty = data.get('total_quantity', 0)
        
        html = """
        <table>
            <tbody>
                <tr class="total-row">
                    <td colspan="2"><strong>TOTAL</strong></td>
                    <td class="text-right" colspan="2">Total Quantity: {}</td>
                    <td class="text-right"><strong>${:.2f}</strong></td>
                </tr>
            </tbody>
        </table>
        
        <div class="footer">
            <div class="signature">
                <p><strong>Authorized Signature</strong></p>
                <div class="signature-line"></div>
                <p style="margin-top: 0.5rem; color: #666;">Warehouse Manager</p>
            </div>
        </div>
        """.format(total_qty, total_value if isinstance(total_value, (int, float)) else 0)
        
        return html
