# news-processor
Scripts to process and split text from different uruguayans newspapers

## Requirements
- AA
- BB

## Before running the scripts
You need to download the dataset to be processed. You can find it [here](https://drive.google.com/drive/folders/1KhlclNOiD1WwB34p5t6HgzHJa93s5PMl?usp=sharing). After download the zip file, remove the actual `input` folder and replace with the one extracted.

## Run scripts
To process all the news datasets from the different newspapers run 
```
python main_parser.py
```

If you want to process a specific newspaper's dataset, just run the corresponding script for it. For example, if you want to process `la_republica` dataset run:
```
python la_republica_parser.py
```

## If you create a new script to parse a new dataset
1. Write the specific code for the dataset as a function. If you also want, create the \_\_main\_\_ method to be called from outside. Please remember to create the corresponding folder into `output` folder.
2. Save the file in `/src/_here_`
3. Import the new script in `/src/main_parser`

## If you have created a new script to parse a new dataset, and don't want to run all previous parsers
**Assuming you** you already have all the other parsed datasets.
1. Run the specific script you've implemented
2. Open a python console and wirte: 
```
import main_parser as mp
mp.join_all_files()
```
