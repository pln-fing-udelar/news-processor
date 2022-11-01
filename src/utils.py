from doctest import OutputChecker
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
  
  regex =  r"Boris Cristoff .*?Digital\n"
  contiene_boris = lambda art: re.search(regex, art) is not None
  contiene_aries = lambda art: 'Aries' in art
  es_horoscopo = lambda art: contiene_boris(art) | contiene_aries(art)

  regex_conde_1 = r"CondeLeonardo@netscape.net"
  contiene_conde_1 = lambda art: re.search(regex_conde_1, art, re.IGNORECASE) is not None
  regex_conde_2 = r"CondeLeonardo@aol.com"
  contiene_conde_2 = lambda art: re.search(regex_conde_2, art, re.IGNORECASE) is not None
  regex_horizontales = r"horizontales.*?\d\)"
  contiene_horizontales = lambda art: re.search(regex_horizontales, art, re.IGNORECASE) is not None
  regex_conde_3 = r"Leonardo Conde"
  contiene_conde_3 = lambda art: re.search(regex_conde_3, art, re.IGNORECASE) is not None
  es_crucigrama = lambda art: contiene_conde_1(art) | contiene_conde_2(art) | contiene_horizontales(art) | contiene_conde_3(art)

  
  resulting_lines = list(filter(lambda line: not(corrupto(line)), lines))

  resulting_lines = list(filter(lambda line: not(es_horoscopo(line)), resulting_lines))

  resulting_lines = list(filter(lambda line: not(es_crucigrama(line)), resulting_lines))

  return resulting_lines

def clean_jorge_chouy(line):
  out = line

  replace_pattern = r' Por Jorge Chouy jchouy@seragro.com.uy'
  out = re.sub(replace_pattern, '.', out)

  replace_pattern = r' Por Jorge Chouy - jchouy@seragro.com.uy'
  out = re.sub(replace_pattern, '.', out)

  replace_pattern = r' Por Jorge Chouy, jchouy@seragro.com.uy'
  out = re.sub(replace_pattern, '.', out)

  replace_pattern = r' INFORME ELABORADO POR JORGE CHOUY Y HÉCTOR LUNA \| jchouy@seragro.com.uy / hluna@seragro.com.uy TRANSCRIPCIÓN DE GRACIELA GIRIBALDI'
  out = re.sub(replace_pattern, '.', out)

  replace_pattern = r' Jorge Chouy \| jchouy@seragro.com.uy'
  out = re.sub(replace_pattern, '.', out)

  replace_pattern = r' jchouy@seragro.com.uy'
  out = re.sub(replace_pattern, '', out)

  return out

def clean_gaston_pergola(line):
  out = line

  replace_pattern = r' Por Gastón Pérgola gpergola@elpais.com.uy'
  out = re.sub(replace_pattern, '.', out, 9999, re.IGNORECASE)

  replace_pattern = r' POR GASTÓN PÉRGOLA - gpergola@elpais.com.uy'
  out = re.sub(replace_pattern, '.', out, 9999, re.IGNORECASE)

  replace_pattern = r' POR GASTÓN PÉRGOLA\| gpergola@elpais.com.uy'
  out = re.sub(replace_pattern, '.', out, 9999, re.IGNORECASE)

  replace_pattern = r' MARCELO GALLARDO Y GASTÓN PÉRGOLA'
  out = re.sub(replace_pattern, '.', out, 9999, re.IGNORECASE)

  replace_pattern = r' Punta del Este \| Gastón Pérgola'
  out = re.sub(replace_pattern, '.', out, 9999, re.IGNORECASE)

  replace_pattern = r'Gastón Pérgola'
  out = re.sub(replace_pattern, '.', out, 9999, re.IGNORECASE)

  replace_pattern = r'gpergola@elpais.com.uy'
  out = re.sub(replace_pattern, '.', out, 9999, re.IGNORECASE)

  return out

def clean_sebastian_panzl(line):
  out = line

  replace_pattern = r' Por Sebastián Panzl spanzl@elpais.com.uy'
  out = re.sub(replace_pattern, '.', out, 9999, re.IGNORECASE)

  replace_pattern = r' Por Sebastián Panzl - spanzl@elpais.com.uy'
  out = re.sub(replace_pattern, '.', out, 9999, re.IGNORECASE)

  replace_pattern = r'spanzl@elpais.com.uy'
  out = re.sub(replace_pattern, '', out, 9999, re.IGNORECASE)

  return out

def clean_claudio_destefano(line):
  out = line

  replace_pattern = r'(Por )?(Claudio Destéfano.*?claudio@bizers.com.ar)'
  out = re.sub(replace_pattern, r'.', out, 9999, re.IGNORECASE)

  return out

def clean_antonio_larronda(line):
  out = line

  replace_pattern = r'(Por)?\s*(Antonio Larronda)?\s*?(alarronda@elpais.com.uy|\|\s*?alarronda@elpais.com.uy|\(alarronda@elpais.com.uy\)|-?\[alarronda@elpais.com.uy\])'
  out = re.sub(replace_pattern, r'\.', out, 999, re.IGNORECASE)
  
  return out

def clean_elbio_rodriguez(line):
  out = line

  replace_pattern = r'(Por )?(Elbio )?(Rodriguez Barilari\s*?barilari@laraza.com)'
  out = re.sub(replace_pattern, r'', out, 9999, re.IGNORECASE)

  replace_pattern = r'(Por )?(Elbio )?(Rodrguez Barilari\s*?barilari@laraza.com)'
  out = re.sub(replace_pattern, r'', out, 9999, re.IGNORECASE)

  replace_pattern = r'barilari@laraza.com'
  out = re.sub(replace_pattern, r'', out, 9999, re.IGNORECASE)

  return out

