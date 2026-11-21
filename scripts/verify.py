from pathlib import Path
import sys,json,zipfile
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.pipeline import validate
r=Path(__file__).resolve().parents[1]
cs=json.loads((r/'catalog.json').read_text());states=json.loads((r/'STATUS.json').read_text())
assert len(cs)==20 and len(states)==20
for c,s in zip(cs,states):
 p=r/'projects'/c['slug']
 for f in ['README.md','sql/analysis.sql','sql/quality.sql','python/run.py','notebooks/analysis.ipynb','powerbi/ImportAnalysis.pq','powerbi/measures.dax','tableau/BUILD.md','excel/analysis.xlsx'] :assert (p/f).stat().st_size>0,f
 with zipfile.ZipFile(p/'excel/analysis.xlsx') as z:
  assert len([n for n in z.namelist() if n.startswith('xl/worksheets/sheet') and n.endswith('.xml')])==3
 if s['status']=='EXECUTED':
  d=pd.read_csv(p/'outputs/observations.csv');validate(d)
  try:validate(pd.concat([d,d.head(1)],ignore_index=True))
  except ValueError:pass
  else:raise AssertionError('Duplicate keys not rejected')
  assert (p/'outputs/analysis.csv').exists()
  n=json.loads((p/'notebooks/analysis.ipynb').read_text());assert all(cell.get('execution_count') for cell in n['cells'] if cell['cell_type']=='code')
 assert s['status'] in ['EXECUTED','AWAITING_PRIMARY_DATA']
print('Verified 20 directories and workbooks; duplicate-key protection checked against actual source records. Native BI not tested.')
