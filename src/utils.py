import re
import html
import unicodedata
import os
from unidecode import unidecode

def sanitice_text(txt):

  # estoy interesado en obtener todos los caracteres que no sean:
  # 1. ASCII
  whiteList = '\x00-\x7F'

  # 2. ¿ ¡ tildes y enies
  whiteList += '¿¡À-ÿñÑ'

  regex = r'[^{}]'.format(whiteList)
  patt = re.compile(regex)
  sanitice_char = lambda c: unidecode(c) if patt.match(c) else c
  
  return "".join([sanitice_char(c) for c in txt])

is_txt_postfix = lambda p: p[-4:] == ".txt"

DEFAULT_VERBOSE = True

def die(msg):
  print(msg)
  os._exit(1)

# si no exite `path`, la crea
def assure_path(path):
  if not os.path.exists(os.path.dirname(path)):
    create_folder(os.path.dirname(path))

def create_folder(folder_path):
  try:
    os.makedirs(folder_path)
  except Exception as e:
    die(e)

def beautify_text(text):
  rs = text.replace('<field name="articulo">', '')
  rs = rs.replace('</field>', '')
  rs = html.unescape(rs)
  rs = unicodedata.normalize("NFKD", rs)
  rs = rs.strip()

  return rs

def removing_date_and_time(text):
  regex = r" Publicado el \d\d?\/\d\d?\/\d?\d\d\d\d - \d?\d:\d?\d"
  subst = "."
  result = re.sub(regex, subst, text, 0, re.MULTILINE)

  return result


## el pais ##

def remove_undesired_lines(lines):
  regex =  r"Boris Cristoff .*?Digital\n"

  resulting_lines = list(filter(lambda line: not(re.search(regex, line)), lines))

  regex =  r"CondeLeonardo@netscape.net"
  resulting_lines = list(filter(lambda line: not(re.search(regex, line, re.IGNORECASE)), resulting_lines))

  regex = r'CondeLeonardo@aol.com'
  resulting_lines = list(filter(lambda line: not(re.search(regex, line, re.IGNORECASE)), resulting_lines))

  return resulting_lines
  
# text = una noticia
def clean_elpais_text(text):
  # sanitizo el texto
  text = sanitice_text(text)

  # Texto "Utilidades" al final
  replace_pattern = r"Utilidades$"
  text = re.sub(replace_pattern, '', text)

  # Texto "Vota por esta noticia:"
  replace_pattern = r"Vota por esta noticia:"
  text = re.sub(replace_pattern, '', text)  

  # Texto "Escribe tu comentario" al final
  replace_pattern = r"Escribe tu comentario$"
  text = re.sub(replace_pattern, '', text)  
  
  # Texto ":: AA ::" al final
  replace_pattern = r":: .*? ::"
  text = re.sub(replace_pattern, '', text)

  # Texto formato "No salgas a la calle sin"
  replace_pattern = r"No salgas a la calle sin saber de qué se habla..."
  text = re.sub(replace_pattern, '', text)

  replace_pattern = r"No salgas a la calle sin ver más► saber de qué se habla"
  text = re.sub(replace_pattern, '', text)

  replace_pattern = r"No salgas a la calle sin$"
  text = re.sub(replace_pattern, '', text)  

  # Texto "¿Te interesa esta noticia?" en el inicio
  replace_pattern = r"\¿?Te interesa esta noticia\?"
  text = re.sub(replace_pattern, '', text)  

  # Texto "AFP"
  replace_pattern = r"AFP"
  text = re.sub(replace_pattern, '', text)  

  # Fechas
  # Formato dd mmm YYYY
  # al inicio
  replace_pattern = r"^\d\d \w\w\w \d\d\d\d"
  text = re.sub(replace_pattern, '', text)  

  # dentro el string
  replace_pattern = r"\d\d \w\w\w \d\d\d\d"
  text = re.sub(replace_pattern, '.', text)  

  # Formato  dia mes nn YYYY hh:mm 
  # al inicio
  replace_pattern = r"^\w\w\w \w\w\w \d\d \d\d\d\d \d\d:\d\d"
  text = re.sub(replace_pattern, '', text)

  # dentro del string
  replace_pattern = r"\w\w\w \w\w\w \d\d \d\d\d\d \d\d:\d\d"
  text = re.sub(replace_pattern, '.', text)

  # Formato -dia mmm dd YYYY- (sin hora)
  # al inicio
  replace_pattern = r"^\w\w\w \w\w\w \d\d \d\d\d\d"
  text = re.sub(replace_pattern, '', text)

  # dentro del string
  replace_pattern = r"\w\w\w \w\w\w \d\d \d\d\d\d"
  text = re.sub(replace_pattern, '.', text) 

  # Elimino autores - formato " Por AAA AAA |"
  replace_pattern = r"(\w)(\s*Por \w* \w* \|)"
  text = re.sub(replace_pattern, r'\1.', text, re.IGNORECASE)

  replace_pattern = r"\s*Por \w* \w* \|"
  text = re.sub(replace_pattern, '', text, 0, re.IGNORECASE)
  
  # Elimino texto "Foto: -origen-"
  replace_pattern = r"(Foto:.*?)(\/|\.|AP|EFE|AFP|Archivo El Pais|Temas|Facebook Comite de los Derechos del Nino del Uruguay Centros del Sirpa|Alexis Ferreira|Gentileza Policia de San Jose|Maria Ines Hiriart|Ricardo Figueredo|Facebook Carolina Mallo Sosa|Facebook Jose Maria Techera|Facebook Roberto Caseres|Facebook Richard Silveira|Dilva Devita|Facebook Comite de los Derechos del Nino|El Pais Entierro del policia Ariel Silva|Ariel Colmegna Primera boda  bajo la ley)"
  text = re.sub(replace_pattern, '.', text)
  # faltan evaluar unnos casos


  return text
