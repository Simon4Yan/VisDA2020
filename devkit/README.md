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