import os
import sys
import subprocess
import importlib.util

def check_python_module(module_name):
    """Check if a Python module is installed."""
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"❌ Python module '{module_name}' is NOT installed.")
        return False
    print(f"✅ Python module '{module_name}' is installed.")
    return True

def check_command(command):
    """Check if a command is available in the system PATH."""
    try:
        # Use 'where' on Windows and 'which' on Unix-like systems
        check_cmd = 'where' if os.name == 'nt' else 'which'
        subprocess.run([check_cmd, command], 
                       check=True, 
                       stdout=subprocess.PIPE, 
                       stderr=subprocess.PIPE)
        print(f"✅ Command '{command}' is available.")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Command '{command}' is NOT available in PATH.")
        return False

def check_wkhtmltopdf():
    """Check if wkhtmltopdf is installed and provide installation instructions if not."""
    if check_command('wkhtmltopdf'):
        return True
    
    print("\nwkhtmltopdf is required for PDF generation. Please install it:")
    if os.name == 'nt':  # Windows
        print("1. Download from: https://wkhtmltopdf.org/downloads.html")
        print("2. Run the installer and follow the instructions")
        print("3. Ensure it's added to your PATH")
    elif sys.platform == 'darwin':  # macOS
        print("Run: brew install wkhtmltopdf")
    else:  # Linux
        print("Run: sudo apt-get install wkhtmltopdf  # For Debian/Ubuntu")
        print("Run: sudo yum install wkhtmltopdf      # For CentOS/RHEL")
    
    return False

def main():
    print("Checking WebShield Scanner dependencies...\n")
    
    # Check Python modules
    modules = ['flask', 'werkzeug', 'pdfkit', 'socketio']
    modules_ok = all(check_python_module(module) for module in modules)
    
    print("\nChecking external dependencies...")
    # Check external commands
    wkhtmltopdf_ok = check_wkhtmltopdf()
    
    # Optional: Check for scanning tools
    print("\nChecking scanning tools (optional)...")
    nmap_ok = check_command('nmap')
    nikto_ok = check_command('nikto')
    wapiti_ok = check_command('wapiti')
    
    # Summary
    print("\nDependency Check Summary:")
    if modules_ok:
        print("✅ All required Python modules are installed.")
    else:
        print("❌ Some Python modules are missing. Run: pip install -r requirements.txt")
    
    if wkhtmltopdf_ok:
        print("✅ wkhtmltopdf is installed and available.")
    else:
        print("❌ wkhtmltopdf is missing. PDF generation will not work.")
    
    if nmap_ok and nikto_ok and wapiti_ok:
        print("✅ All scanning tools are available.")
    else:
        print("⚠️ Some scanning tools are missing. The application will work, but some scan types may not be available.")

if __name__ == "__main__":
    main()