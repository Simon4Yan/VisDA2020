### Index File Format
From left to right:

"image-name" "camera-idex" "person-identity" "image-index"

### Submission Format
Each line of the submitted file contains a list of the top 100 matches from the gallery set for each query, in ascending order of their distance to the query. The delimiter is space. Each match should be represented as its index (from 0000 to 3599 for the validation). 

More specific, the first line of submission file is corresponding to the top 100 matches (represented as indice) of first query (index=0000); the second line is corresponding to the second query (idex=0001).

- Please see a sample submission file in the submission_example.
