"""Extract the two ADAC tyre PDFs used by AutoEcoKG. Python 3.9+, PyMuPDF."""
import argparse
import csv
import re
from pathlib import Path
try:
    import pymupdf as fitz
except ImportError:
    import fitz

ROOT = Path(__file__).resolve().parents[1]
ABRASION = 'adac_tyre_abrasion_2023_2025.pdf'
GUIDE = 'adac_summer_tyres_2025.pdf'
ROW = re.compile(r'^ *([^\n]+?)\s+(\d{3})\s+(\d{2})\s+R\s*(\d{2})\s+(SR|WR|AS)\s+(\d+)\s+(\d+,\d+) *$', re.M)
CATEGORIES = {'SR':'summer', 'WR':'winter', 'AS':'all_season'}
GRADES = [('Fahrsicherheit','safety_grade'),('Trocken','dry_grade'),('Fahrkomfort','comfort_grade'),('Fahrverhalten im Grenzbereich','limit_handling_grade'),('Bremsweg','dry_braking_grade'),('Nass','wet_grade'),('Bremsweg','wet_braking_grade'),('Aquaplaning längs','aquaplaning_longitudinal_grade'),('Aquaplaning quer','aquaplaning_lateral_grade'),('Handling','wet_handling_grade'),('Kreis-/Seitenführung','lateral_grip_grade'),('Umweltbilanz','environment_grade'),('Laufleistung','mileage_grade'),('Abrieb','abrasion_grade'),('Effizienz','efficiency_grade'),('Reifengewicht','weight_grade'),('Kraftstoffverbrauch','fuel_consumption_grade'),('Geräusch','noise_grade'),('Innengeräusch','interior_noise_grade'),('Außengeräusch','exterior_noise_grade'),('Nachhaltigkeit','sustainability_grade'),('Gesamtnote','overall_grade')]

def abrasion(path):
    rows=[]
    with fitz.open(path) as doc:
        for i in range(9,14):
            text=doc[i].get_text(sort=True)
            for m in ROW.finditer(text):
                name,w,a,r,cat,loss,index=m.groups()
                rows.append(dict(abrasion_id=f'ABR-{len(rows)+1:03d}',tyre_name=' '.join(name.split()),tyre_size=f'{w}/{a} R{r}',width_mm=int(w),aspect_ratio=int(a),rim_inches=int(r),category=CATEGORIES[cat],abrasion_mg_km_t=int(loss),estimated_unece_index=float(index.replace(',','.')),test_period='2023-2025',source_file=path.name,source_page=i+1,source_evidence=' '.join(m.group().split())))
    if len(rows)!=160: raise ValueError(f'Expected 160 appendix rows, extracted {len(rows)}. Check PDF edition.')
    return rows

def guide(path):
    rows=[]
    with fitz.open(path) as doc:
        for i,n,year,size in [(12,9,2025,'225/40 R18'),(13,9,2025,'225/40 R18'),(14,11,2024,'215/55 R17'),(15,5,2024,'215/55 R17')]:
            p=doc[i]
            # Page 16 contains unrelated example content on its right half.
            text=p.get_text(clip=fitz.Rect(0,0,p.rect.width/2,p.rect.height)) if i==15 else p.get_text()
            if f'Sommerreifentest {year}' not in text: raise ValueError(f'Unexpected guide page {i+1}')
            header=text.split('Gewichtung',1)[1].split('Labelangaben',1)[0]
            names=[s.strip() for s in header.splitlines() if s.strip()]
            # The 2024 Goodyear model occupies three extracted lines.
            if i==14:
                j=names.index('EfficientGrip'); names[j:j+2]=['EfficientGrip '+names[j+1]]
            if len(names)!=2*n: raise ValueError(f'Unexpected header count on page {i+1}: {names}')
            body=text.split('Labelangaben',1)[1].split('Stärken/Schwächen',1)[0]
            labels=re.findall(r'[A-G]/[A-G]/\d+',body)
            if len(labels)!=n: raise ValueError(f'Unexpected label count on page {i+1}')
            body=re.sub(r'\s+',' ',body.replace('\xad','')).strip()
            pos=0; values={}
            for label,key in GRADES:
                pattern=re.escape(label)+r'\s+(?:\d+\s*%\s+)?((?:\d,\d\s*){'+str(n)+r'})'
                m=re.search(pattern,body[pos:])
                if not m: raise ValueError(f'Missing {label} on guide page {i+1}')
                nums=re.findall(r'\d,\d',m.group(1)); values[key]=[float(v.replace(',','.')) for v in nums]
                pos+=m.end()
            for j in range(n):
                fuel,wet,noise=labels[j].split('/')
                brand,model=names[2*j:2*j+2]
                row=dict(tyre_test_id=f'TEST-{len(rows)+1:03d}',brand=brand,model=model,tyre_name=brand+' '+model,tyre_size=size,category='summer',test_year=year,eu_fuel_efficiency_class=fuel,eu_wet_grip_class=wet,eu_external_noise_db=int(noise),source_file=path.name,source_page=i+1,source_table_column=j+1)
                row.update({key:vals[j] for key,vals in values.items()}); rows.append(row)
    if len(rows)!=34: raise ValueError(f'Expected 34 guide rows, got {len(rows)}')
    return rows

def write_csv(path,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir',type=Path,default=ROOT/'data/raw/tyres')
    parser.add_argument('--output-dir',type=Path,default=ROOT/'data/intermediate/tyres')
    args=parser.parse_args()
    # Complete extraction and validate counts before writing any files.
    a=abrasion(args.input_dir/ABRASION); g=guide(args.input_dir/GUIDE)
    for row in g:
        for _,key in GRADES:
            if not 0.6<=row[key]<=5.5: raise ValueError(f'Out-of-range grade: {row}')
    args.output_dir.mkdir(parents=True,exist_ok=True)
    write_csv(args.output_dir/'tyre_abrasion_raw.csv',a)
    write_csv(args.output_dir/'tyre_test_grades_raw.csv',g)
    write_csv(args.output_dir/'tyre_extraction_summary.csv',[dict(source_file=ABRASION,records=len(a),status='extracted'),dict(source_file=GUIDE,records=len(g),status='extracted')])
    print(f'Extracted {len(a)} abrasion records and {len(g)} tyre grade records.')
    print(f'Output: {args.output_dir}')
if __name__=='__main__':
    main()
