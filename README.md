# UA-DETRAC-Format-Converter
Convert [UA-DETRAC](url) dataset to the dataset format supported by YOLOv5

## 快速开始

1. 首先下载数据集 [UA-DETRAC](url) 到在你希望生成 YOLOv5 所支持格式数据集的根目录下，并将 process.py 文件放在该目录下。例如：

```
├── UA-DETRAC
│   ├── Insight-MVT_Annotation_Train
│   ├── Insight-MVT_Annotation_Test
│   ├── DETRAC-Train-Annotations-XML
│   ├── DETRAC-Test-Annotations-XML
│   └── process.py
├── yolov5
│   └── ......
```

进入到 UA-DETRAC 目录下
```
$ cd UA-DETRAC
```
并执行：
```
$ python process.py
```
等待程序执行完毕，生成 YOLOv5 所支持格式数据集：
```
├── UA-DETRAC
│   ├── Insight-MVT_Annotation_Train
│   ├── Insight-MVT_Annotation_Test
│   ├── DETRAC-Train-Annotations-XML
│   ├── DETRAC-Test-Annotations-XML
│   ├── images
│   │   ├── train
│   │   │   ├── MVI_20011_img00053.jpg
│   │   │   └── ......
│   │   └── val
│   │       ├── MVI_39031_img00164.jpg
│   │       └── ......
│   ├── labels
│   │   ├── train
│   │   │   ├── MVI_20011_img00053.txt
│   │   │   └── ......
│   │   └── val
│   │       ├── MVI_39031_img00164.txt
│   │       └── ......
│   └── process.py
├── yolov5
│   └── ......

```
最后在 YOLOv5 项目中[添加数据集配置文件](url)，并将如下代码填写入文件内：

```
path: ../UA-DETRAC
train: images/train
val: images/val
test:

nc: 5
names: ['others', 'car', 'van', 'bus']
```

