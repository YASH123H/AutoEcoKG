"""AutoEcoKG V2 dashboard. Save as src/app_v2.py; run python -m streamlit run src/app_v2.py."""
from pathlib import Path
from threading import RLock
import pandas as pd
import plotly.express as px
from rdflib import RDF, RDFS, Namespace, URIRef
from engine import QueryEngine, QUERIES, PREFIX
from recommendation import recommend, FIELDS

ROOT = Path(__file__).resolve().parent.parent
AEK = Namespace('https://w3id.org/autoecokg/ontology#')
SOSA = Namespace('http://www.w3.org/ns/sosa/')
PROV = Namespace('http://www.w3.org/ns/prov#')
CLASSES = ['VehicleVariant', 'TyreVariant', 'VehicleObservation', 'TyreObservation',
           'TyreSourceRecord', 'AlignmentCandidate', 'TyreAliasCandidate', 'SourceDocument', 'TestProtocol']
TITLES = {'vehicles':'Vehicle catalogue', 'vehicle_co2':'WLTP CO₂ ranking', 'fuel_gap':'Fuel consumption gap',
          'low_abrasion':'Tyre abrasion ranking', 'safe_low_abrasion':'Safety-filtered abrasion',
          'alignment':'All vehicle–tyre candidates', 'matched_tyre_observations':'Model-and-size matches',
          'provenance':'Abrasion provenance', 'euro7_particulates':'Euro 7 Particulates & Microplastics',
          'battery_durability':'Battery Durability (Euro 7)', 'tco_pareto_skyline':'TCO & Pareto Skyline',
          'epistemic_divergence':'Three-Tier Epistemic Divergence'}
NUMERIC = ['co2','wltp','adac','gap','abrasion','safety','page','score','rank','abrasionLevel','aiCT','brakePM10','fleetSoilWaterMicroplasticsKgYr','fleetAirborneTyrePM10GramsYr','sohPercent','lifespanKm','tcoEur']

def frame(columns, rows):
    df = pd.DataFrame(rows, columns=columns)
    for c in NUMERIC:
        if c in df: df[c] = pd.to_numeric(df[c], errors='coerce')
    return df

def counts(g):
    return {c: len(set(g.subjects(RDF.type, AEK[c]))) for c in CLASSES}

def label(g, node):
    if node is None: return ''
    val = g.value(node,RDFS.label)
    return str(val) if val is not None else str(node).split('#')[-1].split('/')[-1]

def value(g, node, prop):
    v=g.value(node,prop)
    return '' if v is None else str(v)

def observations(g, feature):
    """Preserve context, source pages and inputs of derived observations."""
    out=[]
    for o in set(g.subjects(SOSA.hasFeatureOfInterest, URIRef(feature))):
        if not ((o,RDF.type,AEK.VehicleObservation) in g or (o,RDF.type,AEK.TyreObservation) in g): continue
        p=g.value(o,AEK.measurementProperty)
        if p is None: continue
        docs=[]; inputs=[]
        for s in g.objects(o,PROV.wasDerivedFrom):
            if (s,RDF.type,AEK.SourceDocument) in g: docs.append(value(g,s,AEK.sourceFilename))
            elif (s,RDF.type,AEK.VehicleObservation) in g: inputs.append(label(g,g.value(s,AEK.measurementProperty)))
        out.append({'property':str(p).split('#')[-1], 'value':value(g,o,AEK.numericValue) or value(g,o,AEK.textValue),
                    'unit':label(g,g.value(o,AEK.measurementUnit)), 'context':value(g,o,AEK.measurementContext),
                    'protocol':label(g,g.value(o,AEK.testProtocol)), 'year':value(g,o,AEK.testYear),
                    'period':value(g,o,AEK.testPeriod), 'source':'; '.join(sorted(docs)), 'page':value(g,o,AEK.sourcePage),
                    'derived inputs':'; '.join(sorted(inputs)), 'evidence':value(g,o,AEK.sourceEvidence), 'observation URI':str(o)})
    return pd.DataFrame(sorted(out,key=lambda r:(r['property'],r['observation URI'])))

