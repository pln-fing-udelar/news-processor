# news-processor/parser_data
This project process uruguayans newspapers dataset, and trains a BERT-like models from scratch using this dataset.
This project is hosted by the Natural Language Processing Group from University of the Republic, Uruguay (http://www.fing.edu.uy/inco/grupos/pln/).
## Requirements
- Python

## Content
The project has the following content:
- parser_data: folder cotaining all the source code and datasets to parse the original news dataset.
- train_model: folder containing the source code to train the desired model.
- eval tasks: folder with different challenges to evaluate the created model.


## Manage the dataset
You need to have the depurated dataset with the desired format to train the model. There are 2 ways to do this.

### A - Download the dataset.
Download the file from [this link](https://drive.google.com/file/d/1s3JKWDtEZg-tijZRYxYI57xmTxpLrChi/view?usp=share_link). This link downlads a file called `all_together.txt` that contains the dataset we've already processed with the code at `parse_data`. Please be sure the file is not corrupted:
- size: run in bash:
``` bash
$ du -h all_together.txt # expected result: 1.2 GB
```
- md5: run in bash:
``` bash
$ md5sum all_together.txt # expected result: 62e5e1f28bb9634563eeddb9daf8c098
``` 

### B - Run parsers
1. Move to parser_data and follow instructions. This will generate the cleaned versions of the original uruguayans news datasets.
2. Split all datasets news into sentences. To do this you can use the [sentence-splitter repository](https://github.com/pln-fing-udelar/sentence-splitter). You can run the splitter once with `all_news.txt`.
3. You're expected to have one file with news separated with an empty line. Each news has it's sentences devided in different lines.