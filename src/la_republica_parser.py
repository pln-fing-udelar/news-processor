import os
import re
from pathlib import Path

import utils

def parse_data():
  paths = [str(x) for x in Path("./input/la_republica").glob("*.xml")]

  for path in paths:
    print(f'Processing {path}... ')

    f = open(path, "r")
    file_str = f.read()
    f.close()

    pattern = r'<field name=\"articulo\">.*</field>'

    result = re.findall(pattern, file_str, re.MULTILINE | re.IGNORECASE)

    # Remove special characters
    beautified_result = list(map(utils.beautify_text, result))

    # Remove unuseful text: "Publicado en ..."
    beautified_result = list(map(utils.removing_date_and_time, beautified_result))

    # Delete duplicated text
    beautified_result = list(set(beautified_result))

    new_file = path.split('/')[-1].split('.')[0]
    with open(f'output/la_republica/{new_file}.txt', "w") as f:
      for text in beautified_result:
          f.write(text +"\n")

if __name__ == "__main__":
    parse_data()