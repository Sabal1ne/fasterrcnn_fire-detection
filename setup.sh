#!/bin/bash
# Quick setup script for the project

echo "========================================="
echo "Faster RCNN Fire Detection Setup"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version detected"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create data directories
echo "Creating data directories..."
mkdir -p data/train
mkdir -p data/test
mkdir -p outputs/training
mkdir -p outputs/inference
echo "✓ Data directories created"
echo ""

# Print next steps
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Add your images and XML annotations to:"
echo "   - data/train/ (training data)"
echo "   - data/test/ (validation data)"
echo ""
echo "2. Configure your dataset in data_configs/"
echo "   (or use existing fire.yaml or ppe.yaml)"
echo ""
echo "3. Start training:"
echo "   python train.py --model fasterrcnn_resnet50_fpn_v2 \\"
echo "                   --config data_configs/fire.yaml \\"
echo "                   --epochs 50 \\"
echo "                   --project-name my_project"
echo ""
echo "For more information, see README.md"
echo ""
