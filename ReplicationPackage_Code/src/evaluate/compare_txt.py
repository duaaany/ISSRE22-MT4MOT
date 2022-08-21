import os
import numpy as np
import argparse
from PointTrack_eval.mots_eval import eval
from SORT_CenterTrack_eval import mailpy
from SORT_CenterTrack_eval import evaluate_tracking

def read_indexes_file(index_path):
    file = open(index_path, "r")
    lines = file.readlines()
    lists = []
    for fields in lines:
        fields = fields.strip();
        fields = fields.strip("[]");
        fields = fields.split(",");
        lists.append(fields);
    return lists


#MR1-1: delete odd imgs results generation
def delete_odd_txt(source_dir):
    save_dir = source_dir + "/tmp_results/"
    for n in range(0,29):
        if n<10:
            source_txt = source_dir + "/000"+str(n)+".txt"
        else:
            source_txt = source_dir + "/00" + str(n) + ".txt"
        delete_txt = ""
        source_lines = []
        delete_lines = []
        for line in open(source_txt, "r"):
            str_split = line.split(' ')
            if(int(str_split[0])%2==0):
                new_frame_count = int(int(str_split[0])/2)
                str_split[0] = str(new_frame_count)
                source_lines.append(" ".join(str_split))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        if n < 10:
            save_txt = save_dir + "/000"+str(n)+".txt"
        else:
            save_txt = save_dir + "/00" + str(n) + ".txt"
        file = open(save_txt, 'w')
        for line in source_lines[:-1]:
            file.write(line)
        file.write(source_lines[-1])
        print(save_txt + " output finished")


#MR1-2: random delete img result generation
def delete_random_txt_compare(source_dir,save_dir,delete_index,n):
    #delete_index = [1,4,7]
    source_txt = ""
    save_txt = ""
    if n<10:
        source_txt = source_dir+ "/000"+str(n)+".txt"
    else:
        source_txt = source_dir+ "/00" + str(n) + ".txt"
    delete_txt = ""
    source_lines = []
    i = 0
    temp = 0
    for line in open(source_txt, "r"):
        str_split = line.split(' ')
        frame = int(str_split[0])
        delete = False
        for index in delete_index:
            if frame == int(index):
                delete = True

        if delete == False:
            newframe = frame
            for index in delete_index:
                if frame > index:
                    newframe = newframe - 1
            str_split[0] = str(newframe)
            source_lines.append(" ".join(str_split))
    if n < 10:
        save_txt = save_dir+ "/000"+str(n)+".txt"
    else:
        save_txt = save_dir+ "/00" + str(n) + ".txt"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file = open(save_txt, 'w')
    for line in source_lines[:-1]:
        file.write(line)
    file.write(source_lines[-1])
    print(save_txt + " output finished")


# random delete imgs results generation
def delete_source_generate(source_dir, save_dir, index_path):
    delete_indexes = read_indexes_file(index_path)
    count = 0
    for delete_index in delete_indexes:
        delete_random_txt_compare(source_dir,save_dir,delete_index,count)
        count = count + 1
    #source_noise_txt_compare()


#MR2-1: copy results generation
def copy_detection_generate(source_dir,save_dir,copy_index,n):
    source_txt = ""
    save_txt = ""
    if n<10:
        source_txt = source_dir+ "/000"+str(n)+".txt"
    else:
        source_txt = source_dir+ "/00" + str(n) + ".txt"
    source_lines = []
    tempcount = 0
    templines = []
    for line in open(source_txt, "r"):
        str_split = line.split(',')
        frame = int(str_split[0])
        copy = False
        for index in copy_index:
            if frame == int(index):
                newframe = frame + 1
                str_split[0] = str(newframe)
                templines.append(",".join(str_split))
                tempcount = 0
            if frame == int(index+1):
                copy = True
        if copy == False:
            source_lines.append(line)
        if copy == True and tempcount==0:
            for l in templines:
                source_lines.append(l)
                print(l)
            tempcount = 1
            templines = []
    if n < 10:
        save_txt = save_dir+ "/000"+str(n)+".txt"
    else:
        save_txt = save_dir+ "/00" + str(n) + ".txt"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file = open(save_txt, 'w')
    for line in source_lines[:-1]:
        file.write(line)
    file.write(source_lines[-1])
    print(save_txt + " output finished")


def sort_copy_generate(source_dir, save_dir, index_path):
    copy_indexes = read_indexes_file(index_path)
    count = 0
    for copy_index in copy_indexes:
        copy_detection_generate(source_dir,save_dir,copy_index,count)
        count = count + 1


def copy_s_f_generate(sf,source_dir, follow_dir, index_path):
    save_dir = ""
    if sf == "s":
        save_dir = source_dir +"/tmp_results/"
    if sf == "f":
        save_dir = follow_dir +"/tmp_results/"

    copy_indexes = read_indexes_file(index_path)

    count = 0
    for copy_index in copy_indexes:
        remove_random_txt(source_dir,save_dir,copy_index,count,copy_bool=True)
        count = count + 1


