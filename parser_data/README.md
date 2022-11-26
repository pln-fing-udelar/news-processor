# news-processor/parser_data
Scripts to process and split text from different uruguayans newspapers

## Requirements
- Python
- install requirements from requirements.txt:
``` bash
pip install -r requirements.txt
```

## Before running the scripts
You need to download the dataset to be processed. You can find it [here](https://drive.google.com/drive/folders/1KhlclNOiD1WwB34p5t6HgzHJa93s5PMl?usp=sharing). After download the zip file, remove the actual `input` folder and replace with the one extracted.

## Run scripts
To process all the news datasets from the different newspapers run 
```
python main_parser.py
```
This script will process each one of the different newsletter's datasets with it's correspondig script, and create the dataset processed at '/output' folder.


If you want to process a specific newspaper's dataset, just run the corresponding script for it. For example, if you want to process `la_republica` dataset run:
``` bash
python la_republica_parser.py
```

### Output files:
Every output will be stored at `/output` folder. Each newspaper has it's own folder. There's also another file at `/output/all_news.txt` with all the news from every newspaper.

## If you create a new script to parse a new dataset
1. Write the specific code for the dataset as a function. If you also want, create the \_\_main\_\_ method to be called from outside. Please remember to create the corresponding folder into `output` folder.
2. Save the file in `/src/_here_`
3. Import the new script in `/src/main_parser`

## If you have created a new script to parse a new dataset, and don't want to run all previous parsers
**Assuming you** you already have all the other parsed datasets.
1. Run the specific script you've implemented
2. Open a python console and wirte: 
``` pyhton
import main_parser as mp
mp.join_all_files()
```

**Another option** to add the new dataset to the current one is using the bash command `cat`
``` bash
$ cat <path_to_yout_new_file> >> output/all_news.txt
```

## Notebooks
Folder `/notebooks` contains some jupyter files with the analysis made to create the parser scripts, and also others to analyze the output created.