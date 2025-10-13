"""
Gradio Web Interface for Faster RCNN Fire Detection
Convenient interface for using the fire detection neural network
"""

import numpy as np
import cv2
import torch
import os
import yaml
import gradio as gr
from PIL import Image
import tempfile

from models.create_fasterrcnn_model import create_model
from utils.annotations import inference_annotations
from utils.transforms import infer_transforms

# Environment variables for deployment configuration
GRADIO_SHARE = os.environ.get('GRADIO_SHARE', 'False').lower() in ('true', '1', 't')
GRADIO_SERVER_NAME = os.environ.get('GRADIO_SERVER_NAME', '0.0.0.0')
GRADIO_SERVER_PORT = int(os.environ.get('GRADIO_SERVER_PORT', '7860'))
GRADIO_AUTH = os.environ.get('GRADIO_AUTH', None)  # Format: "username:password"


class FireDetectionApp:
    def __init__(self):
        self.model = None
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.classes = None
        self.colors = None
        self.num_classes = None
        
    def load_model(self, weights_path, config_path=None, model_name=None):
        """Load the model with weights"""
        np.random.seed(42)
        
        # Load data configurations
        data_configs = None
        if config_path and os.path.exists(config_path):
            with open(config_path) as file:
                data_configs = yaml.safe_load(file)
            self.num_classes = data_configs['NC']
            self.classes = data_configs['CLASSES']
        
        # Load pretrained model
        if weights_path and os.path.exists(weights_path):
            checkpoint = torch.load(weights_path, map_location=self.device)
            # If config file is not given, load from model dictionary
            if data_configs is None:
                self.num_classes = checkpoint['config']['NC']
                self.classes = checkpoint['config']['CLASSES']
            try:
                if model_name:
                    build_model = create_model[model_name]
                else:
                    build_model = create_model[checkpoint['model_name']]
            except:
                build_model = create_model['fasterrcnn_resnet50_fpn']
            self.model = build_model(num_classes=self.num_classes, coco_model=False)
            self.model.load_state_dict(checkpoint['model_state_dict'])
        else:
            # Use default COCO model if no weights provided
            if data_configs is None:
                self.classes = ['__background__', 'fire', 'smoke']
                self.num_classes = len(self.classes)
            build_model = create_model['fasterrcnn_resnet50_fpn']
            self.model = build_model(num_classes=self.num_classes, coco_model=True)
        
        self.model.to(self.device).eval()
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        
        return f"✅ Model loaded successfully! Device: {self.device}"
    
    def detect_image(self, image, threshold):
        """Detect objects in image"""
        if self.model is None:
            return None, "❌ Please load a model first!"
        
        if image is None:
            return None, "❌ Please upload an image!"
        
        # Convert PIL Image to OpenCV format
        image = np.array(image)
        orig_image = image.copy()
        
        # BGR to RGB (PIL is already RGB)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2RGB)
        image_tensor = infer_transforms(image_rgb)
        
        # Add batch dimension
        image_tensor = torch.unsqueeze(image_tensor, 0)
        
        # Get predictions
        with torch.no_grad():
            outputs = self.model(image_tensor.to(self.device))
        
        # Load all detections to CPU
        outputs = [{k: v.to('cpu') for k, v in t.items()} for t in outputs]
        
        # Annotate image
        result_image = orig_image.copy()
        detections_info = ""
        
        if len(outputs[0]['boxes']) != 0:
            result_image = inference_annotations(
                outputs, threshold, self.classes,
                self.colors, result_image
            )
            
            # Count detections per class
            labels = outputs[0]['labels'].cpu().numpy()
            scores = outputs[0]['scores'].cpu().numpy()
            
            # Filter by threshold
            valid_indices = scores >= threshold
            filtered_labels = labels[valid_indices]
            filtered_scores = scores[valid_indices]
            
            detections_info = f"📊 **Detections found:** {len(filtered_labels)}\n\n"
            
            # Group by class
            for class_id in np.unique(filtered_labels):
                class_name = self.classes[class_id]
                count = np.sum(filtered_labels == class_id)
                avg_conf = np.mean(filtered_scores[filtered_labels == class_id])
                detections_info += f"- **{class_name}**: {count} (avg confidence: {avg_conf:.2f})\n"
        else:
            detections_info = "ℹ️ No detections found with the current threshold."
        
        return result_image, detections_info
    
    def detect_video(self, video, threshold, progress=gr.Progress()):
        """Detect objects in video"""
        if self.model is None:
            return None, "❌ Please load a model first!"
        
        if video is None:
            return None, "❌ Please upload a video!"
        
        # Open video
        cap = cv2.VideoCapture(video)
        
        # Get video properties
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Create temporary output file
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
        
        frame_count = 0
        detections_summary = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Update progress
            progress((frame_count / total_frames, f"Processing frame {frame_count}/{total_frames}"))
            
            # Prepare image
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_tensor = infer_transforms(image)
            image_tensor = torch.unsqueeze(image_tensor, 0)
            
            # Get predictions
            with torch.no_grad():
                outputs = self.model(image_tensor.to(self.device))
            
            # Load detections to CPU
            outputs = [{k: v.to('cpu') for k, v in t.items()} for t in outputs]
            
            # Annotate frame
            if len(outputs[0]['boxes']) != 0:
                frame = inference_annotations(
                    outputs, threshold, self.classes,
                    self.colors, frame
                )
                
                # Count detections
                labels = outputs[0]['labels'].cpu().numpy()
                scores = outputs[0]['scores'].cpu().numpy()
                valid_indices = scores >= threshold
                filtered_labels = labels[valid_indices]
                detections_summary.append(len(filtered_labels))
            else:
                detections_summary.append(0)
            
            out.write(frame)
            frame_count += 1
        
        cap.release()
        out.release()
        
        # Generate summary
        total_detections = sum(detections_summary)
        avg_detections = total_detections / frame_count if frame_count > 0 else 0
        frames_with_detections = sum(1 for d in detections_summary if d > 0)
        
        summary = f"""
        📹 **Video Processing Complete**
        
        - **Total frames processed**: {frame_count}
        - **Frames with detections**: {frames_with_detections} ({frames_with_detections/frame_count*100:.1f}%)
        - **Total detections**: {total_detections}
        - **Average detections per frame**: {avg_detections:.2f}
        """
        
        return output_path, summary


