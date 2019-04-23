from PIL import Image
import torchvision
import glob
import os
allFiles = glob.glob("*.jpg") #may not work on collab
toTen = torchvision.transforms.ToTensor()
#dont count black padding, value not exactly 0 for padding though padding is 0, 0, 0;
def averageChannel(imgTensorChannel, height, width):
  total = 0.0
  pixels = 0
  excludePadding = 0
  for i in range(0,height):
    for j in range(0,width):
      if(imgTensorChannel[i][j]==0):
        excludePadding+=1
      else:
        total += imgTensorChannel[i][j]
  if(excludePadding == height*width):
    print("wacky image all H or S or V is 0")
  return total/(height*width - excludePadding + 1)
imageSummaries = []  
q=0
for imgName in allFiles:
  q+=1
  if(q%50==0):
    print(q)
  img = Image.open(imgName)
  img = img.convert('HSV')
  img = toTen(img)
  try:
    (h,s,v) = (averageChannel(img[0],len(img[0]),len(img[0][0])),averageChannel(img[1],len(img[1]),len(img[1][0])),averageChannel(img[2],len(img[2]),len(img[2][0])))
    tup = (imgName,h.item(),s.item(),v.item())
    imageSummaries.append(tup)
    if(h.item()==0 or s.item()==0 or v.item()==0):
      print(imgName)
      print("all zeros")
  except:
    print(imgName)
    print("is corrupted")
from sklearn.cluster import KMeans
kmeansList = []
for imgSummary in imageSummaries:
  kmeansList.append(imgSummary[1:4])
km = KMeans(n_clusters=2,random_state=0).fit(kmeansList)
x = km.labels_
y = [i[0] for i in imageSummaries] #print just filenames
renaming = zip(x,y)
for i in renaming:
  old = f'{i[1]}'
  new = f'cstr_{i[0]}_{i[1]}'
  try:
    os.rename(old,new)
  except:
    prefix = old[9:]
    new = f'cstr_{i[0]}_{prefix}'
    os.rename(old,new)
