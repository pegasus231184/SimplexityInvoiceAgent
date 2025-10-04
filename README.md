# SimplexityInvoiceAgent

An automated invoice processing and validation system powered by OpenAI API and Flask. This application allows users to upload invoices in various formats (PDF, images, XML), define validation rules, and receive detailed email reports about the processing results.

## Features

- 📄 **Multi-format Support**: Process invoices from PDF, PNG, JPG, JPEG, and XML files
- 🤖 **AI-Powered Validation**: Uses OpenAI GPT-4 and Vision API for intelligent invoice analysis
- ✅ **Rule-Based Validation**: Define custom limitations (item categories, amount limits, currency)
- 📊 **Detailed Reporting**: Comprehensive email reports with accuracy metrics and violation details
- 🌐 **Web Interface**: User-friendly web UI for easy file uploads and rule definition
- 📧 **Email Notifications**: Automatic report delivery to specified email addresses

## Project Structure

```
SimplexityInvoiceAgent/
├── app.py                  # Flask application with routes
├── invoice_processor.py    # Core invoice processing logic using OpenAI API
├── file_handler.py         # Handle PDF, image, and XML uploads
├── email_service.py        # Email reporting functionality
├── config.py              # Configuration management
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── templates/
│   └── index.html         # Web interface
├── static/
│   └── style.css          # Styling
└── uploads/               # Temporary file storage (auto-created)
```

## Requirements

- Python 3.8+
- OpenAI API key
- Email SMTP credentials (Gmail, SendGrid, or Mailgun)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd SimplexityInvoiceAgent
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your credentials:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `MAIL_USERNAME`: Your email address
   - `MAIL_PASSWORD`: Your email app password (for Gmail, use App Passwords)

## Configuration

### OpenAI API

1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Add it to your `.env` file:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```

### Email Setup

#### Gmail Setup:
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password: [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Add to `.env`:
   ```
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

#### Alternative Email Providers:
- **SendGrid**: Use SendGrid API key
- **Mailgun**: Configure Mailgun domain and API key

## Usage

### Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Access the web interface**:
   Open your browser and navigate to: `http://localhost:5000`

### Using the Web Interface

1. **Define Invoice Limitations**:
   - Enter validation rules in text format
   - Example: "Only food and beverage items allowed. Maximum amount: 100,000 colones (CRC). No alcohol or tobacco products."

2. **Upload Invoices**:
   - Click "Choose Files" and select one or multiple invoices
   - Supported formats: PDF, PNG, JPG, JPEG, XML
   - Maximum file size: 16MB per file

3. **Enter Email Address**:
   - Provide the email where you want to receive the report

4. **Process Invoices**:
   - Click "Process Invoices"
   - Wait for processing to complete
   - Check your email for the detailed report

### Example Validation Rules

```
Only food items allowed, maximum 50000 CRC
```

```
Food and beverage only. Max: $500 USD. No alcohol or tobacco.
```

```
Categories: groceries, fresh produce, dairy products
Maximum amount: 200,000 colones
Currency: CRC
```

## Email Report Contents

The email report includes:

- **Summary Statistics**:
  - Total invoices processed
  - Number of valid/invalid invoices
  - Accuracy percentage

- **Financial Summary**:
  - Total approved amount
  - Total excluded amount
  - Comparison with maximum limit

- **Violations List**:
  - Detailed list of rule violations
  - Non-compliant items
  - Amount limit breaches

- **Detailed Results Table**:
  - Per-invoice breakdown
  - Status (Valid/Invalid)
  - Issues identified

## API Endpoints

### `GET /`
Returns the main web interface

### `POST /process`
Processes uploaded invoices

**Request (multipart/form-data)**:
- `limitations` (text): Validation rules
- `email` (text): Recipient email address
- `invoices` (files[]): Invoice files to process

**Response (JSON)**:
```json
{
  "success": true,
  "message": "Successfully processed 5 invoices. Report sent to user@example.com",
  "summary": {
    "total_processed": 5,
    "accuracy": 80.0,
    "valid_invoices": 4,
    "invalid_invoices": 1
  }
}
```

### `GET /health`
Health check endpoint

**Response**:
```json
{
  "status": "healthy",
  "service": "SimplexityInvoiceAgent"
}
```

## How It Works

1. **File Upload**: User uploads invoices and defines validation rules
2. **File Processing**:
   - PDFs: Text extraction using PyPDF2/pdfplumber
   - Images: OCR and analysis using OpenAI Vision API
   - XML: Parsing with xmltodict
3. **AI Analysis**: OpenAI processes each invoice and extracts:
   - Line items and amounts
   - Total amount and currency
   - Date information
4. **Validation**: Each invoice is validated against user-defined rules
5. **Report Generation**: Comprehensive report with accuracy metrics
6. **Email Delivery**: HTML-formatted report sent to user's email

## Supported File Formats

| Format | Extension | Processing Method |
|--------|-----------|-------------------|
| PDF | `.pdf` | Text extraction (PyPDF2, pdfplumber) |
| Images | `.png`, `.jpg`, `.jpeg` | OpenAI Vision API |
| XML | `.xml` | XML parsing (xmltodict) |

## Error Handling

