/**
 * WebShield Scanner - Main JavaScript
 * Handles UI interactions, scan operations, and real-time updates
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const targetInput = document.getElementById('target');
    const scanCards = document.querySelectorAll('.scan-card');
    const outputArea = document.getElementById('output-area');
    const outputTitle = document.getElementById('output-title');
    const scanStatus = document.getElementById('scan-status');
    const statusText = document.getElementById('status-text');
    const progressBar = document.getElementById('progress-bar');
    const scanControls = document.getElementById('scan-controls');
    const stopScanBtn = document.getElementById('stop-scan');
    const reportSection = document.getElementById('report-section');
    const downloadBtns = document.querySelectorAll('.download-btn');
    
    // Nmap Modal Elements
    const nmapModal = document.getElementById('nmap-modal');
    const closeNmapModal = document.getElementById('close-nmap-modal');
    const nmapOptions = document.querySelectorAll('.nmap-option');
    
    // Variables to track current scan
    let currentScanId = null;
    let currentScanType = null;
    let pollingInterval = null;
    let lastLineIndex = 0;
    let progressValue = 0;
    
    // Initialize download buttons
    downloadBtns.forEach(btn => {
        btn.classList.add('bg-slate-700', 'hover:bg-slate-600', 'text-white', 'px-4', 'py-2', 'rounded-md', 'text-sm', 'transition-colors');
    });
    
    // Handle scan card clicks
    scanCards.forEach(card => {
        card.addEventListener('click', function() {
            const scanType = this.getAttribute('data-scan');
            
            if (scanType === 'nmap') {
                // Show Nmap options modal
                nmapModal.classList.remove('hidden');
            } else {
                // Start other scan types directly
                startScan(scanType);
            }
        });
    });
    
    // Close Nmap modal
    closeNmapModal.addEventListener('click', function() {
        nmapModal.classList.add('hidden');
    });
    
    // Handle Nmap option selection
    nmapOptions.forEach(option => {
        option.addEventListener('click', function() {
            const scanOption = this.getAttribute('data-option');
            startScan('nmap', scanOption);
            nmapModal.classList.add('hidden');
        });
    });
    
    // Start scan function
    function startScan(scanType, scanOption = '') {
        const target = targetInput.value.trim();
        
        if (!target) {
            showError('Please enter a target URL or IP address');
            return;
        }
        
        // Reset UI
        resetUI();
        
        // Update UI for scanning
        currentScanType = scanType;
        outputTitle.textContent = `${scanType.toUpperCase()} Scan Output`;
        scanStatus.classList.remove('hidden');
        scanControls.classList.remove('hidden');
        outputArea.innerHTML = '<div class="text-cyan-400">Initializing scan...</div>';
        
        // Add loader animation
        const loaderDiv = document.createElement('div');
        loaderDiv.classList.add('loader', 'mx-auto', 'my-4');
        outputArea.appendChild(loaderDiv);
        
        // Send request to start scan
        fetch('/api/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                scan_type: scanType,
                target: target,
                scan_option: scanOption
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
                return;
            }
            
            // Store scan ID and start polling for updates
            currentScanId = data.scan_id;
            outputArea.innerHTML = `<div class="text-green-400">${data.message}</div>`;
            startPolling();
        })
        .catch(error => {
            showError('Failed to start scan: ' + error.message);
        });
    }
    
    // Poll for scan updates
    function startPolling() {
        lastLineIndex = 0;
        progressValue = 0;
        
        pollingInterval = setInterval(() => {
            if (!currentScanId) return;
            
            fetch(`/api/scan/${currentScanId}/status?last_line=${lastLineIndex}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        showError(data.error);
                        stopPolling();
                        return;
                    }
                    
                    // Update output with new lines
                    if (data.new_lines && data.new_lines.length > 0) {
                        appendOutput(data.new_lines);
                        lastLineIndex = data.line_count;
                        
                        // Update progress bar (simple animation)
                        updateProgressBar();
                    }
                    
                    // Check if scan is complete
                    if (data.status !== 'running') {
                        scanComplete(data.status);
                        stopPolling();
                    }
                })
                .catch(error => {
                    console.error('Error polling for updates:', error);
                });
        }, 1000);
    }
    
    // Stop polling
    function stopPolling() {
        if (pollingInterval) {
            clearInterval(pollingInterval);
            pollingInterval = null;
        }
    }
    
    // Append output lines
    function appendOutput(lines) {
        const fragment = document.createDocumentFragment();
        
        lines.forEach(line => {
            const div = document.createElement('div');
            div.textContent = line;
            div.classList.add('terminal-line');
            
            // Add some color based on content
            if (line.includes('CRITICAL') || line.includes('ERROR') || line.includes('FAIL') || line.includes('VULNERABILITY')) {
                div.classList.add('text-red-400');
            } else if (line.includes('WARNING')) {
                div.classList.add('text-yellow-400');
            } else if (line.includes('SUCCESS') || line.includes('OPEN') || line.includes('FOUND') || line.includes('Status: 200')) {
                div.classList.add('text-green-400');
            } else if (line.includes('INFO') || line.includes('Starting') || line.includes('Target:')) {
                div.classList.add('text-blue-400');
            } else if (line.includes('Hidi scan') || line.includes('ffuf')) {
                div.classList.add('text-cyan-400');
            } else {
                div.classList.add('text-slate-300');
            }
            
            fragment.appendChild(div);
        });
        
        outputArea.appendChild(fragment);
        outputArea.scrollTop = outputArea.scrollHeight;
    }
    
    // Update progress bar animation
    function updateProgressBar() {
        // Increment progress, but slow down as we approach 90%
        if (progressValue < 90) {
            const increment = progressValue < 30 ? 2 : (progressValue < 60 ? 1 : 0.5);
            progressValue += increment;
            progressBar.style.width = progressValue + '%';
        }
    }
    
    // Handle scan completion
    function scanComplete(status) {
        // Update UI based on status
        if (status === 'completed') {
            statusText.textContent = 'Scan completed successfully';
            statusText.classList.remove('text-cyan-400');
            statusText.classList.add('text-green-400');
            reportSection.classList.remove('hidden');
            
            // Add completion message
            const completionMsg = document.createElement('div');
            completionMsg.textContent = '✅ Scan completed successfully. You can download the report below.';
            completionMsg.classList.add('text-green-400', 'font-bold', 'mt-4', 'mb-2', 'text-center');
            outputArea.appendChild(completionMsg);
        } else if (status === 'failed') {
            statusText.textContent = 'Scan failed';
            statusText.classList.remove('text-cyan-400');
            statusText.classList.add('text-red-400');
            showError('The scan encountered an error and could not complete.');
        } else if (status === 'stopped') {
            statusText.textContent = 'Scan stopped by user';
            statusText.classList.remove('text-cyan-400');
            statusText.classList.add('text-yellow-400');
            appendOutput(['Scan was stopped by user request']);
        }
        
        // Set progress bar to 100%
        progressBar.style.width = '100%';
        
        // Remove the animated pulse from status indicator
        const pulseIndicator = document.querySelector('.animate-pulse-slow');
        if (pulseIndicator) {
            pulseIndicator.classList.remove('animate-pulse-slow');
        }
    }
    
    // Stop scan button
    stopScanBtn.addEventListener('click', function() {
        if (!currentScanId) return;
        
        // Disable button to prevent multiple clicks
        this.disabled = true;
        this.innerHTML = '<i class="fas fa-spinner fa-spin mr-1"></i>Stopping...';
        
        fetch(`/api/scan/${currentScanId}/stop`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
                return;
            }
            
            appendOutput(['Stopping scan...']);
        })
        .catch(error => {
            showError('Failed to stop scan: ' + error.message);
        })
        .finally(() => {
            // Re-enable button
            this.disabled = false;
            this.innerHTML = '<i class="fas fa-stop mr-1"></i>Stop Scan';
        });
    });
    
    // Download report buttons
    downloadBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            if (!currentScanId) return;
            
            const format = this.getAttribute('data-format');
            
            // Add loading indicator
            const originalContent = this.innerHTML;
            this.innerHTML = `<i class="fas fa-spinner fa-spin mr-1"></i>${format.toUpperCase()}`;
            this.disabled = true;
            
            // Create a hidden iframe to handle the download
            const iframe = document.createElement('iframe');
            iframe.style.display = 'none';
            iframe.src = `/api/scan/${currentScanId}/report?format=${format}`;
            document.body.appendChild(iframe);
            
            // Reset button after a short delay
            setTimeout(() => {
                this.innerHTML = originalContent;
                this.disabled = false;
                document.body.removeChild(iframe);
            }, 2000);
        });
    });
    
    // Show error message
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.textContent = `Error: ${message}`;
        errorDiv.classList.add('text-red-400', 'py-1', 'font-bold');
        outputArea.appendChild(errorDiv);
        outputArea.scrollTop = outputArea.scrollHeight;
    }
    
    // Reset UI
    function resetUI() {
        stopPolling();
        currentScanId = null;
        outputTitle.textContent = 'Scan Output';
        scanStatus.classList.add('hidden');
        scanControls.classList.add('hidden');
        reportSection.classList.add('hidden');
        progressBar.style.width = '0%';
        progressValue = 0;
        
        // Reset status text color
        statusText.classList.remove('text-green-400', 'text-red-400', 'text-yellow-400');
        statusText.classList.add('text-cyan-400');
        statusText.textContent = 'Initializing scan...';
        
        // Reset pulse animation
        const pulseIndicator = document.querySelector('.animate-pulse-slow');
        if (pulseIndicator) {
            pulseIndicator.classList.add('animate-pulse-slow');
        }
    }
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === nmapModal) {
            nmapModal.classList.add('hidden');
        }
    });
    
    // Add keyboard shortcut to close modal (Escape key)
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && !nmapModal.classList.contains('hidden')) {
            nmapModal.classList.add('hidden');
        }
    });
    
    // Navigation is now simplified with horizontal links only
});