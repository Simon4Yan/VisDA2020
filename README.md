# VisDA2020: 4th Visual Domain Adaptation Challenge

Welcome to VisDA2020!

This is the development kit repository for [the 2020 Visual Domain Adaptation (VisDA) Challenge](http://ai.bu.edu/visda-2020/). Here you can find details on how to download datasets, run baseline models, and evaluate the performance of your model. Evaluation can be performed either locally on your computer or remotely on the CodeLab evaluation server. Please see the main website for competition details, rules, and dates.

Have fun!

## Overview
This year’s challenge focuses on **Domain Adaptive Pedestrian Re-identification**, where the source and target domains have completely different classes (pedestrian IDs). The particular task is to retrieve the pedestrian instances of the same ID as the query image. This problem is significantly different from previous VisDA challenges, where the source and target domains share some overlapping classes. Moreover, ID matching depends on fine-grained details, making the problem harder than before.

The competition will take place during May -- July 2020, and the top-performing teams will be invited to present their results at the workshop at [ECCV 2020](https://sites.google.com/view/task-cv2020) in September, Glasgow.

## Challenge Data 

[[GoogleDrive]](https://drive.google.com/open?id=18qIbI1XiG2n36qCTS-Te-2XATxiHNVDj) and [[OneDrive]](https://1drv.ms/u/s!AhjrHmxemkOga91UXOVXsVZJqTg?e=kbE1CC)

![enter image description here](https://github.com/sxzrt/The-PersonX-dataset/raw/master/images/logo1.jpg)

The challenge uses synthetic data as the source, which is from [PersonX](https://github.com/sxzrt/Dissecting-Person-Re-ID-from-the-Viewpoint-of-Viewpoint) [1].
The target domain consists of real-world images. We have provided camera index information for both source and target training sets. 
 - For the source dataset, it contains 20,280 images from 700 IDs, which are captured by 6 cameras. 
 - For the target dataset, only the target training set can be used for training models (Please follow the rules in [challenge website](http://ai.bu.edu/visda-2020/)). We also provide a fully labeled validation set for algorithm development. **Note that**, the IDs in the target training set are quite noisy, e.g., images of a person might come from one or multiple cameras, and the number of images per ID varies a lot. We believe this setting is more practical and is significantly different from the current setting [2]. We also provide the camera index of each target training image. 

The challenge dataset split is organized as follows: 
```
├── challenge_datasets/
(Source dataset collected from synthetic simulator)
│   ├── personX/
│       ├── image_train/                   /* source training images 
│           ├── 0001_c3s1_24
|           ├── 0002_c3s1_23
|           ...
(Target dataset collected from real world)
│   ├── target_training/  
│       ├── label_target_training.txt     /* camera index 
│       ├── image_train/
|           ├── 00001.jpg
|           ├── 00011.jpg
|           ...
│   ├── target_validation/               /* validation set
│       ├── image_gallery/
|           ├── 0000_c1s1_001036_07.jpg
|           ├── 0000_c1s1_001046_06.jpg
|           ...
│       ├── image_query/
|           ├── 0001_c1s1_000017_02.jpg
|           ├── 0002_c4s1_000918_04.jpg
|           ...
│   ├── target_test                     /* test set
│       ├── image_gallery
|           ├── 000000.jpg
|           ├── 000001.jpg
|           ...
│       ├── image_query/
|           ├── 0000.jpg
|           ├── 0001.jpg
|           ...
```

By downloading these datasets you agree to the following terms:

### Naming Rule of the bboxes
In bbox "0046_c5s1_004279_02", "c5" is the 5-th camera (there 6 cameras in training and 5 cameras in testing). "s1" is sequence 1 of camera 5. "004279" is the4279-th frame in the sequence "c5s1". The frame rate is 25 frames per sec.
"0046" is the person ID.

Moreover, we have provided a tiny code to read images and get camera & ID information:
https://github.com/Simon4Yan/VisDA2020/tree/master/devkit/data/datasets

### Terms of Use
- You will use the data only for non-commercial research and educational purposes.
- You will NOT distribute the images.
- The organizers make no representations or warranties regarding the data, including but not limited to warranties of non-infringement or fitness for a particular purpose.
- You accept full responsibility for your use of the data.

You can download the datasets with the following link: [GoogleDrive](https://drive.google.com/open?id=18qIbI1XiG2n36qCTS-Te-2XATxiHNVDj) and [OneDrive](https://1drv.ms/u/s!AhjrHmxemkOga91UXOVXsVZJqTg?e=kbE1CC).

Moreover, we also provide translated images from SPGAN [2]. SPGAN conducts source-target image translation, such that the translated images follow the distribution of the target. Thus, the Re-ID model trained on the translated images achieves high accuracy on the test set. OneDrive: [PersonX_SPGAN](https://1drv.ms/u/s!AhjrHmxemkOgbIahEx1m49NDuDI?e=i9wE31) or GoogleDrive: [PersonX_SPGAN](https://drive.google.com/open?id=1HEV_EfnLAWU_a5pyeZ12yl5lRCeivDG-).

### Download the Test Set
- The test set is available [here](https://drive.google.com/file/d/12oWSOK1oQVhTNqoVUli70dboXOxPxG41/view?usp=sharing). You need to fill in the [google form](https://forms.gle/9hjryZ5WDUUEZTAX9) to get the password for unzipping files. If you can not open the form, please fill in the [form offline](https://github.com/Simon4Yan/VisDA2020/tree/master/form/) and send it to (weijian.deng@anu.edu.au).

- We respectfully notice that all participating teams should fill in the form above. If you haven't finished, please fill it online or offline. Thanks!

- Please kindly follow the [RULES](http://ai.bu.edu/visda-2020/#rules) and read the [FAQ](http://ai.bu.edu/visda-2020/#faq), thanks!


## Evaluating Your Model
We have provided the evaluation script used by our server so that *you may evaluate your results offline*. You are encouraged to upload your results to the evaluation server to compare your performance with that of other participants.
We will use CodaLab to evaluate submissions and maintain a leaderboard. To register for the evaluation server, please create an account on CodaLab and enter as a participant in the following competition:

[Domain Adaptive Pedestrian Re-identification](https://competitions.codalab.org/competitions/24664)

If you are working as a team, you have the option to register for one account for your team or register multiple accounts under the same team name. If you choose to use one account, please indicate the names of all of the members on your team. This can be modified in the “User Settings” tab. If your team registers for multiple accounts, please do so using the protocol explained by CodaLab here. Regardless of whether you register for one or multiple accounts, your team must adhere to the per-team submission limits (20 entries per day per team during the validation phase). 

The evaluation metrics used to rank the performance of each team will be mean Average Precision (mAP) and Cumulated Matching Characteristics (CMC) curve. **The metrics evaluate the top-100 matches**. 

### Submission Format
Each line of the submitted file contains a list of the top 100 matches from the gallery set for each query, in ascending order of their distance to the query. The delimiter is space. Each match should be represented as the **index** of the gallery image (from 00000 to 24005 for the test set). 

More specifically, the first line of submission file is corresponding to the top 100 matches (represented as indices) of the first query (index=0000); the second line is corresponding to the second query (idex=0001).

- The index of each image in the validation set can be found in [submit-test](https://github.com/Simon4Yan/VisDA2020/tree/master/submit_test).
- Please see a sample submission file [submission-example]( https://github.com/Simon4Yan/VisDA2020/tree/master/submit_test).

### Submitting to the Evaluation Server
[Domain Adaptive Pedestrian Re-identification](https://competitions.codalab.org/competitions/24664)

Once the servers become available, you will be able to submit your results:

- Generate "result.txt".
- Place the result file into a zip file named [team_name]_submission.
  In this step, please directly zip the result file and get "result.zip". You can choose to 
  rename the zip to [team_name]_submission or just submit the "result.zip" for convenience.
- Submit to the CodaLab evaluation server following the instructions below

To submit your zipped result file to the appropriate VisDA challenge click on the “Participate” tab. Select the phase (validation or testing). Select Submit / View Results, fill in the required fields and click “Submit”. A pop-up will prompt you to select the results zip file for upload. After the file is uploaded, the evaluation server will begin processing. This might take some time. To view the status of your submission please select “Refresh Status”. If the status of your submission is “Failed” please check your file is named correctly and has the right format. You may refer to the scoring output and error logs for more details.

After you submit your results to the evaluation server, you can control whether your results are publicly posted to the CodaLab leaderboard. To toggle the public visibility of your results please select either “post to leaderboard” or “remove from leaderboard.”

## Devkit
We provide a simple baseline code ([based on codes [3]](https://github.com/Simon4Yan/feature_learning)). In the devkit, we provide code for reading the challenge datasets and evaluation code.

- The mAP evaluation code in this github evaluates all matches.  And the server evaluates mAP based on top-100 matches (this is commonly used in the community, such as [Aitychallenge](https://www.aicitychallenge.org/2020-data-and-evaluation/)).
Thus, the CMC ranks are identical, while the mAP in the server is higher.  Consider the generality, I provide the code here to evaluate all matches. You could modify the evaluation code to evaluate the top-100 matches, if you want to calculate the same number of mAP with the codalab.

```bash
python learn/train.py
python learn/test.py
```

The baseline performance is, 
|Methods | Rank@1 | mAP| Reference|
| -------- | ----- | ---- | ---- |
| Source Only |26.53 | 14.19 |  [ResNet-50] |
| SPGAN |41.11 | 21.35  |  [ResNet-50] |

## Broader Impact

This competition is featured by learning from synthetic 3D person data. We are not only advancing state-of-the-art technologies in domain adaptation, metric learning and deep neural networks, but importantly aim to reduce system reliance on real-world datasets. While we evaluate our algorithms on real-world data, we have adopted strict measures to take care of the privacy issue. For example, all the faces have been blurred. The participants have signed to comply with our data protection agreement, where we have forbidden the posting or distribution of test images in papers or other public domains. We believe these measures will significantly improve data safety and privacy, while allowing researchers to develop useful technologies.

## Feedback and Help
If you find any bugs please [open an issue](https://github.com/Simon4Yan/VisDA2020/issues/new).

## References

[1] Sun, Xiaoxiao, and Liang Zheng. "Dissecting person re-identification from the viewpoint of viewpoint." _Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition_. 2019.

[2] W. Deng, L. Zheng, Q. Ye, G. Kang, Y. Yang, and J. Jiao. Image-image domain adaptation with preserved self-similarity and domain-dissimilarity for person re-identification. In CVPR, 2018

[3] Lv, Kai, Weijian Deng, Yunzhong Hou, Heming Du, Hao Sheng, Jianbin Jiao, and Liang Zheng. "Vehicle reidentification with the location and time stamp." In _Proc. CVPR Workshops_. 2019.
