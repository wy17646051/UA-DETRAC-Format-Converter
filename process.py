import argparse
import os
import shutil
from xml.dom.minidom import parse
from tqdm import tqdm


def create_labels(root_node, labels_root):
    img_w = 960
    img_h = 540

    frames = root_node.getElementsByTagName('frame')
    for frame in frames:
        seq_gt = []
        """3903100001"""
        frame_num = frame.getAttribute("num")
        frame_num = frame_num.zfill(5)
        label_name = root_node.getAttribute("name") + '_img' + frame_num

        img_root = './images/train/' if 'train' in labels_root else './images/val/'
        sample_img = os.listdir(img_root)
        if (label_name + '.jpg') in sample_img:
            label_path = os.path.join(labels_root, label_name + '.txt')

            targets = frame.getElementsByTagName('target_list')[0].getElementsByTagName('target')
            for target in targets:
                box = target.getElementsByTagName('box')[0]
                left = float(box.getAttribute('left'))
                top = float(box.getAttribute('top'))
                width = float(box.getAttribute('width'))
                height = float(box.getAttribute('height'))
                type = target.getElementsByTagName('attribute')[0].getAttribute('vehicle_type')
                if type == "car":
                    type = 1
                elif type == "van":
                    type = 2
                elif type == "bus":
                    type = 3
                else:
                    type = 0

                # 中心坐标
                x = left + width / 2
                y = top + height / 2
                # 宽高中心坐标归一化
                x /= img_w
                y /= img_h
                width = width / img_w
                height = height / img_h

                seq_gt.append(str(type) + ' ' + str(round(x, 6)) + ' ' + str(round(y, 6)) + ' ' + str(
                    round(width, 6)) + ' ' + str(round(height, 6)))

            with open(label_path, 'w') as f:
                for i in seq_gt:
                    f.write(i + '\n')


def yolo_img_train(opt):
    # train img
    os.makedirs('./images/train')
    for video_name in tqdm(os.listdir(opt.img_train)):
        if 'MVI' in video_name:
            stride = int(1.0 / opt.sample)
            for i, img_name in enumerate(os.listdir(os.path.join(opt.img_train, video_name))):
                if ((i % stride) == 0) & ('.jpg' in img_name):
                    ori_path = os.path.join(opt.img_train, video_name, img_name)
                    new_path = os.path.join('./images/train/', video_name + '_' + img_name)
                    shutil.copyfile(ori_path, new_path)
    print('YOLO training set image has been generated.')


def yolo_img_val(opt):
    # val img
    os.makedirs('./images/val')
    for video_name in tqdm(os.listdir(opt.img_val)):
        if 'MVI' in video_name:
            stride = int(1.0 / opt.sample)
            for i, img_name in enumerate(os.listdir(os.path.join(opt.img_val, video_name))):
                if ((i % stride) == 0) & ('.jpg' in img_name):
                    ori_path = os.path.join(opt.img_val, video_name, img_name)
                    new_path = os.path.join('./images/val/', video_name + '_' + img_name)
                    shutil.copyfile(ori_path, new_path)
    print('YOLO validation set image has been generated.')


def gen_yolo_dataset(opt):
    yolo_img_train(opt)
    yolo_img_val(opt)

    # train label
    os.makedirs('./labels/train')
    for video_xml in tqdm(os.listdir(opt.lbl_train)):
        if '.xml' in video_xml:
            create_labels(parse(os.path.join(opt.lbl_train, video_xml)).documentElement, './labels/train/')
    print('YOLO training set label has been generated.')

    # val label
    os.makedirs('./labels/val')
    for video_xml in tqdm(os.listdir(opt.lbl_val)):
        if '.xml' in video_xml:
            create_labels(parse(os.path.join(opt.lbl_val, video_xml)).documentElement, './labels/val/')
    print('YOLO validation set label has been generated.')

    print('Mission accomplished.')


def parse_opt():
    parser = argparse.ArgumentParser(prog='test.py')
    parser.add_argument('--img_train', type=str, default='./Insight-MVT_Annotation_Train/', help='train images path')
    parser.add_argument('--img_val', type=str, default='./Insight-MVT_Annotation_Test/', help='validation images path')
    parser.add_argument('--lbl_train', type=str, default='./DETRAC-Train-Annotations-XML/', help='train labels path')
    parser.add_argument('--lbl_val', type=str, default='./DETRAC-Test-Annotations-XML/', help='validation labels path')
    parser.add_argument('--sample', type=float, default=1.0, help='equidistant sampling ratio')
    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    gen_yolo_dataset(opt)






