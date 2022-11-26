# nativas
import re
import sys
import json
import argparse
# 3eros
from bs4 import BeautifulSoup, Tag, NavigableString
from unidecode import unidecode
from tqdm.auto import tqdm
# propias
import utils

# funciones auxiliares
simplify = lambda data: [a.get('html') for a in data['articles']]

"""
notes on BeautifulSoup parsers:
* html.parser- built-in - no extra dependencies needed
* html5lib - the most lenient - better use it if HTML is broken
* lxml - the fastest
"""

# funciones auxiliares
get_hdr_links   = lambda doc: BeautifulSoup(doc, features="lxml").select('div.article-header div.article-date-author a')
is_cat_link     = lambda a: "seccion" in a.get("href")
get_cat_link    = lambda d: next(iter([a.get("href") for a in get_hdr_links(d) if is_cat_link(a)]), "0")
get_cat         = lambda link: next(l for l in link.split("/")[::-1] if len(l) > 0)

# funcion de alto orden. retorna una funcion booleana que 
# retorna `true` si el doc `d` es de la categoria `cat`
# si `cat` es el string vacio, o el caracter "*" tambien 
# retorna `true`
def is_of_cat(cat):
    def of_cat(d):
        links = [a.get("href") for a in get_hdr_links(d) if is_cat_link(a)]
        c = get_cat(links[0]) if len(links) == 1 else str(len(links))
        return c == cat or cat in ["", "*"]
    return of_cat

# auxiliares
get_tags     = lambda el: [tag.name for tag in el.find_all()]
get_children = lambda el: el.findChildren(recursive=False)
last_child   = lambda cs: cs[-1] if cs else None
_is          = lambda el, tagname: el.name == tagname
has_class    = lambda el, cl: el != None and el.get("class") and cl in el.get("class")

def curate(data, verbose):

  if verbose:
    print("curating...", file=sys.stderr)

  curated = []
  cat_blacklist = ['humor', 'humor-lento','0'] # '0' representa "sin categoria"

  for d in tqdm(data[:], disable=not verbose):
    if get_cat(get_cat_link(d)) in cat_blacklist:
      curated.append(None)
      continue
    
    # 1. body-only
    a = BeautifulSoup(d, features="lxml").select_one('div.article-body')
    
    # 2. se eliminan los embebidos
    for el in a.select('div.extension'):
      el.decompose()
    
    # 3. se eliminan las imagenes 
    for el in a.select('div.inline-image-wrap'):
      el.decompose()
    
    # 4. se eliminan los sup
    for el in a.select('sup'):
      el.decompose()
    
    # 5. se eliminan los hr
    for el in a.select('hr'):
      el.decompose()
    
    # 6. se eliminan las tablas
    for el in a.select('table'):
      el.decompose()
    
    # 7. se eliminan las img
    for el in a.select('img'):
      el.decompose()
    
    # 8. si **el ultimo** elem es una lista `ul`, entonces se elimina
    # 9. si **el ultimo** elem es un `div.footnote`, entonces se elimina
    l = last_child(get_children(a))
    while l and (_is(l,"ul") or _is(l,"blockquote") or has_class(l,"footnote")):
      l.decompose()
      l = last_child(get_children(a))
        
    # 10. eliminacion de links de tipo "leé más"
    uls        = a.select('ul')
    deletables = ["Leé más sobre esto" in str(ul) for ul in uls]
    for ul,deletable in zip(uls, deletables):
      if deletable:
        ul.decompose()
        
    curated.append(a)
  
  return curated
    

def sanatice(curated, verbose):

  if verbose:
    print("sanitizing...", file=sys.stderr)
  
  def get_text(tag:Tag) -> str:
    _inline_elements = {"a","span","em","strong","u","i","font","mark","label",
    "s","sub","sup","tt","bdo","button","cite","del","b","a","font"}

    def _get_text(tag:Tag):
      for child in tag.children:
        if type(child) is Tag:
          # if the tag is a block type tag then yield new lines before after
          is_block_element = child.name not in _inline_elements
          if is_block_element: yield "\n"
          yield from ["\n"] if child.name=="br" else  _get_text(child)
          if is_block_element: yield "\n"
        elif type(child) is NavigableString:
          yield child.string
    return "".join(_get_text(tag))

  # estoy interesado en obtener todos los caracteres que no sean:
  # 1. ASCII
  whiteList = '\x00-\x7F'
  # 2. ¿ ¡ tildes y enies
  whiteList += '¿¡À-ÿñÑ'
  regex = r'[^{}]'.format(whiteList)
  patt = re.compile(regex)
  sanitice_char = lambda c: unidecode(c) if patt.match(c) else c
  sanitice_text = lambda txt: "".join([sanitice_char(c) for c in txt])
  sanitized = [
    sanitice_text(get_text(c)) if c else None
    for c in tqdm(curated[:], disable=not verbose)
  ]
  return sanitized

def rm_links(sanitized, verbose):

  if verbose:
    print("removing explicit links...", file=sys.stderr)

  remove_links = lambda txt: re.sub(r'https?://\S+', 'link', txt)
  return [
    remove_links(c) if c else None
    for c in tqdm(sanitized[:], disable=not verbose)
  ]

def rm_shorties(sanitized):
  return [s if s and len(s) > 500 else None for s in sanitized]

# auxiliar
trim = lambda txt: re.sub(r'\n\s*\n', '\n', txt.strip())


def parse_data(
  input='input/la_diaria/Latest20k.json',
  output='output/la_diaria/la-diaria.txt',
  verbose=utils.DEFAULT_VERBOSE,
):
  
  if not utils.is_txt_postfix(output):
    utils.die("el output debe terminar en .txt")

  utils.assure_path(output)

  f = open(input)
  data = json.loads(f.read())
  f.close()

  out = simplify(data)
  out = curate(out, verbose)
  out = sanatice(out,verbose)
  out = rm_links(out,verbose)
  out = rm_shorties(out)

  if verbose:
    print("writing...", file=sys.stderr)

  with open(output, 'w', encoding='utf-8') as f:
    for s in tqdm(out, disable=not verbose):
      if not s: continue;
      f.write(trim(s) + "\n\n")
    
    # se elimina el ultimo \n\n
    f.seek(0,2)        # end of file
    size=f.tell()      # the size...
    f.truncate(size-1) # truncat  
    

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', default='input/la_diaria/Latest20k.json')
  parser.add_argument('-o', '--output', default='output/la_diaria/la-diaria.txt')
  parser.add_argument('-v', '--verbose', action='store_true')
  parser.add_argument('--no-verbose', dest='verbose', action='store_false')
  parser.set_defaults(verbose=utils.DEFAULT_VERBOSE)
  args = parser.parse_args()
  
  parse_data(args.input, args.output, args.verbose)