def create_interface():
    """Create Gradio interface"""
    app = FireDetectionApp()
    
    # Custom CSS for better styling
    custom_css = """
    .gradio-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    """
    
    with gr.Blocks(css=custom_css, title="Fire Detection System") as demo:
        # Header
        gr.HTML("""
        <div class="header">
            <h1>🔥 Faster RCNN Fire Detection System</h1>
            <p>Convenient web interface for fire and smoke detection using neural networks</p>
        </div>
        """)
        
        # Model loading section
        with gr.Accordion("⚙️ Model Configuration", open=True):
            with gr.Row():
                weights_input = gr.File(
                    label="Model Weights (.pth)",
                    file_types=['.pth'],
                    type="filepath"
                )
                config_input = gr.File(
                    label="Config File (optional, .yaml)",
                    file_types=['.yaml', '.yml'],
                    type="filepath"
                )
            
            with gr.Row():
                model_name = gr.Dropdown(
                    choices=['fasterrcnn_resnet50_fpn', 'fasterrcnn_resnet50_fpn_v2'],
                    value='fasterrcnn_resnet50_fpn_v2',
                    label="Model Architecture"
                )
                load_btn = gr.Button("🔄 Load Model", variant="primary")
            
            model_status = gr.Textbox(label="Model Status", interactive=False)
        
        # Tabs for different detection modes
        with gr.Tabs():
            # Image detection tab
            with gr.Tab("📷 Image Detection"):
                with gr.Row():
                    with gr.Column():
                        image_input = gr.Image(
                            type="pil",
                            label="Upload Image"
                        )
                        image_threshold = gr.Slider(
                            minimum=0.1,
                            maximum=1.0,
                            value=0.5,
                            step=0.05,
                            label="Detection Threshold"
                        )
                        image_detect_btn = gr.Button("🔍 Detect Objects", variant="primary")
                    
                    with gr.Column():
                        image_output = gr.Image(label="Detection Result")
                        image_info = gr.Markdown(label="Detection Info")
                
                gr.Examples(
                    examples=[],
                    inputs=image_input,
                    label="Example Images (add your own)"
                )
            
            # Video detection tab
            with gr.Tab("🎥 Video Detection"):
                with gr.Row():
                    with gr.Column():
                        video_input = gr.Video(label="Upload Video")
                        video_threshold = gr.Slider(
                            minimum=0.1,
                            maximum=1.0,
                            value=0.5,
                            step=0.05,
                            label="Detection Threshold"
                        )
                        video_detect_btn = gr.Button("🔍 Process Video", variant="primary")
                    
                    with gr.Column():
                        video_output = gr.Video(label="Processed Video")
                        video_info = gr.Markdown(label="Processing Info")
            
            # Webcam detection tab
            with gr.Tab("📹 Webcam Detection"):
                gr.Markdown("""
                ### Real-time Webcam Detection
                
                **Note**: For real-time webcam detection, use the image detection tab with your webcam.
                You can also use the command line interface for better real-time performance:
                
                ```bash
                python inference_video.py --input 0 --weights your_model.pth --show-image
                ```
                """)
        
        # Instructions section
        with gr.Accordion("📖 Instructions", open=False):
            gr.Markdown("""
            ### How to Use
            
            1. **Load Model**:
               - Upload your trained model weights (.pth file)
               - Optionally, upload a config file (.yaml)
               - Select the model architecture
               - Click "Load Model"
            
            2. **Image Detection**:
               - Upload an image
               - Adjust the detection threshold (higher = fewer, more confident detections)
               - Click "Detect Objects"
            
            3. **Video Detection**:
               - Upload a video file
               - Adjust the detection threshold
               - Click "Process Video" (this may take a while for long videos)
            
            ### Tips
            - **Threshold**: Start with 0.5 and adjust based on results
              - Lower (0.3): More detections, may include false positives
              - Higher (0.7): Fewer, more confident detections
            - **Performance**: GPU is recommended for video processing
            - **Supported formats**: JPG, PNG for images; MP4, AVI for videos
            
            ### Default Model
            If no weights are provided, the system will use a COCO pretrained model.
            For fire detection, please train your own model using `train.py`.
            """)
        
        # Footer
        gr.Markdown("""
        ---
        <center>
        
        **Faster RCNN Fire Detection** | Powered by PyTorch and Gradio
        
        [GitHub Repository](https://github.com/Sabal1ne/fasterrcnn_fire-detection) | 
        [Documentation](https://github.com/Sabal1ne/fasterrcnn_fire-detection/blob/main/README.md)
        
        </center>
        """)
        
        # Event handlers
        load_btn.click(
            fn=lambda w, c, m: app.load_model(w, c, m),
            inputs=[weights_input, config_input, model_name],
            outputs=model_status
        )
        
        image_detect_btn.click(
            fn=lambda img, thresh: app.detect_image(img, thresh),
            inputs=[image_input, image_threshold],
            outputs=[image_output, image_info]
        )
        
        video_detect_btn.click(
            fn=lambda vid, thresh: app.detect_video(vid, thresh),
            inputs=[video_input, video_threshold],
            outputs=[video_output, video_info]
        )
    
    return demo


if __name__ == "__main__":
    demo = create_interface()
    
    # Parse authentication if provided
    auth = None
    if GRADIO_AUTH:
        auth_parts = GRADIO_AUTH.split(':')
        if len(auth_parts) == 2:
            auth = (auth_parts[0], auth_parts[1])
    
    demo.launch(
        server_name=GRADIO_SERVER_NAME,
        server_port=GRADIO_SERVER_PORT,
        share=GRADIO_SHARE,
        show_error=True,
        auth=auth
    )
