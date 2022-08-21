import os
import file_process
from PIL import Image, ImageFilter
import imageio
import numpy as np
import math
import random
import shutil
import sys
import argparse

def copy_img_fold(source_path,target_path):
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    if os.path.exists(source_path):
        shutil.rmtree(target_path)

    shutil.copytree(source_path, target_path)
    print('copy dir finished!')


def rename_img(dir):
    dirpath = ""
    for i in range(0, 29):
        if i < 10:
            dirpath = dir + "000" + str(i)
        else:
            dirpath = dir + "00" + str(i)

        if os.path.exists(dirpath):
            filenames = file_process.get_file_name(dirpath)
            i = 0
            for name in filenames:
                if i < 10:
                    os.rename(os.path.join(dirpath, name),os.path.join(dirpath, "00000"+str(i)+".png"))
                elif i<100:
                    os.rename(os.path.join(dirpath, name), os.path.join(dirpath, "0000" + str(i) + ".png"))
                elif i<1000:
                    os.rename(os.path.join(dirpath, name), os.path.join(dirpath, "000" + str(i) + ".png"))
                else:
                    os.rename(os.path.join(dirpath, name), os.path.join(dirpath, "00" + str(i) + ".png"))
                i = i + 1
            print(str(dirpath)+ " rename finished")


# MR1-1
def delete_odd_img(source_path,target_path):
    copy_img_fold(source_path, target_path)
    target_path = target_path + "/"
    dirpath = ""
    for i in range(0,29):
        if i<10:
            dirpath = target_path + "000" + str(i)
        else:
            dirpath = target_path + "00" + str(i)

        if os.path.exists(dirpath):
            print("delete begin...")
            filenames = file_process.get_file_name(dirpath)
            for name in filenames:
                if int(name.replace(".png", "")) % 2 == 1:
                    os.remove(os.path.join(dirpath, name))
            print(str(dirpath)+ "delete finished")
        else:
            print(dirpath+ " not exist!")
    rename_img(target_path)


# MR1-2
delete_indexes = []
def delete_random_img(source_path,target_path):
    copy_img_fold(source_path,target_path)
    target_path = target_path + "/"
    dirpath = ""
    delete_rate = 0.01
    for i in range(0, 29):
        if i < 10:
            dirpath = target_path + "000" + str(i)
        else:
            dirpath = target_path + "00" + str(i)
        delete_index = []
        if os.path.exists(dirpath):
            filenames = file_process.get_file_name(dirpath)
            file_count = len(filenames)
            delete_num = math.ceil(delete_rate * file_count)
            delete_index = random.sample(range(1, file_count-1), delete_num)
            delete_index.sort()
            print(str(i) + ": " + str(delete_index))
            delete_indexes.append(delete_index)
            for counter, index in enumerate(delete_index):
                #index = index - counter
                delete_img_name = os.path.join(dirpath, filenames[index])
                os.remove(delete_img_name)
            print(str(dirpath) + ": delete finished")
        else:
            print(dirpath+ " not exist!")
    print("random_delete_index: "+ delete_indexes)
    rename_img(target_path)


# MR2-1
copy_indexes = []
def copy_paste_random(source_path,target_path):
    copy_img_fold(source_path,target_path)
    target_path = target_path + "/"
    dirpath = ""
    copy_rate = 0.01
    for i in range(0, 29):
        if i < 10:
            dirpath = target_path + "000" + str(i)
        else:
            dirpath = target_path + "00" + str(i)
        copy_index = []
        if os.path.exists(dirpath):
            filenames = file_process.get_file_name(dirpath)
            file_count = len(filenames)
            copy_num = math.ceil(copy_rate * file_count)
            copy_index = random.sample(range(1, file_count - 1), copy_num)
            copy_index.sort()
            print(str(i) + ": " + str(copy_index))
            copy_indexes.append(copy_index)
            for index in copy_index:
                if int(index) < 9:
                    savepath = dirpath + "/" + "00000" + str(index + 1) + ".png"
                elif int(index) < 99:
                    savepath = dirpath + "/" + "0000" + str(index + 1) + ".png"
                elif int(index) < 999:
                    savepath = dirpath + "/" + "000" + str(index + 1) + ".png"
                else:
                    savepath = dirpath + "/" + "00" + str(index + 1) + ".png"

                if int(index) < 10:
                    imgpath = dirpath + "/" + "00000" + str(index) + ".png"
                elif int(index) < 100:
                    imgpath = dirpath + "/" + "0000" + str(index) + ".png"
                elif int(index) < 1000:
                    imgpath = dirpath + "/" + "000" + str(index) + ".png"
                else:
                    imgpath = dirpath + "/" + "00" + str(index) + ".png"

                img = Image.open(imgpath)
                img_array = np.array(img)
                imageio.imsave(savepath, img_array)
            print(str(dirpath) + ": delete finished")
        else:
            print(dirpath + " not exist!")
    print("random_copy_indexes: "+copy_indexes)


