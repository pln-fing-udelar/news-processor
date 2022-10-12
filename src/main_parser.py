from pathlib import Path

import la_republica_parser
import el_pais_parser

def join_all_files():
  # To Do: agregar rutas absolutas, no relativas

  paths = [str(x) for x in Path('output/').glob("*/*.txt")]
  
  with open('output/all_news.txt', 'w') as outfile:
      for fname in paths:
          with open(fname) as infile:
              for line in infile:
                  outfile.write(line)

  # idea: correr una validacion de que se haya copiado bien los archivos?
  #   - suma de tamanio de archivos?
  #   - suma de cantidad de lineas de entrada?
  return True

if __name__ == "__main__":
  la_republica_parser.parse_data()
  el_pais_parser.parse_data()

  join_all_files()