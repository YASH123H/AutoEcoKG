"""AutoEcoKG regression benchmark against the processed CSV reference snapshot.
Run: python src/evaluate.py. No additional dependencies beyond engine.py.
Tests query completeness, exact answer values, ordering, and recommendation behavior.
Does not establish independent real-world accuracy of the source data.
"""
import argparse
import csv
import math
import time
from collections import Counter
from decimal import Decimal
from pathlib import Path
from urllib.parse import quote
from engine import QueryEngine
from recommendation import recommend

BASE = 'https://w3id.org/autoecokg/resource/'
ROOT = Path(__file__).resolve().parent.parent

def read(folder, name):
    with (folder / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def resource(kind, key):
    return BASE + kind + '/' + quote(key, safe='')

def number(x):
    return Decimal(str(x))

def bag(rows, fields, numeric=()):
    return Counter(tuple(number(r[k]) if k in numeric else str(r[k]) for k in fields) for r in rows)

def compare(actual, expected, fields, numeric=()):
    a, e = bag(actual, fields, numeric), bag(expected, fields, numeric)
    missing, extra = e-a, a-e
    return (a == e, f'expected={sum(e.values())}; actual={sum(a.values())}; missing={sum(missing.values())}; unexpected={sum(extra.values())}' + (f'; example missing={next(iter(missing))}' if missing else '') + (f'; example unexpected={next(iter(extra))}' if extra else ''))

def check(condition, detail):
    return bool(condition), detail

def sorted_by(rows, key, reverse=False):
    vals = [key(r) for r in rows]
    return vals == sorted(vals, reverse=reverse)

def expect_error(fn):
    try:
        fn()
    except ValueError as exc:
        return True, str(exc)
    return False, 'Expected ValueError, but call succeeded'

def reference_rank(joined, size, season='summer', safety=2.5, weight=0.5, abrasion=None):
    # Separate CSV-based reference calculation; never calls recommend or SPARQL.
    candidates = [r for r in joined if r['size']==size and r['category']==season and r['safety']<=number(safety) and (abrasion is None or r['abrasion']<=number(abrasion))]
    if not candidates:
        return []
    a0,a1 = min(r['abrasion'] for r in candidates),max(r['abrasion'] for r in candidates)
    s0,s1 = min(r['safety'] for r in candidates),max(r['safety'] for r in candidates)
    w=number(weight)
    result=[]
    for r in candidates:
        a,s=r['abrasion'],r['safety']
        an=(a-a0)/(a1-a0) if a1!=a0 else Decimal(0)
        sn=(s-s0)/(s1-s0) if s1!=s0 else Decimal(0)
        front=not any((q['abrasion']<=a and q['safety']<=s) and (q['abrasion']<a or q['safety']<s) for q in candidates)
        result.append(dict(r, score=w*an+(1-w)*sn, pareto_optimal=front, fitment_status='not_verified'))
    return sorted(result,key=lambda r:(r['score'],r['safety'],r['abrasion'],r['tyre']))

def rank_compare(actual, expected):
    if len(actual)!=len(expected):
        return False, f'expected {len(expected)} candidates; got {len(actual)}'
    fields=('tyre','name','size','category','fitment_status','pareto_optimal')
    for i,(a,e) in enumerate(zip(actual,expected),1):
        if a['rank']!=i or any(a[k]!=e[k] for k in fields) or any(number(a[k])!=number(e[k]) for k in ('abrasion','safety')) or not math.isclose(float(a['score']),float(e['score']),rel_tol=0,abs_tol=0.00000051):
            return False,f'row {i}: expected {e["name"]} score={e["score"]}; actual={a}'
    return True,f'all {len(expected)} ordered candidates, scores, flags and ranks agree'

def evaluate(engine, folder):
    vehicles=read(folder,'adac_vehicles.csv')
    tyres={r['tyre_id']:r for r in read(folder,'tyres.csv')}
    abr=read(folder,'tyre_abrasion.csv')
    grades={r['tyre_id']:r for r in read(folder,'tyre_test_grades.csv')}
    matches=read(folder,'vehicle_tyre_matches.csv')
    ev=[dict(vehicle=resource('vehicle',r['vehicle_id']),name=r['vehicle_name'],powertrain=r['powertrain']) for r in vehicles]
    eco2=[dict(vehicle=resource('vehicle',r['vehicle_id']),name=r['vehicle_name'],co2=r['wltp_co2_g_km']) for r in vehicles if r['wltp_co2_g_km']]
    gaps=[]
    for r in vehicles:
        if not r['fuel_l_100km_gap_pct']: continue
        w,a=number(r['wltp_fuel_l_100km']),number(r['adac_fuel_l_100km'])
        gaps.append(dict(name=r['vehicle_name'],wltp=w,adac=a,gap=((a-w)/w*100).quantize(Decimal('0.01'))))
    ea=[dict(tyre=resource('tyre',r['tyre_id']),name=tyres[r['tyre_id']]['tyre_name'],size=tyres[r['tyre_id']]['tyre_size'],category=tyres[r['tyre_id']]['category'],abrasion=number(r['abrasion_mg_km_t'])) for r in abr]
    joined=[dict(r,safety=number(grades[r['tyre'].rsplit('/',1)[1]]['safety_grade'])) for r in ea if r['tyre'].rsplit('/',1)[1] in grades]
    def esafe(threshold): return [r for r in joined if r['safety']<=number(threshold)]
    em=[dict(vehicleName=r['vehicle_name'],tyreName=tyres[r['tyre_id']]['tyre_name'],size=tyres[r['tyre_id']]['tyre_size'],matchType=r['match_type'],identity=r['identity_verified'].lower(),fitment=r['fitment_verified'].lower()) for r in matches]
    by_id={r['tyre_id']:r for r in abr}
    ej=[dict(vehicleName=r['vehicle_name'],tyreName=tyres[r['tyre_id']]['tyre_name'],abrasion=by_id[r['tyre_id']]['abrasion_mg_km_t'],safety=grades[r['tyre_id']]['safety_grade'] if r['tyre_id'] in grades else '',identity=r['identity_verified'].lower(),fitment=r['fitment_verified'].lower()) for r in matches if r['match_type']=='model_size_match' and r['tyre_id'] in by_id]
    ep=[dict(name=tyres[r['tyre_id']]['tyre_name'],abrasion=r['abrasion_mg_km_t'],file=r['source_file'],page=r['source_page']) for r in abr]
    cache={}; rankings={}
    def query(name, threshold=2.5):
        key=(name,threshold)
        if key not in cache: cache[key]=engine.run(name,max_safety=threshold)[1]
        return cache[key]
    def rank(size='225/40 R18',season='summer',safety=2.5,weight=0.5,abrasion=None):
        key=(size,season,safety,weight,abrasion)
        if key not in rankings: rankings[key]=recommend(engine,size,season,safety,weight,abrasion)
        return rankings[key]
    def rank_test(size='225/40 R18',season='summer',safety=2.5,weight=0.5,abrasion=None):
        return rank_compare(rank(size,season,safety,weight,abrasion),reference_rank(joined,size,season,safety,weight,abrasion))
    tests=[]
    def case(group,question,fn): tests.append((group,question,fn))
    case('query','All vehicle identities, names and powertrains match CSV',lambda:compare(query('vehicles'),ev,('vehicle','name','powertrain')))
    case('query','Vehicle identifiers are unique',lambda:check(len({r['vehicle'] for r in query('vehicles')})==len(ev),'unique vehicle URIs'))
    case('query','Vehicle list is alphabetically ordered',lambda:check(sorted_by(query('vehicles'),lambda r:r['name']),'name ascending'))
    case('query','All WLTP CO2 values and vehicle IDs match CSV',lambda:compare(query('vehicle_co2'),eco2,('vehicle','name','co2'),('co2',)))
    case('query','WLTP CO2 ranking is ascending',lambda:check(sorted_by(query('vehicle_co2'),lambda r:(number(r['co2']),r['name'])),'CO2 then name'))
    case('query','All fuel gaps match independently recalculated CSV inputs',lambda:compare(query('fuel_gap'),gaps,('name','wltp','adac','gap'),('wltp','adac','gap')))
    case('query','Fuel gaps are descending',lambda:check(sorted_by(query('fuel_gap'),lambda r:number(r['gap']),True),'gap descending'))
    case('anchor','Renault Espace has the largest current fuel gap',lambda:check(query('fuel_gap')[0]['name'].startswith('Renault Espace') and number(query('fuel_gap')[0]['gap'])==Decimal('24.49'),'Renault Espace: 24.49%'))
    case('query','All abrasion observations match CSV identity and value',lambda:compare(query('low_abrasion'),ea,('tyre','name','size','category','abrasion'),('abrasion',)))
    case('query','Abrasion ordering is ascending',lambda:check(sorted_by(query('low_abrasion'),lambda r:(number(r['abrasion']),r['name'],r['size'])),'abrasion then name and size'))
    case('anchor','Michelin e Primacy is minimum abrasion record',lambda:check(query('low_abrasion')[0]['name']=='Michelin e Primacy' and query('low_abrasion')[0]['size']=='205/55 R16' and number(query('low_abrasion')[0]['abrasion'])==35,'35 mg/km/t, 205/55 R16'))
    for threshold in (2.5,2.0,1.5,0.6,5.5):
        case('query',f'Complete safety-abrasion join at threshold {threshold}',lambda t=threshold:compare(query('safe_low_abrasion',t),esafe(t),('tyre','name','size','abrasion','safety'),('abrasion','safety')))
    case('query','Default joined results sorted by abrasion and safety',lambda:check(sorted_by(query('safe_low_abrasion'),lambda r:(number(r['abrasion']),number(r['safety']),r['name'])),'ascending abrasion and safety'))
    case('query','All alignment candidates match source CSV',lambda:compare(query('alignment'),em,('vehicleName','tyreName','size','matchType','identity','fitment')))
    case('query','No unsupported fitment or identity confirmation',lambda:check(bool(query('alignment')) and all(r['identity']==r['fitment']=='false' for r in query('alignment')),'all alignment flags false'))
    case('query','Model-size match joins return exact vehicles and observations',lambda:compare(query('matched_tyre_observations'),ej,('vehicleName','tyreName','abrasion','safety','identity','fitment'),('abrasion',)))
    case('anchor','Both Audi A3 matches return Nexen 75 and safety 2.4',lambda:check(len(query('matched_tyre_observations'))==2 and all(r['vehicleName'].startswith('Audi A3') and r['tyreName']=='Nexen N Fera Sport' and number(r['abrasion'])==75 and number(r['safety'])==Decimal('2.4') for r in query('matched_tyre_observations')),'two Audi variants; unverified candidate links'))
    case('query','All abrasion provenance document and page values match CSV',lambda:compare(query('provenance'),ep,('name','abrasion','file','page'),('abrasion','page')))
    case('recommendation','Balanced 225/40 R18 ranking matches full reference',rank_test)
    case('recommendation','Abrasion-only ranking matches full reference',lambda:rank_test(weight=1))
    case('recommendation','Safety-only ranking matches full reference',lambda:rank_test(weight=0))
    case('recommendation','Combined safety and abrasion limits match full reference',lambda:rank_test(safety=2.0,abrasion=70))
    case('recommendation','Alternative 215/55 R17 size matches full reference',lambda:rank_test(size='215/55 R17'))
    case('recommendation','Missing winter grading coverage yields no eligible tyres',lambda:rank_test(season='winter'))
    case('recommendation','Unrepresented dimension returns empty list',lambda:check(rank(size='999/99 R99')==[],'no fabricated alternatives'))
    case('recommendation','Impossible abrasion threshold returns empty list',lambda:check(rank(abrasion=1)==[],'no eligible candidates'))
    case('recommendation','Equivalent ZR size spelling normalizes identically',lambda:check(rank(size='225 40 ZR18')==rank(),'identical complete rankings'))
    case('anchor','Balanced top tyre and Pareto set match known snapshot',lambda:check(rank()[0]['name']=='Continental Sport Contact 7' and {r['name'] for r in rank() if r['pareto_optimal']}=={'Continental Sport Contact 7','Michelin Pilot Sport 5'},'Continental first; two Pareto-optimal tyres'))
    case('negative','Invalid weight rejected',lambda:expect_error(lambda:rank(weight=1.1)))
    case('negative','Invalid safety threshold rejected',lambda:expect_error(lambda:rank(safety=6)))
    case('negative','Malformed dimension rejected',lambda:expect_error(lambda:rank(size='bad-size')))
    case('negative','Nonpositive abrasion threshold rejected',lambda:expect_error(lambda:rank(abrasion=0)))
    case('negative','Unknown SPARQL query rejected',lambda:expect_error(lambda:engine.run('unknown_query')))

    # AutoEcoKG 2.0 Competency Questions
    def test_euro7_particulates():
        cols, rows = engine.run('euro7_particulates')
        if not rows: return False, 'No Euro 7 particulate rows returned'
        bev_rows = [r for r in rows if r['powertrain'] == 'electric']
        ice_rows = [r for r in rows if r['powertrain'] != 'electric']
        if not bev_rows or not ice_rows: return False, 'Missing BEV or ICE rows'
        if not all(r['brakeCompliant'] in ('true', 'True') for r in rows):
            return False, 'Compliance flag error'
        return True, f'{len(rows)} Euro 7 vehicle-tyre particulate configurations screened'

    def test_microplastic_math():
        from recommendation import calculate_euro7_particulates
        res = calculate_euro7_particulates(abrasion_level_mg_km_t=70, vehicle_mass_kg=1500, powertrain='BEV', annual_km=25000, fleet_size=100)
        ok = res['veh_abrasion_rate_mg_km'] == 105.0 and res['soil_water_microplastics_kg_yr'] == 236.25 and res['airborne_pm10_grams_yr'] == 26250.0
        return ok, f"Calculated: {res['soil_water_microplastics_kg_yr']} kg/yr soil/water, {res['airborne_pm10_grams_yr']} g/yr air"

    def test_battery_durability():
        cols, rows = engine.run('battery_durability')
        if len(rows) != 8: return False, f'Expected 8 electric vehicles, got {len(rows)}'
        ok = all(number(r['sohPercent']) >= 80 and r['milestoneYears'] == '5' and r['euro7Compliant'] in ('true', 'True') for r in rows)
        return ok, f'{len(rows)} BEV battery durability records conform to Euro 7 milestone'

    def test_tco_skyline():
        cols, rows = engine.run('tco_pareto_skyline')
        if not rows: return False, 'No TCO skyline rows returned'
        ok = all(number(r['tcoEur']) > 0 and number(r['lifespanKm']) >= 10000 for r in rows)
        return ok, f'{len(rows)} TCO configuration records evaluated'

    def test_epistemic_divergence():
        cols, rows = engine.run('epistemic_divergence')
        if len(rows) != 23: return False, f'Expected 23 comparable gap rows, got {len(rows)}'
        return True, f'{len(rows)} three-tier epistemic divergence records verified'

    case('euro7', 'Euro 7 brake dust observation presence and BEV limit screening', test_euro7_particulates)
    case('euro7', 'Microplastic fleet load calculation is mathematically consistent', test_microplastic_math)
    case('durability', 'Battery durability observations conform to Euro 7 5-year milestone', test_battery_durability)
    case('tco', 'Multi-criteria TCO skyline query returns valid configurations', test_tco_skyline)
    case('epistemic', 'Three-tier epistemic divergence returns populated records', test_epistemic_divergence)

    results=[]
    for i,(group,question,fn) in enumerate(tests,1):
        start=time.perf_counter()
        try: ok,detail=fn()
        except Exception as exc: ok,detail=False,f'{type(exc).__name__}: {exc}'
        result=dict(test_id=f'CQ-{i:02d}',group=group,question=question,status='PASS' if ok else 'FAIL',detail=detail,elapsed_ms=round((time.perf_counter()-start)*1000,2))
        results.append(result)
        print(f'{result["test_id"]} {result["status"]}: {question}')
    return results

def write(path,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--graph',type=Path,default=ROOT/'data/autoecokg_triples.ttl')
    p.add_argument('--input',type=Path,default=ROOT/'data/processed')
    p.add_argument('--output',type=Path,default=ROOT/'evaluation')
    args=p.parse_args()
    engine=QueryEngine(args.graph)
    results=evaluate(engine,args.input)
    args.output.mkdir(parents=True,exist_ok=True)
    write(args.output/'benchmark_results.csv',results)
    passed=sum(r['status']=='PASS' for r in results)
    summary=dict(rdf_triples=len(engine.graph),total_tests=len(results),passed=passed,failed=len(results)-passed,pass_rate_pct=round(passed/len(results)*100,2),reference='processed CSV snapshot; not external ground truth')
    write(args.output/'benchmark_summary.csv',[summary])
    print('\n'+str(summary))
    print('Saved:',args.output/'benchmark_results.csv')
    return 0 if passed==len(results) else 1

if __name__=='__main__':
    raise SystemExit(main())
