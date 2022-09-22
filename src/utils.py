import re
import html
import unicodedata

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
