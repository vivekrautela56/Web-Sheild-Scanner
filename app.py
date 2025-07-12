from flask import Flask, render_template, request, jsonify, send_file
import os
import threading
import uuid
from datetime import datetime

# Import utility modules
from utils import (
    validate_target, start_scan, run_scan_process, stop_scan,
    running_processes, get_report_file, handle_scan_error,
    ScanError, TargetError, ScanConfigError, ScanExecutionError, ReportGenerationError
)

app = Flask(__name__)

# Store scan results
scan_results = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scan')
def scan():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/scan', methods=['POST'])
def api_start_scan():
    try:
        # Get scan parameters
        scan_type = request.json.get('scan_type')
        target = request.json.get('target')
        scan_option = request.json.get('scan_option', '')
        
        # Start the scan
        scan_info = start_scan(scan_type, target, scan_option)
        scan_id = scan_info['scan_id']
        cmd = scan_info['cmd']
        output_file = scan_info['output_file']
        
        # Initialize scan results
        scan_results[scan_id] = {
            'output': [],
            'status': 'running',
            'file_path': output_file,
            'scan_type': scan_type,
            'target': target,
            'scan_option': scan_option,
            'timestamp': scan_info['timestamp']
        }
        
        # Start the scan in a separate thread
        thread = threading.Thread(
            target=run_scan_process, 
            args=(cmd, scan_id, output_file, scan_results)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'scan_id': scan_id,
            'status': 'started',
            'message': f'{scan_type.capitalize()} scan started for {target}'
        })
        
    except TargetError as e:
        return jsonify({'error': str(e)}), 400
    except ScanConfigError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        error_info = handle_scan_error(e)
        return jsonify({'error': error_info['error']}), 500

@app.route('/api/scan/<scan_id>/status', methods=['GET'])
def get_scan_status(scan_id):
    if scan_id not in scan_results:
        return jsonify({'error': 'Scan not found'}), 404
    
    # Get the latest output lines
    last_line_index = request.args.get('last_line', 0, type=int)
    new_lines = scan_results[scan_id]['output'][last_line_index:]
    
    return jsonify({
        'status': scan_results[scan_id]['status'],
        'new_lines': new_lines,
        'line_count': len(scan_results[scan_id]['output'])
    })

@app.route('/api/scan/<scan_id>/stop', methods=['POST'])
def api_stop_scan(scan_id):
    try:
        if scan_id not in running_processes:
            return jsonify({'error': 'No running scan found with this ID'}), 404
        
        # Stop the scan
        if stop_scan(scan_id):
            # Update status
            if scan_id in scan_results:
                scan_results[scan_id]['status'] = 'stopped'
            
            return jsonify({
                'status': 'stopped',
                'message': 'Scan stopped successfully'
            })
        else:
            return jsonify({'error': 'Failed to stop scan'}), 500
            
    except Exception as e:
        error_info = handle_scan_error(e, scan_results)
        return jsonify({'error': error_info['error']}), 500

@app.route('/api/scan/<scan_id>/report', methods=['GET'])
def get_report(scan_id):
    try:
        format_type = request.args.get('format', 'txt')
        
        # Get the report file
        file_path = get_report_file(scan_id, scan_results, format_type)
        
        # Get filename for download
        filename = f"{scan_results[scan_id]['scan_type']}_{scan_results[scan_id]['timestamp']}.{format_type}"
        
        return send_file(file_path, as_attachment=True, download_name=filename)
        
    except ReportGenerationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        error_info = handle_scan_error(e)
        return jsonify({'error': error_info['error']}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    # Create results directory if it doesn't exist
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Create scripts directory if it doesn't exist
    scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        
    app.run(debug=True)