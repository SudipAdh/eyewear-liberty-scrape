from glob import glob
import pandas as pd
import requests
import boto3

df = pd.read_csv("./liberty_import.csv")

jpeg_files = glob("./*.jpeg")
def requester_and_uploader(x):
    if x and not isinstance(x, float):
        file_name = x.rsplit("/", 1)[-1].split(".")[0]+".jpeg"
        if not "./"+file_name in jpeg_files:
            resp = requests.get(x, stream=True)
            file = open(file_name, "wb")
            file.write(resp.content)
            print("NEW");
        else:
            print("Already Done")
        

df["Image Src"] = df["Image Src"].apply(requester_and_uploader)