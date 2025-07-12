# Error handling utilities for WebShield Scanner

class ScanError(Exception):
    """Base exception class for scan-related errors"""
    def __init__(self, message, scan_id=None, scan_type=None):
        self.message = message
        self.scan_id = scan_id
        self.scan_type = scan_type
        super().__init__(self.message)

class TargetError(ScanError):
    """Exception raised for errors related to the target"""
    pass

class ScanConfigError(ScanError):
    """Exception raised for errors in scan configuration"""
    pass

class ScanExecutionError(ScanError):
    """Exception raised when a scan fails during execution"""
    pass

class ReportGenerationError(ScanError):
    """Exception raised when report generation fails"""
    pass

def handle_scan_error(error, scan_results=None):
    """Handle scan errors and update scan results if provided"""
    error_message = str(error)
    error_type = type(error).__name__
    
    # Log the error
    print(f"Error: {error_type} - {error_message}")
    
    # Update scan results if provided
    if scan_results and hasattr(error, 'scan_id') and error.scan_id in scan_results:
        scan_results[error.scan_id]['status'] = 'failed'
        scan_results[error.scan_id]['error'] = error_message
    
    # Return error information
    return {
        'error': error_message,
        'error_type': error_type
    }