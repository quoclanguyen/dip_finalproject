import gradio as gr
import cv2
import os
import moviepy.editor as moviepy
import yaml

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

gr.TabbedInterface(
    [interface_image, interface_video],
    tab_names=["Image input", "Video input"]
).queue().launch()
