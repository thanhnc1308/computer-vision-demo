import mmdet
from mmdet.apis import init_detector, inference_detector, show_result_pyplot
import mmcv
# Load model
config_file = './CascadeTabNet/Config/cascade_mask_rcnn_hrnetv2p_w32_20e.py'
checkpoint_file = './models/epoch_36.pth'
model = init_detector(config_file, checkpoint_file, device='cuda:0')

# Test a single image
# img = "/raw_image/CascadeTabNet/Demo/demo.png"

def show_result(img_path):
    # Run Inference
    result = inference_detector(model, img_path)

    # Visualization results
    show_result_pyplot(img_path, result,('Bordered', 'cell', 'Borderless'), score_thr=0.85)
