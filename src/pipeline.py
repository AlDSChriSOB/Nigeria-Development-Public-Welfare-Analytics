"""Aggregate indicator pipeline; source-specific primary-data mappings are separate work."""
from pathlib import Path
import json, hashlib, sqlite3, urllib.request, datetime, sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

COLUMNS=['period','geography','metric','value','unit','source_url','vintage']
KEY=['period','geography','metric','unit','vintage']
def validate(d):
    missing=set(COLUMNS)-set(d.columns)
    if missing: raise ValueError('Missing columns: '+str(sorted(missing)))
    d=d[COLUMNS].copy()
    for col in KEY+['source_url']:
        if d[col].isna().any() or d[col].astype(str).str.strip().eq('').any():raise ValueError('Missing key/source: '+col)
    d['period']=pd.to_datetime(d.period,errors='raise').dt.strftime('%Y-%m-%d')
    original=d.value.copy();d['value']=pd.to_numeric(d.value,errors='coerce')
    if (original.notna()&d.value.isna()).any():raise ValueError('Non-numeric value')
    if np.isinf(d.value.dropna()).any():raise ValueError('Infinite value')
    if d.duplicated(KEY).any():raise ValueError('Duplicate observation keys; resolve joins/vintages before analysis')
    return d.sort_values(KEY)

def wdi(c,project):
    rows=[];raw=project/'data/raw';raw.mkdir(parents=True,exist_ok=True);sources=[]
    for code,label in c['indicators'].items():
        url=f'https://api.worldbank.org/v2/country/NGA/indicator/{code}?format=json&per_page=100'
        cache=raw/(code+'.json')
        if not cache.exists():
            req=urllib.request.Request(url,headers={'User-Agent':'NigeriaPortfolio/1.0'})
            with urllib.request.urlopen(req,timeout=45) as response: cache.write_bytes(response.read())
        payload=json.loads(cache.read_text())
        if not isinstance(payload,list) or len(payload)<2 or not isinstance(payload[1],list):raise ValueError('Unexpected WDI response for '+code)
        vintage=payload[0].get('lastupdated','unknown')
        for r in payload[1]:
            if int(r['date'])>=2000:
                rows.append([r['date']+'-01-01','Nigeria',label,r['value'],label.split('(')[-1].rstrip(')'),url,vintage])
        sources.append({'url':url,'sha256':hashlib.sha256(cache.read_bytes()).hexdigest(),'lastupdated':vintage})
    return pd.DataFrame(rows,columns=COLUMNS),sources

def run(project):
    project=Path(project);c=json.loads((project/'project.json').read_text());out=project/'outputs';out.mkdir(exist_ok=True)
    if (project/'data/input.csv').exists():
        prov=project/'data/provenance.json'
        if not prov.exists():raise ValueError('Supply data/provenance.json documenting original sources and transformation before analysis')
        d=pd.read_csv(project/'data/input.csv');sources=json.loads(prov.read_text());scope='PRIMARY_AGGREGATES_SUPPLIED'
    elif c['indicators']:
        d,sources=wdi(c,project);scope='NATIONAL_PREVIEW_ONLY'
    else:
        status={'status':'AWAITING_PRIMARY_DATA','scope':'NOT_EXECUTED','reason':'Obtain and transform the primary source into data/input.csv and document data/provenance.json. No fabricated data was used.'}
        (out/'status.json').write_text(json.dumps(status,indent=2));return status
    d=validate(d)
    if d.value.notna().sum()==0:raise ValueError('Source contains no observed numeric data')
    d.to_csv(out/'observations.csv',index=False)
    with sqlite3.connect(out/'analysis.sqlite') as conn:
        d.to_sql('observations',conn,if_exists='replace',index=False)
        duplicate=pd.read_sql_query((project/'sql/quality.sql').read_text(),conn)
        if len(duplicate):raise ValueError('SQL duplicate key audit failed')
        a=pd.read_sql_query((project/'sql/analysis.sql').read_text(),conn)
    # Independent reconciliation prevents mixing adjacent metrics in LAG calculations.
    expected=d.dropna(subset=['value']).sort_values(['geography','metric','unit','vintage','period']).copy()
    expected['absolute_change']=expected.groupby(['geography','metric','unit','vintage']).value.diff()
    expected=expected.sort_values(['metric','geography','period'])
    if not np.allclose(expected.absolute_change,a.absolute_change,equal_nan=True):raise AssertionError('SQL/pandas change mismatch')
    a.to_csv(out/'analysis.csv',index=False)
    quality={'rows':len(d),'observed_rows':int(d.value.notna().sum()),'missing_value_rows':int(d.value.isna().sum()),'duplicate_keys':0}
    (out/'quality.json').write_text(json.dumps(quality,indent=2))
    (out/'sources.json').write_text(json.dumps(sources,indent=2))
    first=a.metric.iloc[0];s=a[a.metric==first];fig,ax=plt.subplots(figsize=(10,5));ax.plot(pd.to_datetime(s.period),s.value,marker='o',markersize=3,color='#087F5B');ax.set(title=c['title']+' — national preview' if scope=='NATIONAL_PREVIEW_ONLY' else c['title'],xlabel='Observation year',ylabel=first);fig.tight_layout();fig.savefig(out/'trend.png',dpi=150);plt.close(fig)
    latest=a.sort_values('period').groupby(['geography','metric','unit','vintage'],as_index=False).tail(1)
    latest.to_csv(out/'latest.csv',index=False)
    status={'status':'EXECUTED','scope':scope,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':len(d),'metrics':list(a.metric.unique()),'primary_case_complete':False,'native_bi_validated':False}
    (out/'status.json').write_text(json.dumps(status,indent=2))
    (project/'reports/RESULTS.md').write_text('# '+c['title']+'\n\nScope: '+scope+'\n\n'+c['caveat']+'\n\nSQL change calculations were independently reconciled against pandas. See outputs/latest.csv for last observed values by metric; different indicators can end in different years. No cross-indicator total is meaningful. Missing values were not set to zero.\n\n![First indicator](../outputs/trend.png)\n\nPrimary case study and native BI dashboards remain incomplete.\n')
    return status

if __name__=='__main__':print(run(sys.argv[1]))
