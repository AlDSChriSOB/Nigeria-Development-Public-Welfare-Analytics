import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=process.env.NIGERIA_REPO_ROOT || process.cwd();
const items=JSON.parse(await fs.readFile(process.env.NIGERIA_EXCEL_INPUT || '/tmp/nigeria_excel_build/inputs.json','utf8'));
const log=[];
for(const {config:c,rows} of items){
 const p=`${root}/projects/${c.slug}`;const wb=Workbook.create();
 const overview=wb.worksheets.add('Overview'),data=wb.worksheets.add('Data'),sources=wb.worksheets.add('Methods');
 for(const sh of [overview,data,sources]){sh.showGridLines=false;sh.getRange('A1:L60').format.font={name:'Arial',size:10};sh.getRange('A1:L60').format.columnWidth=18;}
 overview.getRange('A2').values=[[c.title]];overview.getRange('A2').format.font={name:'Arial',size:15,bold:true};
 overview.getRange('A4:B8').values=[['Scope',rows.length?'National indicator preview':'Awaiting primary data'],['Metric',rows.length?rows[0].metric:'No observations supplied'],['Unit',rows.length?rows[0].unit:'Not yet defined'],['Observations',null],['Latest observed value',null]];
 overview.getRange('A4:A8').format.font={bold:true};overview.getRange('B4:B6').format.columnWidth=48;
 const headers=['period','geography','metric','value','unit','source_url','vintage','previous_value','absolute_change'];
 data.getRange('A1:I1').values=[headers];data.getRange('A1:I1').format={fill:'#174D3C',font:{bold:true,color:'#FFFFFF'}};
 if(rows.length){data.getRange(`A2:I${rows.length+1}`).values=rows.map(r=>headers.map(h=>h==='period'?new Date(r[h]+'T00:00:00Z'):r[h]??null));}
 const end=Math.max(2,rows.length+1);data.getRange(`A2:A${end}`).setNumberFormat('yyyy-mm-dd');data.getRange(`D2:D${end}`).setNumberFormat('#,##0.00');data.getRange(`H2:I${end}`).setNumberFormat('#,##0.00');data.freezePanes.freezeRows(1);data.getRange('C1:C30').format.columnWidth=52;data.getRange('F1:F30').format.columnWidth=64;
 overview.getRange('B7').formulas=[[`=COUNT(Data!D2:D${end})`]];
 const first=rows.length?rows.filter(r=>r.metric===rows[0].metric):[];
 overview.getRange('B8').formulas=[[first.length?`=Data!D${first.length+1}`:'=IF(B7=0,"No observations","")']];overview.getRange('B8').setNumberFormat('#,##0.00');
 overview.getRange('A11').values=[['One selected metric is shown; do not total different units.']];
 if(first.length){overview.getRange('A14:B14').values=[['Year','Observed value']];overview.getRange(`A15:B${first.length+14}`).formulas=first.map((r,i)=>[`=YEAR(Data!A${i+2})`,`=Data!D${i+2}`]);overview.getRange(`B15:B${first.length+14}`).setNumberFormat('#,##0.00');const chart=overview.charts.add('line',overview.getRange(`A14:B${first.length+14}`));chart.title=rows[0].metric;chart.setPosition('D14','L29');}
 sources.getRange('A2:B8').values=[['Question',c.question],['Source',c.source],['URL',c.source_url],['Limits',c.caveat],['Native BI','Power BI and Tableau dashboards pending authoring and validation'],['Refresh','Rerun Python, then rebuild this workbook; no automatic connection'],['Interpretation','Changes are between available observations, not necessarily consecutive years.']];sources.getRange('A2:A8').format.font={bold:true};sources.getRange('B2:B8').format.columnWidth=110;sources.getRange('B2:B8').format.wrapText=true;sources.getRange('A2:B8').format.rowHeight=44;
 wb.recalculate();const check=await wb.inspect({kind:'table',range:'Overview!A4:B8',include:'values,formulas',tableMaxRows:5,tableMaxCols:2});
 const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!',options:{useRegex:true,maxResults:10}});
 for(const [sheet,range] of [['Overview','A1:L30'],['Data','A1:I8'],['Methods','A1:B9']]){const png=await wb.render({sheetName:sheet,range,scale:1,format:'png'});await fs.writeFile(`/tmp/nigeria_excel_build/${c.id}_${sheet}.png`,new Uint8Array(await png.arrayBuffer()));}
 await(await SpreadsheetFile.exportXlsx(wb)).save(`${p}/excel/analysis.xlsx`);
 log.push({project:c.slug,rows:rows.length,inspection:check.ndjson,errors:errors.ndjson});console.log('EXPORTED',c.id,rows.length);
}
await fs.writeFile(`${root}/EXCEL_VALIDATION.json`,JSON.stringify(log,null,2));
