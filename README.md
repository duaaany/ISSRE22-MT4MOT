# **Replication Package for the Paper "Towards the Robustness of Multiple Object Tracking Systems"**

This is the replication package for the ISSRE 2022 Research Track paper "*Towards the Robustness of Multiple Object Tracking Systems*". 

It contains: 
1. **The scripts to replicate our experiments:** 1) the implementation of our proposed five MRs. 2) the scripts to replicate our extensive evaluation experiments.
2. **The complete experimental results:** 1) the tracking results of three models on the test cases of five MRs. 

------

## Scripts to Relicate Our Experiments

We release the relevant code and data to replicate our experiments. Specifically, we provide: (a) the implementation to apply our proposed five MRs to the source data and (b) the instruction and scripts to replicate our evaluation experiments.


### File Structure

```
ReplicationPackage_Code.zip
└─src
    ├─MR_transform  # The scripts to generate follow-up test cases with our MRs. 
    └─evaluate  # The scripts to measure consistence between the source and follow-up outputs and calculates metrics. 
```

### Replication Instruction

0. Prepare the source dataset. The dataset "KITTI tracking" used in our evaluation can be found in [KITTI tracking website](http://www.cvlibs.net/datasets/kitti/eval_tracking.php).

1. Run `src/MR_transform/MR_apply_img.py`  to apply the MR transformation to source test cases and get the follow-up test cases.
```bash
cd src/MR_transform
python MR_apply_img.py --MR selected_MR --source-path /path/to/source/files --out-path /path/to/follow-up/files

# --MR specifies the MR to apply, whose value can be one of "MR1-1", "MR1-2", "MR2-1", "MR2-2", and "MR2-3".
# --source-path specifies the path to the directory storing the source test cases (the path of dataset KITTI tracking).
# --out-path specifies the path to the directory to store the follow-up test cases generated with the selected MR. 
```

2. Execute tested MOT systems on the source and follow-up test cases to obtain the source and follow-up tracking results. 
(Due to the copyright, please follow the official instructions of the tested MOT systems ([SORT](https://github.com/abewley/sort)+ [YOLOv3](https://github.com/ultralytics/yolov3) , [PointTrack](https://github.com/detectRecog/PointTrack), [CenterTrack](https://github.com/xingyizhou/CenterTrack)) to execute these systems and get the tracking results.)

3. Run `src/evaluate/compare_txt.py`  to identify violations in the tracking results, as well as calculate the ratio of the frames with tracking errors detected and the amount of three types of errors. 
```bash
cd src/evaluate
python compare_txt.py --MR selected_MR --source-path /path/to/source/files --follow-path /path/to/follow-up/files --index-path /path/to/index/file --seqmap-path /path/to/seqmap/file --default test_type

# --default specifies the evaluation mode. If it is set as "0", the scripts will summarize all the test results (we have provided the complete tracking results in our evaluation to illustrate the directory structure of the test results supported by this mode); while if it is set as "1", you can use the other parameters to evaluate your own test results. 
# --MR specifies the MR transformation applied, whose value can be one of "MR1-1", "MR1-2", "MR2-1", "MR2-2", and "MR2-3".
# --source-path specifies the path to the directory storing the source tracking results derived from step 2.
# --follow-path specifies the path to the directory storing the follow-up tracking results derived from step 2. 
# --index-path specifies the path to the file of frame indexes in random experiments (MR1-2. MR2-1, MR2-2, MR2-3). We have provided an example of indexes in "index_test.txt". You can put your own frame indexes in this file.
# --seqmap-path specifies the path to the file of seqmap for tracking evaluation. We have provided an example of seqmap in "random_exp.seqmap". It can be used for MR1-2. MR2-1, MR2-2, MR2-3.
```

------

## Complete Experimental Results

We also release the tracking results of three tested models on five MRs obtained in our experiment. 

### File Structure

```
CompleteResults.zip
└─tracking_results  # The tracking results (source and follow-up outputs) derived in our evaluation experiment. 
    ├─CenterTrack
    ├─PointTrack
    └─SORT_YOLO
````
