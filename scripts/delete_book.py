"""Delete a book and its generated pages from every published version."""
import argparse,json,re
from pathlib import Path
SLUGS={'choices':'养育的选择','wholebrain':'全脑教养法','stepdad':'The Smart Stepdad','world-order':'世界秩序','missing':'影子里的中国'}
def remove(root,slug):
 if slug not in SLUGS:raise ValueError('Unknown book')
 removed=[]
 for f in list(root.rglob('*')):
  if f.is_file() and (f.name==slug+'.html' or f.name.startswith(slug+'-')):
   removed.append(str(f.relative_to(root)));f.unlink()
 for f in root.rglob('catalog*.js'):
  s=f.read_text();m=re.fullmatch(r'\s*const books\s*=\s*(\[.*\]);?\s*',s,re.S)
  if not m:raise ValueError('Unrecognized catalog: '+str(f))
  data=json.loads(m[1]);data=[b for b in data if b.get('slug')!=slug]
  f.write_text('const books='+json.dumps(data,ensure_ascii=False)+';')
 return removed
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--slug',required=True,choices=SLUGS);p.add_argument('--confirm',required=True);p.add_argument('--root',default='docs');a=p.parse_args()
 if a.confirm!=a.slug:p.error('Confirmation must exactly match book ID')
 print(json.dumps({'book':a.slug,'removed':remove(Path(a.root),a.slug)},ensure_ascii=False))
