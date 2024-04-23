cd YOLOv6
python tools/infer.py --weights ..\trained_model\weights\best_ckpt.pt --yaml ..\dataset\data.yaml --save-dir ..\labeled_images --source ..\test_images\a.jpg