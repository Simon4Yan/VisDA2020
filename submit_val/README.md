### Index File Format
From left to right:

"image-name" "camera-index" "person-identity" "image-index"

### Submission Format
Each line of the submitted file contains a list of the top 100 matches from the gallery set for each query, in ascending order of their distance to the query. The delimiter is space. Each match should be represented as its index (from 0000 to 3599 for the validation). 

More specifically, the first line of submission file is corresponding to the top 100 matches (represented as indices) of the first query (index=0000); the second line is corresponding to the second query (idex=0001).

- Please see a sample submission file in the submission_example.

Follow the following steps to submit your results:

- Generate "result.txt".
- Place the result file into a zip file named [team_name]_submission.
  In this step, please directly zip the result file and get "result.zip". You can choose to 
  rename the zip to [team_name]_submission or just submit the "result.zip" for convenience.
- Submit to the CodaLab evaluation server following the instructions below
