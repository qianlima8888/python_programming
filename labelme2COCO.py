# -*- coding: utf-8 -*-
import os
import json
import numpy as np
import glob
import shutil
from sklearn.model_selection import train_test_split
np.random.seed(41)
import cv2
#0为背景
classname_to_id = {'person': 1, 'bicycle': 2, 'car': 3, 'motorcycle': 4, 'airplane': 5, 'bus': 6, 'train': 7, 'truck': 8, 'boat': 9, 'traffic light': 10, 'fire hydrant': 11, 'stop sign': 13, 'parking meter': 14, 'bench': 15, 'bird': 16, 'cat': 17, 'dog': 18, 'horse': 19, 'sheep': 20, 'cow': 21, 'elephant': 22, 'bear': 23, 'zebra': 24, 'giraffe': 25, 'backpack': 27, 'umbrella': 28, 'handbag': 31, 'tie': 32, 'suitcase': 33, 'frisbee': 34, 'skis': 35, 'snowboard': 36, 'sports ball': 37, 'kite': 38, 'baseball bat': 39, 'baseball glove': 40, 'skateboard': 41, 'surfboard': 42, 'tennis racket': 43, 'bottle': 44, 'wine glass': 46, 'cup': 47, 'fork': 48, 'knife': 49, 'spoon': 50, 'bowl': 51, 'banana': 52, 'apple': 53, 'sandwich': 54, 'orange': 55, 'broccoli': 56, 'carrot': 57, 'hot dog': 58, 'pizza': 59, 'donut': 60, 'cake': 61, 'chair': 62, 'couch': 63, 'potted plant': 64, 'bed': 65, 'dining table': 67, 'toilet': 70, 'tv': 72, 'laptop': 73, 'mouse': 74, 'remote': 75, 'keyboard': 76, 'cell phone': 77, 'microwave': 78, 'oven': 79, 'toaster': 80, 'sink': 81, 'refrigerator': 82, 'book': 84, 'clock': 85, 'vase': 86, 'scissors': 87, 'teddy bear': 88, 'hair drier': 89, 'toothbrush': 90}
 
class Lableme2CoCo:
 
    def __init__(self):
        self.images = []
        self.annotations = []
        self.categories = []
        self.img_id = 0
        self.ann_id = 0
 
    def save_coco_json(self, instance, save_path):
        import io
        #json.dump(instance, io.open(save_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)  # indent=2 更加美观显示
        with io.open(save_path, 'w', encoding="utf-8") as outfile:
            my_json_str = json.dumps(instance, ensure_ascii=False, indent=1)
            if isinstance(my_json_str, str):
                my_json_str = my_json_str.encode('utf-8').decode('utf-8')
            outfile.write(my_json_str)
 
    # 由json文件构建COCO
    def to_coco(self, json_path_list):
        self._init_categories()
        for json_path in json_path_list:
            obj = self.read_jsonfile(json_path)
            self.images.append(self._image(obj, json_path))
            shapes = obj['shapes']
            for shape in shapes:
                annotation = self._annotation(shape)
                self.annotations.append(annotation)
                self.ann_id += 1
            self.img_id += 1
        instance = {}
        instance['info'] = 'spytensor created'
        instance['license'] = ['license']
        instance['images'] = self.images
        instance['annotations'] = self.annotations
        instance['categories'] = self.categories
        return instance
 
    # 构建类别
    def _init_categories(self):
        for k, v in classname_to_id.items():
            category = {}
            category['id'] = v
            category['name'] = k
            self.categories.append(category)
 
    # 构建COCO的image字段
    def _image(self, obj, path):
        image = {}
        from labelme import utils
        #img_x = utils.img_b64_to_arr(obj['imageData'])
        img_x = cv2.imread("d:\\data\\floor13_images\\"+str(obj['imagePath'])[-8:])#需要修改
        img_x = cv2.cvtColor(img_x, cv2.COLOR_BGR2RGB)
        h, w = img_x.shape[:-1]
        image['height'] = h
        image['width'] = w
        image['id'] = self.img_id
        image['file_name'] = os.path.basename(path).replace(".json", ".png")
        return image
 
    # 构建COCO的annotation字段
    def _annotation(self, shape):
        label = shape['label']
        #因为coco数据集中不包含door cabinet trash三类
        #因此将door --> pizza, cabinet --> donut, trash --> cake
        if(label == 'door'):
            label = 'pizza'
        if(label == 'cabinet'):
            label = 'donut'
        if(label == 'trash'):
            label = 'cake'
        points = shape['points']
        annotation = {}
        annotation['id'] = self.ann_id
        annotation['image_id'] = self.img_id
        annotation['category_id'] = int(classname_to_id[label])
        annotation['segmentation'] = [np.asarray(points).flatten().tolist()]
        annotation['bbox'] = self._get_box(points)
        annotation['iscrowd'] = 0
        annotation['area'] = 1.0
        return annotation
 
    # 读取json文件，返回一个json对象
    def read_jsonfile(self, path):
        import io
        #with io.open(path, "r", encoding='utf-8') as f:
        with open(path, "r") as f:
            return json.load(f)
 
    # COCO的格式： [x1,y1,w,h] 对应COCO的bbox格式
    def _get_box(self, points):
        min_x = min_y = np.inf
        max_x = max_y = 0
        for x, y in points:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        return [min_x, min_y, max_x - min_x, max_y - min_y]
 
 
if __name__ == '__main__':
    labelme_path = "D:\\data\\bob"
    saved_coco_path = "./"
    # 创建文件
    if not os.path.exists("%scoco/annotations/"%saved_coco_path):
        os.makedirs("%scoco/annotations/"%saved_coco_path)
    if not os.path.exists("%scoco/images/train2017/"%saved_coco_path):
        os.makedirs("%scoco/images/train2017"%saved_coco_path)
    if not os.path.exists("%scoco/images/val2017/"%saved_coco_path):
        os.makedirs("%scoco/images/val2017"%saved_coco_path)
    # 获取images目录下所有的joson文件列表
    json_list_path = glob.glob(labelme_path + "\\*.json")
    # 数据划分,这里没有区分val2017和tran2017目录，所有图片都放在images目录下
    train_path, val_path = train_test_split(json_list_path, test_size=0.1, random_state=42)
    #val_path = train_path
    #train_path = []
    print("train_n:", len(train_path), 'val_n:', len(val_path))

    # 把训练集转化为COCO的json格式
    if len(train_path):
        l2c_train = Lableme2CoCo()
        train_instance = l2c_train.to_coco(train_path)
        l2c_train.save_coco_json(train_instance, '%scoco/annotations/instances_train2017.json'%saved_coco_path)
        for file in train_path:
            name = file.split('\\')[-1]
            name = "D:\\data\\floor13_images\\" + name
            shutil.copy(name.replace("json","png"),"%scoco/images/train2017/"%saved_coco_path)
 
    if len(val_path):
        # 把验证集转化为COCO的json格式
        l2c_val = Lableme2CoCo()
        val_instance = l2c_val.to_coco(val_path)
        l2c_val.save_coco_json(val_instance, '%scoco/annotations/instances_val2017.json'%saved_coco_path)
        for file in val_path:
            name = file.split('\\')[-1]
            name = "D:\\data\\floor13_images\\" + name
            shutil.copy(name.replace("json","png"),"%scoco/images/val2017/"%saved_coco_path)
    print(classname_to_id)