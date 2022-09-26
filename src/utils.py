import re
import html
import unicodedata
import os

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

def create_folder(folder_path):
  try:
    os.makedirs(folder_path)
  except:
    pass