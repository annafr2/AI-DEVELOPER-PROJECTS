#!/bin/bash
# Global Virtual Environment Activation Script for D25 Projects
# Usage: source activate_global.sh

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate the global virtual environment
source "$SCRIPT_DIR/venv_global/bin/activate"

echo "Global D25 virtual environment activated!"
echo "Python: $(which python)"
echo "All packages from requirements.txt are available."
echo ""
echo "To deactivate, run: deactivate"
