# WebShield Scanner

A modern, responsive, and professional web application for vulnerability scanning with multiple scanning options through a simple, attractive frontend and a Python Flask backend.

## Features

- **Multiple Scanning Options**:
  - Nmap Scan (with Open Ports and Version Detection sub-options)
  - Nikto Scan
  - Wapiti Scan
- **Real-time Output Display**: See scan progress and results as they happen
- **Downloadable Reports**: Get your results in TXT, HTML, or PDF formats
- **Process Management**: Start and stop scans with ease
- **Modern UI**: Responsive design that works on desktop and mobile devices

## Prerequisites

- Python 3.7 or higher
- Nmap (for Nmap scanning functionality)
- Nikto (for Nikto scanning functionality)
- Wapiti (for web application vulnerability scanning)
- wkhtmltopdf (for PDF report generation)

## Installation

### Standard Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/webshield-scanner.git
   cd webshield-scanner
   ```

2. Create a virtual environment and activate it:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Install wkhtmltopdf:
   - Windows: Download and install from [wkhtmltopdf downloads](https://wkhtmltopdf.org/downloads.html)
   - macOS: `brew install wkhtmltopdf`
   - Linux: `sudo apt-get install wkhtmltopdf` (Ubuntu/Debian) or `sudo yum install wkhtmltopdf` (CentOS/RHEL)

### Docker Installation

1. Make sure you have Docker and Docker Compose installed

2. Build and start the container:
   ```bash
   docker-compose up -d
   ```

## Usage

### Standard Usage

1. Start the application:
   ```bash
   # On Windows
   run.bat
   
   # On macOS/Linux
   ./run.sh
   ```
   Or manually with:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`

3. Enter the target IP or URL in the input field

4. Select a scan type and configure any options if prompted

5. Click the scan button to start the scan

6. View real-time results in the output area

7. When the scan completes, download the report in your preferred format

### Docker Usage

1. Access the application at `http://localhost:5000`

2. Follow steps 3-7 from the Standard Usage section

## Development

### Project Structure

```
webshield-scanner/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── run.bat                # Windows startup script
├── run.sh                 # Unix startup script
├── static/                # Static assets
│   ├── css/
│   │   └── style.css      # Custom CSS styles
│   └── js/
│       └── main.js        # Frontend JavaScript
├── templates/
│   └── index.html         # Main HTML template
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── error_handler.py   # Error handling utilities
│   ├── report_utils.py    # Report generation utilities
│   └── scan_utils.py      # Scanning utilities
└── results/               # Scan results storage
    └── .gitkeep
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security Considerations

- This tool is intended for security professionals to scan systems they have permission to test
- Always ensure you have proper authorization before scanning any system
- The developers are not responsible for any misuse of this tool

## Wapiti Configuration

To use the Wapiti scanning functionality:

1. Install Wapiti on your system
2. Wapiti will be used with the following command format: