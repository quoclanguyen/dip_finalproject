from zipfile import ZipFile 
import requests
from tqdm import tqdm
  
file_name = "dataset.zip"
downloadUrl = "https://drive.usercontent.google.com/download?id=1TUAU_FBA20IM8mhR9hTR_BH-wI-t1niv&export=download&authuser=0&confirm=t&uuid=3f7d1797-0167-4f40-b7f0-033b330df92e&at=APZUnTUHY-8yedRo05kqZ5q07rr3%3A1713027117725"

def download_file(url, filename):
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get('content-length', 0))
    progress_bar = tqdm(total=file_size, unit='B', unit_scale=True)
    with open(filename, 'wb') as file:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            progress_bar.update(len(data))
    progress_bar.close()

download_file(downloadUrl, file_name)

with ZipFile(file_name, 'r') as zip: 
    zip.printdir() 
    print('Extracting all the files now...') 
    zip.extractall()
    print('Done!') 