# MR2-2
mosaic_indexes = []
def add_mosaic_random(source_path,target_path):
    copy_img_fold(source_path,target_path)
    target_path = target_path + "/"
    dirpath = ""
    mosaic_rate = 0.01
    for i in range(0, 29):
        if i < 10:
            dirpath = target_path + "000" + str(i)
        else:
            dirpath = target_path + "00" + str(i)
        mosaic_index = []
        if os.path.exists(dirpath):
            filenames = file_process.get_file_name(dirpath)
            file_count = len(filenames)
            mosaic_num = math.ceil(mosaic_rate * file_count)
            mosaic_index = random.sample(range(1, file_count - 1), mosaic_num)
            mosaic_index.sort()
            print(str(i) + ": " + str(mosaic_index))
            mosaic_indexes.append(mosaic_index)
            for index in mosaic_index:
                if int(index) < 10:
                    imgpath = dirpath + "/" + "00000" + str(index) + ".png"
                elif int(index) < 100:
                    imgpath = dirpath + "/" + "0000" + str(index) + ".png"
                elif int(index) < 1000:
                    imgpath = dirpath + "/" + "000" + str(index) + ".png"
                else:
                    imgpath = dirpath + "/" + "00" + str(index) + ".png"

                img = Image.open(imgpath)
                img_array = np.array(img)
                rows, cols, dims = img_array.shape

                for m in range(rows - 5):
                    for n in range(cols - 5):
                        if m % 5 == 0 and n % 5 == 0:
                            for i in range(5):
                                for j in range(5):
                                    b, g, r = img_array[m, n]
                                    img_array[m + i, n + j] = (b, g, r)

                savepath = imgpath
                imageio.imsave(savepath, img_array)
            print(str(dirpath) + ": delete finished")
        else:
            print(dirpath + " not exist!")
    print("random_pixelated_indexes: "+ mosaic_indexes)


# MR2-3
noise_indexes = []
def gaussian_noise_random(source_path,target_path):
    copy_img_fold(source_path,target_path)
    target_path = target_path + "/"
    dirpath = ""
    noise_rate = 0.01
    for i in range(0, 29):
        if i < 10:
            dirpath = target_path + "000" + str(i)
        else:
            dirpath = target_path + "00" + str(i)
        noise_index = []
        if os.path.exists(dirpath):
            filenames = file_process.get_file_name(dirpath)
            file_count = len(filenames)
            noise_num = math.ceil(noise_rate * file_count)
            noise_index = random.sample(range(1, file_count - 1), noise_num)
            noise_index.sort()
            print(str(i) + ": " + str(noise_index))
            noise_indexes.append(noise_index)
            for index in noise_index:
                if int(index) < 10:
                    imgpath = dirpath + "/" + "00000" + str(index) + ".png"
                elif int(index) < 100:
                    imgpath = dirpath + "/" + "0000" + str(index) + ".png"
                elif int(index) < 1000:
                    imgpath = dirpath + "/" + "000" + str(index) + ".png"
                else:
                    imgpath = dirpath + "/" + "00" + str(index) + ".png"
                img = Image.open(imgpath)
                img_noise = img.filter(ImageFilter.GaussianBlur)
                savepath = imgpath
                img_noise.save(savepath)
            print(str(dirpath) + ": delete finished")
        else:
            print(dirpath + " not exist!")
    print("random_blurred_indexes: "+ noise_indexes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--MR', type=str, default=None)
    parser.add_argument('--source-path', type=str, default="../dataset/KITTI/")
    parser.add_argument('--out-path', type=str, default="./out/")
    args = parser.parse_args()
    mr = args.MR
    source_path = args.source_path
    target_path = args.out_path
    if(mr=="MR1-1"):
        delete_odd_img(source_path,target_path)
    elif mr=="MR1-2":
        delete_random_img(source_path,target_path)
    elif mr=="MR2-1":
        copy_paste_random(source_path,target_path)
    elif mr=="MR2-2":
        add_mosaic_random(source_path,target_path)
    elif mr=="MR2-3":
        gaussian_noise_random(source_path,target_path)
    else:
        print("incorrect command!")