from .base import ReportGenerator
from typing import Dict, Any
import datetime

class ActGenerator(ReportGenerator):
    def header(self, data: Dict[str, Any], date: datetime.date) -> str:
        report_type = data.get('report_type', 'Inventory Act')
        return f"""
        <div class="doc-header">
            <div class="doc-title">Warehouse Management System</div>
            <h1>Official Act</h1>
            <div class="doc-info">
                <span><strong>Subject:</strong> {report_type}</span>
                <span><strong>Date of Issue:</strong> {date}</span>
            </div>
        </div>
        """

    def body(self, data: Dict[str, Any]) -> str:
        html = '<h2>Findings</h2>'
        
        if 'details' in data:
            html += """
            <table>
                <thead>
                    <tr>
                        <th>Status</th>
                        <th>ID</th>
                        <th>Product Name</th>
                        <th class="text-right">Stock Quantity</th>
                        <th class="text-right">Unit Price</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for item in data['details']:
                item_id = item.get('id', '-')
                name = item.get('name', 'Unknown')
                quantity = item.get('quantity', 0)
                price = item.get('price', 0.0)
                
                html += f"""
                    <tr>
                        <td><span class="badge">OK</span></td>
                        <td>{item_id}</td>
                        <td>{name}</td>
                        <td class="text-right">{quantity}</td>
                        <td class="text-right">${price:.2f}</td>
                    </tr>
                """
            
            html += '</tbody></table>'
            
        elif 'summary' in data:
            # Handle historical movement summary
            html += '<div style="padding: 1.5rem; background: #f8f9fa; border-radius: 6px; margin: 1rem 0;">'
            html += '<strong>Movement Summary:</strong><br><br>'
            summary = data['summary']
            for movement_type, count in summary.items():
                badge_color = '#28a745' if movement_type == 'ARRIVAL' else '#dc3545' if movement_type == 'SHIPMENT' else '#ffc107'
                html += f'<div style="margin: 0.5rem 0;"><span class="badge" style="background: {badge_color};">{movement_type}</span> {count} units</div>'
            html += '</div>'
        
        return html

    def footer(self, data: Dict[str, Any]) -> str:
        total_qty = data.get('total_quantity', data.get('total_transactions', 0))
        
        html = f"""
        <div class="footer">
            <p style="margin-bottom: 1rem;"><strong>Total Items Inspected:</strong> {total_qty}</p>
            <p style="margin-bottom: 2rem; color: #666;">This act certifies that all items listed above have been inspected and verified according to warehouse standards.</p>
            
            <div class="signature">
                <p><strong>Certified by:</strong></p>
                <div class="signature-line"></div>
                <p style="margin-top: 0.5rem; color: #666;">Warehouse Manager</p>
                <p style="margin-top: 0.25rem; font-size: 12px; color: #999;">Signature & Official Stamp</p>
            </div>
        </div>
        """
        
        return html