# for MR2-2 MR2-3: random copy_paste/pixelate/blur imgs results generation
def remove_random_txt(source_dir,save_dir,noise_index,n,copy_bool):
    source_txt = ""
    save_txt = ""
    if n<10:
        source_txt = source_dir + "/000"+str(n)+".txt"
    else:
        source_txt = source_dir + "/00" + str(n) + ".txt"
    delete_txt = ""
    source_lines = []
    for line in open(source_txt, "r"):
        str_split = line.split()
        frame = int(str_split[0])
        delete = False
        for index in noise_index:
            if copy_bool == True:
                if frame == int(index)+1:
                    delete = True
            else:
                if frame == int(index):
                    delete = True
        if delete == False:
            source_lines.append(line)
    if n < 10:
        save_txt = save_dir + "/000"+ str(n) + ".txt"
    else:
        save_txt = save_dir + "/00" + str(n) + ".txt"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file = open(save_txt, 'w')
    for line in source_lines[:-1]:
        file.write(line)
        # file.write("\r\n")
    file.write(source_lines[-1])
    print(save_txt + " output finished")


def mosaic_s_f_generate(sf,source_dir, follow_dir, index_path):
    save_dir = ""
    if sf == "s":
        save_dir = source_dir +"/tmp_results/"
    if sf == "f":
        save_dir = follow_dir +"/tmp_results/"

    mosaic_indexes = read_indexes_file(index_path)
    count = 0
    for mosaic_index in mosaic_indexes:
        remove_random_txt(source_dir,save_dir,mosaic_index,count,copy_bool=False)
        count = count + 1


def noise_s_f_generate(sf, source_dir, follow_dir, index_path):
    save_dir = ""
    if sf == "s":
        save_dir = source_dir +"/tmp_results/"
    if sf == "f":
        save_dir = follow_dir +"/tmp_results/"

    noise_indexes = read_indexes_file(index_path)
    count = 0
    for noise_index in noise_indexes:
        remove_random_txt(source_dir,save_dir,noise_index,count,copy_bool=False)
        count = count + 1


def source_noise_txt_compare():
    source_txt = ""
    noise_txt = ""
    source_frame_0 = []
    i = 0
    #for i in range(0,28):
    if i<10:
        source_txt = "D:/exp/CenterTrack/txt_results/copy_random_1_source//000" + str(i) + ".txt"
        noise_txt = "D:/exp/CenterTrack/txt_results/copy_random_1_follow//000" + str(i) + ".txt"
    else:
        source_txt = "D:/exp/CenterTrack/txt_results/copy_random_1_source//00" + str(i) + ".txt"
        noise_txt = "D:/exp/CenterTrack/txt_results/copy_random_1_follow//00" + str(i) + ".txt"

    for j in range(0,465):
            source_lines = open(source_txt, "r")
            noise_lines = open(noise_txt, "r")
            if not frame_compare(source_lines,noise_lines,j):
                print("in 000" + str(i) + ".txt")


def frame_compare(source_lines,follw_lines,n):
    source_frame = []
    follow_frame = []
    source_dic = {}
    follow_dic = {}
    same = True
    for sline in source_lines:
        sline_split = sline.split()
        if (int(sline_split[0]) == n):
            source_frame.append(sline_split[1])
            source_dic[sline_split[1]] = sline_split[-1]

    for fline in follw_lines:
        fline_split = fline.split()
        if (int(fline_split[0]) == n):
            follow_frame.append(fline_split[1])
            follow_dic[fline_split[1]] = fline_split[-1]

    source_frame.sort()
    follow_frame.sort()
    if (len(source_frame)!= len(follow_frame)):
        print("frame" + str(n) + " diff")
        print("source: " + str(source_frame))
        print("follow: " + str(follow_frame))
        same = False
    return same


