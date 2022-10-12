import re
import argparse
from pathlib import Path

import utils

def parse_data(
  input='input/el_pais',
  output='output/el_pais/',
  verbose=utils.DEFAULT_VERBOSE,
):

  utils.create_folder(output)

  paths = [str(x) for x in Path(input).glob("*.xml")]

  for path in paths:
    print(f'Processing {path}... ')

    f = open(path, "r")
    file_str = f.read()
    f.close()

    pattern = r'<field name=\"articulo\">.*</field>'

    result = re.findall(pattern, file_str, re.MULTILINE | re.IGNORECASE)

    # Remove undesired lines
    result = utils.remove_undesired_lines(result)

    # Remove special characters
    beautified_result = list(map(utils.beautify_text, result))

    # Remove unuseful text: "Publicado en ..."
    beautified_result = list(map(utils.removing_date_and_time, beautified_result))

    # Delete duplicated text
    beautified_result = list(set(beautified_result))

    beautified_result = list(map(utils.clean_elpais_text, beautified_result))

    new_file = path.split('/')[-1].split('.')[0]
    with open(f'{output}{new_file}.txt', "w") as f:
      for text in beautified_result:
          f.write(text +"\n")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', default='input/el_pais')
    parser.add_argument('-o', '--output', default='output/el_pais/')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--no-verbose', dest='verbose', action='store_false')
    parser.set_defaults(verbose=utils.DEFAULT_VERBOSE)
    args = parser.parse_args()
    
    parse_data(args.input, args.output, args.verbose)