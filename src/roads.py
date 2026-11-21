"""NBS/FRSC primary-table adapter. Workbook layout and totals validated before use."""
from pathlib import Path
import urllib.request,zipfile,io,re,json,hashlib,sqlite3
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
URL='https://microdata.nigerianstat.gov.ng/index.php/catalog/164/download/1405'
SOURCE='https://microdata.nigerianstat.gov.ng/index.php/catalog/164'
LABELS=['Fatal crashes','Serious crashes','Minor crashes','Total crashes','Injured persons','Killed persons','Casualties','Persons involved']

def tables(root):
 raw=root/'data/raw';raw.mkdir(parents=True,exist_ok=True);cache=raw/'nbs_roads_q1_2026.zip'
 if not cache.exists():
  with urllib.request.urlopen(URL,timeout=60) as res:blob=res.read()
  if not zipfile.is_zipfile(io.BytesIO(blob)):raise ValueError('NBS did not return a ZIP')
  cache.write_bytes(blob)
 z=zipfile.ZipFile(cache);names=[n for n in z.namelist() if n.lower().endswith('.xlsx')]
 if len(names)!=1:raise ValueError('Expected exactly one workbook')
 b=z.read(names[0]);x=pd.read_excel(io.BytesIO(b),header=None)
 audit=[];rows=[]
 for col in x.columns:
  if str(x.iloc[2,col]).strip().upper()!='STATE':continue
  match=re.search(r'Q([1-4])\s+(20\d\d)',str(x.iloc[0,col]))
  if not match:continue
  q,year=map(int,match.groups());period=f'{year}-{3*q-2:02d}-01'
  d=x.iloc[3:40,col:col+9].copy();d.columns=['state']+LABELS
  if len(d)!=37 or d.state.nunique()!=37:raise ValueError('State coverage changed')
  v=d[LABELS].apply(pd.to_numeric,errors='raise');total=pd.to_numeric(x.iloc[40,col+1:col+9],errors='raise').to_numpy(dtype=float)
  if v.isna().any().any() or (v<0).any().any():raise ValueError('Missing or negative state counts')
  if not np.allclose(v.sum(),total):raise ValueError('State sums differ from published totals')
  if not np.allclose(v['Fatal crashes']+v['Serious crashes']+v['Minor crashes'],v['Total crashes']):raise ValueError('Crash severity reconciliation failed')
  if not np.allclose(v['Injured persons']+v['Killed persons'],v['Casualties']):raise ValueError('Casualty reconciliation failed')
  audit.append({'period':period,'states':37,'published_total_crashes':float(total[3]),'state_sum_crashes':float(v['Total crashes'].sum()),'reconciled':True})
  for j in range(37):
   row={'period':period,'state':str(d.iloc[j,0]).strip(),'quarter':q,'year':year}
   row.update({k:float(v.iloc[j][k]) for k in LABELS});rows.append(row)
 fact=pd.DataFrame(rows);assert len(fact)==22*37
 # Latest-quarter factor block; validate labels, state alignment and national totals.
 target=[i for i in x.columns if re.match(r'Q1\s+2026',str(x.iloc[98,i]))]
 if len(target)!=1:raise ValueError('Latest factor block ambiguous')
 c=target[0]
 if str(x.iloc[99,c]).strip()!='STATE':raise ValueError('Factor header moved')
 factors=[]
 for j in range(c+1,c+19):
  code=str(x.iloc[99,j]).strip();vals=pd.to_numeric(x.iloc[100:137,j],errors='raise')
  if vals.isna().any() or (vals<0).any():raise ValueError('Invalid factor counts')
  published=float(x.iloc[137,j])
  if not np.isclose(vals.sum(),published):raise ValueError('Factor total does not reconcile: '+code)
  for k,val in enumerate(vals):factors.append({'period':'2026-01-01','state':str(x.iloc[100+k,c]).strip(),'factor':code,'reported_mentions':float(val)})
 return fact,pd.DataFrame(factors),audit,{'source_url':URL,'sha256_zip':hashlib.sha256(cache.read_bytes()).hexdigest(),'sha256_workbook':hashlib.sha256(b).hexdigest(),'sheet':'Sheet1','vintage':'NBS Q1 2026 release','state_rows_1based':'4–40','state_header_row_1based':3,'factor_rows_1based':'101–137','factor_header_row_1based':100}

def prepare(project):
 root=project.parents[1];fact,factors,audit,prov=tables(root)
 out=project/'outputs';out.mkdir(exist_ok=True)
 fact.to_csv(out/'state_quarter.csv',index=False);factors.to_csv(out/'factor_mentions_q1_2026.csv',index=False)
 pd.DataFrame(audit).to_csv(out/'published_total_audit.csv',index=False)
 records=[];id=json.loads((project/'project.json').read_text())['id']
 if id==16:
  for _,r in fact.iterrows():
   for m in ['Total crashes','Killed persons','Injured persons']:
    records.append([r.period,r.state,m,r[m],'crashes' if m=='Total crashes' else 'persons',URL,prov['vintage']])
 elif id==17:
  for period,d in fact.groupby('period'):
   records.append([period,'Nigeria','Total crashes',d['Total crashes'].sum(),'crashes',URL,prov['vintage']])
 else:
  for _,r in factors.iterrows():records.append([r.period,r.state,'Reported factor: '+r.factor,r.reported_mentions,'mentions',URL,prov['vintage']])
 df=pd.DataFrame(records,columns=['period','geography','metric','value','unit','source_url','vintage'])
 df.to_csv(project/'data/input.csv',index=False);(project/'data/provenance.json').write_text(json.dumps(prov,indent=2))

