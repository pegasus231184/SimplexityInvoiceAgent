from flask_mail import Mail, Message
from typing import Dict
from datetime import datetime


class EmailService:
    """Handle email reporting functionality"""

    def __init__(self, app=None):
        self.mail = Mail(app) if app else None

    def init_app(self, app):
        """Initialize with Flask app"""
        self.mail = Mail(app)

    def format_report_html(self, report_data: Dict) -> str:
        """Format report data as HTML email"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .summary {{ background-color: #f4f4f4; padding: 15px; margin: 20px 0; border-radius: 5px; }}
                .metric {{ display: inline-block; margin: 10px 20px; }}
                .metric-label {{ font-weight: bold; color: #666; }}
                .metric-value {{ font-size: 24px; color: #4CAF50; }}
                .violations {{ background-color: #ffebee; padding: 15px; margin: 10px 0; border-left: 4px solid #f44336; }}
                .success {{ color: #4CAF50; }}
                .error {{ color: #f44336; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th {{ background-color: #4CAF50; color: white; padding: 10px; text-align: left; }}
                td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                tr:hover {{ background-color: #f5f5f5; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Invoice Processing Report</h1>
                <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>

            <div class="summary">
                <h2>Summary</h2>
                <div class="metric">
                    <div class="metric-label">Total Processed</div>
                    <div class="metric-value">{report_data['total_processed']}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Valid Invoices</div>
                    <div class="metric-value success">{report_data['valid_invoices']}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Invalid Invoices</div>
                    <div class="metric-value error">{report_data['invalid_invoices']}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Accuracy</div>
                    <div class="metric-value">{report_data['accuracy_percentage']}%</div>
                </div>
            </div>

            <div class="summary">
                <h3>Financial Summary</h3>
                <p><strong>Approved Amount:</strong> {report_data['currency']} {report_data['total_approved_amount']:,.2f}</p>
                <p><strong>Excluded Amount:</strong> {report_data['currency']} {report_data['total_excluded_amount']:,.2f}</p>
                <p><strong>Maximum Limit:</strong> {report_data['currency']} {report_data['max_limit']:,.2f}</p>
            </div>
        """

        # Add violations if any
        if report_data['violations']:
            html += """
            <div class="violations">
                <h3>Violations Found</h3>
                <ul>
            """
            for violation in report_data['violations']:
                html += f"<li>{violation}</li>"
            html += """
                </ul>
            </div>
            """

        # Add detailed results table
        html += """
            <h3>Detailed Results</h3>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Total Amount</th>
                        <th>Currency</th>
                        <th>Date</th>
                        <th>Status</th>
                        <th>Issues</th>
                    </tr>
                </thead>
                <tbody>
        """

        for idx, result in enumerate(report_data['detailed_results'], 1):
            status = "✓ Valid" if result.get('is_valid', False) else "✗ Invalid"
            status_class = "success" if result.get('is_valid', False) else "error"
            violations = ", ".join(result.get('violations', [])) or "None"

            html += f"""
                <tr>
                    <td>{idx}</td>
                    <td>{result.get('total_amount', 0):,.2f}</td>
                    <td>{result.get('currency', 'Unknown')}</td>
                    <td>{result.get('date', 'Unknown')}</td>
                    <td class="{status_class}">{status}</td>
                    <td>{violations}</td>
                </tr>
            """

        html += """
                </tbody>
            </table>

            <div style="margin-top: 30px; padding: 20px; background-color: #f4f4f4; text-align: center;">
                <p>This report was automatically generated by SimplexityInvoiceAgent</p>
            </div>
        </body>
        </html>
        """

        return html

    def send_report(self, recipient_email: str, report_data: Dict) -> bool:
        """Send email report to recipient"""
        try:
            subject = f"Invoice Processing Report - {report_data['accuracy_percentage']}% Accuracy"
            html_body = self.format_report_html(report_data)

            msg = Message(
                subject=subject,
                recipients=[recipient_email],
                html=html_body
            )

            self.mail.send(msg)
            return True

        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def send_error_notification(self, recipient_email: str, error_message: str) -> bool:
        """Send error notification email"""
        try:
            msg = Message(
                subject="Invoice Processing Error",
                recipients=[recipient_email],
                html=f"""
                <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2 style="color: #f44336;">Invoice Processing Error</h2>
                    <p>An error occurred while processing your invoices:</p>
                    <div style="background-color: #ffebee; padding: 15px; border-left: 4px solid #f44336;">
                        <pre>{error_message}</pre>
                    </div>
                    <p>Please check your files and try again.</p>
                </body>
                </html>
                """
            )

            self.mail.send(msg)
            return True

        except Exception as e:
            print(f"Error sending error notification: {e}")
            return False