- **File Size Limit**: Maximum 16MB per file
- **Invalid File Types**: Only supported formats accepted
- **API Errors**: Graceful degradation with error notifications
- **Email Failures**: Error notifications sent if report delivery fails

## Security Considerations

- API keys stored in environment variables (not in code)
- File uploads validated for type and size
- Uploaded files automatically cleaned up after processing
- Secure file naming with werkzeug's `secure_filename`

## Troubleshooting

### Common Issues

1. **OpenAI API Error**:
   - Verify your API key is correct
   - Check your OpenAI account has credits
   - Ensure internet connection is stable

2. **Email Not Sent**:
   - Verify SMTP credentials are correct
   - For Gmail, use App Passwords (not regular password)
   - Check firewall/antivirus settings

3. **File Upload Failed**:
   - Check file size (max 16MB)
   - Ensure file format is supported
   - Verify sufficient disk space

4. **Processing Takes Too Long**:
   - Large files may take time to process
   - Images require Vision API processing
   - Check OpenAI API response times

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development
python app.py
```

### Running in Production

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `dev-secret-key-change-in-production` |
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_MODEL` | GPT model to use | `gpt-4-turbo-preview` |
| `OPENAI_VISION_MODEL` | Vision model | `gpt-4-vision-preview` |
| `MAIL_SERVER` | SMTP server | `smtp.gmail.com` |
| `MAIL_PORT` | SMTP port | `587` |
| `MAIL_USE_TLS` | Use TLS | `True` |
| `MAIL_USERNAME` | Email username | Required |
| `MAIL_PASSWORD` | Email password | Required |

## Dependencies

- **Flask** (3.0.0): Web framework
- **OpenAI** (1.12.0): AI processing
- **PyPDF2** (3.0.1): PDF text extraction
- **pdfplumber** (0.10.3): Advanced PDF parsing
- **Pillow** (10.2.0): Image processing
- **xmltodict** (0.13.0): XML parsing
- **Flask-Mail** (0.9.1): Email functionality
- **python-dotenv** (1.0.0): Environment variable management

## License

This project is provided as-is for educational and commercial use.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For issues, questions, or feature requests, please create an issue in the repository.

## Despliegue en Railway

### Paso 1: Preparación del Proyecto

El proyecto ya está configurado para Railway con los siguientes archivos:
- `Procfile`: Define el comando de inicio
- `railway.json`: Configuración de Railway
- `runtime.txt`: Especifica la versión de Python
- `requirements.txt`: Incluye gunicorn para producción

### Paso 2: Crear Cuenta en Railway

1. Ve a [Railway.app](https://railway.app)
2. Regístrate con GitHub
3. Autoriza Railway para acceder a tus repositorios

### Paso 3: Desplegar el Proyecto

#### Opción A: Desde GitHub
1. Sube el proyecto a GitHub
2. En Railway, haz clic en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Selecciona el repositorio `SimplexityInvoiceAgent`
5. Railway detectará automáticamente la configuración

#### Opción B: Desde Railway CLI
```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Inicializar proyecto
railway init

# Deploy
railway up
```

### Paso 4: Configurar Variables de Entorno

En el dashboard de Railway, ve a tu proyecto > Variables y agrega:

```
OPENAI_API_KEY=tu-api-key-de-openai
MAIL_USERNAME=tu-correo@gmail.com
MAIL_PASSWORD=tu-app-password-de-gmail
SECRET_KEY=genera-una-clave-secreta-aleatoria
```

**Variables opcionales:**
```
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_VISION_MODEL=gpt-4-vision-preview
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
```

### Paso 5: Generar Domain

1. En Railway, ve a Settings
2. En la sección "Domains", haz clic en "Generate Domain"
3. Railway te dará una URL como: `simplexityinvoiceagent.up.railway.app`

### Paso 6: Verificar Deployment

1. Visita la URL generada
2. Deberías ver la interfaz del Agente de Procesamiento de Facturas
3. Prueba subiendo una factura de prueba

### Troubleshooting

**Error: Application failed to respond**
- Verifica que las variables de entorno estén configuradas
- Revisa los logs en Railway Dashboard

**Error: OpenAI API**
- Verifica que tu API key sea válida
- Asegúrate de tener créditos en tu cuenta de OpenAI

**Error: Email no se envía**
- Verifica las credenciales SMTP
- Para Gmail, usa App Passwords, no tu contraseña regular

### Monitoreo

Railway proporciona:
- **Logs**: Ver logs en tiempo real
- **Metrics**: CPU, memoria, red
- **Deployments**: Historial de despliegues

### Costos

- Railway ofrece $5 USD de crédito gratis mensual
- Uso adicional se cobra por hora de uso
- Monitorea tu uso en el Dashboard

## Roadmap

- [ ] Support for additional file formats (Excel, CSV)
- [ ] Multi-language invoice support
- [ ] Dashboard for tracking historical processing
- [ ] API authentication and rate limiting
- [ ] Batch processing queue system
- [ ] Integration with accounting software
- [ ] Custom email templates
- [ ] Advanced reporting with charts and graphs

## Credits

Built with:
- OpenAI API for intelligent document processing
- Flask for web framework
- Python for backend processing
- Deployed on Railway

---

**Note**: Make sure to keep your API keys and credentials secure. Never commit `.env` files to version control.
