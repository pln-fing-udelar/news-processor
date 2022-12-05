from pathlib import Path

import la_republica_parser
import el_pais_parser

def join_all_files():
  paths = [str(x) for x in Path('output/').glob("*/*.txt")]
  
  with open('output/all_news.txt', 'w') as outfile:
      for fname in paths:
          with open(fname) as infile:
              for line in infile:
                  outfile.write(line)

  return True

if __name__ == "__main__":
  la_republica_parser.parse_data()
  el_pais_parser.parse_data()

  join_all_files()