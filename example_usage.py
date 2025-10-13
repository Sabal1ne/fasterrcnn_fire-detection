"""
Example: Using the Fire Detection System Programmatically

This example shows how to use the FireDetectionApp class without the web interface.
Useful for automation, batch processing, or integration with other systems.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import FireDetectionApp
import numpy as np
from PIL import Image


def example_load_and_detect():
    """
    Example 1: Load model and detect objects in an image
    """
    print("=" * 60)
    print("Example 1: Load model and detect in image")
    print("=" * 60)
    
    # Initialize the app
    app = FireDetectionApp()
    
    # Load model (use your trained weights)
    weights_path = "outputs/training/your_model/best_model.pth"  # Change this
    config_path = "data_configs/fire.yaml"  # Optional
    
    if os.path.exists(weights_path):
        status = app.load_model(weights_path, config_path)
        print(status)
        
        # Load an image
        image_path = "path/to/your/image.jpg"  # Change this
        if os.path.exists(image_path):
            image = Image.open(image_path)
            
            # Detect objects
            result_image, detection_info = app.detect_image(image, threshold=0.5)
            
            print("\nDetection Results:")
            print(detection_info)
            
            # Save result
            if result_image is not None:
                output_path = "detection_result.jpg"
                Image.fromarray(result_image).save(output_path)
                print(f"\n✅ Result saved to: {output_path}")
        else:
            print(f"❌ Image not found: {image_path}")
    else:
        print(f"❌ Model weights not found: {weights_path}")
        print("Train a model first using: python train.py --config data_configs/fire.yaml")


def example_batch_processing():
    """
    Example 2: Batch process multiple images
    """
    print("\n" + "=" * 60)
    print("Example 2: Batch process multiple images")
    print("=" * 60)
    
    app = FireDetectionApp()
    
    # Load model
    weights_path = "outputs/training/your_model/best_model.pth"
    
    if os.path.exists(weights_path):
        app.load_model(weights_path)
        
        # Process multiple images
        image_folder = "data/test_images/"  # Change this
        output_folder = "outputs/batch_results/"
        
        if os.path.exists(image_folder):
            os.makedirs(output_folder, exist_ok=True)
            
            image_files = [f for f in os.listdir(image_folder) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            print(f"\nProcessing {len(image_files)} images...")
            
            for i, image_file in enumerate(image_files):
                image_path = os.path.join(image_folder, image_file)
                image = Image.open(image_path)
                
                # Detect
                result_image, info = app.detect_image(image, threshold=0.5)
                
                # Save
                output_path = os.path.join(output_folder, f"result_{image_file}")
                Image.fromarray(result_image).save(output_path)
                
                print(f"[{i+1}/{len(image_files)}] Processed: {image_file}")
            
            print(f"\n✅ All results saved to: {output_folder}")
        else:
            print(f"❌ Folder not found: {image_folder}")
    else:
        print(f"❌ Model weights not found: {weights_path}")


def example_custom_threshold_testing():
    """
    Example 3: Test different thresholds on the same image
    """
    print("\n" + "=" * 60)
    print("Example 3: Test different detection thresholds")
    print("=" * 60)
    
    app = FireDetectionApp()
    
    weights_path = "outputs/training/your_model/best_model.pth"
    image_path = "path/to/test/image.jpg"
    
    if os.path.exists(weights_path) and os.path.exists(image_path):
        app.load_model(weights_path)
        image = Image.open(image_path)
        
        thresholds = [0.3, 0.5, 0.7, 0.9]
        
        print(f"\nTesting image: {image_path}")
        print("-" * 60)
        
        for threshold in thresholds:
            result_image, info = app.detect_image(image, threshold=threshold)
            
            # Extract number of detections
            num_detections = info.count("**Detections found:**")
            
            print(f"\nThreshold: {threshold}")
            print(info)
            
            # Save result
            output_path = f"threshold_{threshold}_result.jpg"
            Image.fromarray(result_image).save(output_path)
        
        print("\n✅ Threshold comparison complete!")
    else:
        if not os.path.exists(weights_path):
            print(f"❌ Model weights not found: {weights_path}")
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")


def example_model_comparison():
    """
    Example 4: Compare different model architectures
    """
    print("\n" + "=" * 60)
    print("Example 4: Compare model architectures")
    print("=" * 60)
    
    models = {
        "ResNet50 FPN": {
            "weights": "outputs/training/fpn_model/best_model.pth",
            "name": "fasterrcnn_resnet50_fpn"
        },
        "ResNet50 FPN V2": {
            "weights": "outputs/training/fpn_v2_model/best_model.pth",
            "name": "fasterrcnn_resnet50_fpn_v2"
        }
    }
    
    image_path = "path/to/test/image.jpg"
    
    if os.path.exists(image_path):
        image = Image.open(image_path)
        
        for model_name, model_info in models.items():
            if os.path.exists(model_info["weights"]):
                print(f"\n--- Testing {model_name} ---")
                
                app = FireDetectionApp()
                app.load_model(
                    model_info["weights"],
                    model_name=model_info["name"]
                )
                
                result_image, info = app.detect_image(image, threshold=0.5)
                print(info)
                
                # Save result
                output_path = f"{model_name.replace(' ', '_')}_result.jpg"
                Image.fromarray(result_image).save(output_path)
            else:
                print(f"\n❌ Model not found: {model_info['weights']}")
        
        print("\n✅ Model comparison complete!")
    else:
        print(f"❌ Image not found: {image_path}")


def print_usage():
    """Print usage instructions"""
    print("""
╔════════════════════════════════════════════════════════════╗
║  Fire Detection System - Programmatic Usage Examples      ║
╚════════════════════════════════════════════════════════════╝

This script demonstrates how to use the FireDetectionApp class
without the web interface.

Available examples:
1. Load model and detect in single image
2. Batch process multiple images
3. Test different detection thresholds
4. Compare different model architectures

To run an example, uncomment the corresponding function call
at the bottom of this script.

For web interface, use:
    python launch_ui.py

For command line inference, use:
    python inference.py --input image.jpg --weights model.pth

Documentation:
- README.md          - Main documentation
- WEB_INTERFACE.md   - Web interface guide
- QUICKSTART.md      - Getting started guide
    """)


if __name__ == "__main__":
    print_usage()
    
    print("\n" + "=" * 60)
    print("NOTE: Update file paths in the script before running!")
    print("=" * 60)
    
    # Uncomment the example you want to run:
    
    # example_load_and_detect()
    # example_batch_processing()
    # example_custom_threshold_testing()
    # example_model_comparison()
    
    print("\n💡 To run the web interface instead, use: python launch_ui.py")
