# WebShield Scanner Utilities Package

from .error_handler import (
    ScanError, TargetError, ScanConfigError, 
    ScanExecutionError, ReportGenerationError, 
    handle_scan_error
)

from .scan_utils import (
    validate_target, prepare_scan_command, 
    start_scan, run_scan_process, stop_scan,
    running_processes
)

from .report_utils import (
    generate_html_report, 
    get_report_file
)

__all__ = [
    'ScanError', 'TargetError', 'ScanConfigError', 
    'ScanExecutionError', 'ReportGenerationError',
    'handle_scan_error', 'validate_target', 
    'prepare_scan_command', 'start_scan', 
    'run_scan_process', 'stop_scan', 'running_processes',
    'generate_html_report', 
    'get_report_file'
]