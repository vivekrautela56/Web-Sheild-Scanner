# Contributing to WebShield Scanner

Thank you for your interest in contributing to WebShield Scanner! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with the following information:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Environment details (OS, browser, etc.)

### Suggesting Enhancements

We welcome suggestions for enhancements! Please create an issue with:

- A clear, descriptive title
- A detailed description of the proposed enhancement
- Any relevant examples, mockups, or references

### Pull Requests

1. Fork the repository
2. Create a new branch from `main`
3. Make your changes
4. Run tests if available
5. Submit a pull request

#### Pull Request Guidelines

- Follow the existing code style
- Include comments where necessary
- Update documentation if needed
- Add tests for new features
- Ensure all tests pass

## Development Setup

1. Clone your fork of the repository
2. Create a virtual environment and activate it
3. Install dependencies with `pip install -r requirements.txt`
4. Make your changes
5. Test your changes locally before submitting a PR

## Project Structure

```
webshield-scanner/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
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
```

## Coding Standards

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Write docstrings for functions and classes
- Keep functions small and focused on a single task
- Comment complex code sections

## Testing

- Add tests for new features
- Ensure existing tests pass
- Test on different browsers and devices for frontend changes

## Documentation

- Update README.md if necessary
- Document new features or changes in behavior
- Include docstrings for new functions and classes

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.