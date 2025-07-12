# Scan utilities for WebShield Scanner

import subprocess
import os
import signal
import threading
import time
from datetime import datetime
import uuid
import platform
from .error_handler import TargetError, ScanConfigError, ScanExecutionError

# Store running processes
running_processes = {}

def validate_target(target):
    """Validate the target input"""
    if not target:
        raise TargetError("Target is required")

    if len(target) < 3:
        raise TargetError("Target is too short")

    clean_target = target
    for prefix in ['http://', 'https://', 'ftp://']:
        if clean_target.startswith(prefix):
            clean_target = clean_target[len(prefix):]

    if not ('.' in clean_target or ':' in clean_target):
        raise TargetError("Target does not appear to be a valid domain or IP address")

    return target

def prepare_scan_command(scan_type, target, scan_option=''):
    """Prepare the command to run based on scan type"""
    validated_target = validate_target(target)

    if scan_type == 'nmap':
        if scan_option == 'open_ports':
            return ['nmap', validated_target]
        elif scan_option == 'version_detection':
            return ['nmap', '-sV', validated_target]
        else:
            raise ScanConfigError(f"Invalid scan option for Nmap: {scan_option}")

    elif scan_type == 'nikto':
        return ['nikto', '-h', validated_target]

    elif scan_type == 'wapiti':
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Check if target already includes a protocol prefix
        if validated_target.startswith('http://') or validated_target.startswith('https://'):
            target_url = validated_target
        else:
            # If no protocol is specified, add http:// as default
            # Wapiti requires a protocol to be specified
            target_url = f"http://{validated_target}"
        
        # Wapiti command implementation with automatic protocol handling
        return f"wapiti -u {target_url} -m all -f html -o /home/priyanshu/project/wapiti_report"
    
    elif scan_type == 'hidi':
        # Create results directory if it doesn't exist
        results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
            
        # Check if target already includes a protocol prefix
        if validated_target.startswith('http://') or validated_target.startswith('https://'):
            target_url = validated_target
        else:
            # If no protocol is specified, add http:// as default
            target_url = f"http://{validated_target}"
            
        # Ffuf command for hidden directory discovery
        # Using common.txt wordlist and filtering out 404 responses
        # Output to HTML format in the results directory
        return f"ffuf -u {target_url}/FUZZ -w /usr/share/wordlists/dirb/common.txt -fc 404 -o /home/priyanshu/project/dirResult.html -of html"

    else:
        raise ScanConfigError(f"Invalid scan type: {scan_type}")

def start_scan(scan_type, target, scan_option=''):
    """Start a new scan and return scan information"""
    try:
        scan_id = str(uuid.uuid4())

        results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(results_dir, f"{scan_type}_{timestamp}_{scan_id}.txt")

        cmd = prepare_scan_command(scan_type, target, scan_option)

        return {
            'scan_id': scan_id,
            'cmd': cmd,
            'output_file': output_file,
            'timestamp': timestamp,
            'scan_type': scan_type,
            'target': target,
            'scan_option': scan_option
        }

    except (TargetError, ScanConfigError) as e:
        raise e
    except Exception as e:
        raise ScanExecutionError(f"Failed to start scan: {str(e)}")

def run_scan_process(cmd, scan_id, output_file, scan_results):
    """Run the scan process and update results"""
    try:
        # Handle both string commands and list commands
        if isinstance(cmd, str):
            # For string commands (like Wapiti or Ffuf), use subprocess.getoutput
            result = subprocess.getoutput(cmd)
            
            # Write the output to file
            with open(output_file, 'w') as f:
                f.write(result)
                
            # Update scan results
            if scan_id in scan_results:
                scan_results[scan_id]['output'] = result.splitlines()
                scan_results[scan_id]['status'] = 'completed'
                
            # Add tool-specific messages
            if 'wapiti' in output_file.lower():
                scan_results[scan_id]['output'].append("\n\nWapiti scan completed. Check /home/priyanshu/project/wapiti_report for full report.")
            elif 'hidi' in output_file.lower() or 'ffuf' in output_file.lower():
                scan_results[scan_id]['output'].append("\n\nHidi scan completed. Check /home/priyanshu/project/dirResult.html for full report.")
                
            return
        
        # Original process handling for list commands
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        running_processes[scan_id] = process

        with open(output_file, 'w') as f:
            for line in iter(process.stdout.readline, ''):
                f.write(line)
                f.flush()
                if scan_id in scan_results:
                    scan_results[scan_id]['output'].append(line.strip())

        process.wait()

        if scan_id in scan_results:
            if process.returncode == 0:
                scan_results[scan_id]['status'] = 'completed'
            else:
                scan_results[scan_id]['status'] = 'failed'
                scan_results[scan_id]['error'] = f"Process exited with code {process.returncode}"

        if scan_id in running_processes:
            del running_processes[scan_id]

    except Exception as e:
        if scan_id in scan_results:
            scan_results[scan_id]['status'] = 'failed'
            scan_results[scan_id]['error'] = str(e)
        if scan_id in running_processes:
            del running_processes[scan_id]
        raise ScanExecutionError(f"Error during scan execution: {str(e)}", scan_id=scan_id)

def stop_scan(scan_id):
    """Stop a running scan process"""
    if scan_id not in running_processes:
        return False

    process = running_processes[scan_id]
    try:
        if platform.system() == 'Windows':
            process.terminate()
        else:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        del running_processes[scan_id]
        return True
    except Exception as e:
        raise ScanExecutionError(f"Failed to stop scan: {str(e)}", scan_id=scan_id)

def create_wapiti_report_parser(output_file):
    """Parse Wapiti HTML report to extract key findings"""
    try:
        # This function could be implemented to parse the Wapiti HTML report
        # and extract key findings for display in the UI
        # For now, we'll just return a simple message
        return "Wapiti scan completed. Check the HTML report for detailed findings."

    except Exception as e:
        raise ScanExecutionError(f"Failed to parse Wapiti report: {str(e)}")
        
def create_ffuf_report_parser(output_file):
    """Parse Ffuf HTML report to extract key findings"""
    try:
        # This function could be implemented to parse the Ffuf HTML report
        # and extract key findings for display in the UI
        # For now, we'll just return a simple message
        return "Hidi scan completed. Check the HTML report for discovered directories."

    except Exception as e:
        raise ScanExecutionError(f"Failed to parse Ffuf report: {str(e)}")