def clean_stella_maris(line):
  out = line

  replace_pattern = r'POR STELLA M. PUSINO \/ spusino@elpais.com.uy'
  out = re.sub(replace_pattern, r'.', out, 9999, re.IGNORECASE)

  replace_pattern = r'POR STELLA M. PUSINO \| spusino@elpais.com.uy'
  out = re.sub(replace_pattern, r'.', out, 9999, re.IGNORECASE)

  replace_pattern = r'Stella Maris Pusino - spusino@elpais.com.uy'
  out = re.sub(replace_pattern, r'.', out, 9999, re.IGNORECASE)

  replace_pattern = r'Stella Maris Pusino \[spusino@elpais.com.uy\]'
  out = re.sub(replace_pattern, r'.', out, 9999, re.IGNORECASE)

  replace_pattern = r'spusino@elpais.com.uy'
  out = re.sub(replace_pattern, r'.', out, 9999, re.IGNORECASE)

  return out

def clean_mariana_goday(line):
  out = line

  replace_pattern = r'(POR Mariana Goday.*?)?(mgoday@elpais.com.uy]?)'
  out = re.sub(replace_pattern, r'.', out, 9999, re.IGNORECASE)

  return out

def clean_gabriela_rocha(line):
  out = line

  replace_pattern = r'(POR Gabriela Rocha.*?)?(grocha@elpais.com.uy)'
  out = re.sub(replace_pattern, r'.', out, 9999, re.IGNORECASE)

  return out

def clean_diego_ferreira(line):
  out = line

  replace_pattern = r'(Por )?(DIEGO FERREIRA.*?)?(dferreira@elpais.com.uy]?)'
  out = re.sub(replace_pattern, r'.', out, 9999, re.IGNORECASE)

  return out

def clean_silvana_nicola(line):
  out = line

  replace_pattern = r'(Por )?(SILVANA NICOLA.*?)?(snicola@elpais.com.uy]?)'
  out = re.sub(replace_pattern, r'.', out, 9999, re.IGNORECASE)

  return out


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
  replace_pattern = r"No salgas a la calle sin saber de qué se habla..."
  text = re.sub(replace_pattern, '', text)

  replace_pattern = r"No salgas a la calle sin ver más► saber de qué se habla"
  text = re.sub(replace_pattern, '', text)

  replace_pattern = r"No salgas a la calle sin ver más> saber de qué se habla"
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
  replace_pattern = r"^\d?\d \w\w\w \d\d\d\d"
  text = re.sub(replace_pattern, '', text)  

  # dentro el string
  replace_pattern = r"\d?\d \w\w\w \d\d\d\d"
  text = re.sub(replace_pattern, '.', text)  

  # Formato  dia mes nn YYYY hh:mm 
  # al inicio
  replace_pattern = r"^\w\w\w \w\w\w \d?\d \d\d\d\d \d\d:\d\d"
  text = re.sub(replace_pattern, '', text)

  # dentro del string
  replace_pattern = r"\w\w\w \w\w\w \d?\d \d\d\d\d \d\d:\d\d"
  text = re.sub(replace_pattern, '.', text)

  # Formato -dia mmm dd YYYY- (sin hora)
  # al inicio
  replace_pattern = r"^\w\w\w \w\w\w \d?\d \d\d\d\d"
  text = re.sub(replace_pattern, '', text)

  # dentro del string
  replace_pattern = r"\w\w\w \w\w\w \d?\d \d\d\d\d"
  text = re.sub(replace_pattern, '.', text) 

  text = clean_jorge_chouy(text)
  text = clean_gaston_pergola(text)
  text = clean_sebastian_panzl(text)
  text = clean_claudio_destefano(text)
  text = clean_antonio_larronda(text)
  text = clean_elbio_rodriguez(text)
  text = clean_stella_maris(text)
  text = clean_mariana_goday(text)
  text = clean_gabriela_rocha(text)
  text = clean_diego_ferreira(text)
  text = clean_silvana_nicola(text)

  # Elimino correos de autores
  # reemplazo con un punto
  replace_pattern = r'( jcraffo@elpais.com.uy| vdiaz@elpais.com.uy| pjimenez@seragro.com.uy| lmelendez@elpais.com.uy| nlussich@seragro.com.uy| claudio@bizers.com.ar)'
  text = re.sub(replace_pattern, r'.', text, 9999, re.IGNORECASE)

  # elimino sin reemplazar el correo
  replace_pattern = r'(barilarius@yahoo.com|elpepepregunton@gmail.com)'
  text = re.sub(replace_pattern, r'', text, 9999, re.IGNORECASE)

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
  replace_pattern = r"(AFP)? El Pais Digital$"
  text = re.sub(replace_pattern, '', text, re.IGNORECASE)  

  replace_pattern = r"AFP El Pais Digital."
  text = re.sub(replace_pattern, '', text, re.IGNORECASE) 

  # texto "El Pais Digital" se reserva el derecho de editar......
  replace_pattern = r"El Pais Digital se reserva el derecho de editar los mensajes que usted envie a los efectos de su mejor comprension por otros usuarios. (Nuevo seudonimo:)?"
  text = re.sub(replace_pattern, '', text)

  # texto "EFE"
  replace_pattern = r" EFE "
  text = re.sub(replace_pattern, '', text)  

  replace_pattern = r"\(EFE\)"
  text = re.sub(replace_pattern, '', text)  
  # To Do: tengo que seguir revisando este caso  de del contexto de EFE ------------------------------------------------------------------------------------------------------------------------------

  # texto "Otras notas de Editorial"
  replace_pattern = r"Otras notas de Editorial"
  text = re.sub(replace_pattern, '', text, re.IGNORECASE)  
  return text
