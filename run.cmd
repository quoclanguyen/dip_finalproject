cd YOLOv6
python tools/infer.py --weights ..\trained_model\weights\best_ckpt.pt --yaml ..\dataset\data.yaml --save-dir ..\labeled_images --source ..\test_images\a.jpg


python tools/infer.py --weights ..\\trained_model\\weights\\best_ckpt.pt --yaml ..\\dataset\\data.yaml --save-dir ..\\labeled_images --source "http://giaothong.hochiminhcity.gov.vn:8007/Render/CameraHandler.ashx?id=5d8cdb4b766c880017188966&bg=black&w=300&h=230" --save-txt