def id_frame_query(source_txt,txt_i,car_id,car_times):
    frame = 0
    #car_id = 53
    #car_times = 8

    #source_txt = 'D:/exp/SORT/txt_results/delete_half_source/'
    noise_txt = ""
    # txt_i = 0
    if txt_i<10:
        source_txt = source_txt + "/000" + str(txt_i) + ".txt"
        noise_txt = "D:/exp/object tracking/txt_result/random/copy_random_1_follow/000" + str(txt_i) + ".txt"
    else:
        source_txt = source_txt + "/00" + str(txt_i) + ".txt"
        noise_txt = "D:/exp/object tracking/txt_result/random/copy_random_1_follow//00" + str(txt_i) + ".txt"

    noise_lines = open(source_txt, "r")
    N = 0
    for lines in noise_lines:
        line_split = lines.split()
        if int(line_split[1]) == car_id:
            N = N + 1
            # print(str(N))
            if N == car_times:
                return(int(line_split[0]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--MR', type=str, default=None)
    parser.add_argument('--Model', type=str, default=None)
    parser.add_argument('--source-path', type=str, default="../out/source/")
    parser.add_argument('--follow-path', type=str, default="./out/follow/")
    parser.add_argument('--index-path', type=str, default="indexes_test.txt")
    parser.add_argument('--seqmap-path', type=str, default="random_exp.seqmap")
    parser.add_argument('--default', type=int, default="0")
    args = parser.parse_args()
    mr = args.MR
    model = args.Model
    source_path = args.source_path
    follow_path = args.follow_path
    index_path = args.index_path
    seqmap_path = args.seqmap_path
    de = args.default
    if(de==0):
        if (model == "SORT" or model == "CenterTrack"):
            split_version = "test"
            mail = mailpy.Mail("")
            evaluate_tracking.evaluate(follow_path,source_path, mail, split_version=split_version,
                                       filename_test_mapping=seqmap_path)
        elif (model == "PointTrack"):
            eval.run_eval(follow_path, source_path, seqmap_path)
        else:
            print("incorrect command of Model!")
    else:
        if(mr=="MR1-1"):
            delete_odd_txt(source_path)
            if(model=="SORT" or model=="CenterTrack"):
                gt_path = source_path + "/tmp_results/"
                result_sha = follow_path + "/"
                split_version = "test"
                mail = mailpy.Mail("")
                evaluate_tracking.evaluate(result_sha,gt_path,mail,split_version=split_version,filename_test_mapping = seqmap_path)
            elif(model=="PointTrack"):
                results_folder = follow_path + "/"
                gt_folder = source_path + "/tmp_results/"
                eval.run_eval(results_folder, gt_folder, seqmap_path)
            else:
                print("incorrect command of Model!")

        elif(mr=="MR1-2"):
            delete_source_generate(source_path,source_path+"/tmp_results/",index_path)
            if (model == "SORT" or model == "CenterTrack"):
                gt_path = source_path + "/tmp_results/"
                result_sha = follow_path + "/"
                split_version = "test"
                mail = mailpy.Mail("")
                evaluate_tracking.evaluate(result_sha,gt_path, mail, split_version=split_version,
                                           filename_test_mapping=seqmap_path)
            elif (model == "PointTrack"):
                results_folder = follow_path + "/"
                gt_folder = source_path + "/tmp_results/"
                eval.run_eval(results_folder, gt_folder, seqmap_path)
            else:
                print("incorrect command of Model!")

        elif(mr=="MR2-1"):
            copy_s_f_generate("s",source_path,follow_path,index_path)
            copy_s_f_generate("f", source_path, follow_path, index_path)
            if (model == "SORT" or model == "CenterTrack"):
                gt_path = source_path + "/tmp_results/"
                result_sha = follow_path + "/tmp_results/"
                split_version = "test"
                mail = mailpy.Mail("")
                evaluate_tracking.evaluate(result_sha,gt_path, mail, split_version=split_version,
                                           filename_test_mapping=seqmap_path)
            elif (model == "PointTrack"):
                results_folder = follow_path + "/tmp_results/"
                gt_folder = source_path + "/tmp_results/"
                eval.run_eval(results_folder, gt_folder, seqmap_path)
            else:
                print("incorrect command of Model!")


        elif(mr=="MR2-2"):
            mosaic_s_f_generate("s", source_path, follow_path, index_path)
            mosaic_s_f_generate("f", source_path, follow_path, index_path)
            copy_s_f_generate("s", source_path, follow_path, index_path)
            copy_s_f_generate("f", source_path, follow_path, index_path)
            if (model == "SORT" or model == "CenterTrack"):
                gt_path = source_path + "/tmp_results/"
                result_sha = follow_path + "/tmp_results/"
                split_version = "test"
                mail = mailpy.Mail("")
                evaluate_tracking.evaluate(result_sha,gt_path, mail, split_version=split_version,
                                           filename_test_mapping=seqmap_path)
            elif (model == "PointTrack"):
                results_folder = follow_path + "/tmp_results/"
                gt_folder = source_path + "/tmp_results/"
                eval.run_eval(results_folder, gt_folder, seqmap_path)
            else:
                print("incorrect command of Model!")

        elif(mr=="MR2-3"):
            noise_s_f_generate("s", source_path, follow_path, index_path)
            noise_s_f_generate("f", source_path, follow_path, index_path)
            copy_s_f_generate("s", source_path, follow_path, index_path)
            copy_s_f_generate("f", source_path, follow_path, index_path)
            if (model == "SORT" or model == "CenterTrack"):
                gt_path = source_path + "/tmp_results/"
                result_sha = follow_path + "/tmp_results/"
                split_version = "test"
                mail = mailpy.Mail("")
                evaluate_tracking.evaluate(result_sha, gt_path, mail, split_version=split_version,
                                           filename_test_mapping=seqmap_path)
            elif (model == "PointTrack"):
                results_folder = follow_path + "/tmp_results/"
                gt_folder = source_path + "/tmp_results/"
                eval.run_eval(results_folder, gt_folder, seqmap_path)
            else:
                print("incorrect command of Model!")

        else:
            print("incorrect command of MR!")
