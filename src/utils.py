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
def replace_characters(text):
  replace_dict = {
                  'á': 'á',
                  'é': 'é',
                  'í': 'í',
                  'ó': 'ó',
                  'ú': 'ú',
                  'ñ': 'ñ',
                  'Á': 'Á',
                  'É': 'É',
                  'Í': 'Í',
                  'Ó': 'Ó',
                  'Ú': 'Ú',
                  'Ñ': 'Ñ'
                  }
  output = text
  for original, replacement in replace_dict.items():
    print(replacement)
    output = output.replace(original, replacement)
    
  return output


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
  # elimino lineas con caracteres corruptos
  corrupto = lambda art: '�' in art
  resulting_lines = list(filter(lambda line: not(corrupto(line)), lines))

  regex =  r"Boris Cristoff .*?Digital\n"
  resulting_lines = list(filter(lambda line: not(re.search(regex, line)), lines))

  regex =  r"CondeLeonardo@netscape.net"
  resulting_lines = list(filter(lambda line: not(re.search(regex, line, re.IGNORECASE)), resulting_lines))

  regex = r'CondeLeonardo@aol.com'
  resulting_lines = list(filter(lambda line: not(re.search(regex, line, re.IGNORECASE)), resulting_lines))

  regex =  r"horizontales.*?\d\)"
  resulting_lines = list(filter(lambda line: not(re.search(regex, line, re.IGNORECASE)), resulting_lines))

  regex = r"Leonardo Conde"
  resulting_lines = list(filter(lambda line: not(re.search(regex, line, re.IGNORECASE)), resulting_lines))

  return resulting_lines
  
# text = una noticia
def clean_elpais_text(text):
  # sanitizo el texto
  text = replace_characters(text)
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
  r"(Foto:.*?)(\/|\.|AP|EFE|AFP|Archivo El Pais|Temas|Facebook Comite de los Derechos del Nino del Uruguay Centros del Sirpa|Alexis Ferreira|Gentileza Policia de San Jose|Maria Ines Hiriart|Ricardo Figueredo|Facebook Carolina Mallo Sosa|Facebook Jose Maria Techera|Facebook Roberto Caseres|Facebook Richard Silveira|Dilva Devita|Facebook Comite de los Derechos del Nino|El Pais Entierro del policia Ariel Silva|Ariel Colmegna Primera boda  bajo la ley|Alicia Brassesco|BQB|ARCHIVO|Carnan Abona|)"
  text = re.sub(replace_pattern, '.', text)
  r"(Foto:.*?)(Daniel Ayala|Daniel Rojas|Julio Barcelos|LA NACION|GDA|Gentileza de Jose Luis Cuna|Archivo de El Pais|Marcelo Bonjour|Gentileza de Jose Luis Cuna Temas Sinies|Archivo de El Pais|Archivo El Pais)"
  text = re.sub(replace_pattern, '.', text)
  # To Do: faltan evaluar unos casos  -----------------------------------------------------------------------------------------------------------------------------

  # Texto "Otras Ediciones" - Ambas letras en mayuscula
  replace_pattern = r"Otras Ediciones$"
  text = re.sub(replace_pattern, '', text) 

  # Texto entre pipes, formato "| PALABRA (SIMBOLO)|"
  replace_pattern = r"\| \w*? .?\|"
  text = re.sub(replace_pattern, '', text)  
  # To Do: tengo que seguir revisando este caso  de pipes ------------------------------------------------------------------------------------------------------------------------------
 
  # Elimino texto "El Pais Digital"  
  replace_pattern = r"(AFP)? El Pais Digital\n"
  text = re.sub(replace_pattern, '', text, re.IGNORECASE)  

  replace_pattern = r"AFP El Pais Digital."
  text = re.sub(replace_pattern, '', text, re.IGNORECASE) 

  # texto "El Pais Digital" se reserva el derecho de editar......
  replace_pattern = r"El Pais Digital se reserva el derecho de editar los mensajes que usted envie a los efectos de su mejor comprension por otros usuarios. (Nuevo seudonimo:)?"
  text = re.sub(replace_pattern, '', text)

  # texto "EFE"
  replace_pattern = r" EFE "
  total_result = re.sub(replace_pattern, '', text)  

  replace_pattern = r"\(EFE\)"
  total_result = re.sub(replace_pattern, '', total_result)  
  # To Do: tengo que seguir revisando este caso  de del contexto de EFE ------------------------------------------------------------------------------------------------------------------------------


  return text