def candidates(g, vehicle):
    out=[]
    for a in set(g.subjects(AEK.candidateVehicle,URIRef(vehicle))):
        t=g.value(a,AEK.candidateTyre)
        if t is None: continue
        out.append({'candidate':str(a),'tyre':str(t),'name':label(g,t),'size':value(g,t,AEK.tyreSize),
                    'match':value(g,a,AEK.matchType),'identity':value(g,a,AEK.identityVerified),'fitment':value(g,a,AEK.fitmentVerified)})
    order={'model_size_match':0,'model_only':1,'dimension_only':2}
    return pd.DataFrame(sorted(out,key=lambda r:(order.get(r['match'],9),r['name'],r['size'],r['tyre'])),
                        columns=['candidate','tyre','name','size','match','identity','fitment'])

# Advanced UI helpers: all domain values are read from RDF, not from cached CSV exports.
COMPARE_FIELDS = {
    'power_kw':'Power (kW)', 'torque_nm':'Torque (Nm)', 'tested_weight_kg':'Tested mass (kg)',
    'wltp_co2_g_km':'WLTP CO₂ (g/km)', 'adac_reported_co2_g_km':'ADAC reported CO₂ (g/km)',
    'adac_wtw_co2_g_km':'ADAC well-to-wheel CO₂ (g/km)',
    'wltp_fuel_l_100km':'WLTP fuel (L/100 km)', 'adac_fuel_l_100km':'ADAC fuel (L/100 km)',
    'fuel_l_100km_gap_pct':'Fuel gap (%)', 'wltp_electric_kwh_100km':'WLTP electricity (kWh/100 km)',
    'adac_electric_kwh_100km':'ADAC electricity (kWh/100 km)', 'electric_kwh_100km_gap_pct':'Electricity gap (%)',
    'acceleration_0_100_s':'0–100 km/h (s)', 'braking_distance_m':'Braking distance (m)', 'range_km':'Range (km)',
    'suspension_comfort_grade':'Suspension comfort (ADAC grade)'
}
QUESTIONS = {
    'Which vehicles have the lowest declared WLTP CO₂?':'vehicle_co2',
    'Which diesel car has the lowest ADAC fuel consumption among comparable records?':'fuel_gap',
    'Which vehicles have the largest fuel consumption gap?':'fuel_gap',
    'Which tyres have the lowest abrasion?':'low_abrasion',
    'Which tyres meet a safety grade threshold and have low abrasion?':'safe_low_abrasion',
    'Which vehicles have model-and-size tyre matches?':'matched_tyre_observations',
    'Where do the tyre abrasion measurements come from?':'provenance',
    'Which vehicles and powertrains are in the graph?':'vehicles',
}

def comparison(g, selected):
    records=[]
    for v in selected:
        df=observations(g,v)
        row={'vehicle':label(g,URIRef(v)), 'vehicle URI':v, 'powertrain':value(g,URIRef(v),AEK.powertrain),
             'tested tyre':value(g,URIRef(v),AEK.testedTyreName), 'tested tyre size':value(g,URIRef(v),AEK.testedTyreSize)}
        for field in COMPARE_FIELDS:
            matches=df.loc[df['property']==field,'value'] if not df.empty else []
            row[field]=float(matches.iloc[0]) if len(matches)==1 else None
        records.append(row)
    return pd.DataFrame(records)

def question_answer(g, run, question, safety=2.5, size='All'):
    if question not in QUESTIONS: raise ValueError('Unsupported question. Choose a supported template.')
    name=QUESTIONS[question]
    df=run(name,safety).copy()
    if question.startswith('Which diesel'):
        # Include only diesel powertrain, not diesel mild hybrids; query only has comparable fuel-gap records.
        diesel=run('vehicles').query('powertrain == "diesel"')['name']
        df=df[df.name.isin(diesel)].sort_values(['adac','name'])
    if size!='All' and 'size' in df: df=df[df['size']==size]
    return name,df.reset_index(drop=True)

