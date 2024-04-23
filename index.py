import gradio as gr
import cv2
import os
import moviepy.editor as moviepy
import yaml
import requests
from dotenv import load_dotenv

load_dotenv()
vdms = os.environ.get(".VDMS")
sessionID = os.environ.get("ASP.NET_SessionId")

inputs_image = [
    gr.components.Image(type="filepath", label="Input Image")
]

outputs_image = [
    gr.components.Image(type="numpy", label="Output Image"),
    gr.components.Label(label="Output labels")
]

inputs_video = [
    gr.components.Video()
]

outputs_video = [
    gr.components.Video(format='mp4')
]

outputs_cctv = [
    gr.components.Image(),
    gr.components.Label(label="Output labels")
]

def show_preds_image(image_path):
    cv2.imwrite("test_images\\test_img.jpg", cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB))
    labelsPath = "labeled_images\\labels\\test_img.txt"
    if os.path.exists(labelsPath):
        os.remove(labelsPath)
    else:
        print("The file does not exist")
    
    os.system(f"cd YOLOv6 && python tools/infer.py --weights ..\\trained_model\\weights\\best_ckpt.pt --yaml ..\\dataset\\data.yaml --save-dir ..\\labeled_images --source ..\\test_images\\test_img.jpg --save-txt")
    with open('dataset\\data.yaml', 'r') as file:
        classesName = yaml.safe_load(file)['names']
    classesInImage = {}
    try:
        labels = open(labelsPath, 'r')
    except FileNotFoundError:
        labels = []
    total = 0
    for line in labels:
        classIndex = int(line.split(' ')[0])
        name = classesName[classIndex]
        if classesInImage.get(name, None) == None:
            classesInImage[name] = 1
        else:
            classesInImage[name] += 1
        total += 1
    for name in classesName:
        if total == 0:
            break
        if classesInImage.get(name, None) != None:
            newName = name + ': ' + str(classesInImage[name])
            classesInImage[newName] = classesInImage.pop(name)
            classesInImage[newName] /= total
    print(classesInImage)
    return cv2.imread("labeled_images\\test_img.jpg"), classesInImage

def show_preds_video(video_path):
    filename = video_path.split("\\")[-1]
    os.system(f"cd YOLOv6 && python tools/infer.py --weights ..\\trained_model\\weights\\best_ckpt.pt --yaml ..\\dataset\\data.yaml --save-dir ..\\labeled_videos --source {video_path}")
    outpath = f"labeled_videos\\{filename}"
    outpathConverted = "labeled_videos\\out_vid.mp4"
    clip = moviepy.VideoFileClip(outpath)
    clip.write_videofile(outpathConverted, codec='libx264')
    clip.close()
    return outpathConverted

def show_preds_cctv(_, VDMS, SessId):
    cctvUrl = 'http://giaothong.hochiminhcity.gov.vn:8007/Render/CameraHandler.ashx?id=56df8159c062921100c143dc&bg=black&w=640&h=640&t=1713849941612'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'}
    cookies = {
        '.VDMS': vdms,
        'ASP.NET_SessionId': sessionID
    }
    labelsPath = "labeled_images\\labels\\cctv.txt"
    if os.path.exists(labelsPath):
        os.remove(labelsPath)
    else:
        print("The file does not exist")
    
    response = requests.get(cctvUrl, headers=header, cookies=cookies)
    if response.status_code == 200:
        with open("test_images\\cctv.jpg", 'wb') as f:
            f.write(response.content)
    os.system(f"cd YOLOv6 && python tools/infer.py --weights ..\\trained_model\\weights\\best_ckpt.pt --yaml ..\\dataset\\data.yaml --save-dir ..\\labeled_images --source ..\\test_images\\cctv.jpg --save-txt")
    with open('dataset\\data.yaml', 'r') as file:
        classesName = yaml.safe_load(file)['names']
    classesInImage = {}
    try:
        labels = open(labelsPath, 'r')
    except FileNotFoundError:
        labels = []
    total = 0
    for line in labels:
        classIndex = int(line.split(' ')[0])
        name = classesName[classIndex]
        if classesInImage.get(name, None) == None:
            classesInImage[name] = 1
        else:
            classesInImage[name] += 1
        total += 1
    for name in classesName:
        if total == 0:
            break
        if classesInImage.get(name, None) != None:
            newName = name + ': ' + str(classesInImage[name])
            classesInImage[newName] = classesInImage.pop(name)
            classesInImage[newName] /= total
    print(classesInImage)
    return cv2.cvtColor(cv2.imread("labeled_images\\cctv.jpg"), cv2.COLOR_BGR2RGB), classesInImage

interface_image = gr.Interface(
    fn=show_preds_image, 
    inputs=inputs_image, 
    outputs=outputs_image,
    title="Vehicle Traffic Detection - Image",
    cache_examples=False
)

interface_video = gr.Interface(
    fn=show_preds_video, 
    inputs=inputs_video, 
    outputs=outputs_video,
    title="Vehicle Traffic Detection - Video"
)

interface_cctv = gr.Interface(
    fn=show_preds_cctv,
    inputs=outputs_cctv, 
    outputs=outputs_cctv,
    title="Vehicle Traffic Detection - CCTV View"
)

mainInterface = gr.TabbedInterface(
    [interface_image, interface_video, interface_cctv],
    tab_names=["Image input", "Video input", "CCTV View"]
)
mainInterface.queue().launch()
