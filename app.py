from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from config import Config
from file_handler import FileHandler
from invoice_processor import InvoiceProcessor
from email_service import EmailService

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# Initialize services
email_service = EmailService(app)
invoice_processor = InvoiceProcessor()
file_handler = FileHandler()


@app.route('/')
def index():
    """Render the main upload form"""
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_invoices():
    """Process uploaded invoices and send report"""
    try:
        # Get form data
        limitations_text = request.form.get('limitations', '')
        recipient_email = request.form.get('email', '')
        uploaded_files = request.files.getlist('invoices')

        # Validate inputs
        if not limitations_text:
            return jsonify({'error': 'Por favor proporciona las limitaciones de factura'}), 400

        if not recipient_email:
            return jsonify({'error': 'Por favor proporciona un correo electrónico'}), 400

        if not uploaded_files or uploaded_files[0].filename == '':
            return jsonify({'error': 'Por favor carga al menos un archivo de factura'}), 400

        # Parse limitations
        rules = invoice_processor.parse_limitations(limitations_text)

        # Process each file
        results = []
        processed_files = []

        for file in uploaded_files:
            if file and file_handler.allowed_file(file.filename):
                # Save file
                filepath = file_handler.save_uploaded_file(file)
                if filepath:
                    processed_files.append(filepath)

                    # Extract data from file
                    file_data = file_handler.process_file(filepath)

                    # Process based on file type
                    if file_data['extension'] in ['pdf', 'xml']:
                        # Text-based processing
                        result = invoice_processor.process_text_invoice(
                            file_data['text'],
                            rules
                        )
                    elif file_data['extension'] in ['png', 'jpg', 'jpeg']:
                        # Image-based processing
                        result = invoice_processor.process_image_invoice(
                            file_data['base64'],
                            file_data['extension'],
                            rules
                        )
                    else:
                        continue

                    result['filename'] = file.filename
                    results.append(result)

        # Generate report
        report_data = invoice_processor.generate_report_data(results, rules)

        # Store report in session for viewing
        session['last_report'] = report_data
        session['report_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Send email report
        email_sent = email_service.send_report(recipient_email, report_data)

        # Cleanup uploaded files
        for filepath in processed_files:
            file_handler.cleanup_file(filepath)

        # Return response with report URL
        response_data = {
            'success': True,
            'message': f'Se procesaron exitosamente {len(results)} facturas.',
            'report_url': '/report',
            'email_sent': email_sent,
            'report': report_data,
            'summary': {
                'total_processed': report_data['total_processed'],
                'accuracy': report_data['accuracy_percentage'],
                'valid_invoices': report_data['valid_invoices'],
                'invalid_invoices': report_data['invalid_invoices']
            }
        }

        if email_sent:
            response_data['message'] += f' Reporte enviado a {recipient_email}'
        else:
            response_data['message'] += ' (El envío de correo falló, pero puedes ver el reporte a continuación)'

        return jsonify(response_data)

    except Exception as e:
        # Send error notification
        if recipient_email:
            email_service.send_error_notification(recipient_email, str(e))

        return jsonify({'error': f'Error de procesamiento: {str(e)}'}), 500


@app.route('/report')
def view_report():
    """Display the last processed report"""
    report_data = session.get('last_report')
    timestamp = session.get('report_timestamp', 'Unknown')

    if not report_data:
        return redirect(url_for('index'))

    return render_template('report.html', report=report_data, timestamp=timestamp)


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'SimplexityInvoiceAgent'})


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file size exceeded error"""
    return jsonify({'error': 'Archivo demasiado grande. El tamaño máximo es 16MB'}), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Punto de acceso no encontrado'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    return jsonify({'error': 'Error interno del servidor'}), 500


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)

    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5001)