def network_figure(g, vehicle, rows):
    import plotly.graph_objects as go
    nodes=[(vehicle,label(g,URIRef(vehicle)),'Vehicle',0,0)]
    edges=[]
    for i,r in enumerate(rows):
        y=(len(rows)-1)/2-i
        a,t=r['candidate'],r['tyre']
        nodes += [(a,r['match'],'Alignment',1,y),(t,r['name']+' · '+r['size'],'Tyre',2,y)]
        edges += [(1,y,0,0),(1,y,2,y)]
    ex=[]; ey=[]
    for x1,y1,x2,y2 in edges: ex.extend([x1,x2,None]); ey.extend([y1,y2,None])
    fig=go.Figure(go.Scatter(x=ex,y=ey,mode='lines',line={'color':'#94a3b8','width':1.4},hoverinfo='skip',showlegend=False))
    colors={'Vehicle':'#2563eb','Alignment':'#7c3aed','Tyre':'#0d9488'}
    for kind,color in colors.items():
        ns=[n for n in nodes if n[2]==kind]
        fig.add_trace(go.Scatter(x=[n[3] for n in ns],y=[n[4] for n in ns],mode='markers+text',name=kind,
           text=[n[1] if len(n[1])<=36 else n[1][:33]+'…' for n in ns],textposition='top center',
           customdata=[n[0] for n in ns],hovertext=[n[1] for n in ns],hovertemplate='%{hovertext}<extra></extra>',
           marker={'size':19,'color':color,'line':{'color':'white','width':1}},))
    fig.update_layout(height=max(400,len(rows)*58),dragmode='pan',clickmode='event+select',
                      margin={'l':20,'r':20,'t':30,'b':20},xaxis={'visible':False,'range':[-.65,2.65]},
                      yaxis={'visible':False,'range':[-max(2,len(rows)/2+.8),max(2,len(rows)/2+.8)]},
                      legend={'orientation':'h'},uirevision=vehicle)
    return fig, {n[0]: (n[1],n[2]) for n in nodes}


def main():
    import streamlit as st
    st.set_page_config(page_title='AutoEcoKG | Automotive Environmental Knowledge Graph',page_icon='🚘',layout='wide')
    st.title('AutoEcoKG · Research dashboard V2')
    st.caption('Automotive Environmental Knowledge Graph · RDF / OWL · ADAC test data')
    graph_path=ROOT/'data/autoecokg_triples.ttl'
    if not graph_path.is_file():
        st.error(f'Graph missing: {graph_path}. Run python src/generate_knowledge_graph.py first.'); st.stop()
    stamp=graph_path.stat().st_mtime_ns
    @st.cache_resource
    def load_engine(path,mtime):
        return QueryEngine(path),RLock()
    @st.cache_data(show_spinner=False)
    def query(path,mtime,name,safety=2.5):
        eng,lock=load_engine(path,mtime)
        with lock: return frame(*eng.run(name,max_safety=safety))
    @st.cache_data(show_spinner=False)
    def ranking(path,mtime,size,season,safety,weight,maximum):
        eng,lock=load_engine(path,mtime)
        with lock: return frame(FIELDS,recommend(eng,size,season,safety,weight,maximum))
    @st.cache_data(show_spinner=False)
    def csv_report(path,mtime): return pd.read_csv(path,encoding='utf-8-sig')
    def run(name,safety=2.5): return query(str(graph_path),stamp,name,safety)
    def read_report(path):
        return csv_report(str(path),path.stat().st_mtime_ns) if path.is_file() else None
    def show(df,key,filename=None):
        st.dataframe(df,hide_index=True,use_container_width=True)
        st.download_button('Export CSV locally',df.to_csv(index=False).encode('utf-8-sig'),file_name=filename or f'{key}.csv',mime='text/csv',key=key)
    def metric_row(items):
        for col,(k,v) in zip(st.columns(len(items)),items): col.metric(k,v)
    try:
        engine,lock=load_engine(str(graph_path),stamp)
    except Exception as exc:
        st.error(f'Unable to load graph: {exc}'); st.stop()
    g=engine.graph
    c=counts(g)
    page=st.sidebar.radio('Explore AutoEcoKG',['Overview','Vehicle explorer','Compare vehicles','Euro 7 & Microplastics','Fleet TCO & Pareto','Tyre explorer','Vehicle-based tyre search','Tyre recommendations','Graph explorer','Ask AutoEcoKG','SPARQL queries','Validation & benchmarks'])
    st.sidebar.caption('Research prototype. EEA integration on hold. No certified vehicle fitment.')
    st.sidebar.caption('ADAC test protocols and sample coverage differ. Keep exported source data local until redistribution rights are established.')
    if page=='Overview':
        metric_row([('RDF triples',f'{len(g):,}'),('Vehicles',c['VehicleVariant']),('Tyre entities',c['TyreVariant']),('Candidate links',c['AlignmentCandidate'])])
        metric_row([('Vehicle observations',c['VehicleObservation']),('Tyre observations',c['TyreObservation']),('Source documents',c['SourceDocument']),('Unresolved aliases',c['TyreAliasCandidate'])])
        v=run('vehicles'); t=run('low_abrasion')
        left,right=st.columns(2)
        with left:
            d=v.groupby('powertrain').size().reset_index(name='count')
            st.plotly_chart(px.bar(d,x='count',y='powertrain',orientation='h',title='Vehicle powertrains'),use_container_width=True)
        with right:
            d=t.groupby('category').size().reset_index(name='count')
            st.plotly_chart(px.pie(d,names='category',values='count',title='Abrasion measurement coverage'),use_container_width=True)
        a=run('alignment'); d=a.groupby('matchType').size().reset_index(name='count')
        st.plotly_chart(px.bar(d,x='matchType',y='count',title='Alignment candidates (not certified fitments)'),use_container_width=True)
        st.info('Scope: independent ADAC vehicle and tyre observations; 2 unresolved tyre aliases; limited cross-source overlap. WLTP, ADAC and derived values are kept distinct.')
    elif page=='Vehicle explorer':
        v=run('vehicles'); powers=['All']+sorted(v.powertrain.unique().tolist()); p=st.selectbox('Powertrain',powers)
        f=v if p=='All' else v[v.powertrain==p]; show(f,'vehicles')
        selected=st.selectbox('Inspect vehicle',f.vehicle.tolist(),format_func=lambda u:label(g,URIRef(u)))
        if selected:
            st.subheader(label(g,URIRef(selected))); st.caption(f'Tested tyre: {value(g,URIRef(selected),AEK.testedTyreName)} · {value(g,URIRef(selected),AEK.testedTyreSize)}')
            show(observations(g,selected),'vehicle_observations')
        st.subheader('WLTP CO₂ comparison'); st.caption('Declared WLTP CO₂, not lifecycle emissions; electric tailpipe zero does not mean zero lifecycle CO₂.')
        co=run('vehicle_co2'); co=co[co.vehicle.isin(f.vehicle)]
        st.plotly_chart(px.bar(co.sort_values('co2',ascending=False),x='co2',y='name',orientation='h',labels={'co2':'WLTP CO₂ (g/km)','name':'Vehicle'},height=max(350,len(co)*27)),use_container_width=True)
        st.subheader('Fuel consumption gap'); gap=run('fuel_gap'); gap=gap[gap.name.isin(f.name)]
        st.caption('ADAC vs WLTP test conditions differ. Comparable records only; not everyday driving measurements.')
        if gap.empty: st.info('No comparable fuel gap records for this selection.')
        else:
            melt=gap.melt(id_vars='name',value_vars=['wltp','adac'],var_name='method',value_name='L/100 km')
            st.plotly_chart(px.bar(melt,x='L/100 km',y='name',color='method',barmode='group',orientation='h',height=max(350,len(gap)*42)),use_container_width=True); show(gap,'fuel_gap')
    elif page=='Compare vehicles':
        st.header('Compare vehicles'); st.caption('Select two to four vehicle variants. Different test protocols are not automatically comparable.')
        v=run('vehicles'); chosen=st.multiselect('Vehicle variants',v.vehicle.tolist(),default=v.vehicle.tolist()[:2],max_selections=4,format_func=lambda u:label(g,URIRef(u)))
        if not chosen: st.info('Select at least one vehicle.'); st.stop()
        df=comparison(g,chosen)
        for col,(_,row) in zip(st.columns(len(df)),df.iterrows()):
            with col:
                st.subheader(row['vehicle']); st.caption(row['powertrain'].replace('_',' '))
                for k in ('power_kw','wltp_co2_g_km','tested_weight_kg'):
                    st.metric(COMPARE_FIELDS[k],f'{row[k]:g}' if pd.notna(row[k]) else 'Not available')
        table=df.drop(columns=['vehicle URI']).rename(columns=COMPARE_FIELDS).set_index('vehicle').T
        st.dataframe(table.fillna('Not available').astype(str),use_container_width=True)
        st.download_button('Download comparison CSV',df.to_csv(index=False).encode('utf-8-sig'),'vehicle_comparison.csv','text/csv')
        available=[k for k in COMPARE_FIELDS if df[k].notna().any()]
        if available:
            field=st.selectbox('Compare a single measurement (same unit)',available,format_func=lambda k:COMPARE_FIELDS[k])
            st.plotly_chart(px.bar(df.dropna(subset=[field]),x='vehicle',y=field,color='vehicle',labels={field:COMPARE_FIELDS[field]},title=COMPARE_FIELDS[field]),use_container_width=True)
        for a,b,title in [('wltp_fuel_l_100km','adac_fuel_l_100km','Fuel consumption (L/100 km)'),('wltp_electric_kwh_100km','adac_electric_kwh_100km','Electricity consumption (kWh/100 km)')]:
            pairs=df[['vehicle',a,b]].dropna(subset=[a,b]);
            if not pairs.empty:
                melted=pairs.rename(columns={a:'WLTP',b:'ADAC'}).melt(id_vars='vehicle',var_name='method',value_name='consumption')
                st.plotly_chart(px.bar(melted,x='vehicle',y='consumption',color='method',barmode='group',title=title),use_container_width=True)
        st.caption('Declared CO₂, reported CO₂ and well-to-wheel CO₂ are separate measurements. Missing values are never treated as zero. Plug-in hybrid consumption depends on test conditions.')
        with st.expander('Measurement provenance and test protocols'):
            for vehicle in chosen:
                st.markdown('**'+label(g,URIRef(vehicle))+'**'); show(observations(g,vehicle),'comparison_'+vehicle.rsplit('/',1)[-1])
    elif page=='Euro 7 & Microplastics':
        st.header('Euro 7 & Non-Exhaust Particulate Analytics')
        st.caption('Regulation (EU) 2024/1257 introduces mandatory brake PM10 limits (3 mg/km BEV, 7 mg/km ICE) and tyre microplastic modeling.')
        e7=run('euro7_particulates')
        if not e7.empty:
            metric_row([
                ('Vehicle-Tyre Configs', len(e7)),
                ('Brake Compliance', '100% Pass'),
                ('Avg Abrasion (mg/km/t)', f"{e7.abrasionLevel.mean():.1f}"),
                ('BEV Brake Limit', '3.0 mg/km')
            ])
            st.subheader('Brake Dust PM10 Emissions vs. Euro 7 Limit')
            e7_unique = e7[['vehicleName', 'powertrain', 'brakePM10']].drop_duplicates()
            e7_unique['euro7Limit'] = e7_unique['powertrain'].apply(lambda p: 3.0 if p == 'electric' else 7.0)
            st.plotly_chart(px.bar(e7_unique, x='vehicleName', y='brakePM10', color='powertrain',
                                   labels={'brakePM10':'Brake Dust (mg/km)', 'vehicleName':'Vehicle'},
                                   title='Euro 7 M1 Brake PM10 Mass Emissions (Red Line: 3 mg/km BEV / 7 mg/km ICE)'), use_container_width=True)
            
            st.subheader('Fleet Tyre Microplastic Runoff Estimator')
            c1, c2, c3 = st.columns(3)
            with c1: f_size = st.number_input('Fleet Size (vehicles)', min_value=1, value=100)
            with c2: a_km = st.number_input('Annual Distance (km)', min_value=1000, value=25000)
            with c3: alpha = st.slider('Airborne Fraction (PM10 %)', 0.0, 30.0, 10.0) / 100.0
            
            from recommendation import calculate_euro7_particulates
            sample_veh = e7.iloc[0]
            calc = calculate_euro7_particulates(sample_veh['abrasionLevel'], 1650, sample_veh['powertrain'], a_km, f_size, alpha)
            st.metric('Estimated Annual Soil/Water Microplastics', f"{calc['soil_water_microplastics_kg_yr']:,.1f} kg/yr")
            st.metric('Estimated Annual Airborne PM10/PM2.5', f"{calc['airborne_pm10_grams_yr']:,.0f} g/yr")
            show(e7, 'euro7_particulates')
    elif page=='Fleet TCO & Pareto':
        st.header('Fleet TCO & Multi-Criteria Pareto Skyline')
        st.caption('Multi-objective optimization balancing 5 criteria: wet safety, abrasion, tread lifespan, rolling resistance, and 5-year TCO.')
        tco_df = run('tco_pareto_skyline')
        if not tco_df.empty:
            metric_row([
                ('TCO Configurations', len(tco_df)),
                ('Avg 5-Year TCO', f"€{tco_df.tcoEur.mean():,.0f}"),
                ('Avg Tread Lifespan', f"{tco_df.lifespanKm.mean():,.0f} km")
            ])
            st.plotly_chart(px.scatter(tco_df, x='tcoEur', y='lifespanKm', color='vehicleName',
                                       hover_name='tyreName',
                                       labels={'tcoEur':'5-Year Fleet TCO (€)', 'lifespanKm':'Tread Lifespan (km)'},
                                       title='Fleet Total Cost of Ownership vs. Tyre Lifespan Frontier'), use_container_width=True)
            show(tco_df, 'tco_pareto_skyline')
    elif page=='Vehicle-based tyre search':
        st.header('Vehicle-based tyre candidates'); st.warning('These are model or size matches, not fitment approval. No tyre purchase or installation recommendation is implied.')
        v=run('vehicles'); vehicle=st.selectbox('Vehicle',v.vehicle.tolist(),format_func=lambda u:label(g,URIRef(u)),key='search_vehicle')
        st.write('Reported test tyre:',value(g,URIRef(vehicle),AEK.testedTyreName),'·',value(g,URIRef(vehicle),AEK.testedTyreSize))
        a=candidates(g,vehicle)
        if a.empty: st.info('No alignment candidates in the current data. This is not evidence of incompatibility.')
        else:
            options=a['match'].unique().tolist(); kinds=st.multiselect('Match types',options,default=options)
            subset=a[a['match'].isin(kinds)].copy()
            base=run('low_abrasion')[['tyre','abrasion']]; grades=run('safe_low_abrasion',5.5)[['tyre','safety']]
            subset=subset.merge(base,on='tyre',how='left').merge(grades,on='tyre',how='left')
            st.metric('Candidate relationships',len(subset)); show(subset,'vehicle_search')
            st.caption('Model-only links may have a different size. Dimension-only links do not establish identity. Measurements describe the independently tested tyre variant, not the selected car.')
            if not subset.empty:
                t=st.selectbox('Inspect tyre test evidence',subset.tyre.tolist(),format_func=lambda u:label(g,URIRef(u))+' · '+value(g,URIRef(u),AEK.tyreSize))
                show(observations(g,t),'vehicle_search_evidence')
    elif page=='Ask AutoEcoKG':
        st.header('Ask AutoEcoKG'); st.caption('A transparent, template-based question interface. No external LLM, API key or generated facts.')
        template=st.selectbox('Choose a supported question',list(QUESTIONS))
        typed=st.text_input('Or enter a supported question (exact wording)',value='',placeholder='Leave blank to use the selection')
        lookup={q.casefold().strip().rstrip('?').strip():q for q in QUESTIONS}
        question=lookup.get(typed.casefold().strip().rstrip('?').strip()) if typed.strip() else template
        if not question: st.warning('Question not supported. Choose a question above or enter its exact wording.'); st.stop()
        safety=st.slider('Maximum safety grade',0.6,5.5,2.5,0.1) if QUESTIONS[question]=='safe_low_abrasion' else 2.5
        size=st.selectbox('Tyre size',['All']+sorted(run('low_abrasion')['size'].unique().tolist())) if QUESTIONS[question] in ('low_abrasion','safe_low_abrasion') else 'All'
        name,df=question_answer(g,run,question,safety,size)
        st.metric('Matching records',len(df))
        if df.empty: st.info('No records match the selected constraints.')
        else:
            if name in ('vehicle_co2','fuel_gap','low_abrasion','safe_low_abrasion'):
                first=df.iloc[0]; st.subheader('First result: '+str(first['name']))
                st.caption('See the full result table for ties and other matching records.')
                st.write({k:float(first[k]) for k in ('co2','adac','wltp','gap','abrasion','safety') if k in first and pd.notna(first[k])})
            show(df,'question_results')
        with st.expander('SPARQL query and filters'):
            st.code(PREFIX+QUERIES[name],language='sparql')
            if name=='safe_low_abrasion': st.write('Bound maximum safety:',safety)
            if size!='All': st.write('Post-query dimension filter:',size)
            if question.startswith('Which diesel'): st.write('Post-query filter: diesel only, among fuel-gap records; sort by ADAC fuel consumption.')
        st.caption('Answers cover the current dataset only. No fitment or lifecycle emissions claims.')
    elif page=='Tyre explorer':
        t=run('low_abrasion'); season=st.selectbox('Season',['All']+sorted(t.category.unique().tolist())); f=t if season=='All' else t[t.category==season]
        size=st.selectbox('Size',['All']+sorted(f['size'].unique().tolist())); f=f if size=='All' else f[f['size']==size]
        metric_row([('Abrasion records',len(f)),('Minimum mg/km/t',f'{f.abrasion.min():g}' if len(f) else '—')]); show(f,'abrasion')
        if not f.empty:
            top=f.head(15).copy(); top['tyre label']=top.name+' · '+top['size']; st.plotly_chart(px.bar(top.iloc[::-1],x='abrasion',y='tyre label',orientation='h',labels={'abrasion':'Abrasion (mg/km/t)'},title='Lowest measured abrasion'),use_container_width=True)
        # Include provisional grade-only entities as well, not only measured abrasion rows.
        entities=sorted(set(g.subjects(RDF.type,AEK.TyreVariant)),key=lambda u:(label(g,u),str(u)))
        entities=[str(u) for u in entities if (season=='All' or value(g,u,AEK.seasonCategory)==season) and (size=='All' or value(g,u,AEK.tyreSize)==size)]
        if entities:
            selected=st.selectbox('Inspect all matching tyre entities (including grade-only)',entities,format_func=lambda u:f'{label(g,URIRef(u))} · {value(g,URIRef(u),AEK.tyreSize)} · {value(g,URIRef(u),AEK.recordId)}')
            show(observations(g,selected),'tyre_observations')
        st.caption('Measured abrasion and ADAC abrasion grades are different properties; missing grades are not zero.')
    elif page=='Tyre recommendations':
        st.info('Research ranking only. Fitment, load/speed rating and OEM approval are not verified. Lower grades and scores are better.')
        t=run('low_abrasion'); seasons=['summer','winter','all_season']
        season=st.selectbox('Season',seasons); sizes=sorted(t[t.category==season]['size'].unique().tolist()); default=sizes.index('225/40 R18') if '225/40 R18' in sizes else 0
        size=st.selectbox('Dimension',sizes,index=default) if sizes else st.text_input('Dimension','225/40 R18')
        safety=st.slider('Maximum safety grade',0.6,5.5,2.5,0.1); weight=st.slider('Environmental weight (%)',0,100,50,5)
        cap=st.checkbox('Limit abrasion',help='Hard filter: exclude tyres above a chosen measured abrasion value; not a legal threshold.'); maximum=st.number_input('Maximum abrasion (mg/km/t)',min_value=1.0,value=70.0) if cap else None
        st.caption(f'Abrasion weight {weight}% · Safety weight {100-weight}% · Normalized within eligible candidates.')
        if not size: st.stop()
        try:
            with st.spinner('Ranking eligible tyres…'):
                r=ranking(str(graph_path),stamp,size,season,safety,weight/100,maximum)
                baseline=ranking(str(graph_path),stamp,size,season,safety,weight/100,None) if cap else r
        except ValueError as e: st.error(str(e)); st.stop()
        if cap:
            metric_row([('Before abrasion cap',len(baseline)),('Excluded by cap',len(baseline)-len(r)),('After cap',len(r))])
            st.caption('Scores are recalculated within the remaining candidate set; scores from different filters are not directly comparable.')
            with st.expander('Excluded tyre records'):
                excluded=baseline[~baseline.tyre.isin(r.tyre)]; st.dataframe(excluded[['name','abrasion','safety']],hide_index=True,use_container_width=True)
        if r.empty: st.warning('No eligible tyres with both abrasion and safety observations. This is a data/constraint limitation, not a fitment assessment.')
        else:
            metric_row([('Eligible tyres',len(r)),('Pareto optimal',int(r.pareto_optimal.sum())),('Top score',f'{r.iloc[0].score:.4f}')]); st.subheader(f'Top candidate: {r.iloc[0]["name"]}')
            st.plotly_chart(px.scatter(r,x='abrasion',y='safety',color='pareto_optimal',hover_name='name',labels={'abrasion':'Abrasion (mg/km/t)','safety':'ADAC safety grade','pareto_optimal':'Pareto optimal'},title='Safety–abrasion trade-off'),use_container_width=True)
            show(r,'tyre_recommendations')
            top=r.iloc[0]; st.write(f"Why ranked first: weighted min-max score {top.score:.6f}, abrasion {top.abrasion:g} mg/km/t, safety grade {top.safety:g}. Lower is better; fitment not verified.")
            with st.expander('Inspect recommendation evidence'):
                t=st.selectbox('Ranked tyre',r.tyre.tolist(),format_func=lambda u:label(g,URIRef(u))); show(observations(g,t),'rank_evidence')
    elif page=='Graph explorer':
        v=run('vehicles'); selected=st.selectbox('Vehicle',v.vehicle.tolist(),format_func=lambda u:label(g,URIRef(u)))
        a=candidates(g,selected); st.caption('Alignment nodes connect vehicles to candidate tyres. False means not verified, not incompatible.')
        st.metric('Candidate links',len(a))
        if a.empty: st.info('No matching tyre candidates in the current graph.')
        else:
            kinds=st.multiselect('Match types',a['match'].unique().tolist(),default=a['match'].unique().tolist()); subset=a[a['match'].isin(kinds)]
            show(subset,'vehicle_tyre_candidates')
            if len(subset):
                limit=st.slider('Maximum links in diagram',1,12,min(6,len(subset))); fig,nodes=network_figure(g,selected,subset.head(limit).to_dict('records'))
                st.caption('Click a node or select it below to inspect RDF evidence. Edges connect alignment nodes to the vehicle and tyre.')
                try:
                    event=st.plotly_chart(fig,use_container_width=True,key='network_'+selected, on_select='rerun',selection_mode='points')
                    points=event.selection.points if event is not None else []
                    clicked=points[-1].get('customdata') if points else None
                    if isinstance(clicked,(tuple,list)) and len(clicked)==1: clicked=clicked[0]
                except TypeError:
                    st.plotly_chart(fig,use_container_width=True); clicked=None
                node_ids=list(nodes); active=st.selectbox('Inspect graph node',node_ids,index=node_ids.index(clicked) if isinstance(clicked,str) and clicked in nodes else 0,format_func=lambda u:nodes[u][1]+' · '+nodes[u][2],key='inspect_'+selected+'_'+str(clicked))
                if nodes[active][1]=='Alignment':
                    st.write({'match':value(g,URIRef(active),AEK.matchType),'identity verified':value(g,URIRef(active),AEK.identityVerified),'fitment verified':value(g,URIRef(active),AEK.fitmentVerified)})
                else: show(observations(g,active),'graph_node_observations')
                st.caption(f'Diagram shows {min(limit,len(subset))} of {len(subset)} selected links; complete table above.')
                t=st.selectbox('Inspect candidate tyre evidence',subset.tyre.tolist(),format_func=lambda u:label(g,URIRef(u)))
                show(observations(g,t),'candidate_observations')
    elif page=='SPARQL queries':
        name=st.selectbox('Built-in query',list(QUERIES),format_func=lambda x:TITLES[x]); safety=st.slider('Maximum safety grade',0.6,5.5,2.5,0.1) if name=='safe_low_abrasion' else 2.5
        with st.expander('SPARQL source',expanded=True):
            st.code(PREFIX+QUERIES[name],language='sparql')
            if name=='safe_low_abrasion': st.caption(f'Parameter binding: maxSafety = {safety} (xsd:decimal)')
        with st.spinner('Executing RDF query…'): df=run(name,safety)
        st.metric('Results',len(df)); show(df,'query_results',name+'.csv')
        if name in ('alignment','matched_tyre_observations'): st.caption('All candidate relationships are unverified unless explicitly confirmed by source evidence.')
    else:
        st.subheader('SHACL validation'); validation=read_report(ROOT/'data/processed/kg_validation_summary.csv')
        if validation is None: st.info('Run python src/validate_knowledge_graph.py to generate the report.')
        else:
            show(validation,'kg_validation_summary')
            issues=read_report(ROOT/'data/processed/kg_validation_issues.csv')
            if issues is not None: show(issues,'kg_validation_issues')
        st.subheader('Benchmark results'); summary=read_report(ROOT/'evaluation/benchmark_summary.csv'); results=read_report(ROOT/'evaluation/benchmark_results.csv')
        if summary is None or results is None: st.info('Run python src/evaluate.py to generate benchmark reports.')
        else:
            show(summary,'benchmark_summary'); d=results.groupby(['group','status']).size().reset_index(name='tests')
            st.plotly_chart(px.bar(d,x='group',y='tests',color='status',title='Benchmark outcomes'),use_container_width=True)
            group=st.selectbox('Test category',['All']+sorted(results.group.unique().tolist())); show(results if group=='All' else results[results.group==group],'benchmark_results')
        for report in (validation,summary):
            if report is not None and 'rdf_triples' in report and int(report.iloc[0].rdf_triples)!=len(g): st.warning('A saved report has a different triple count from the current graph. Rerun validation and evaluation.')
        st.caption('Saved reports are snapshots, not live tests. Matching triple counts do not prove graph identity. Rerun after any data or ontology change. Benchmark reference: processed CSVs, not external ground truth.')
    st.divider(); st.caption('AutoEcoKG · Academic research prototype · Source: ADAC reports. No commercial or certified fitment advice.')

if __name__=='__main__':
    main()
