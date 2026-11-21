from pathlib import Path
import json
from src.pipeline import run
root=Path(__file__).resolve().parent
results=[]
for p in sorted((root/'projects').iterdir()):
 try: status=run(p)
 except Exception as e:status={'status':'FAILED','reason':str(e)}
 results.append({'project':p.name,**status});print(p.name,status['status'],flush=True)
(root/'STATUS.json').write_text(json.dumps(results,indent=2))
if any(x['status']=='FAILED' for x in results):raise SystemExit(1)