def analyse(project):
 out=project/'outputs';fact=pd.read_csv(out/'state_quarter.csv');factors=pd.read_csv(out/'factor_mentions_q1_2026.csv')
 c=json.loads((project/'project.json').read_text());id=c['id'];conn=sqlite3.connect(out/'analysis.sqlite');fact.to_sql('state_quarter',conn,index=False,if_exists='replace');factors.to_sql('factor_mentions',conn,index=False,if_exists='replace')
 queries={16:'''SELECT state, "Total crashes" AS crashes, "Killed persons" AS deaths, "Injured persons" AS injuries, 100.0*"Fatal crashes"/NULLIF("Total crashes",0) AS fatal_crash_percentage,100.0*"Killed persons"/NULLIF("Total crashes",0) AS deaths_per_100_crashes FROM state_quarter WHERE period=(SELECT MAX(period) FROM state_quarter) ORDER BY crashes DESC;''',17:'''WITH totals AS (SELECT period,year,quarter,SUM("Total crashes") AS crashes,SUM("Killed persons") AS deaths FROM state_quarter GROUP BY period,year,quarter) SELECT a.*,b.crashes AS same_quarter_previous_year,100.0*(a.crashes-b.crashes)/NULLIF(b.crashes,0) AS yoy_change_pct FROM totals a LEFT JOIN totals b ON a.year=b.year+1 AND a.quarter=b.quarter ORDER BY a.period;''',18:'''SELECT factor,SUM(reported_mentions) AS reported_mentions FROM factor_mentions GROUP BY factor ORDER BY reported_mentions DESC;'''}
 sql=queries[id];(project/'sql/primary_analysis.sql').write_text(sql+'\n');a=pd.read_sql_query(sql,conn);a.to_csv(out/'primary_analysis.csv',index=False)
 conn.close();fig,ax=plt.subplots(figsize=(11,5))
 if id==16:ax.barh(a.state.head(12)[::-1],a.crashes.head(12)[::-1]);ax.set(xlabel='Reported crashes',title='Highest recorded crash counts: Q1 2026');r=a.iloc[0];finding=f'{r.state} recorded the largest crash count in Q1 2026: {r.crashes:,.0f}. This is a count ranking, not a road-user risk ranking.'
 elif id==17:
  ax.plot(pd.to_datetime(a.period),a.crashes,marker='o');ax.set(xlabel='Quarter',ylabel='Reported crashes',title='Quarterly reported crashes: Q4 2020–Q1 2026');last=a.iloc[-1];finding=f'Q1 2026 recorded {last.crashes:,.0f} crashes, a {last.yoy_change_pct:+.2f}% change from Q1 2025.'
  complete=a[a.year.between(2021,2025)];season=complete.groupby('quarter',as_index=False).agg(mean_crashes=('crashes','mean'),years=('year','nunique'));season.to_csv(out/'balanced_quarter_comparison.csv',index=False)
 else:
  ax.barh(a.factor.head(12)[::-1],a.reported_mentions.head(12)[::-1]);ax.set(xlabel='Reported factor mentions',title='Reported contributing factors: Q1 2026');r=a.iloc[0];finding=f'{r.factor} has the most recorded mentions: {r.reported_mentions:,.0f}. Factor mentions are not mutually exclusive crash outcomes.'
 fig.tight_layout();fig.savefig(out/'trend.png',dpi=150);plt.close(fig)
 caveat=('No mileage or journey exposure denominator is available. Reporting and traffic volumes differ across states.' if id==16 else 'Only quarterly timing is observed. The balanced seasonality comparison uses 2021–2025, five complete years. No hour-of-day risk or prospective safety advice is inferred.' if id==17 else 'Factor mentions and severity are separate aggregate tables. They cannot establish factor-specific fatality risk, causal effects or individual crash mechanisms. The intended factor-by-severity analysis remains blocked by missing linked incident records.')
 text=f'# {c["title"]}: primary NBS analysis\n\n{finding}\n\n## Evidence and validation\n22 quarters × 37 states/FCT = 814 state-quarter records. All eight state-count columns reconcile to source national totals in every quarter. Severity categories and casualty components reconcile for every state-quarter. The latest-quarter factor columns separately reconcile to published national totals. The adapter records source hashes and exact workbook rows.\n\n## Methods\nSQL is in sql/primary_analysis.sql. Source: {URL}. Data tables and a balanced-period seasonality comparison are exported in outputs/.\n\n![Primary chart](../outputs/trend.png)\n\n## Limits\n{caveat}\n\n## Decision use\nUse counts to select locations or periods for a more detailed reporting and exposure audit. Do not equate fewer reports with safer roads.\n\nNative Power BI and Tableau authoring/validation is deferred to the user’s desktop session.\n'
 (project/'reports/RESULTS.md').write_text(text)
 s=json.loads((out/'status.json').read_text());s.update(scope='PRIMARY_NBS_TABLES',primary_analysis_executed=True,primary_case_complete=id in [16,17],native_bi_validated=False,remaining_limit=caveat);(out/'status.json').write_text(json.dumps(s,indent=2));return s
