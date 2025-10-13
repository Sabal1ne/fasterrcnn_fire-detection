#!/usr/bin/env python3
"""
Example script for training a fire detection model.

This script demonstrates basic usage of the training pipeline.
"""

import os
import sys

def check_data_directory():
    """Check if data directory exists and has required structure."""
    required_dirs = ['data/train', 'data/test']
    missing_dirs = [d for d in required_dirs if not os.path.exists(d)]
    
    if missing_dirs:
        print("❌ Missing required directories:")
        for d in missing_dirs:
            print(f"   - {d}")
        print("\nPlease create the data directories and add your images:")
        print("  mkdir -p data/train data/test")
        return False
    
    # Check if directories have images
    train_images = len([f for f in os.listdir('data/train') if f.endswith(('.jpg', '.png', '.jpeg'))])
    test_images = len([f for f in os.listdir('data/test') if f.endswith(('.jpg', '.png', '.jpeg'))])
    
    print(f"✓ Found {train_images} training images")
    print(f"✓ Found {test_images} test images")
    
    if train_images == 0 or test_images == 0:
        print("\n⚠️  Warning: No images found in data directories")
        return False
    
    return True

def main():
    """Main function to run training example."""
    print("=" * 60)
    print("Fire Detection Training Example")
    print("=" * 60)
    print()
    
    # Check data directory
    print("Checking data directory...")
    if not check_data_directory():
        print("\n❌ Data directory check failed.")
        print("Please prepare your dataset before running training.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Starting training with default parameters...")
    print("=" * 60)
    print()
    
    # Build training command
    cmd = [
        "python", "train.py",
        "--model", "fasterrcnn_resnet50_fpn_v2",
        "--config", "data_configs/fire.yaml",
        "--epochs", "50",
        "--batch-size", "4",
        "--project-name", "fire_detection_example",
        "--use-train-aug",
        "--no-mosaic"
    ]
    
    print("Training command:")
    print(" ".join(cmd))
    print()
    
    # Execute training
    os.system(" ".join(cmd))
    
    print("\n" + "=" * 60)
    print("Training completed!")
    print("=" * 60)
    print("\nTo run inference on an image:")
    print("python inference.py \\")
    print("  --input path/to/image.jpg \\")
    print("  --weights outputs/training/fire_detection_example/best_model.pth \\")
    print("  --threshold 0.5 \\")
    print("  --show-image")

if __name__ == "__main__":
    main()
