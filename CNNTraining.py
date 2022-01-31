
import matplotlib.pyplot as plt
import imagesize
import numpy as np
import os
import cv2
import pickle 

'''
# Get the Image Resolutions
root = "/home/darryen/Documents/Dataset/"
imgs = [img.name for img in Path(root).iterdir() if img.suffix == ".png"]
img_meta = {}
for f in imgs: img_meta[str(f)] = imagesize.get(root+f)

# Convert it to Dataframe and compute aspect ratio
img_meta_df = pd.DataFrame.from_dict([img_meta]).T.reset_index().set_axis(['FileName', 'Size'], axis='columns', inplace=False)
img_meta_df[["Width", "Height"]] = pd.DataFrame(img_meta_df["Size"].tolist(), index=img_meta_df.index)
img_meta_df["Aspect Ratio"] = round(img_meta_df["Width"] / img_meta_df["Height"], 2)

print(f'Total Nr of Images in the dataset: {len(img_meta_df)}')
print(img_meta_df.head())
'''


classNames = ["Signal", "Noise"] # These are the names of the folders 
directory = "/home/darryen/Documents/thesis-project-2021/Dataset/"
trainingData = []
imgSize = 400

def CreateTrainingData():
    for category in classNames:
        path = os.path.join(directory, category)
        classNumber = classNames.index(category)
        for img in os.listdir(path):
            imgArray = cv2.imread(os.path.join(path, img), cv2.IMREAD_UNCHANGED)
            print('Original Dimensions : ',imgArray.shape)
            newArray = cv2.resize(imgArray, (imgSize, imgSize))
            print('Resized Dimensions : ',newArray.shape)
            trainingData.append([newArray, classNumber])
           

CreateTrainingData()




#np.random.shuffle(trainingData)

X = [] # The features (e.g the image data)
y = [] # The labels (e.g. Whether the image has a signal or not)

for features, label in trainingData:
    X.append(features)
    y.append(label)

X = np.array(X)
y = np.array(y)

print(X.shape[0])
print(y.shape[0])

pickle_out = open("X.pickle", "wb")
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open("y.pickle", "wb")
pickle.dump(y, pickle_out)
pickle_out.close()

pickle_in = open("X.pickle", "rb")
X = pickle.load(pickle_in)
