# AutoEcoKG 2.0: Technical Blueprint & Implementation Roadmap
*Generated in Gemini Notebook: https://gemini.google.com/app/35d95c5963695f32*

Gemini said
AutoEcoKG 2.0: Technical Blueprint & Implementation Roadmap

A Real-World Automotive & Environmental Knowledge Graph for Euro 7 Compliance, Non-Exhaust Microplastic Modeling, Fleet TCO, and Sovereign Data Spaces

1. Executive Summary & Problem Formulation

Automotive environmental assessment faces a structural epistemic crisis at the exact moment European emissions regulation expands beyond the tailpipe. With Regulation (EU) 2024/1257 (Euro 7) entering mandatory application for new M1 passenger car and N1 light commercial vehicle type approvals on 29 November 2026 (and all newly registered M1/N1 vehicles on 29 November 2027), regulators, OEMs, tyre manufacturers, and corporate fleet operators can no longer rely on isolated laboratory homologation figures. Existing environmental data remains fragmented across three structurally incompatible evidentiary regimes: declared laboratory homologation (WLTP), independent standardized consumer and technical testing (ADAC Ecotest, UNECE tyre test protocols), and uncontrolled real-world operational telemetry (OBFCM, crowdsourced consumption platforms, and periodic technical inspections).

AutoEcoKG 2.0 resolves this fragmentation by evolving the AutoEcoKG 1.0 prototype (26,822 RDF triples) into a federated, provenance-preserving, enterprise-grade Semantic Knowledge Graph. It unifies >10 million annual European vehicle registrations, crowdsourced real-world energy consumption, multi-year mechanical durability curves, Euro 7 non-exhaust particulate emissions (tyre abrasion microplastics and brake dust 
PM
10
PM
10
	​

), cradle-to-grave EV battery Life Cycle Assessment (LCA), and CSRD (ESRS E1/E2) fleet sustainability reporting within a single standards-aligned architecture.

1.1 The Three-Tier Epistemic Gap
Evidentiary Tier	Representative Sources	Primary Metrics	Systemic Bias & Blind Spots	AutoEcoKG 2.0 Epistemic Role
Tier 1: Laboratory Homologation	EEA 
CO
2
	​

 Monitoring Registry (Reg. (EU) 2019/631), CoC, WLTP, UNECE R117	Declared 
CO
2
	​

 (
g/km), WLTP energy (
kWh/100 km), curb mass, nominal rolling resistance	Standardized ambient temperature (
23
∘
C), optimized test tyres, zero auxiliary HVAC load, idealized gear/regen profiles	Canonical entity backbone & legal compliance baseline
Tier 2: Independent Standardized Testing	ADAC Ecotest, UNECE WP.29 C1 Drum/Convoy Tyre Tests, Euro NCAP	Standardized highway/cold-start emissions, wet/dry braking, tyre abrasion level (
mg/(km⋅t)), 
AI
CT
	​

	Limited model-year and trim coverage; fixed test fleet vehicles; controlled reference road surfaces	Empirical calibration bridge & independent verification anchor
Tier 3: Real-World Operational Conditions	Spritmonitor, OBFCM/OBM telemetry, TÜV Periodic Inspection Reports, COVESA VSS streams	Empirical fuel/energy distributions, seasonal winter penalties, multi-year component defect rates, live battery SoH	Driver self-selection bias, uncalibrated tyre pressure, heterogeneous road roughness and topography	Ground-truth operational distribution & lifecycle degradation layer
1.2 Formal Problem Formulation: Divergence & Non-Exhaust Microplastics

Let 
𝑉
V denote the set of canonical European vehicle configurations and 
𝑇
T the set of pneumatic tyre models (classes C1, C2, C3). For any vehicle-tyre pairing 
(
𝑣
,
𝑡
)
∈
𝑉
×
𝑇
(v,t)∈V×T operating under regime 
𝑟
∈
{
WLTP
,
ADAC
,
RealWorld
}
r∈{WLTP,ADAC,RealWorld}, we define an observation vector 
𝑦
(
𝑟
)
(
𝑣
,
𝑡
)
y
(r)
(v,t) anchored to explicit provenance metadata 
𝜋
𝑟
π
r
	​

. The homologation-to-reality divergence vector is formalized as:

𝛥
real-lab
(
𝑣
,
𝑡
)
=
𝐸
[
𝑦
(
RealWorld
)
(
𝑣
,
𝑡
)
]
−
𝑦
(
WLTP
)
(
𝑣
,
𝑡
)
Δ
real-lab
	​

(v,t)=E[y
(RealWorld)
(v,t)]−y
(WLTP)
(v,t)

Historically, policy focused exclusively on the tailpipe 
CO
2
CO
2
	​

 and 
NO
𝑥
NO
x
	​

 components of 
𝛥
real-lab
Δ
real-lab
	​

. However, powertrain electrification creates an emission-shifting paradox: battery electric vehicles (BEVs) eliminate tailpipe exhaust and substantially reduce friction-brake dust via regenerative braking, yet their elevated kerb mass (typically 
+
250
 to 
+
500
 kg
+250 to +500 kg over equivalent ICE platforms) and instantaneous peak torque amplify vehicle-induced tyre abrasion.

Under Regulation (EU) 2024/1257, tyre abrasion is recognized as the largest source of microplastics released into the environment. Following the formal metrology adopted in UNECE ECE/TRANS/WP.29/2026/138 for Class C1 passenger car tyres, AutoEcoKG 2.0 models tyre particulate generation across three coupled physical quantities:

Abrasion Rate (
𝑅
abr
R
abr
	​

): Total elastomeric and polymer mass lost per unit distance, expressed in 
mg/km
mg/km.

Load-Normalized Abrasion Level (
𝐿
abr
L
abr
	​

): Abrasion rate normalized to the vertical load 
𝑀
load
M
load
	​

 (in metric tonnes) carried by the tyre:

𝐿
abr
=
𝑅
abr
𝑀
load
[
mg
/
(
km
⋅
t
)
]
L
abr
	​

=
M
load
	​

R
abr
	​

	​

[mg/(km⋅t)]

Abrasion Index (
AI
CT
AI
CT
	​

): Dimensionless compliance ratio comparing the candidate tyre's abrasion level against the applicable ASTM Standard Reference Test Tyre (SRTT17S per ASTM F3676-24 for summer tyres; SRTT17W per ASTM F3675-24 for winter tyres):

AI
CT
=
𝐿
abr
(
Candidate
)
𝐿
abr
(
SRTT
)
AI
CT
	​

=
L
abr
	​

(SRTT)
L
abr
	​

(Candidate)
	​


To support both air quality health modeling and ecological microplastic accounting, total vehicle-level tyre mass loss 
𝐸
tyre,total
(
𝑣
,
𝑡
)
=
∑
𝑖
=
1
4
𝑅
abr
,
𝑖
E
tyre,total
	​

(v,t)=∑
i=1
4
	​

R
abr,i
	​

 is partitioned into environmental transport compartments via empirically parameterized emission fractions:

𝐸
PM
10
tyre
=
𝛼
PM
10
⋅
𝐸
tyre,total
,
𝐸
PM
2.5
tyre
=
𝛼
PM
2.5
⋅
𝐸
tyre,total
,
𝐸
runoff/soil
MP
=
(
1
−
𝛼
PM
10
)
⋅
𝐸
tyre,total
E
PM
10
	​

tyre
	​

=α
PM
10
	​

	​

⋅E
tyre,total
	​

,E
PM
2.5
	​

tyre
	​

=α
PM
2.5
	​

	​

⋅E
tyre,total
	​

,E
runoff/soil
MP
	​

=(1−α
PM
10
	​

	​

)⋅E
tyre,total
	​


where 
𝛼
PM
10
∈
[
0.01
,
0.10
]
α
PM
10
	​

	​

∈[0.01,0.10] captures the airborne respirable fraction of Tyre and Road Wear Particles (TRWP) and 
(
1
−
𝛼
PM
10
)
(1−α
PM
10
	​

	​

) captures coarse polymer microplastics depositing onto road surfaces, stormwater runoff, aquatic sediments, and roadside soils. AutoEcoKG 2.0 treats these coefficients as first-class, provenance-tracked graph entities rather than hardcoded constants, enabling transparent sensitivity analysis as empirical road-surface and wet-weather studies evolve.

2. Existing Baseline: AutoEcoKG 1.0 Architecture & Limitations

AutoEcoKG 1.0 established the semantic and validation foundations for cross-source automotive environmental reasoning. Its verified baseline architecture consists of four tightly coupled layers:

RDF Graph Footprint: 26,822 RDF triples encoded in standard W3C RDF 1.1 (Turtle serialization), representing curated vehicle trims, laboratory WLTP ratings, ADAC Ecotest scores, and initial tyre test records.

Ontology Backbone (SOSA & PROV-O): Measurement modeling adheres strictly to the W3C SOSA (Sensor, Observation, Sample, and Actuator) ontology—representing every test score, fuel consumption reading, and emission measurement as an immutable sosa:Observation linked to a sosa:FeatureOfInterest (vehicle or tyre), a sosa:ObservableProperty, and a sosa:Procedure. Data lineage is captured via W3C PROV-O (prov:Entity, prov:Activity, prov:Agent, prov:wasDerivedFrom), preventing silent conflation of laboratory versus independent test figures.

SHACL Structural Validation: Automated W3C SHACL shape graphs enforce schema conformance prior to graph ingestion, checking mandatory provenance links, numeric range boundaries, datatype integrity (xsd:decimal, xsd:gYear), and measurement unit presence.

Competency Question Benchmark: 37/37 benchmark competency questions (CQs) pass deterministic validation, executed via 8 rigid parameterized SPARQL query templates covering single-hop lookups, WLTP-vs-ADAC deltas, and basic ranking.

Structural Bottlenecks Driving the 2.0 Redesign
Architectural Dimension	AutoEcoKG 1.0 Baseline	AutoEcoKG 2.0 Target State	Engineering Driver
Data Scale & Ingestion	26,822 triples; manual batch scripts	
>150M virtualized/materialized triples; automated RML + OBDA pipelines	Ingesting EEA Registry (
>10M rows/yr), Spritmonitor, and TÜV multi-year datasets
Emission & Lifecycle Scope	Exhaust 
CO
2
	​

/pollutants & basic tyre ratings	Full Euro 7 non-exhaust (tyre abrasion 
mg/(km⋅t), brake 
PM
10
	​

), EV battery SoH, Cradle-to-Grave LCA	Mandatory Euro 7 enforcement (Nov 2026) and UNECE WP.29 C1 abrasion rules
Decision & ESG Analytics	Single-metric sorting	5-objective Pareto TCO optimizer + audit-ready CSRD ESRS E1/E2 generator	Enterprise fleet procurement & EU statutory sustainability assurance
Query Interface	8 rigid parameterized SPARQL templates	Neuro-symbolic GraphRAG with schema-constrained Text2SPARQL & provenance binding	Handling arbitrary ad-hoc, multi-hop analytical questions without template maintenance
Interoperability & Storage	Local RDF file / single-node store	COVESA VSS + Catena-X SAMM/AAS/EDC federation over GraphDB Enterprise + Neo4j GDS + Parquet OBDA	Sovereign OEM–supplier–fleet data exchange & horizontal query scalability
3. Five Pillars for Real-World Expansion
Pillar 1: Large-Scale European Fleet & Telemetry Integration

Scaling AutoEcoKG from 26,822 triples to pan-European coverage requires ingesting three heterogeneous macro-datasets without causing catastrophic triple bloat or entity fragmentation.

1.1 EEA European Vehicle Registry (
>
10
M
>10M Rows/Year)

Published annually under Regulation (EU) 2019/631, the European Environment Agency (EEA) passenger car and van 
CO
2
CO
2
	​

 monitoring registry tracks every new vehicle registered across EU Member States, exceeding 10 million annual records and 37 million cumulative rows since 2012. Materializing every individual registration row as full SOSA/PROV-O RDF (~30 triples/row) would generate 
>
1.1
 billion
>1.1 billion redundant triples.

AutoEcoKG 2.0 solves this via a Hybrid Canonical Aggregation & Virtualization Strategy:

Canonical Type-Variant-Version (TVV) Grouping: Raw EEA records are deterministically aggregated along (RegistrationYear, MemberState, Manufacturer, CommercialName, TypeApprovalNumber, Variant, Version, FuelType, FuelMode)—compressing tens of millions of registration rows into ~250K–400K unique technical vehicle variants while preserving exact fleet volume (aekg:registrationCount), mean/median/std of mass in running order (m), WLTP 
CO
2
CO
2
	​

 (Ewltp), electric energy consumption (z), and wheelbase/axle width.

OBDA Lakehouse Virtualization: Granular row-level EEA tables remain stored in partitioned Apache Parquet queried via DuckDB/PostgreSQL and exposed on demand as virtual RDF graphs through Ontop (OBDA) using R2RML mappings for deep statistical drill-downs.

1.2 Spritmonitor Crowdsourced Real-World Consumption

To bridge Tier 1 (EEA WLTP) and Tier 2 (ADAC Ecotest) with empirical driver behavior, AutoEcoKG 2.0 ingests aggregated Spritmonitor fuel and electric consumption profiles. Because crowdsourced entries contain noisy free-text trim names and outlier fuelings, ingestion applies:

Robust Statistical Profiling: Trimmed distributions (filtering the bottom/top 2.5% data-entry errors, requiring minimum sample size 
𝑁
≥
15
N≥15 vehicles and 
≥
5,000
 km
≥5,000 km logged per vehicle) storing aekg:meanValue, aekg:medianValue, aekg:p10Value, aekg:p90Value, aekg:sampleSize, and stratified sub-profiles for driving environment (urban/rural/Autobahn) and seasonality (summer vs. winter tyre penalty).

Probabilistic Entity Resolution (ER): Cross-source linking across EEA, ADAC, and Spritmonitor uses Fellegi-Sunter probabilistic record linkage (implemented via Splink) blocking on (Manufacturer, FuelType, ModelYear ± 1) and scoring on normalized model-name token similarity, engine displacement (
±
25
 cc
±25 cc), and rated power (
±
3
 kW
±3 kW). Every cross-source link is stored as a reified aekg:EntityAlignment with confidence score 
𝜎
∈
[
0
,
1
]
σ∈[0,1], preserving auditability rather than asserting blind owl:sameAs identity.

1.3 TÜV Periodic Technical Inspection Durability

Environmental impact cannot be separated from service life: a vehicle requiring premature suspension, brake, or structural replacement incurs substantial embodied carbon and TCO penalties. AutoEcoKG 2.0 models TÜV Report inspection cohorts across five standardized vehicle age brackets (2–3, 4–5, 6–7, 8–9, and 10–11 years), capturing:

Significant Defect Rate (aekg:significantDefectRate, EM-Quote %) and cohort average odometer mileage (aekg:meanCohortMileage).

Subsystem Failure Decomposition: Disaggregated failure propensities for chassis/axles/springs, brake discs/lines, and environmental/exhaust systems, quantifying how heavier EV and SUV platforms accelerate mechanical wear relative to lighter reference segments.

Pillar 2: Euro 7 Regulatory Compliance & Particulate Modeling

AutoEcoKG 2.0 embeds executable regulatory logic aligned with Regulation (EU) 2024/1257 (Euro 7) and UNECE WP.29 technical regulations, transforming the knowledge graph into an automated compliance engine.

Euro 7 / UNECE Compliance Domain	Mandatory Regulatory Threshold / Metric	Enforcement Timeline	Knowledge Graph Representation
Exhaust Particle Number (
PN
10
	​

)	Particle counting lowered from 
23 nm (
PN
23
	​

) to 
10 nm (
PN
10
	​

) for M1/N1; stricter heavy-duty 
NO
x
	​

 (
200 mg/kWh lab / 
260 mg/kWh RDE), 
N
2
	​

O, 
HCHO	29 Nov 2026 (new M1/N1 types); 29 Nov 2027 (all new M1/N1); May 2028/2029 (HDV)	aekg:ExhaustPN10Observation linked to RDE & WLTP sosa:Procedure
Brake Dust Emissions (
PM
10
	​

)	
3 mg/km (pure BEVs); 
7 mg/km (ICE, HEV, PHEV, FCEV cars); 
11 mg/km (large ICE N1 vans); uniform 
3 mg/km from 2035	29 Nov 2026 (new M1/N1 types); 29 Nov 2027 (all new M1/N1)	aekg:BrakeDustObservation parameterized by regen-braking fraction & WLTP-Brake cycle
Tyre Abrasion & Microplastics	Abrasion rate (
mg/km), load-normalized abrasion level (
mg/(km⋅t)), and Abrasion Index 
AI
CT
	​

 vs. SRTT17S/SRTT17W via on-road convoy or indoor drum test	C1: 1 Jul 2028 (new types) / 1 Jul 2030 (ban); C2: Apr 2030/2032; C3: Apr 2032/2034	aekg:TyreAbrasionObservation + aekg:MicroplasticEmissionFraction
EV/PHEV Battery Durability & Cold Range	Minimum State-of-Health (SoH): 
80% at 5 yr / 
100,000 km and 
72% at 8 yr / 
160,000 km (M1 cars); 
75% / 
67% (N1 vans); mandatory 
−7
∘
C winter range test	29 Nov 2026 (new M1/N1 types); 29 Nov 2027 (all new M1/N1)	aekg:BatteryDurabilityObservation, aekg:ColdRangeObservation
Digital Monitoring & Passports	Mandatory Environmental Vehicle Passport (EVP) at registration & continuous quantitative On-Board Monitoring (OBM) with anti-tampering integrity	Concurrent with Euro 7 M1/N1/HDV rollouts	aekg:EnvironmentalVehiclePassport + OBM telemetry streams
Cradle-to-Grave EV Battery & Vehicle LCA Sub-Graph

To prevent narrow operational optimization that obscures upstream manufacturing impacts, Pillar 2 implements an ISO 14040/14044 Cradle-to-Grave LCA ontology module decomposing total lifecycle Global Warming Potential (
GWP
100
GWP
100
	​

, in 
kg CO
2
e
kg CO
2
	​

e) into five traceable stages:

LCA
total
(
𝑣
)
=
𝐸
glider
+
𝐸
battery_mfg
(
𝑐
,
𝑄
,
𝑔
mfg
)
+
∫
0
𝐷
life
𝑒
use
(
𝑣
,
𝑥
,
𝑔
grid
(
𝑡
)
)
𝑑
𝑥
+
𝐸
maint
(
𝑣
,
T
U
¨
V
)
−
𝐶
EoL
(
𝑐
,
𝜂
rec
)
LCA
total
	​

(v)=E
glider
	​

+E
battery_mfg
	​

(c,Q,g
mfg
	​

)+∫
0
D
life
	​

	​

e
use
	​

(v,x,g
grid
	​

(t))dx+E
maint
	​

(v,T
U
¨
V)−C
EoL
	​

(c,η
rec
	​

)

Cathode Chemistry & Capacity Parameterization (
𝑐
,
𝑄
,
𝑔
mfg
c,Q,g
mfg
	​

): Explicitly distinguishes LFP, NMC622, NMC811, NCA, and Na-ion pack chemistries, nominal energy capacity 
𝑄
Q (
kWh
kWh), and cell manufacturing region grid carbon intensity 
𝑔
mfg
g
mfg
	​

 (
g CO
2
e/kWh
g CO
2
	​

e/kWh), ingesting Catena-X Product Carbon Footprints (PCFs) when primary supplier data is available and falling back to ecoinvent/GREET secondary factors with explicit aekg:DataQualityRating.

Dynamic Use-Phase & Maintenance Integration: Multiplies real-world Spritmonitor/OBFCM consumption against Member-State hourly or annual average grid carbon intensity 
𝑔
grid
(
𝑡
)
g
grid
	​

(t), adding replacement tyre embodied carbon (driven by tread lifespan) and battery second-life / hydrometallurgical recycling credits 
𝐶
EoL
C
EoL
	​

 aligned with the EU Battery Regulation (EU) 2023/1542.

Pillar 3: Fleet Total Cost of Ownership (TCO) & CSRD ESG Reporting
3.1 Multi-Criteria Pareto Decision Engine

Fleet procurement decisions rarely hinge on a single KPI. A low-rolling-resistance tyre that cuts BEV energy consumption may sacrifice wet-braking distance or increase abrasion mass loss. AutoEcoKG 2.0 exposes a Multi-Criteria Pareto Optimization Engine evaluating every valid vehicle-tyre pairing 
𝑥
=
(
𝑣
,
𝑡
)
∈
𝐹
x=(v,t)∈F (filtered by load index, speed rating, rim diameter, and Euro 7 compliance) across a 5-dimensional objective vector:

min
⁡
𝑥
∈
𝐹
𝐹
(
𝑥
)
=
[
−
𝑓
safety
(
𝑥
)
,
𝑓
abrasion
(
𝑥
)
,
−
𝑓
lifespan
(
𝑥
)
,
𝑓
RRC
(
𝑥
)
,
𝑓
TCO
(
𝑥
)
]
𝑇
x∈F
min
	​

F(x)=[−f
safety
	​

(x),f
abrasion
	​

(x),−f
lifespan
	​

(x),f
RRC
	​

(x),f
TCO
	​

(x)]
T

Safety Score (
𝑓
safety
f
safety
	​

, maximize): Composite of EU Tyre Label wet-grip class, ADAC wet/dry braking deceleration (
m/s
2
m/s
2
), aquaplaning resistance, and Euro NCAP adult/vulnerable-road-user ratings.

Tyre Abrasion & Microplastics (
𝑓
abrasion
f
abrasion
	​

, minimize): Vehicle-load-adjusted abrasion rate 
𝐸
tyre,total
(
𝑣
,
𝑡
)
E
tyre,total
	​

(v,t) in 
mg/km
mg/km and cumulative microplastic release (kg) over the fleet holding period 
𝐻
H.

Combined Lifespan & Durability (
𝑓
lifespan
f
lifespan
	​

, maximize): Predicted tyre tread life 
𝐷
tread
(
𝑣
,
𝑡
)
D
tread
	​

(v,t) (km to 
1.6
 mm
1.6 mm legal / 
3.0
 mm
3.0 mm fleet-safety threshold) paired with TÜV cohort mechanical durability index.

Rolling Resistance (
𝑓
RRC
f
RRC
	​

, minimize): Tyre Rolling Resistance Coefficient (
kg/t
kg/t) mapped via physics-based elasticity (
≈
1.5
–
2.0
%
≈1.5–2.0% real-world energy change per 
1
 kg/t
1 kg/t RRC shift) onto Spritmonitor baseline consumption.

5-Year Real-World Fleet TCO (
𝑓
TCO
f
TCO
	​

, minimize):

TCO
(
𝑣
,
𝑡
,
𝐻
,
𝐷
ann
)
=
CAPEX
(
𝑣
)
−
RV
(
𝑣
,
𝐻
,
SoH
)
+
∑
𝑦
=
1
𝐻
𝐶
energy
,
𝑦
+
𝐶
tyres
,
𝑦
+
𝐶
maint
,
𝑦
(
T
U
¨
V
)
+
𝐶
tax/CO
2
,
𝑦
(
1
+
𝑟
)
𝑦
TCO(v,t,H,D
ann
	​

)=CAPEX(v)−RV(v,H,SoH)+
y=1
∑
H
	​

(1+r)
y
C
energy,y
	​

+C
tyres,y
	​

+C
maint,y
	​

(T
U
¨
V)+C
tax/CO
2
	​

,y
	​

	​


where residual value 
RV
RV explicitly incorporates Euro 7 battery SoH retention curves and 
𝐶
tyres
,
𝑦
C
tyres,y
	​

 models exact replacement cadence 
⌈
(
𝐻
⋅
𝐷
ann
)
/
𝐷
tread
(
𝑣
,
𝑡
)
⌉
⌈(H⋅D
ann
	​

)/D
tread
	​

(v,t)⌉.

The engine first prunes dominated pairings via exact Pareto Skyline filtering (executed directly in SPARQL 1.1 or Neo4j/Python via NSGA-II for continuous fleet-mix allocation), then ranks the non-dominated frontier using configurable TOPSIS weights so corporate fleet managers can trade off cost, safety, and microplastic reduction transparently.

3.2 Audit-Grade CSRD (ESRS E1 & E2) Reporting Pipeline

Under the EU Corporate Sustainability Reporting Directive (CSRD), large enterprises must disclose auditable climate and pollution metrics across own operations and value chains. AutoEcoKG 2.0 automates machine-readable ESRS JSON-LD / ESEF-ready disclosures directly from graph queries:

ESRS E1 (Climate Change): Aggregates absolute energy consumption in MWh disaggregated by renewable vs. non-renewable fuels and electricity, alongside Scope 1 (owned ICE fleet real-world fuel combustion), Scope 2 (location- and market-based BEV charging), and Scope 3 (Cat. 1/2 embodied vehicle & tyre production, Cat. 3 well-to-tank energy, Cat. 11/12 leased fleet & end-of-life).

ESRS E2 (Pollution): Directly satisfies Disclosure Requirement E2-4 (pollution of air, water, and soil—quantifying 
NO
𝑥
NO
x
	​

, exhaust 
PN
10
PN
10
	​

, brake 
PM
10
PM
10
	​

, and tyre-derived microplastics partitioned into atmospheric vs. soil/water loads, together with the measurement methodology) and E2-5 (Substances of Concern and SVHCs such as 6PPD antioxidants, zinc oxide vulcanization activators, and PAHs in tyre tread compounds).

Assurance-Ready Provenance: Every reported KPI binds to its underlying prov:Activity, dataset version URI, emission-factor timestamp, and uncertainty interval, giving external CSRD auditors deterministic lineage from executive summary down to individual vehicle cohorts.

Pillar 4: Production GraphRAG & Conversational AI

AutoEcoKG 1.0 relied on 8 rigid parameterized SPARQL templates—adequate for fixed dashboards, but brittle against novel regulatory, fleet-planning, or cross-domain questions. AutoEcoKG 2.0 replaces static templates with a Neuro-Symbolic Hybrid GraphRAG Engine engineered for zero-hallucination analytical querying.

4.1 Five-Stage Neuro-Symbolic Query Pipeline

Ontology-Aware Schema & Entity Linking: Incoming natural language queries are embedded and matched against two vector indices (Qdrant / GraphDB Similarity Index): (a) a TBox Schema Index over OWL classes, properties, and SHACL definitions, and (b) an ABox Entity Index resolving colloquial references (e.g., "VW ID.4 Pro on Michelin e.Primacy" or "Euro 7 BEV brake limit") into canonical URIs.

Few-Shot Schema-Constrained Text2SPARQL: A domain-tuned LLM (e.g., Qwen/Llama/Gemini class via constrained decoding) receives the pruned relevant TBox subgraph, resolved entity URIs, and top-
𝑘
k structurally similar verified SPARQL exemplars to synthesize a SPARQL 1.1 query.

Static AST & SHACL Semantic Verification Gate: Before touching the triple store, a deterministic symbolic verifier parses the generated SPARQL AST (rdflib/Apache Jena), validating:

Read-only safety (blocking INSERT/DELETE/DROP injection and unbounded SERVICE calls).

Predicate domain/range consistency against the OWL TBox (catching hallucinated predicates or inverted triples).

Query complexity and timeout bounds (enforcing LIMIT and preventing Cartesian-product joins).

Iterative Self-Correction Loop: If static verification fails or execution yields an unexpected empty result set, the verifier extracts structured error diagnostics (e.g., "Property aekg:hasAbrasionRate attaches to aekg:TyreAbrasionObservation, not aekg:TyreModel"), triggers up to 
𝑁
=
3
N=3 targeted repair iterations, or gracefully falls back to an explicit calibrated abstention explaining the exact data gap.

Provenance-Bound Answer Synthesis: Query results are returned alongside mandatory provenance bindings (?sourceAgent, ?procedure, ?testDate, ?confidenceScore). The synthesis module generates natural language responses and structured tables where every numerical assertion carries an inline clickable citation to its graph prov:Entity URI.

4.2 AutoEcoBench 2.0 Evaluation Suite

The 37 CQs from AutoEcoKG 1.0 are preserved as a mandatory regression suite and expanded into AutoEcoBench 2.0 (150+ benchmark tasks) spanning five difficulty tiers:

Tier A (37 legacy CQs): Single/two-hop WLTP & ADAC lookups.

Tier B (35 CQs): EEA–Spritmonitor–TÜV real-world divergence & cohort aggregation.

Tier C (30 CQs): Euro 7 non-exhaust compliance, 
AI
CT
AI
CT
	​

, brake 
PM
10
PM
10
	​

, and EV battery durability.

Tier D (28 CQs): Multi-criteria Pareto TCO & CSRD ESRS E1/E2 rollup queries.

Tier E (20+ adversarial CQs): Out-of-scope or missing-data probes measuring Abstention Precision (target 
≥
98
%
≥98%), Execution Accuracy (EX) (target 
≥
92
%
≥92%), and Provenance Citation Faithfulness (target 
100
%
100%).

Pillar 5: Automotive Standards & Enterprise Deployment

To operate inside real European OEM, Tier-1 supplier, and fleet ecosystems rather than as an academic silo, AutoEcoKG 2.0 natively adopts two core automotive industry standards.

5.1 COVESA Vehicle Signal Specification (VSS) Alignment

The COVESA Vehicle Signal Specification (VSS) defines the industry-standard hierarchical tree for in-vehicle telemetry attributes, sensors, and actuators. AutoEcoKG 2.0 bridges live vehicle telemetry into the semantic graph via W3C VSSo (VSS Ontology) mappings:

Static attributes (e.g., Vehicle.VehicleIdentification.VIN, Vehicle.CurrentOverallWeight, Vehicle.Powertrain.TractionBattery.GrossCapacity) map to aekg:VehicleInstance properties.

Dynamic time-series signals (Vehicle.Powertrain.TractionBattery.StateOfHealth, Vehicle.Chassis.Axle.Row1.Wheel.Left.Tire.Pressure, Vehicle.OBD.Odometer, Vehicle.Powertrain.ElectricMotor.Power) map directly to sosa:ObservableProperty instances. High-frequency telemetry (1–100 Hz) is never dumped raw into RDF; instead, edge/cloud stream processors (Apache Kafka + Flink) compute rolling trip/monthly aggregations (e.g., mean regenerative braking ratio, winter Wh/km, quarterly SoH snapshots) and commit compact sosa:ObservationCollection summaries into the Knowledge Graph.

5.2 Catena-X Data Space Integration

For sovereign B2B exchange of primary supplier data (e.g., tyre compound SVHC declarations, laboratory drum abrasion reports, and battery cell Product Carbon Footprints), AutoEcoKG 2.0 aligns with the Catena-X Data Ecosystem across all three interoperability layers:

Semantic Interoperability: Core AutoEcoKG 2.0 modules are published as SAMM (Semantic Aspect Meta Model) Aspect Models (TTL/JSON-LD) and packaged inside Asset Administration Shells (AAS) for Digital Battery Passports, Tyre Environmental Passports, and PCF exchange.

Technical Interoperability: External partner graphs connect through Tractus-X Eclipse Dataspace Components (EDC) implementing the Data Spaces Protocol (DSP) and Decentralized Claims Protocol (DCP). Federated cross-company SPARQL queries execute through Catena-X Knowledge Agents (Binding Agents) without centralizing proprietary OEM or Tier-1 test databases.

Legal & Policy Interoperability: Usage control policies (ODRL contracts enforced by EDC) restrict how sensitive supplier abrasion or battery degradation data may be used (e.g., "permitted for CSRD ESRS E2 aggregation; prohibited for public model-level benchmarking"), preserving commercial confidentiality.

5.3 Scalable Enterprise Storage Architecture
Storage Tier	Recommended Engine	Workload Role	Scaling & Performance Strategy
Primary Semantic Core	Ontotext GraphDB Enterprise (Cluster)	Authoritative OWL 2 / RDF-star / SHACL triple store, SPARQL 1.1 federation, provenance graphs	High-availability Raft cluster; named-graph partitioning by source & year; built-in Lucene/vector connectors for GraphRAG
High-Speed Analytical Projection	Neo4j Enterprise (via n10s / Neosemantics)	Optional synchronized LPG projection for sub-second Graph Data Science (GDS) similarity, clustering, and fleet Pareto routing	Incremental CDC sync from GraphDB; dedicated read replicas for Fleet TCO SaaS UI
Cold Raw & Time-Series Lakehouse	Apache Parquet / TimescaleDB + Ontop OBDA	Raw 37M+ EEA registration rows, granular Spritmonitor refueling logs, and raw COVESA VSS telemetry streams	Columnar compression; virtualized via R2RML/Ontop only when deep row-level drill-down is requested
4. Concrete Ontology Extensions & Sample SPARQL 1.1 Queries
4.1 Modular Ontology Extensions (Turtle / OWL 2 + SOSA + PROV-O + SAMM/VSS)
Code snippet
@prefix aekg:  <https://w3id.org/autoecokg/ontology#> .
@prefix sosa:  <http://www.w3.org/ns/sosa/> .
@prefix prov:  <http://www.w3.org/ns/prov#> .
@prefix qudt:  <http://qudt.org/schema/qudt/> .
@prefix unit:  <http://qudt.org/vocab/unit/> .
@prefix owl:   <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix skos:  <http://www.w3.org/2004/02/skos/core#> .
@prefix vsso:  <https://github.com/w3c/vsso#> .
@prefix samm:  <urn:samm:org.eclipse.esmf.samm:meta-model:2.1.0#> .

<https://w3id.org/autoecokg/ontology/2.0> a owl:Ontology ;
    owl:versionIRI <https://w3id.org/autoecokg/ontology/2.0.0> ;
    rdfs:label "AutoEcoKG 2.0 Automotive & Environmental Ontology"@en ;
    owl:imports <http://www.w3.org/ns/sosa/> ,
                <http://www.w3.org/ns/prov-o#> .

# =====================================================================
# 1. CANONICAL FLEET, ENTITY ALIGNMENT & DURABILITY CLASSES (Pillar 1)
# =====================================================================

aekg:VehicleModelVariant a owl:Class ;
    rdfs:subClassOf sosa:FeatureOfInterest , prov:Entity ;
    rdfs:comment "Canonical EU Type-Variant-Version (TVV) vehicle specification aggregated from EEA CoC data."@en .

aekg:TyreModel a owl:Class ;
    rdfs:subClassOf sosa:FeatureOfInterest , prov:Entity ;
    rdfs:comment "Pneumatic tyre SKU classified under UNECE Class C1, C2, or C3."@en .

aekg:VehicleTyreConfiguration a owl:Class ;
    rdfs:subClassOf sosa:FeatureOfInterest ;
    rdfs:comment "Valid operational pairing of a VehicleModelVariant and TyreModel for compliance and Pareto TCO."@en .

aekg:RealWorldConsumptionDistribution a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "Statistically aggregated real-world fuel/energy consumption (e.g., Spritmonitor or OBFCM cohort)."@en .

aekg:TUVInspectionCohort a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "Age-bracketed periodic technical inspection (HU) defect rate and mileage cohort."@en .

aekg:EntityAlignment a owl:Class ;
    rdfs:subClassOf prov:Entity ;
    rdfs:comment "Probabilistic cross-dataset entity match with explicit linkage confidence score."@en .

# =====================================================================
# 2. EURO 7 NON-EXHAUST, BATTERY DURABILITY & LCA CLASSES (Pillar 2)
# =====================================================================

aekg:TyreAbrasionObservation a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "UNECE WP.29 / Euro 7 tyre abrasion measurement capturing rate (mg/km), level (mg/km/t), and AI_CT."@en .

aekg:BrakeDustObservation a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "Euro 7 WLTP-Brake PM10 mass emission observation (mg/km)."@en .

aekg:BatteryDurabilityObservation a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "EV/PHEV traction battery State-of-Health (SoH %) observation at milestone age/mileage."@en ;
    skos:relatedMatch vsso:TractionBatteryStateOfHealth .

aekg:EnvironmentalVehiclePassport a owl:Class ;
    rdfs:subClassOf prov:Entity ;
    rdfs:comment "Digital Euro 7 Environmental Vehicle Passport (EVP) aligned with Catena-X AAS/SAMM."@en .

aekg:LifecycleStageImpact a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "ISO 14040/14044 Cradle-to-Grave GWP100 impact for a specific lifecycle stage (Production, Use, EoL)."@en .

# =====================================================================
# 3. FLEET TCO & CSRD ESRS E1/E2 CLASSES (Pillar 3)
# =====================================================================

aekg:TCOCalculation a owl:Class ;
    rdfs:subClassOf prov:Entity ;
    rdfs:comment "Discounted multi-year Fleet Total Cost of Ownership calculation bound to operational parameters."@en .

aekg:ESRSE2PollutionDisclosure a owl:Class ;
    rdfs:subClassOf prov:Entity ;
    rdfs:comment "Audit-ready CSRD ESRS E2-4 / E2-5 air, soil, and water particulate/microplastic disclosure."@en .

# =====================================================================
# 4. CORE OBJECT & DATATYPE PROPERTIES
# =====================================================================

aekg:hasVehicleVariant a owl:ObjectProperty ;
    rdfs:domain aekg:VehicleTyreConfiguration ;
    rdfs:range aekg:VehicleModelVariant .

aekg:hasTyreModel a owl:ObjectProperty ;
    rdfs:domain aekg:VehicleTyreConfiguration ;
    rdfs:range aekg:TyreModel .

aekg:referenceSRTT a owl:ObjectProperty ;
    rdfs:domain aekg:TyreAbrasionObservation ;
    rdfs:range aekg:TyreModel ;
    rdfs:comment "Reference ASTM Standard Reference Test Tyre (SRTT17S or SRTT17W) used for AI_CT normalization."@en .

aekg:vssSignalPath a owl:DatatypeProperty ;
    rdfs:domain sosa:ObservableProperty ;
    rdfs:range xsd:string ;
    rdfs:comment "Canonical COVESA VSS dot-notation path (e.g., Vehicle.Powertrain.TractionBattery.StateOfHealth)."@en .

aekg:sammAspectUrn a owl:DatatypeProperty ;
    rdfs:domain owl:Class ;
    rdfs:range xsd:anyURI ;
    rdfs:comment "Corresponding Catena-X SAMM Aspect Model URN."@en .

aekg:abrasionRateMgKm a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreAbrasionObservation ; rdfs:range xsd:decimal .

aekg:abrasionLevelMgKmTonne a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreAbrasionObservation ; rdfs:range xsd:decimal .

aekg:abrasionIndexAICT a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreAbrasionObservation ; rdfs:range xsd:decimal .

aekg:airbornePM10Fraction a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreAbrasionObservation ; rdfs:range xsd:decimal .

aekg:brakePM10MgKm a owl:DatatypeProperty ;
    rdfs:domain aekg:BrakeDustObservation ; rdfs:range xsd:decimal .

aekg:batterySoHPercent a owl:DatatypeProperty ;
    rdfs:domain aekg:BatteryDurabilityObservation ; rdfs:range xsd:decimal .

aekg:milestoneYears a owl:DatatypeProperty ;
    rdfs:domain aekg:BatteryDurabilityObservation ; rdfs:range xsd:integer .

aekg:milestoneKm a owl:DatatypeProperty ;
    rdfs:domain aekg:BatteryDurabilityObservation ; rdfs:range xsd:integer .

aekg:wetGripScore a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreModel ; rdfs:range xsd:decimal .

aekg:rollingResistanceCoeff a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreModel ; rdfs:range xsd:decimal .

aekg:predictedTreadLifespanKm a owl:DatatypeProperty ;
    rdfs:domain aekg:VehicleTyreConfiguration ; rdfs:range xsd:integer .

aekg:fiveYearTCOEur a owl:DatatypeProperty ;
    rdfs:domain aekg:TCOCalculation ; rdfs:range xsd:decimal .

aekg:significantDefectRatePct a owl:DatatypeProperty ;
    rdfs:domain aekg:TUVInspectionCohort ; rdfs:range xsd:decimal .

aekg:confidenceScore a owl:DatatypeProperty ;
    rdfs:domain aekg:EntityAlignment ; rdfs:range xsd:decimal .

4.2 SHACL Validation Shapes (Euro 7 & Provenance Gatekeeper)

Every ETL pipeline and Catena-X partner ingestion must pass pySHACL / GraphDB SHACL validation prior to graph commit:

Code snippet
@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix aekg: <https://w3id.org/autoecokg/ontology#> .
@prefix sosa: <http://www.w3.org/ns/sosa/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

aekg:TyreAbrasionObservationShape a sh:NodeShape ;
    sh:targetClass aekg:TyreAbrasionObservation ;
    sh:property [
        sh:path sosa:hasFeatureOfInterest ;
        sh:class aekg:TyreModel ;
        sh:minCount 1 ; sh:maxCount 1 ;
        sh:message "TyreAbrasionObservation must reference exactly one TyreModel."@en ;
    ] ;
    sh:property [
        sh:path aekg:abrasionLevelMgKmTonne ;
        sh:datatype xsd:decimal ;
        sh:minExclusive 0.0 ; sh:maxInclusive 500.0 ;
        sh:minCount 1 ;
        sh:message "Abrasion level (mg/km/t) must be within physically valid bounds (0, 500]."@en ;
    ] ;
    sh:property [
        sh:path aekg:referenceSRTT ;
        sh:class aekg:TyreModel ;
        sh:minCount 1 ;
        sh:message "UNECE WP.29 compliance requires linking the Standard Reference Test Tyre (SRTT17S/SRTT17W)."@en ;
    ] ;
    sh:property [
        sh:path sosa:usedProcedure ;
        sh:minCount 1 ;
        sh:message "Test method (on-road convoy or indoor drum) must be declared via sosa:usedProcedure."@en ;
    ] ;
    sh:property [
        sh:path prov:wasAttributedTo ;
        sh:minCount 1 ;
        sh:message "Every observation requires explicit PROV-O source attribution."@en ;
    ] .

aekg:BatteryDurabilityShape a sh:NodeShape ;
    sh:targetClass aekg:BatteryDurabilityObservation ;
    sh:property [
        sh:path aekg:batterySoHPercent ;
        sh:datatype xsd:decimal ;
        sh:minInclusive 0.0 ; sh:maxInclusive 100.0 ;
        sh:minCount 1 ;
    ] ;
    sh:property [
        sh:path aekg:milestoneYears ;
        sh:datatype xsd:integer ;
        sh:in ( 5 8 ) ;
        sh:severity sh:Warning ;
        sh:message "Euro 7 M1/N1 durability compliance milestones are defined at 5 years (100k km) and 8 years (160k km)."@en ;
    ] .

4.3 Sample Production SPARQL 1.1 Queries
Query 1: Three-Tier Epistemic Divergence (EEA WLTP vs. ADAC Ecotest vs. Spritmonitor)

Quantifies the real-world energy consumption gap across European BEV variants weighted by EEA registration volume, returning full provenance citations for GraphRAG synthesis.

Code snippet
PREFIX aekg: <https://w3id.org/autoecokg/ontology#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?modelName ?regCount
       ?wltpKwh ?adacKwh ?realWorldMeanKwh
       (ROUND(((?realWorldMeanKwh - ?wltpKwh) / ?wltpKwh) * 1000) / 10.0 AS ?realVsWltpGapPct)
       (ROUND(((?realWorldMeanKwh - ?adacKwh) / ?adacKwh) * 1000) / 10.0 AS ?realVsAdacGapPct)
       ?sampleSize ?eeaSource ?smSource
WHERE {
  ?vehicle a aekg:VehicleModelVariant ;
           rdfs:label ?modelName ;
           aekg:powertrainType "BEV" ;
           aekg:registrationCount ?regCount .

  # Tier 1: EEA WLTP Homologation Observation
  ?wltpObs a sosa:Observation ;
           sosa:hasFeatureOfInterest ?vehicle ;
           sosa:observedProperty aekg:ElectricEnergyConsumptionWLTP ;
           sosa:hasSimpleResult ?wltpKwh ;
           prov:wasAttributedTo ?eeaSource .

  # Tier 2: ADAC Ecotest Independent Measurement
  ?adacObs a sosa:Observation ;
           sosa:hasFeatureOfInterest ?vehicle ;
           sosa:observedProperty aekg:ElectricEnergyConsumptionADAC ;
           sosa:hasSimpleResult ?adacKwh .

  # Tier 3: Spritmonitor Crowdsourced Distribution (linked via verified EntityAlignment)
  ?alignment a aekg:EntityAlignment ;
             aekg:canonicalEntity ?vehicle ;
             aekg:externalEntity ?smVehicle ;
             aekg:confidenceScore ?conf .
  FILTER (?conf >= 0.90)

  ?smObs a aekg:RealWorldConsumptionDistribution ;
         sosa:hasFeatureOfInterest ?smVehicle ;
         aekg:meanValue ?realWorldMeanKwh ;
         aekg:sampleSize ?sampleSize ;
         prov:wasAttributedTo ?smSource .
  FILTER (?sampleSize >= 30 && ?regCount >= 5000)
}
ORDER BY DESC(?realVsWltpGapPct)
LIMIT 25

Query 2: Euro 7 Brake Dust Compliance & Annual Tyre Microplastic Load (Pillar 2)

Screens vehicle-tyre pairings against Euro 7 M1 brake 
PM
10
PM
10
	​

 limits (
3
 mg/km
3 mg/km BEV; 
7
 mg/km
7 mg/km ICE/HEV) and computes annual fleet-level tyre microplastic runoff (kg/yr) and airborne 
PM
10
PM
10
	​

 (g/yr) for a 100-vehicle fleet driving 
25,000
 km/yr
25,000 km/yr.

Code snippet
PREFIX aekg: <https://w3id.org/autoecokg/ontology#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?vehicleName ?powertrain ?tyreName ?abrasionLevel ?aiCT ?brakePM10 ?brakeCompliant
       (ROUND(?annualMicroplasticSoilWaterKg * 100) / 100.0 AS ?fleetSoilWaterMicroplasticsKgYr)
       (ROUND(?annualAirbornePM10Grams * 10) / 10.0 AS ?fleetAirborneTyrePM10GramsYr)
WHERE {
  BIND(100 AS ?fleetSize)
  BIND(25000 AS ?annualKmPerVehicle)

  ?cfg a aekg:VehicleTyreConfiguration ;
       aekg:hasVehicleVariant ?vehicle ;
       aekg:hasTyreModel ?tyre .

  ?vehicle rdfs:label ?vehicleName ;
           aekg:powertrainType ?powertrain ;
           aekg:massInRunningOrderKg ?massKg .
  ?tyre rdfs:label ?tyreName ;
        aekg:tyreClass "C1" .

  # Tyre Abrasion Observation (load-normalized mg/km/t)
  ?abrObs a aekg:TyreAbrasionObservation ;
          sosa:hasFeatureOfInterest ?tyre ;
          aekg:abrasionLevelMgKmTonne ?abrasionLevel ;
          aekg:abrasionIndexAICT ?aiCT ;
          aekg:airbornePM10Fraction ?alphaPM10 .

  # Brake Dust Observation (PM10 mg/km)
  ?brakeObs a aekg:BrakeDustObservation ;
            sosa:hasFeatureOfInterest ?vehicle ;
            aekg:brakePM10MgKm ?brakePM10 .

  # Euro 7 M1 Brake Dust Limit Logic (3 mg/km BEV, 7 mg/km ICE/HEV/PHEV)
  BIND(IF(?powertrain = "BEV", 3.0, 7.0) AS ?euro7BrakeLimit)
  BIND(?brakePM10 <= ?euro7BrakeLimit AS ?brakeCompliant)

  # Total vehicle tyre abrasion rate (mg/km) = abrasionLevel (mg/km/t) * vehicle mass (t)
  BIND(?abrasionLevel * (?massKg / 1000.0) AS ?vehAbrasionMgKm)
  # Convert mg -> kg (divide by 1e6) for soil/water microplastic fraction (1 - alpha)
  BIND((?vehAbrasionMgKm * (1.0 - ?alphaPM10) * ?annualKmPerVehicle * ?fleetSize) / 1000000.0
       AS ?annualMicroplasticSoilWaterKg)
  # Convert mg -> g (divide by 1e3) for airborne PM10 fraction
  BIND((?vehAbrasionMgKm * ?alphaPM10 * ?annualKmPerVehicle * ?fleetSize) / 1000.0
       AS ?annualAirbornePM10Grams)
}
ORDER BY ASC(?fleetSoilWaterMicroplasticsKgYr)

Query 3: Exact Pareto Skyline Query for Fleet Vehicle-Tyre Selection (Pillar 3)

Returns strictly non-dominated vehicle-tyre configurations across five criteria—maximizing wet safety and tread lifespan while minimizing tyre abrasion, rolling resistance, and 5-year TCO—using pure SPARQL 1.1 FILTER NOT EXISTS skyline semantics.

Code snippet
PREFIX aekg: <https://w3id.org/autoecokg/ontology#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?vehicleName ?tyreName ?safety ?abrasion ?lifespanKm ?rrc ?tcoEur
WHERE {
  ?cfg a aekg:VehicleTyreConfiguration ;
       aekg:hasVehicleVariant ?v ;
       aekg:hasTyreModel ?t ;
       aekg:predictedTreadLifespanKm ?lifespanKm ;
       aekg:hasTCOCalculation/aekg:fiveYearTCOEur ?tcoEur .

  ?v rdfs:label ?vehicleName ; aekg:segment "C-SUV" .
  ?t rdfs:label ?tyreName ;
     aekg:wetGripScore ?safety ;
     aekg:rollingResistanceCoeff ?rrc .
  ?abrObs a aekg:TyreAbrasionObservation ;
          sosa:hasFeatureOfInterest ?t ;
          aekg:abrasionLevelMgKmTonne ?abrasion .

  # Pareto Skyline condition: No alternative configuration ?cfg2 dominates ?cfg
  FILTER NOT EXISTS {
    ?cfg2 a aekg:VehicleTyreConfiguration ;
          aekg:hasVehicleVariant/aekg:segment "C-SUV" ;
          aekg:hasTyreModel ?t2 ;
          aekg:predictedTreadLifespanKm ?lifespan2 ;
          aekg:hasTCOCalculation/aekg:fiveYearTCOEur ?tco2 .
    ?t2 aekg:wetGripScore ?safety2 ;
        aekg:rollingResistanceCoeff ?rrc2 .
    ?abrObs2 a aekg:TyreAbrasionObservation ;
             sosa:hasFeatureOfInterest ?t2 ;
             aekg:abrasionLevelMgKmTonne ?abrasion2 .

    FILTER (
      ?safety2   >= ?safety     &&
      ?lifespan2 >= ?lifespanKm &&
      ?abrasion2 <= ?abrasion   &&
      ?rrc2      <= ?rrc        &&
      ?tco2      <= ?tcoEur     &&
      ( ?safety2 > ?safety || ?lifespan2 > ?lifespanKm ||
        ?abrasion2 < ?abrasion || ?rrc2 < ?rrc || ?tco2 < ?tcoEur )
    )
  }
}
ORDER BY ASC(?tcoEur)

Query 4: Federated Catena-X Battery LCA & COVESA VSS Euro 7 Durability Audit (Pillars 4 & 5)

Demonstrates cross-organizational sovereign federation via a Catena-X Knowledge Agent endpoint, joining live VSS fleet State-of-Health observations against Euro 7 5-year/100,000 km (
80
%
80%) thresholds and primary supplier cradle-to-gate battery PCFs.

Code snippet
PREFIX aekg: <https://w3id.org/autoecokg/ontology#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX cx:   <https://w3id.org/catenax/ontology/pcf#>

SELECT ?vehicleModel ?cathodeChem ?soh5yr ?euro7SoHCompliant
       ?batteryMfgCO2eKg ?supplierAgent ?vssObsURI
WHERE {
  # Local AutoEcoKG 2.0 Graph: Aggregated COVESA VSS Fleet Telemetry
  ?vssObsURI a aekg:BatteryDurabilityObservation ;
             sosa:hasFeatureOfInterest ?vehicle ;
             aekg:milestoneYears 5 ;
             aekg:batterySoHPercent ?soh5yr ;
             sosa:observedProperty ?prop .
  ?prop aekg:vssSignalPath "Vehicle.Powertrain.TractionBattery.StateOfHealth" .

  ?vehicle a aekg:VehicleModelVariant ;
           rdfs:label ?vehicleModel ;
           aekg:batteryPackPartId ?partId ;
           aekg:cathodeChemistry ?cathodeChem .

  BIND(?soh5yr >= 80.0 AS ?euro7SoHCompliant)

  # Sovereign Catena-X EDC / Knowledge Agent Federated Subquery
  SERVICE <https://edc-agent.catena-x.internal/sparql/pcf> {
    ?pcfEntity a cx:ProductCarbonFootprint ;
               cx:materialPartId ?partId ;
               cx:fossilGhgEmissionsKgCO2e ?batteryMfgCO2eKg ;
               prov:wasAttributedTo ?supplierAgent .
  }
}
ORDER BY DESC(?soh5yr)

5. Implementation Architecture & Phased Roadmap
5.1 Layered Production System Architecture
Plaintext
+=========================================================================================+
|  LAYER 6: CONSUMERS, GOVERNANCE & OBSERVABILITY                                         |
|  [Fleet TCO & Pareto UI]  [CSRD ESRS E1/E2 Auditor]  [GraphRAG Chat]  [AutoEcoBench CI] |
+=========================================================================================+
                                          ^
                                          | REST / GraphQL / SPARQL / JSON-LD
+=========================================================================================+
|  LAYER 5: NEURO-SYMBOLIC GRAPHRAG & ANALYTICS ENGINE                                    |
|  +------------------------------------------+  +--------------------------------------+ |
|  | Hybrid GraphRAG Pipeline                 |  | Domain Decision & Compliance Engines | |
|  | - Vector TBox/ABox Linker (Qdrant)       |  | - Euro 7 Compliance Evaluator        | |
|  | - Schema-Constrained Text2SPARQL LLM     |  | - Cradle-to-Grave Battery LCA Engine | |
|  | - AST + SHACL Verifier & Repair Loop     |  | - NSGA-II / TOPSIS Pareto Optimizer  | |
|  | - PROV-O Citation Binder (Zero-Halluc.)  |  | - CSRD ESRS E1/E2 XBRL/JSON Exporter | |
|  +------------------------------------------+  +--------------------------------------+ |
+=========================================================================================+
                                          ^
                                          | SPARQL 1.1 / Cypher / SQL-OBDA
+=========================================================================================+
|  LAYER 4: FEDERATED SEMANTIC STORAGE & REASONING CORE                                   |
|  +----------------------------+  +------------------------+  +------------------------+ |
|  | Ontotext GraphDB Cluster   |  | Neo4j Enterprise (GDS) |  | Ontop OBDA Lakehouse   | |
|  | - OWL 2 RL/QL Reasoner     |<-| - n10s RDF Sync        |  | - Apache Parquet (EEA) | |
|  | - Native SHACL Gatekeeper  |  | - Fleet Graph Analytics|  | - TimescaleDB (VSS)    | |
|  | - Named Graphs & RDF-star  |  |                        |  | - R2RML Virtual Views  | |
|  +----------------------------+  +------------------------+  +------------------------+ |
+=========================================================================================+
                                          ^
                                          | Validated RDF / SAMM Aspect Streams
+=========================================================================================+
|  LAYER 3: ETL, ENTITY RESOLUTION & QUALITY PIPELINE                                     |
|  [RML / YARRRML Mapper] -> [Splink Probabilistic ER] -> [pySHACL / ROBOT Quality Gate]  |
+=========================================================================================+
                                          ^
+=========================================================================================+
|  LAYER 2: STANDARDS & DATASPACE CONNECTIVITY                                            |
|  [COVESA VSS Kafka/Flink Stream Aggregator]   [Catena-X Tractus-X EDC + AAS/SAMM Agent] |
+=========================================================================================+
                                          ^
+=========================================================================================+
|  LAYER 1: HETEROGENEOUS DATA SOURCES                                                    |
|  [EEA Registry >10M/yr] [ADAC Ecotest] [Spritmonitor] [TÜV Reports] [OEM EVP / OEM PCF] |
+=========================================================================================+

5.2 Phased Implementation Roadmap (18 Months)
Phase & Timeline	Core Deliverables	Key Engineering Activities	Quantitative Exit Criteria
Phase 1: Scale-Up & Semantic Backbone (Months 1–4)	AutoEcoKG 2.0 Core Ontology (v2.0); GraphDB + Ontop OBDA cluster; EEA, Spritmonitor & TÜV ingestion	Migrate 26,822 legacy triples; automate RML/YARRRML pipelines; deploy Splink probabilistic ER across EEA/ADAC/Spritmonitor; integrate pySHACL & ROBOT into GitLab/GitHub CI	
>10M annual EEA rows virtualized & canonically aggregated; ER precision 
≥96%; 37/37 legacy CQs passing; 0 SHACL errors
Phase 2: Euro 7 & LCA Compliance Core (Months 5–9)	Non-Exhaust Particulate Engine (Tyre Abrasion & Brake 
PM
10
	​

); EV Battery Durability & Cradle-to-Grave LCA module	Implement UNECE ECE/TRANS/WP.29/2026/138 SRTT/
AI
CT
	​

 schema; ingest Euro 7 EVP specs & brake 
PM
10
	​

 curves; connect ecoinvent/GREET LCA factors + EU grid intensities	100% automated Euro 7 M1/N1 compliance screening; validated microplastic mass-balance equations; full ISO 14040/44 provenance tracking
Phase 3: Fleet Pareto TCO, CSRD & GraphRAG (Months 10–14)	5-Objective Pareto TCO Optimizer; CSRD ESRS E1/E2 Report Generator; Production Neuro-Symbolic GraphRAG	Build NSGA-II/skyline optimizer + TOPSIS UI; map graph KPIs to ESRS E1 & E2-4/E2-5 schemas; retire 8 rigid templates; deploy Text2SPARQL + AST verifier + AutoEcoBench 2.0 (150+ CQs)	Text2SPARQL Execution Accuracy 
≥92% on AutoEcoBench 2.0; 
100% provenance citation faithfulness; 
<3s P95 Pareto query latency
Phase 4: COVESA VSS, Catena-X & Enterprise GA (Months 15–18)	COVESA VSS Telemetry Bridge; Catena-X SAMM/AAS/EDC Federation; Enterprise Multi-Tenant Release	Deploy Kafka/Flink VSSo aggregators; publish SAMM Aspect Models & AAS templates; configure Tractus-X EDC + ODRL usage policies & Knowledge Agent federation; SOC 2 / ISO 27001 hardening	Live federated SPARQL PCF/abrasion exchange across 
≥2 Catena-X pilot partners; 99.9% cluster SLA; external CSRD pilot audit sign-off
5.3 Risk Register & Architectural Mitigations
Risk Category	Specific Failure Mode	Concrete Technical Mitigation
Triple Bloat & Query Latency	Materializing 37M+ raw EEA rows or 10 Hz VSS telemetry collapses triple-store join performance	Enforce Canonical TVV aggregation in GraphDB; keep raw rows in Parquet/TimescaleDB behind Ontop OBDA; pre-aggregate VSS signals into monthly sosa:ObservationCollection summaries
Cross-Source Entity Mismatch	Erroneous owl:sameAs merges across European trim naming variants corrupt real-world divergence metrics	Replace owl:sameAs with reified aekg:EntityAlignment nodes carrying Splink confidence scores; enforce human-in-the-loop review for 
0.75≤σ<0.90 matches
LLM Hallucination in Text2SPARQL	Conversational AI invents non-existent predicates, drops provenance filters, or fabricates regulatory thresholds	Enforce grammar/schema-constrained decoding, mandatory AST/TBox static verification prior to execution, and strict zero-citation blocking (responses fail closed if numeric claims lack prov:Entity bindings)
Data Licensing & Privacy (GDPR)	Crowdsourced driver logs (Spritmonitor), proprietary test publishers (ADAC/TÜV), and VIN-linked VSS telemetry carry strict legal constraints	Strip all PII/VINs at ingestion edge (k-anonymity 
k≥15 for real-world cohorts); enforce ODRL usage policies inside Tractus-X EDC and named-graph RBAC in GraphDB so licensed commercial feeds never leak into public exports
Regulatory Drift (C2/C3 & Phase 2 Limits)	UNECE WP.29 updates to C2/C3 tyre abrasion thresholds (2030–2034) or Euro 7 delegated acts invalidate hardcoded rules	Externalize all regulatory limits as versioned, time-stamped OWL/SHACL Policy Graphs (aekg:effectiveFrom, aekg:supersededBy), enabling historical back-testing and seamless rule updates without code redeployment

By grounding every real-world observation, regulatory threshold, lifecycle inventory factor, and Pareto trade-off in W3C SOSA, PROV-O, SHACL, COVESA VSS, and Catena-X SAMM standards, AutoEcoKG 2.0 establishes a verifiable semantic infrastructure capable of bridging European environmental law, automotive engineering, and corporate climate accountability at continental scale.

---

AutoEcoKG 2.0: Technical Blueprint & Implementation Roadmap

A Real-World Automotive & Environmental Knowledge Graph for Euro 7 Compliance, Non-Exhaust Microplastic Modeling, Fleet TCO, and Sovereign Data Spaces

1. Executive Summary & Problem Formulation

Automotive environmental assessment faces a structural epistemic crisis at the exact moment European emissions regulation expands beyond the tailpipe. With Regulation (EU) 2024/1257 (Euro 7) entering mandatory application for new M1 passenger car and N1 light commercial vehicle type approvals on 29 November 2026 (and all newly registered M1/N1 vehicles on 29 November 2027), regulators, OEMs, tyre manufacturers, and corporate fleet operators can no longer rely on isolated laboratory homologation figures. Existing environmental data remains fragmented across three structurally incompatible evidentiary regimes: declared laboratory homologation (WLTP), independent standardized consumer and technical testing (ADAC Ecotest, UNECE tyre test protocols), and uncontrolled real-world operational telemetry (OBFCM, crowdsourced consumption platforms, and periodic technical inspections).

AutoEcoKG 2.0 resolves this fragmentation by evolving the AutoEcoKG 1.0 prototype (26,822 RDF triples) into a federated, provenance-preserving, enterprise-grade Semantic Knowledge Graph. It unifies >10 million annual European vehicle registrations, crowdsourced real-world energy consumption, multi-year mechanical durability curves, Euro 7 non-exhaust particulate emissions (tyre abrasion microplastics and brake dust 
PM
10
PM
10
	​

), cradle-to-grave EV battery Life Cycle Assessment (LCA), and CSRD (ESRS E1/E2) fleet sustainability reporting within a single standards-aligned architecture.

1.1 The Three-Tier Epistemic Gap
Evidentiary Tier	Representative Sources	Primary Metrics	Systemic Bias & Blind Spots	AutoEcoKG 2.0 Epistemic Role
Tier 1: Laboratory Homologation	EEA 
CO
2
	​

 Monitoring Registry (Reg. (EU) 2019/631), CoC, WLTP, UNECE R117	Declared 
CO
2
	​

 (
g/km), WLTP energy (
kWh/100 km), curb mass, nominal rolling resistance	Standardized ambient temperature (
23
∘
C), optimized test tyres, zero auxiliary HVAC load, idealized gear/regen profiles	Canonical entity backbone & legal compliance baseline
Tier 2: Independent Standardized Testing	ADAC Ecotest, UNECE WP.29 C1 Drum/Convoy Tyre Tests, Euro NCAP	Standardized highway/cold-start emissions, wet/dry braking, tyre abrasion level (
mg/(km⋅t)), 
AI
CT
	​

	Limited model-year and trim coverage; fixed test fleet vehicles; controlled reference road surfaces	Empirical calibration bridge & independent verification anchor
Tier 3: Real-World Operational Conditions	Spritmonitor, OBFCM/OBM telemetry, TÜV Periodic Inspection Reports, COVESA VSS streams	Empirical fuel/energy distributions, seasonal winter penalties, multi-year component defect rates, live battery SoH	Driver self-selection bias, uncalibrated tyre pressure, heterogeneous road roughness and topography	Ground-truth operational distribution & lifecycle degradation layer
1.2 Formal Problem Formulation: Divergence & Non-Exhaust Microplastics

Let 
𝑉
V denote the set of canonical European vehicle configurations and 
𝑇
T the set of pneumatic tyre models (classes C1, C2, C3). For any vehicle-tyre pairing 
(
𝑣
,
𝑡
)
∈
𝑉
×
𝑇
(v,t)∈V×T operating under regime 
𝑟
∈
{
WLTP
,
ADAC
,
RealWorld
}
r∈{WLTP,ADAC,RealWorld}, we define an observation vector 
𝑦
(
𝑟
)
(
𝑣
,
𝑡
)
y
(r)
(v,t) anchored to explicit provenance metadata 
𝜋
𝑟
π
r
	​

. The homologation-to-reality divergence vector is formalized as:

𝛥
real-lab
(
𝑣
,
𝑡
)
=
𝐸
[
𝑦
(
RealWorld
)
(
𝑣
,
𝑡
)
]
−
𝑦
(
WLTP
)
(
𝑣
,
𝑡
)
Δ
real-lab
	​

(v,t)=E[y
(RealWorld)
(v,t)]−y
(WLTP)
(v,t)

Historically, policy focused exclusively on the tailpipe 
CO
2
CO
2
	​

 and 
NO
𝑥
NO
x
	​

 components of 
𝛥
real-lab
Δ
real-lab
	​

. However, powertrain electrification creates an emission-shifting paradox: battery electric vehicles (BEVs) eliminate tailpipe exhaust and substantially reduce friction-brake dust via regenerative braking, yet their elevated kerb mass (typically 
+
250
 to 
+
500
 kg
+250 to +500 kg over equivalent ICE platforms) and instantaneous peak torque amplify vehicle-induced tyre abrasion.

Under Regulation (EU) 2024/1257, tyre abrasion is recognized as the largest source of microplastics released into the environment. Following the formal metrology adopted in UNECE ECE/TRANS/WP.29/2026/138 for Class C1 passenger car tyres, AutoEcoKG 2.0 models tyre particulate generation across three coupled physical quantities:

Abrasion Rate (
𝑅
abr
R
abr
	​

): Total elastomeric and polymer mass lost per unit distance, expressed in 
mg/km
mg/km.

Load-Normalized Abrasion Level (
𝐿
abr
L
abr
	​

): Abrasion rate normalized to the vertical load 
𝑀
load
M
load
	​

 (in metric tonnes) carried by the tyre:

𝐿
abr
=
𝑅
abr
𝑀
load
[
mg
/
(
km
⋅
t
)
]
L
abr
	​

=
M
load
	​

R
abr
	​

	​

[mg/(km⋅t)]

Abrasion Index (
AI
CT
AI
CT
	​

): Dimensionless compliance ratio comparing the candidate tyre's abrasion level against the applicable ASTM Standard Reference Test Tyre (SRTT17S per ASTM F3676-24 for summer tyres; SRTT17W per ASTM F3675-24 for winter tyres):

AI
CT
=
𝐿
abr
(
Candidate
)
𝐿
abr
(
SRTT
)
AI
CT
	​

=
L
abr
	​

(SRTT)
L
abr
	​

(Candidate)
	​


To support both air quality health modeling and ecological microplastic accounting, total vehicle-level tyre mass loss 
𝐸
tyre,total
(
𝑣
,
𝑡
)
=
∑
𝑖
=
1
4
𝑅
abr
,
𝑖
E
tyre,total
	​

(v,t)=∑
i=1
4
	​

R
abr,i
	​

 is partitioned into environmental transport compartments via empirically parameterized emission fractions:

𝐸
PM
10
tyre
=
𝛼
PM
10
⋅
𝐸
tyre,total
,
𝐸
PM
2.5
tyre
=
𝛼
PM
2.5
⋅
𝐸
tyre,total
,
𝐸
runoff/soil
MP
=
(
1
−
𝛼
PM
10
)
⋅
𝐸
tyre,total
E
PM
10
	​

tyre
	​

=α
PM
10
	​

	​

⋅E
tyre,total
	​

,E
PM
2.5
	​

tyre
	​

=α
PM
2.5
	​

	​

⋅E
tyre,total
	​

,E
runoff/soil
MP
	​

=(1−α
PM
10
	​

	​

)⋅E
tyre,total
	​


where 
𝛼
PM
10
∈
[
0.01
,
0.10
]
α
PM
10
	​

	​

∈[0.01,0.10] captures the airborne respirable fraction of Tyre and Road Wear Particles (TRWP) and 
(
1
−
𝛼
PM
10
)
(1−α
PM
10
	​

	​

) captures coarse polymer microplastics depositing onto road surfaces, stormwater runoff, aquatic sediments, and roadside soils. AutoEcoKG 2.0 treats these coefficients as first-class, provenance-tracked graph entities rather than hardcoded constants, enabling transparent sensitivity analysis as empirical road-surface and wet-weather studies evolve.

2. Existing Baseline: AutoEcoKG 1.0 Architecture & Limitations

AutoEcoKG 1.0 established the semantic and validation foundations for cross-source automotive environmental reasoning. Its verified baseline architecture consists of four tightly coupled layers:

RDF Graph Footprint: 26,822 RDF triples encoded in standard W3C RDF 1.1 (Turtle serialization), representing curated vehicle trims, laboratory WLTP ratings, ADAC Ecotest scores, and initial tyre test records.

Ontology Backbone (SOSA & PROV-O): Measurement modeling adheres strictly to the W3C SOSA (Sensor, Observation, Sample, and Actuator) ontology—representing every test score, fuel consumption reading, and emission measurement as an immutable sosa:Observation linked to a sosa:FeatureOfInterest (vehicle or tyre), a sosa:ObservableProperty, and a sosa:Procedure. Data lineage is captured via W3C PROV-O (prov:Entity, prov:Activity, prov:Agent, prov:wasDerivedFrom), preventing silent conflation of laboratory versus independent test figures.

SHACL Structural Validation: Automated W3C SHACL shape graphs enforce schema conformance prior to graph ingestion, checking mandatory provenance links, numeric range boundaries, datatype integrity (xsd:decimal, xsd:gYear), and measurement unit presence.

Competency Question Benchmark: 37/37 benchmark competency questions (CQs) pass deterministic validation, executed via 8 rigid parameterized SPARQL query templates covering single-hop lookups, WLTP-vs-ADAC deltas, and basic ranking.

Structural Bottlenecks Driving the 2.0 Redesign
Architectural Dimension	AutoEcoKG 1.0 Baseline	AutoEcoKG 2.0 Target State	Engineering Driver
Data Scale & Ingestion	26,822 triples; manual batch scripts	
>150M virtualized/materialized triples; automated RML + OBDA pipelines	Ingesting EEA Registry (
>10M rows/yr), Spritmonitor, and TÜV multi-year datasets
Emission & Lifecycle Scope	Exhaust 
CO
2
	​

/pollutants & basic tyre ratings	Full Euro 7 non-exhaust (tyre abrasion 
mg/(km⋅t), brake 
PM
10
	​

), EV battery SoH, Cradle-to-Grave LCA	Mandatory Euro 7 enforcement (Nov 2026) and UNECE WP.29 C1 abrasion rules
Decision & ESG Analytics	Single-metric sorting	5-objective Pareto TCO optimizer + audit-ready CSRD ESRS E1/E2 generator	Enterprise fleet procurement & EU statutory sustainability assurance
Query Interface	8 rigid parameterized SPARQL templates	Neuro-symbolic GraphRAG with schema-constrained Text2SPARQL & provenance binding	Handling arbitrary ad-hoc, multi-hop analytical questions without template maintenance
Interoperability & Storage	Local RDF file / single-node store	COVESA VSS + Catena-X SAMM/AAS/EDC federation over GraphDB Enterprise + Neo4j GDS + Parquet OBDA	Sovereign OEM–supplier–fleet data exchange & horizontal query scalability
3. Five Pillars for Real-World Expansion
Pillar 1: Large-Scale European Fleet & Telemetry Integration

Scaling AutoEcoKG from 26,822 triples to pan-European coverage requires ingesting three heterogeneous macro-datasets without causing catastrophic triple bloat or entity fragmentation.

1.1 EEA European Vehicle Registry (
>
10
M
>10M Rows/Year)

Published annually under Regulation (EU) 2019/631, the European Environment Agency (EEA) passenger car and van 
CO
2
CO
2
	​

 monitoring registry tracks every new vehicle registered across EU Member States, exceeding 10 million annual records and 37 million cumulative rows since 2012. Materializing every individual registration row as full SOSA/PROV-O RDF (~30 triples/row) would generate 
>
1.1
 billion
>1.1 billion redundant triples.

AutoEcoKG 2.0 solves this via a Hybrid Canonical Aggregation & Virtualization Strategy:

Canonical Type-Variant-Version (TVV) Grouping: Raw EEA records are deterministically aggregated along (RegistrationYear, MemberState, Manufacturer, CommercialName, TypeApprovalNumber, Variant, Version, FuelType, FuelMode)—compressing tens of millions of registration rows into ~250K–400K unique technical vehicle variants while preserving exact fleet volume (aekg:registrationCount), mean/median/std of mass in running order (m), WLTP 
CO
2
CO
2
	​

 (Ewltp), electric energy consumption (z), and wheelbase/axle width.

OBDA Lakehouse Virtualization: Granular row-level EEA tables remain stored in partitioned Apache Parquet queried via DuckDB/PostgreSQL and exposed on demand as virtual RDF graphs through Ontop (OBDA) using R2RML mappings for deep statistical drill-downs.

1.2 Spritmonitor Crowdsourced Real-World Consumption

To bridge Tier 1 (EEA WLTP) and Tier 2 (ADAC Ecotest) with empirical driver behavior, AutoEcoKG 2.0 ingests aggregated Spritmonitor fuel and electric consumption profiles. Because crowdsourced entries contain noisy free-text trim names and outlier fuelings, ingestion applies:

Robust Statistical Profiling: Trimmed distributions (filtering the bottom/top 2.5% data-entry errors, requiring minimum sample size 
𝑁
≥
15
N≥15 vehicles and 
≥
5,000
 km
≥5,000 km logged per vehicle) storing aekg:meanValue, aekg:medianValue, aekg:p10Value, aekg:p90Value, aekg:sampleSize, and stratified sub-profiles for driving environment (urban/rural/Autobahn) and seasonality (summer vs. winter tyre penalty).

Probabilistic Entity Resolution (ER): Cross-source linking across EEA, ADAC, and Spritmonitor uses Fellegi-Sunter probabilistic record linkage (implemented via Splink) blocking on (Manufacturer, FuelType, ModelYear ± 1) and scoring on normalized model-name token similarity, engine displacement (
±
25
 cc
±25 cc), and rated power (
±
3
 kW
±3 kW). Every cross-source link is stored as a reified aekg:EntityAlignment with confidence score 
𝜎
∈
[
0
,
1
]
σ∈[0,1], preserving auditability rather than asserting blind owl:sameAs identity.

1.3 TÜV Periodic Technical Inspection Durability

Environmental impact cannot be separated from service life: a vehicle requiring premature suspension, brake, or structural replacement incurs substantial embodied carbon and TCO penalties. AutoEcoKG 2.0 models TÜV Report inspection cohorts across five standardized vehicle age brackets (2–3, 4–5, 6–7, 8–9, and 10–11 years), capturing:

Significant Defect Rate (aekg:significantDefectRate, EM-Quote %) and cohort average odometer mileage (aekg:meanCohortMileage).

Subsystem Failure Decomposition: Disaggregated failure propensities for chassis/axles/springs, brake discs/lines, and environmental/exhaust systems, quantifying how heavier EV and SUV platforms accelerate mechanical wear relative to lighter reference segments.

Pillar 2: Euro 7 Regulatory Compliance & Particulate Modeling

AutoEcoKG 2.0 embeds executable regulatory logic aligned with Regulation (EU) 2024/1257 (Euro 7) and UNECE WP.29 technical regulations, transforming the knowledge graph into an automated compliance engine.

Euro 7 / UNECE Compliance Domain	Mandatory Regulatory Threshold / Metric	Enforcement Timeline	Knowledge Graph Representation
Exhaust Particle Number (
PN
10
	​

)	Particle counting lowered from 
23 nm (
PN
23
	​

) to 
10 nm (
PN
10
	​

) for M1/N1; stricter heavy-duty 
NO
x
	​

 (
200 mg/kWh lab / 
260 mg/kWh RDE), 
N
2
	​

O, 
HCHO	29 Nov 2026 (new M1/N1 types); 29 Nov 2027 (all new M1/N1); May 2028/2029 (HDV)	aekg:ExhaustPN10Observation linked to RDE & WLTP sosa:Procedure
Brake Dust Emissions (
PM
10
	​

)	
3 mg/km (pure BEVs); 
7 mg/km (ICE, HEV, PHEV, FCEV cars); 
11 mg/km (large ICE N1 vans); uniform 
3 mg/km from 2035	29 Nov 2026 (new M1/N1 types); 29 Nov 2027 (all new M1/N1)	aekg:BrakeDustObservation parameterized by regen-braking fraction & WLTP-Brake cycle
Tyre Abrasion & Microplastics	Abrasion rate (
mg/km), load-normalized abrasion level (
mg/(km⋅t)), and Abrasion Index 
AI
CT
	​

 vs. SRTT17S/SRTT17W via on-road convoy or indoor drum test	C1: 1 Jul 2028 (new types) / 1 Jul 2030 (ban); C2: Apr 2030/2032; C3: Apr 2032/2034	aekg:TyreAbrasionObservation + aekg:MicroplasticEmissionFraction
EV/PHEV Battery Durability & Cold Range	Minimum State-of-Health (SoH): 
80% at 5 yr / 
100,000 km and 
72% at 8 yr / 
160,000 km (M1 cars); 
75% / 
67% (N1 vans); mandatory 
−7
∘
C winter range test	29 Nov 2026 (new M1/N1 types); 29 Nov 2027 (all new M1/N1)	aekg:BatteryDurabilityObservation, aekg:ColdRangeObservation
Digital Monitoring & Passports	Mandatory Environmental Vehicle Passport (EVP) at registration & continuous quantitative On-Board Monitoring (OBM) with anti-tampering integrity	Concurrent with Euro 7 M1/N1/HDV rollouts	aekg:EnvironmentalVehiclePassport + OBM telemetry streams
Cradle-to-Grave EV Battery & Vehicle LCA Sub-Graph

To prevent narrow operational optimization that obscures upstream manufacturing impacts, Pillar 2 implements an ISO 14040/14044 Cradle-to-Grave LCA ontology module decomposing total lifecycle Global Warming Potential (
GWP
100
GWP
100
	​

, in 
kg CO
2
e
kg CO
2
	​

e) into five traceable stages:

LCA
total
(
𝑣
)
=
𝐸
glider
+
𝐸
battery_mfg
(
𝑐
,
𝑄
,
𝑔
mfg
)
+
∫
0
𝐷
life
𝑒
use
(
𝑣
,
𝑥
,
𝑔
grid
(
𝑡
)
)
𝑑
𝑥
+
𝐸
maint
(
𝑣
,
T
U
¨
V
)
−
𝐶
EoL
(
𝑐
,
𝜂
rec
)
LCA
total
	​

(v)=E
glider
	​

+E
battery_mfg
	​

(c,Q,g
mfg
	​

)+∫
0
D
life
	​

	​

e
use
	​

(v,x,g
grid
	​

(t))dx+E
maint
	​

(v,T
U
¨
V)−C
EoL
	​

(c,η
rec
	​

)

Cathode Chemistry & Capacity Parameterization (
𝑐
,
𝑄
,
𝑔
mfg
c,Q,g
mfg
	​

): Explicitly distinguishes LFP, NMC622, NMC811, NCA, and Na-ion pack chemistries, nominal energy capacity 
𝑄
Q (
kWh
kWh), and cell manufacturing region grid carbon intensity 
𝑔
mfg
g
mfg
	​

 (
g CO
2
e/kWh
g CO
2
	​

e/kWh), ingesting Catena-X Product Carbon Footprints (PCFs) when primary supplier data is available and falling back to ecoinvent/GREET secondary factors with explicit aekg:DataQualityRating.

Dynamic Use-Phase & Maintenance Integration: Multiplies real-world Spritmonitor/OBFCM consumption against Member-State hourly or annual average grid carbon intensity 
𝑔
grid
(
𝑡
)
g
grid
	​

(t), adding replacement tyre embodied carbon (driven by tread lifespan) and battery second-life / hydrometallurgical recycling credits 
𝐶
EoL
C
EoL
	​

 aligned with the EU Battery Regulation (EU) 2023/1542.

Pillar 3: Fleet Total Cost of Ownership (TCO) & CSRD ESG Reporting
3.1 Multi-Criteria Pareto Decision Engine

Fleet procurement decisions rarely hinge on a single KPI. A low-rolling-resistance tyre that cuts BEV energy consumption may sacrifice wet-braking distance or increase abrasion mass loss. AutoEcoKG 2.0 exposes a Multi-Criteria Pareto Optimization Engine evaluating every valid vehicle-tyre pairing 
𝑥
=
(
𝑣
,
𝑡
)
∈
𝐹
x=(v,t)∈F (filtered by load index, speed rating, rim diameter, and Euro 7 compliance) across a 5-dimensional objective vector:

min
⁡
𝑥
∈
𝐹
𝐹
(
𝑥
)
=
[
−
𝑓
safety
(
𝑥
)
,
𝑓
abrasion
(
𝑥
)
,
−
𝑓
lifespan
(
𝑥
)
,
𝑓
RRC
(
𝑥
)
,
𝑓
TCO
(
𝑥
)
]
𝑇
x∈F
min
	​

F(x)=[−f
safety
	​

(x),f
abrasion
	​

(x),−f
lifespan
	​

(x),f
RRC
	​

(x),f
TCO
	​

(x)]
T

Safety Score (
𝑓
safety
f
safety
	​

, maximize): Composite of EU Tyre Label wet-grip class, ADAC wet/dry braking deceleration (
m/s
2
m/s
2
), aquaplaning resistance, and Euro NCAP adult/vulnerable-road-user ratings.

Tyre Abrasion & Microplastics (
𝑓
abrasion
f
abrasion
	​

, minimize): Vehicle-load-adjusted abrasion rate 
𝐸
tyre,total
(
𝑣
,
𝑡
)
E
tyre,total
	​

(v,t) in 
mg/km
mg/km and cumulative microplastic release (kg) over the fleet holding period 
𝐻
H.

Combined Lifespan & Durability (
𝑓
lifespan
f
lifespan
	​

, maximize): Predicted tyre tread life 
𝐷
tread
(
𝑣
,
𝑡
)
D
tread
	​

(v,t) (km to 
1.6
 mm
1.6 mm legal / 
3.0
 mm
3.0 mm fleet-safety threshold) paired with TÜV cohort mechanical durability index.

Rolling Resistance (
𝑓
RRC
f
RRC
	​

, minimize): Tyre Rolling Resistance Coefficient (
kg/t
kg/t) mapped via physics-based elasticity (
≈
1.5
–
2.0
%
≈1.5–2.0% real-world energy change per 
1
 kg/t
1 kg/t RRC shift) onto Spritmonitor baseline consumption.

5-Year Real-World Fleet TCO (
𝑓
TCO
f
TCO
	​

, minimize):

TCO
(
𝑣
,
𝑡
,
𝐻
,
𝐷
ann
)
=
CAPEX
(
𝑣
)
−
RV
(
𝑣
,
𝐻
,
SoH
)
+
∑
𝑦
=
1
𝐻
𝐶
energy
,
𝑦
+
𝐶
tyres
,
𝑦
+
𝐶
maint
,
𝑦
(
T
U
¨
V
)
+
𝐶
tax/CO
2
,
𝑦
(
1
+
𝑟
)
𝑦
TCO(v,t,H,D
ann
	​

)=CAPEX(v)−RV(v,H,SoH)+
y=1
∑
H
	​

(1+r)
y
C
energy,y
	​

+C
tyres,y
	​

+C
maint,y
	​

(T
U
¨
V)+C
tax/CO
2
	​

,y
	​

	​


where residual value 
RV
RV explicitly incorporates Euro 7 battery SoH retention curves and 
𝐶
tyres
,
𝑦
C
tyres,y
	​

 models exact replacement cadence 
⌈
(
𝐻
⋅
𝐷
ann
)
/
𝐷
tread
(
𝑣
,
𝑡
)
⌉
⌈(H⋅D
ann
	​

)/D
tread
	​

(v,t)⌉.

The engine first prunes dominated pairings via exact Pareto Skyline filtering (executed directly in SPARQL 1.1 or Neo4j/Python via NSGA-II for continuous fleet-mix allocation), then ranks the non-dominated frontier using configurable TOPSIS weights so corporate fleet managers can trade off cost, safety, and microplastic reduction transparently.

3.2 Audit-Grade CSRD (ESRS E1 & E2) Reporting Pipeline

Under the EU Corporate Sustainability Reporting Directive (CSRD), large enterprises must disclose auditable climate and pollution metrics across own operations and value chains. AutoEcoKG 2.0 automates machine-readable ESRS JSON-LD / ESEF-ready disclosures directly from graph queries:

ESRS E1 (Climate Change): Aggregates absolute energy consumption in MWh disaggregated by renewable vs. non-renewable fuels and electricity, alongside Scope 1 (owned ICE fleet real-world fuel combustion), Scope 2 (location- and market-based BEV charging), and Scope 3 (Cat. 1/2 embodied vehicle & tyre production, Cat. 3 well-to-tank energy, Cat. 11/12 leased fleet & end-of-life).

ESRS E2 (Pollution): Directly satisfies Disclosure Requirement E2-4 (pollution of air, water, and soil—quantifying 
NO
𝑥
NO
x
	​

, exhaust 
PN
10
PN
10
	​

, brake 
PM
10
PM
10
	​

, and tyre-derived microplastics partitioned into atmospheric vs. soil/water loads, together with the measurement methodology) and E2-5 (Substances of Concern and SVHCs such as 6PPD antioxidants, zinc oxide vulcanization activators, and PAHs in tyre tread compounds).

Assurance-Ready Provenance: Every reported KPI binds to its underlying prov:Activity, dataset version URI, emission-factor timestamp, and uncertainty interval, giving external CSRD auditors deterministic lineage from executive summary down to individual vehicle cohorts.

Pillar 4: Production GraphRAG & Conversational AI

AutoEcoKG 1.0 relied on 8 rigid parameterized SPARQL templates—adequate for fixed dashboards, but brittle against novel regulatory, fleet-planning, or cross-domain questions. AutoEcoKG 2.0 replaces static templates with a Neuro-Symbolic Hybrid GraphRAG Engine engineered for zero-hallucination analytical querying.

4.1 Five-Stage Neuro-Symbolic Query Pipeline

Ontology-Aware Schema & Entity Linking: Incoming natural language queries are embedded and matched against two vector indices (Qdrant / GraphDB Similarity Index): (a) a TBox Schema Index over OWL classes, properties, and SHACL definitions, and (b) an ABox Entity Index resolving colloquial references (e.g., "VW ID.4 Pro on Michelin e.Primacy" or "Euro 7 BEV brake limit") into canonical URIs.

Few-Shot Schema-Constrained Text2SPARQL: A domain-tuned LLM (e.g., Qwen/Llama/Gemini class via constrained decoding) receives the pruned relevant TBox subgraph, resolved entity URIs, and top-
𝑘
k structurally similar verified SPARQL exemplars to synthesize a SPARQL 1.1 query.

Static AST & SHACL Semantic Verification Gate: Before touching the triple store, a deterministic symbolic verifier parses the generated SPARQL AST (rdflib/Apache Jena), validating:

Read-only safety (blocking INSERT/DELETE/DROP injection and unbounded SERVICE calls).

Predicate domain/range consistency against the OWL TBox (catching hallucinated predicates or inverted triples).

Query complexity and timeout bounds (enforcing LIMIT and preventing Cartesian-product joins).

Iterative Self-Correction Loop: If static verification fails or execution yields an unexpected empty result set, the verifier extracts structured error diagnostics (e.g., "Property aekg:hasAbrasionRate attaches to aekg:TyreAbrasionObservation, not aekg:TyreModel"), triggers up to 
𝑁
=
3
N=3 targeted repair iterations, or gracefully falls back to an explicit calibrated abstention explaining the exact data gap.

Provenance-Bound Answer Synthesis: Query results are returned alongside mandatory provenance bindings (?sourceAgent, ?procedure, ?testDate, ?confidenceScore). The synthesis module generates natural language responses and structured tables where every numerical assertion carries an inline clickable citation to its graph prov:Entity URI.

4.2 AutoEcoBench 2.0 Evaluation Suite

The 37 CQs from AutoEcoKG 1.0 are preserved as a mandatory regression suite and expanded into AutoEcoBench 2.0 (150+ benchmark tasks) spanning five difficulty tiers:

Tier A (37 legacy CQs): Single/two-hop WLTP & ADAC lookups.

Tier B (35 CQs): EEA–Spritmonitor–TÜV real-world divergence & cohort aggregation.

Tier C (30 CQs): Euro 7 non-exhaust compliance, 
AI
CT
AI
CT
	​

, brake 
PM
10
PM
10
	​

, and EV battery durability.

Tier D (28 CQs): Multi-criteria Pareto TCO & CSRD ESRS E1/E2 rollup queries.

Tier E (20+ adversarial CQs): Out-of-scope or missing-data probes measuring Abstention Precision (target 
≥
98
%
≥98%), Execution Accuracy (EX) (target 
≥
92
%
≥92%), and Provenance Citation Faithfulness (target 
100
%
100%).

Pillar 5: Automotive Standards & Enterprise Deployment

To operate inside real European OEM, Tier-1 supplier, and fleet ecosystems rather than as an academic silo, AutoEcoKG 2.0 natively adopts two core automotive industry standards.

5.1 COVESA Vehicle Signal Specification (VSS) Alignment

The COVESA Vehicle Signal Specification (VSS) defines the industry-standard hierarchical tree for in-vehicle telemetry attributes, sensors, and actuators. AutoEcoKG 2.0 bridges live vehicle telemetry into the semantic graph via W3C VSSo (VSS Ontology) mappings:

Static attributes (e.g., Vehicle.VehicleIdentification.VIN, Vehicle.CurrentOverallWeight, Vehicle.Powertrain.TractionBattery.GrossCapacity) map to aekg:VehicleInstance properties.

Dynamic time-series signals (Vehicle.Powertrain.TractionBattery.StateOfHealth, Vehicle.Chassis.Axle.Row1.Wheel.Left.Tire.Pressure, Vehicle.OBD.Odometer, Vehicle.Powertrain.ElectricMotor.Power) map directly to sosa:ObservableProperty instances. High-frequency telemetry (1–100 Hz) is never dumped raw into RDF; instead, edge/cloud stream processors (Apache Kafka + Flink) compute rolling trip/monthly aggregations (e.g., mean regenerative braking ratio, winter Wh/km, quarterly SoH snapshots) and commit compact sosa:ObservationCollection summaries into the Knowledge Graph.

5.2 Catena-X Data Space Integration

For sovereign B2B exchange of primary supplier data (e.g., tyre compound SVHC declarations, laboratory drum abrasion reports, and battery cell Product Carbon Footprints), AutoEcoKG 2.0 aligns with the Catena-X Data Ecosystem across all three interoperability layers:

Semantic Interoperability: Core AutoEcoKG 2.0 modules are published as SAMM (Semantic Aspect Meta Model) Aspect Models (TTL/JSON-LD) and packaged inside Asset Administration Shells (AAS) for Digital Battery Passports, Tyre Environmental Passports, and PCF exchange.

Technical Interoperability: External partner graphs connect through Tractus-X Eclipse Dataspace Components (EDC) implementing the Data Spaces Protocol (DSP) and Decentralized Claims Protocol (DCP). Federated cross-company SPARQL queries execute through Catena-X Knowledge Agents (Binding Agents) without centralizing proprietary OEM or Tier-1 test databases.

Legal & Policy Interoperability: Usage control policies (ODRL contracts enforced by EDC) restrict how sensitive supplier abrasion or battery degradation data may be used (e.g., "permitted for CSRD ESRS E2 aggregation; prohibited for public model-level benchmarking"), preserving commercial confidentiality.

5.3 Scalable Enterprise Storage Architecture
Storage Tier	Recommended Engine	Workload Role	Scaling & Performance Strategy
Primary Semantic Core	Ontotext GraphDB Enterprise (Cluster)	Authoritative OWL 2 / RDF-star / SHACL triple store, SPARQL 1.1 federation, provenance graphs	High-availability Raft cluster; named-graph partitioning by source & year; built-in Lucene/vector connectors for GraphRAG
High-Speed Analytical Projection	Neo4j Enterprise (via n10s / Neosemantics)	Optional synchronized LPG projection for sub-second Graph Data Science (GDS) similarity, clustering, and fleet Pareto routing	Incremental CDC sync from GraphDB; dedicated read replicas for Fleet TCO SaaS UI
Cold Raw & Time-Series Lakehouse	Apache Parquet / TimescaleDB + Ontop OBDA	Raw 37M+ EEA registration rows, granular Spritmonitor refueling logs, and raw COVESA VSS telemetry streams	Columnar compression; virtualized via R2RML/Ontop only when deep row-level drill-down is requested
4. Concrete Ontology Extensions & Sample SPARQL 1.1 Queries
4.1 Modular Ontology Extensions (Turtle / OWL 2 + SOSA + PROV-O + SAMM/VSS)
Code snippet
@prefix aekg:  <https://w3id.org/autoecokg/ontology#> .
@prefix sosa:  <http://www.w3.org/ns/sosa/> .
@prefix prov:  <http://www.w3.org/ns/prov#> .
@prefix qudt:  <http://qudt.org/schema/qudt/> .
@prefix unit:  <http://qudt.org/vocab/unit/> .
@prefix owl:   <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix skos:  <http://www.w3.org/2004/02/skos/core#> .
@prefix vsso:  <https://github.com/w3c/vsso#> .
@prefix samm:  <urn:samm:org.eclipse.esmf.samm:meta-model:2.1.0#> .

<https://w3id.org/autoecokg/ontology/2.0> a owl:Ontology ;
    owl:versionIRI <https://w3id.org/autoecokg/ontology/2.0.0> ;
    rdfs:label "AutoEcoKG 2.0 Automotive & Environmental Ontology"@en ;
    owl:imports <http://www.w3.org/ns/sosa/> ,
                <http://www.w3.org/ns/prov-o#> .

# =====================================================================
# 1. CANONICAL FLEET, ENTITY ALIGNMENT & DURABILITY CLASSES (Pillar 1)
# =====================================================================

aekg:VehicleModelVariant a owl:Class ;
    rdfs:subClassOf sosa:FeatureOfInterest , prov:Entity ;
    rdfs:comment "Canonical EU Type-Variant-Version (TVV) vehicle specification aggregated from EEA CoC data."@en .

aekg:TyreModel a owl:Class ;
    rdfs:subClassOf sosa:FeatureOfInterest , prov:Entity ;
    rdfs:comment "Pneumatic tyre SKU classified under UNECE Class C1, C2, or C3."@en .

aekg:VehicleTyreConfiguration a owl:Class ;
    rdfs:subClassOf sosa:FeatureOfInterest ;
    rdfs:comment "Valid operational pairing of a VehicleModelVariant and TyreModel for compliance and Pareto TCO."@en .

aekg:RealWorldConsumptionDistribution a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "Statistically aggregated real-world fuel/energy consumption (e.g., Spritmonitor or OBFCM cohort)."@en .

aekg:TUVInspectionCohort a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "Age-bracketed periodic technical inspection (HU) defect rate and mileage cohort."@en .

aekg:EntityAlignment a owl:Class ;
    rdfs:subClassOf prov:Entity ;
    rdfs:comment "Probabilistic cross-dataset entity match with explicit linkage confidence score."@en .

# =====================================================================
# 2. EURO 7 NON-EXHAUST, BATTERY DURABILITY & LCA CLASSES (Pillar 2)
# =====================================================================

aekg:TyreAbrasionObservation a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "UNECE WP.29 / Euro 7 tyre abrasion measurement capturing rate (mg/km), level (mg/km/t), and AI_CT."@en .

aekg:BrakeDustObservation a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "Euro 7 WLTP-Brake PM10 mass emission observation (mg/km)."@en .

aekg:BatteryDurabilityObservation a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "EV/PHEV traction battery State-of-Health (SoH %) observation at milestone age/mileage."@en ;
    skos:relatedMatch vsso:TractionBatteryStateOfHealth .

aekg:EnvironmentalVehiclePassport a owl:Class ;
    rdfs:subClassOf prov:Entity ;
    rdfs:comment "Digital Euro 7 Environmental Vehicle Passport (EVP) aligned with Catena-X AAS/SAMM."@en .

aekg:LifecycleStageImpact a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "ISO 14040/14044 Cradle-to-Grave GWP100 impact for a specific lifecycle stage (Production, Use, EoL)."@en .

# =====================================================================
# 3. FLEET TCO & CSRD ESRS E1/E2 CLASSES (Pillar 3)
# =====================================================================

aekg:TCOCalculation a owl:Class ;
    rdfs:subClassOf prov:Entity ;
    rdfs:comment "Discounted multi-year Fleet Total Cost of Ownership calculation bound to operational parameters."@en .

aekg:ESRSE2PollutionDisclosure a owl:Class ;
    rdfs:subClassOf prov:Entity ;
    rdfs:comment "Audit-ready CSRD ESRS E2-4 / E2-5 air, soil, and water particulate/microplastic disclosure."@en .

# =====================================================================
# 4. CORE OBJECT & DATATYPE PROPERTIES
# =====================================================================

aekg:hasVehicleVariant a owl:ObjectProperty ;
    rdfs:domain aekg:VehicleTyreConfiguration ;
    rdfs:range aekg:VehicleModelVariant .

aekg:hasTyreModel a owl:ObjectProperty ;
    rdfs:domain aekg:VehicleTyreConfiguration ;
    rdfs:range aekg:TyreModel .

aekg:referenceSRTT a owl:ObjectProperty ;
    rdfs:domain aekg:TyreAbrasionObservation ;
    rdfs:range aekg:TyreModel ;
    rdfs:comment "Reference ASTM Standard Reference Test Tyre (SRTT17S or SRTT17W) used for AI_CT normalization."@en .

aekg:vssSignalPath a owl:DatatypeProperty ;
    rdfs:domain sosa:ObservableProperty ;
    rdfs:range xsd:string ;
    rdfs:comment "Canonical COVESA VSS dot-notation path (e.g., Vehicle.Powertrain.TractionBattery.StateOfHealth)."@en .

aekg:sammAspectUrn a owl:DatatypeProperty ;
    rdfs:domain owl:Class ;
    rdfs:range xsd:anyURI ;
    rdfs:comment "Corresponding Catena-X SAMM Aspect Model URN."@en .

aekg:abrasionRateMgKm a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreAbrasionObservation ; rdfs:range xsd:decimal .

aekg:abrasionLevelMgKmTonne a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreAbrasionObservation ; rdfs:range xsd:decimal .

aekg:abrasionIndexAICT a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreAbrasionObservation ; rdfs:range xsd:decimal .

aekg:airbornePM10Fraction a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreAbrasionObservation ; rdfs:range xsd:decimal .

aekg:brakePM10MgKm a owl:DatatypeProperty ;
    rdfs:domain aekg:BrakeDustObservation ; rdfs:range xsd:decimal .

aekg:batterySoHPercent a owl:DatatypeProperty ;
    rdfs:domain aekg:BatteryDurabilityObservation ; rdfs:range xsd:decimal .

aekg:milestoneYears a owl:DatatypeProperty ;
    rdfs:domain aekg:BatteryDurabilityObservation ; rdfs:range xsd:integer .

aekg:milestoneKm a owl:DatatypeProperty ;
    rdfs:domain aekg:BatteryDurabilityObservation ; rdfs:range xsd:integer .

aekg:wetGripScore a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreModel ; rdfs:range xsd:decimal .

aekg:rollingResistanceCoeff a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreModel ; rdfs:range xsd:decimal .

aekg:predictedTreadLifespanKm a owl:DatatypeProperty ;
    rdfs:domain aekg:VehicleTyreConfiguration ; rdfs:range xsd:integer .

aekg:fiveYearTCOEur a owl:DatatypeProperty ;
    rdfs:domain aekg:TCOCalculation ; rdfs:range xsd:decimal .

aekg:significantDefectRatePct a owl:DatatypeProperty ;
    rdfs:domain aekg:TUVInspectionCohort ; rdfs:range xsd:decimal .

aekg:confidenceScore a owl:DatatypeProperty ;
    rdfs:domain aekg:EntityAlignment ; rdfs:range xsd:decimal .

4.2 SHACL Validation Shapes (Euro 7 & Provenance Gatekeeper)

Every ETL pipeline and Catena-X partner ingestion must pass pySHACL / GraphDB SHACL validation prior to graph commit:

Code snippet
@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix aekg: <https://w3id.org/autoecokg/ontology#> .
@prefix sosa: <http://www.w3.org/ns/sosa/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

aekg:TyreAbrasionObservationShape a sh:NodeShape ;
    sh:targetClass aekg:TyreAbrasionObservation ;
    sh:property [
        sh:path sosa:hasFeatureOfInterest ;
        sh:class aekg:TyreModel ;
        sh:minCount 1 ; sh:maxCount 1 ;
        sh:message "TyreAbrasionObservation must reference exactly one TyreModel."@en ;
    ] ;
    sh:property [
        sh:path aekg:abrasionLevelMgKmTonne ;
        sh:datatype xsd:decimal ;
        sh:minExclusive 0.0 ; sh:maxInclusive 500.0 ;
        sh:minCount 1 ;
        sh:message "Abrasion level (mg/km/t) must be within physically valid bounds (0, 500]."@en ;
    ] ;
    sh:property [
        sh:path aekg:referenceSRTT ;
        sh:class aekg:TyreModel ;
        sh:minCount 1 ;
        sh:message "UNECE WP.29 compliance requires linking the Standard Reference Test Tyre (SRTT17S/SRTT17W)."@en ;
    ] ;
    sh:property [
        sh:path sosa:usedProcedure ;
        sh:minCount 1 ;
        sh:message "Test method (on-road convoy or indoor drum) must be declared via sosa:usedProcedure."@en ;
    ] ;
    sh:property [
        sh:path prov:wasAttributedTo ;
        sh:minCount 1 ;
        sh:message "Every observation requires explicit PROV-O source attribution."@en ;
    ] .

aekg:BatteryDurabilityShape a sh:NodeShape ;
    sh:targetClass aekg:BatteryDurabilityObservation ;
    sh:property [
        sh:path aekg:batterySoHPercent ;
        sh:datatype xsd:decimal ;
        sh:minInclusive 0.0 ; sh:maxInclusive 100.0 ;
        sh:minCount 1 ;
    ] ;
    sh:property [
        sh:path aekg:milestoneYears ;
        sh:datatype xsd:integer ;
        sh:in ( 5 8 ) ;
        sh:severity sh:Warning ;
        sh:message "Euro 7 M1/N1 durability compliance milestones are defined at 5 years (100k km) and 8 years (160k km)."@en ;
    ] .

4.3 Sample Production SPARQL 1.1 Queries
Query 1: Three-Tier Epistemic Divergence (EEA WLTP vs. ADAC Ecotest vs. Spritmonitor)

Quantifies the real-world energy consumption gap across European BEV variants weighted by EEA registration volume, returning full provenance citations for GraphRAG synthesis.

Code snippet
PREFIX aekg: <https://w3id.org/autoecokg/ontology#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?modelName ?regCount
       ?wltpKwh ?adacKwh ?realWorldMeanKwh
       (ROUND(((?realWorldMeanKwh - ?wltpKwh) / ?wltpKwh) * 1000) / 10.0 AS ?realVsWltpGapPct)
       (ROUND(((?realWorldMeanKwh - ?adacKwh) / ?adacKwh) * 1000) / 10.0 AS ?realVsAdacGapPct)
       ?sampleSize ?eeaSource ?smSource
WHERE {
  ?vehicle a aekg:VehicleModelVariant ;
           rdfs:label ?modelName ;
           aekg:powertrainType "BEV" ;
           aekg:registrationCount ?regCount .

  # Tier 1: EEA WLTP Homologation Observation
  ?wltpObs a sosa:Observation ;
           sosa:hasFeatureOfInterest ?vehicle ;
           sosa:observedProperty aekg:ElectricEnergyConsumptionWLTP ;
           sosa:hasSimpleResult ?wltpKwh ;
           prov:wasAttributedTo ?eeaSource .

  # Tier 2: ADAC Ecotest Independent Measurement
  ?adacObs a sosa:Observation ;
           sosa:hasFeatureOfInterest ?vehicle ;
           sosa:observedProperty aekg:ElectricEnergyConsumptionADAC ;
           sosa:hasSimpleResult ?adacKwh .

  # Tier 3: Spritmonitor Crowdsourced Distribution (linked via verified EntityAlignment)
  ?alignment a aekg:EntityAlignment ;
             aekg:canonicalEntity ?vehicle ;
             aekg:externalEntity ?smVehicle ;
             aekg:confidenceScore ?conf .
  FILTER (?conf >= 0.90)

  ?smObs a aekg:RealWorldConsumptionDistribution ;
         sosa:hasFeatureOfInterest ?smVehicle ;
         aekg:meanValue ?realWorldMeanKwh ;
         aekg:sampleSize ?sampleSize ;
         prov:wasAttributedTo ?smSource .
  FILTER (?sampleSize >= 30 && ?regCount >= 5000)
}
ORDER BY DESC(?realVsWltpGapPct)
LIMIT 25

Query 2: Euro 7 Brake Dust Compliance & Annual Tyre Microplastic Load (Pillar 2)

Screens vehicle-tyre pairings against Euro 7 M1 brake 
PM
10
PM
10
	​

 limits (
3
 mg/km
3 mg/km BEV; 
7
 mg/km
7 mg/km ICE/HEV) and computes annual fleet-level tyre microplastic runoff (kg/yr) and airborne 
PM
10
PM
10
	​

 (g/yr) for a 100-vehicle fleet driving 
25,000
 km/yr
25,000 km/yr.

Code snippet
PREFIX aekg: <https://w3id.org/autoecokg/ontology#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?vehicleName ?powertrain ?tyreName ?abrasionLevel ?aiCT ?brakePM10 ?brakeCompliant
       (ROUND(?annualMicroplasticSoilWaterKg * 100) / 100.0 AS ?fleetSoilWaterMicroplasticsKgYr)
       (ROUND(?annualAirbornePM10Grams * 10) / 10.0 AS ?fleetAirborneTyrePM10GramsYr)
WHERE {
  BIND(100 AS ?fleetSize)
  BIND(25000 AS ?annualKmPerVehicle)

  ?cfg a aekg:VehicleTyreConfiguration ;
       aekg:hasVehicleVariant ?vehicle ;
       aekg:hasTyreModel ?tyre .

  ?vehicle rdfs:label ?vehicleName ;
           aekg:powertrainType ?powertrain ;
           aekg:massInRunningOrderKg ?massKg .
  ?tyre rdfs:label ?tyreName ;
        aekg:tyreClass "C1" .

  # Tyre Abrasion Observation (load-normalized mg/km/t)
  ?abrObs a aekg:TyreAbrasionObservation ;
          sosa:hasFeatureOfInterest ?tyre ;
          aekg:abrasionLevelMgKmTonne ?abrasionLevel ;
          aekg:abrasionIndexAICT ?aiCT ;
          aekg:airbornePM10Fraction ?alphaPM10 .

  # Brake Dust Observation (PM10 mg/km)
  ?brakeObs a aekg:BrakeDustObservation ;
            sosa:hasFeatureOfInterest ?vehicle ;
            aekg:brakePM10MgKm ?brakePM10 .

  # Euro 7 M1 Brake Dust Limit Logic (3 mg/km BEV, 7 mg/km ICE/HEV/PHEV)
  BIND(IF(?powertrain = "BEV", 3.0, 7.0) AS ?euro7BrakeLimit)
  BIND(?brakePM10 <= ?euro7BrakeLimit AS ?brakeCompliant)

  # Total vehicle tyre abrasion rate (mg/km) = abrasionLevel (mg/km/t) * vehicle mass (t)
  BIND(?abrasionLevel * (?massKg / 1000.0) AS ?vehAbrasionMgKm)
  # Convert mg -> kg (divide by 1e6) for soil/water microplastic fraction (1 - alpha)
  BIND((?vehAbrasionMgKm * (1.0 - ?alphaPM10) * ?annualKmPerVehicle * ?fleetSize) / 1000000.0
       AS ?annualMicroplasticSoilWaterKg)
  # Convert mg -> g (divide by 1e3) for airborne PM10 fraction
  BIND((?vehAbrasionMgKm * ?alphaPM10 * ?annualKmPerVehicle * ?fleetSize) / 1000.0
       AS ?annualAirbornePM10Grams)
}
ORDER BY ASC(?fleetSoilWaterMicroplasticsKgYr)

Query 3: Exact Pareto Skyline Query for Fleet Vehicle-Tyre Selection (Pillar 3)

Returns strictly non-dominated vehicle-tyre configurations across five criteria—maximizing wet safety and tread lifespan while minimizing tyre abrasion, rolling resistance, and 5-year TCO—using pure SPARQL 1.1 FILTER NOT EXISTS skyline semantics.

Code snippet
PREFIX aekg: <https://w3id.org/autoecokg/ontology#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?vehicleName ?tyreName ?safety ?abrasion ?lifespanKm ?rrc ?tcoEur
WHERE {
  ?cfg a aekg:VehicleTyreConfiguration ;
       aekg:hasVehicleVariant ?v ;
       aekg:hasTyreModel ?t ;
       aekg:predictedTreadLifespanKm ?lifespanKm ;
       aekg:hasTCOCalculation/aekg:fiveYearTCOEur ?tcoEur .

  ?v rdfs:label ?vehicleName ; aekg:segment "C-SUV" .
  ?t rdfs:label ?tyreName ;
     aekg:wetGripScore ?safety ;
     aekg:rollingResistanceCoeff ?rrc .
  ?abrObs a aekg:TyreAbrasionObservation ;
          sosa:hasFeatureOfInterest ?t ;
          aekg:abrasionLevelMgKmTonne ?abrasion .

  # Pareto Skyline condition: No alternative configuration ?cfg2 dominates ?cfg
  FILTER NOT EXISTS {
    ?cfg2 a aekg:VehicleTyreConfiguration ;
          aekg:hasVehicleVariant/aekg:segment "C-SUV" ;
          aekg:hasTyreModel ?t2 ;
          aekg:predictedTreadLifespanKm ?lifespan2 ;
          aekg:hasTCOCalculation/aekg:fiveYearTCOEur ?tco2 .
    ?t2 aekg:wetGripScore ?safety2 ;
        aekg:rollingResistanceCoeff ?rrc2 .
    ?abrObs2 a aekg:TyreAbrasionObservation ;
             sosa:hasFeatureOfInterest ?t2 ;
             aekg:abrasionLevelMgKmTonne ?abrasion2 .

    FILTER (
      ?safety2   >= ?safety     &&
      ?lifespan2 >= ?lifespanKm &&
      ?abrasion2 <= ?abrasion   &&
      ?rrc2      <= ?rrc        &&
      ?tco2      <= ?tcoEur     &&
      ( ?safety2 > ?safety || ?lifespan2 > ?lifespanKm ||
        ?abrasion2 < ?abrasion || ?rrc2 < ?rrc || ?tco2 < ?tcoEur )
    )
  }
}
ORDER BY ASC(?tcoEur)

Query 4: Federated Catena-X Battery LCA & COVESA VSS Euro 7 Durability Audit (Pillars 4 & 5)

Demonstrates cross-organizational sovereign federation via a Catena-X Knowledge Agent endpoint, joining live VSS fleet State-of-Health observations against Euro 7 5-year/100,000 km (
80
%
80%) thresholds and primary supplier cradle-to-gate battery PCFs.

Code snippet
PREFIX aekg: <https://w3id.org/autoecokg/ontology#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX cx:   <https://w3id.org/catenax/ontology/pcf#>

SELECT ?vehicleModel ?cathodeChem ?soh5yr ?euro7SoHCompliant
       ?batteryMfgCO2eKg ?supplierAgent ?vssObsURI
WHERE {
  # Local AutoEcoKG 2.0 Graph: Aggregated COVESA VSS Fleet Telemetry
  ?vssObsURI a aekg:BatteryDurabilityObservation ;
             sosa:hasFeatureOfInterest ?vehicle ;
             aekg:milestoneYears 5 ;
             aekg:batterySoHPercent ?soh5yr ;
             sosa:observedProperty ?prop .
  ?prop aekg:vssSignalPath "Vehicle.Powertrain.TractionBattery.StateOfHealth" .

  ?vehicle a aekg:VehicleModelVariant ;
           rdfs:label ?vehicleModel ;
           aekg:batteryPackPartId ?partId ;
           aekg:cathodeChemistry ?cathodeChem .

  BIND(?soh5yr >= 80.0 AS ?euro7SoHCompliant)

  # Sovereign Catena-X EDC / Knowledge Agent Federated Subquery
  SERVICE <https://edc-agent.catena-x.internal/sparql/pcf> {
    ?pcfEntity a cx:ProductCarbonFootprint ;
               cx:materialPartId ?partId ;
               cx:fossilGhgEmissionsKgCO2e ?batteryMfgCO2eKg ;
               prov:wasAttributedTo ?supplierAgent .
  }
}
ORDER BY DESC(?soh5yr)

5. Implementation Architecture & Phased Roadmap
5.1 Layered Production System Architecture
Plaintext
+=========================================================================================+
|  LAYER 6: CONSUMERS, GOVERNANCE & OBSERVABILITY                                         |
|  [Fleet TCO & Pareto UI]  [CSRD ESRS E1/E2 Auditor]  [GraphRAG Chat]  [AutoEcoBench CI] |
+=========================================================================================+
                                          ^
                                          | REST / GraphQL / SPARQL / JSON-LD
+=========================================================================================+
|  LAYER 5: NEURO-SYMBOLIC GRAPHRAG & ANALYTICS ENGINE                                    |
|  +------------------------------------------+  +--------------------------------------+ |
|  | Hybrid GraphRAG Pipeline                 |  | Domain Decision & Compliance Engines | |
|  | - Vector TBox/ABox Linker (Qdrant)       |  | - Euro 7 Compliance Evaluator        | |
|  | - Schema-Constrained Text2SPARQL LLM     |  | - Cradle-to-Grave Battery LCA Engine | |
|  | - AST + SHACL Verifier & Repair Loop     |  | - NSGA-II / TOPSIS Pareto Optimizer  | |
|  | - PROV-O Citation Binder (Zero-Halluc.)  |  | - CSRD ESRS E1/E2 XBRL/JSON Exporter | |
|  +------------------------------------------+  +--------------------------------------+ |
+=========================================================================================+
                                          ^
                                          | SPARQL 1.1 / Cypher / SQL-OBDA
+=========================================================================================+
|  LAYER 4: FEDERATED SEMANTIC STORAGE & REASONING CORE                                   |
|  +----------------------------+  +------------------------+  +------------------------+ |
|  | Ontotext GraphDB Cluster   |  | Neo4j Enterprise (GDS) |  | Ontop OBDA Lakehouse   | |
|  | - OWL 2 RL/QL Reasoner     |<-| - n10s RDF Sync        |  | - Apache Parquet (EEA) | |
|  | - Native SHACL Gatekeeper  |  | - Fleet Graph Analytics|  | - TimescaleDB (VSS)    | |
|  | - Named Graphs & RDF-star  |  |                        |  | - R2RML Virtual Views  | |
|  +----------------------------+  +------------------------+  +------------------------+ |
+=========================================================================================+
                                          ^
                                          | Validated RDF / SAMM Aspect Streams
+=========================================================================================+
|  LAYER 3: ETL, ENTITY RESOLUTION & QUALITY PIPELINE                                     |
|  [RML / YARRRML Mapper] -> [Splink Probabilistic ER] -> [pySHACL / ROBOT Quality Gate]  |
+=========================================================================================+
                                          ^
+=========================================================================================+
|  LAYER 2: STANDARDS & DATASPACE CONNECTIVITY                                            |
|  [COVESA VSS Kafka/Flink Stream Aggregator]   [Catena-X Tractus-X EDC + AAS/SAMM Agent] |
+=========================================================================================+
                                          ^
+=========================================================================================+
|  LAYER 1: HETEROGENEOUS DATA SOURCES                                                    |
|  [EEA Registry >10M/yr] [ADAC Ecotest] [Spritmonitor] [TÜV Reports] [OEM EVP / OEM PCF] |
+=========================================================================================+

5.2 Phased Implementation Roadmap (18 Months)
Phase & Timeline	Core Deliverables	Key Engineering Activities	Quantitative Exit Criteria
Phase 1: Scale-Up & Semantic Backbone (Months 1–4)	AutoEcoKG 2.0 Core Ontology (v2.0); GraphDB + Ontop OBDA cluster; EEA, Spritmonitor & TÜV ingestion	Migrate 26,822 legacy triples; automate RML/YARRRML pipelines; deploy Splink probabilistic ER across EEA/ADAC/Spritmonitor; integrate pySHACL & ROBOT into GitLab/GitHub CI	
>10M annual EEA rows virtualized & canonically aggregated; ER precision 
≥96%; 37/37 legacy CQs passing; 0 SHACL errors
Phase 2: Euro 7 & LCA Compliance Core (Months 5–9)	Non-Exhaust Particulate Engine (Tyre Abrasion & Brake 
PM
10
	​

); EV Battery Durability & Cradle-to-Grave LCA module	Implement UNECE ECE/TRANS/WP.29/2026/138 SRTT/
AI
CT
	​

 schema; ingest Euro 7 EVP specs & brake 
PM
10
	​

 curves; connect ecoinvent/GREET LCA factors + EU grid intensities	100% automated Euro 7 M1/N1 compliance screening; validated microplastic mass-balance equations; full ISO 14040/44 provenance tracking
Phase 3: Fleet Pareto TCO, CSRD & GraphRAG (Months 10–14)	5-Objective Pareto TCO Optimizer; CSRD ESRS E1/E2 Report Generator; Production Neuro-Symbolic GraphRAG	Build NSGA-II/skyline optimizer + TOPSIS UI; map graph KPIs to ESRS E1 & E2-4/E2-5 schemas; retire 8 rigid templates; deploy Text2SPARQL + AST verifier + AutoEcoBench 2.0 (150+ CQs)	Text2SPARQL Execution Accuracy 
≥92% on AutoEcoBench 2.0; 
100% provenance citation faithfulness; 
<3s P95 Pareto query latency
Phase 4: COVESA VSS, Catena-X & Enterprise GA (Months 15–18)	COVESA VSS Telemetry Bridge; Catena-X SAMM/AAS/EDC Federation; Enterprise Multi-Tenant Release	Deploy Kafka/Flink VSSo aggregators; publish SAMM Aspect Models & AAS templates; configure Tractus-X EDC + ODRL usage policies & Knowledge Agent federation; SOC 2 / ISO 27001 hardening	Live federated SPARQL PCF/abrasion exchange across 
≥2 Catena-X pilot partners; 99.9% cluster SLA; external CSRD pilot audit sign-off
5.3 Risk Register & Architectural Mitigations
Risk Category	Specific Failure Mode	Concrete Technical Mitigation
Triple Bloat & Query Latency	Materializing 37M+ raw EEA rows or 10 Hz VSS telemetry collapses triple-store join performance	Enforce Canonical TVV aggregation in GraphDB; keep raw rows in Parquet/TimescaleDB behind Ontop OBDA; pre-aggregate VSS signals into monthly sosa:ObservationCollection summaries
Cross-Source Entity Mismatch	Erroneous owl:sameAs merges across European trim naming variants corrupt real-world divergence metrics	Replace owl:sameAs with reified aekg:EntityAlignment nodes carrying Splink confidence scores; enforce human-in-the-loop review for 
0.75≤σ<0.90 matches
LLM Hallucination in Text2SPARQL	Conversational AI invents non-existent predicates, drops provenance filters, or fabricates regulatory thresholds	Enforce grammar/schema-constrained decoding, mandatory AST/TBox static verification prior to execution, and strict zero-citation blocking (responses fail closed if numeric claims lack prov:Entity bindings)
Data Licensing & Privacy (GDPR)	Crowdsourced driver logs (Spritmonitor), proprietary test publishers (ADAC/TÜV), and VIN-linked VSS telemetry carry strict legal constraints	Strip all PII/VINs at ingestion edge (k-anonymity 
k≥15 for real-world cohorts); enforce ODRL usage policies inside Tractus-X EDC and named-graph RBAC in GraphDB so licensed commercial feeds never leak into public exports
Regulatory Drift (C2/C3 & Phase 2 Limits)	UNECE WP.29 updates to C2/C3 tyre abrasion thresholds (2030–2034) or Euro 7 delegated acts invalidate hardcoded rules	Externalize all regulatory limits as versioned, time-stamped OWL/SHACL Policy Graphs (aekg:effectiveFrom, aekg:supersededBy), enabling historical back-testing and seamless rule updates without code redeployment

By grounding every real-world observation, regulatory threshold, lifecycle inventory factor, and Pareto trade-off in W3C SOSA, PROV-O, SHACL, COVESA VSS, and Catena-X SAMM standards, AutoEcoKG 2.0 establishes a verifiable semantic infrastructure capable of bridging European environmental law, automotive engineering, and corporate climate accountability at continental scale.

---

AutoEcoKG 2.0: Technical Blueprint & Implementation Roadmap

A Real-World Automotive & Environmental Knowledge Graph for Euro 7 Compliance, Non-Exhaust Microplastic Modeling, Fleet TCO, and Sovereign Data Spaces

1. Executive Summary & Problem Formulation

Automotive environmental assessment faces a structural epistemic crisis at the exact moment European emissions regulation expands beyond the tailpipe. With Regulation (EU) 2024/1257 (Euro 7) entering mandatory application for new M1 passenger car and N1 light commercial vehicle type approvals on 29 November 2026 (and all newly registered M1/N1 vehicles on 29 November 2027), regulators, OEMs, tyre manufacturers, and corporate fleet operators can no longer rely on isolated laboratory homologation figures. Existing environmental data remains fragmented across three structurally incompatible evidentiary regimes: declared laboratory homologation (WLTP), independent standardized consumer and technical testing (ADAC Ecotest, UNECE tyre test protocols), and uncontrolled real-world operational telemetry (OBFCM, crowdsourced consumption platforms, and periodic technical inspections).

AutoEcoKG 2.0 resolves this fragmentation by evolving the AutoEcoKG 1.0 prototype (26,822 RDF triples) into a federated, provenance-preserving, enterprise-grade Semantic Knowledge Graph. It unifies >10 million annual European vehicle registrations, crowdsourced real-world energy consumption, multi-year mechanical durability curves, Euro 7 non-exhaust particulate emissions (tyre abrasion microplastics and brake dust 
PM
10
PM
10
	​

), cradle-to-grave EV battery Life Cycle Assessment (LCA), and CSRD (ESRS E1/E2) fleet sustainability reporting within a single standards-aligned architecture.

1.1 The Three-Tier Epistemic Gap
Evidentiary Tier	Representative Sources	Primary Metrics	Systemic Bias & Blind Spots	AutoEcoKG 2.0 Epistemic Role
Tier 1: Laboratory Homologation	EEA 
CO
2
	​

 Monitoring Registry (Reg. (EU) 2019/631), CoC, WLTP, UNECE R117	Declared 
CO
2
	​

 (
g/km), WLTP energy (
kWh/100 km), curb mass, nominal rolling resistance	Standardized ambient temperature (
23
∘
C), optimized test tyres, zero auxiliary HVAC load, idealized gear/regen profiles	Canonical entity backbone & legal compliance baseline
Tier 2: Independent Standardized Testing	ADAC Ecotest, UNECE WP.29 C1 Drum/Convoy Tyre Tests, Euro NCAP	Standardized highway/cold-start emissions, wet/dry braking, tyre abrasion level (
mg/(km⋅t)), 
AI
CT
	​

	Limited model-year and trim coverage; fixed test fleet vehicles; controlled reference road surfaces	Empirical calibration bridge & independent verification anchor
Tier 3: Real-World Operational Conditions	Spritmonitor, OBFCM/OBM telemetry, TÜV Periodic Inspection Reports, COVESA VSS streams	Empirical fuel/energy distributions, seasonal winter penalties, multi-year component defect rates, live battery SoH	Driver self-selection bias, uncalibrated tyre pressure, heterogeneous road roughness and topography	Ground-truth operational distribution & lifecycle degradation layer
1.2 Formal Problem Formulation: Divergence & Non-Exhaust Microplastics

Let 
𝑉
V denote the set of canonical European vehicle configurations and 
𝑇
T the set of pneumatic tyre models (classes C1, C2, C3). For any vehicle-tyre pairing 
(
𝑣
,
𝑡
)
∈
𝑉
×
𝑇
(v,t)∈V×T operating under regime 
𝑟
∈
{
WLTP
,
ADAC
,
RealWorld
}
r∈{WLTP,ADAC,RealWorld}, we define an observation vector 
𝑦
(
𝑟
)
(
𝑣
,
𝑡
)
y
(r)
(v,t) anchored to explicit provenance metadata 
𝜋
𝑟
π
r
	​

. The homologation-to-reality divergence vector is formalized as:

𝛥
real-lab
(
𝑣
,
𝑡
)
=
𝐸
[
𝑦
(
RealWorld
)
(
𝑣
,
𝑡
)
]
−
𝑦
(
WLTP
)
(
𝑣
,
𝑡
)
Δ
real-lab
	​

(v,t)=E[y
(RealWorld)
(v,t)]−y
(WLTP)
(v,t)

Historically, policy focused exclusively on the tailpipe 
CO
2
CO
2
	​

 and 
NO
𝑥
NO
x
	​

 components of 
𝛥
real-lab
Δ
real-lab
	​

. However, powertrain electrification creates an emission-shifting paradox: battery electric vehicles (BEVs) eliminate tailpipe exhaust and substantially reduce friction-brake dust via regenerative braking, yet their elevated kerb mass (typically 
+
250
 to 
+
500
 kg
+250 to +500 kg over equivalent ICE platforms) and instantaneous peak torque amplify vehicle-induced tyre abrasion.

Under Regulation (EU) 2024/1257, tyre abrasion is recognized as the largest source of microplastics released into the environment. Following the formal metrology adopted in UNECE ECE/TRANS/WP.29/2026/138 for Class C1 passenger car tyres, AutoEcoKG 2.0 models tyre particulate generation across three coupled physical quantities:

Abrasion Rate (
𝑅
abr
R
abr
	​

): Total elastomeric and polymer mass lost per unit distance, expressed in 
mg/km
mg/km.

Load-Normalized Abrasion Level (
𝐿
abr
L
abr
	​

): Abrasion rate normalized to the vertical load 
𝑀
load
M
load
	​

 (in metric tonnes) carried by the tyre:

𝐿
abr
=
𝑅
abr
𝑀
load
[
mg
/
(
km
⋅
t
)
]
L
abr
	​

=
M
load
	​

R
abr
	​

	​

[mg/(km⋅t)]

Abrasion Index (
AI
CT
AI
CT
	​

): Dimensionless compliance ratio comparing the candidate tyre's abrasion level against the applicable ASTM Standard Reference Test Tyre (SRTT17S per ASTM F3676-24 for summer tyres; SRTT17W per ASTM F3675-24 for winter tyres):

AI
CT
=
𝐿
abr
(
Candidate
)
𝐿
abr
(
SRTT
)
AI
CT
	​

=
L
abr
	​

(SRTT)
L
abr
	​

(Candidate)
	​


To support both air quality health modeling and ecological microplastic accounting, total vehicle-level tyre mass loss 
𝐸
tyre,total
(
𝑣
,
𝑡
)
=
∑
𝑖
=
1
4
𝑅
abr
,
𝑖
E
tyre,total
	​

(v,t)=∑
i=1
4
	​

R
abr,i
	​

 is partitioned into environmental transport compartments via empirically parameterized emission fractions:

𝐸
PM
10
tyre
=
𝛼
PM
10
⋅
𝐸
tyre,total
,
𝐸
PM
2.5
tyre
=
𝛼
PM
2.5
⋅
𝐸
tyre,total
,
𝐸
runoff/soil
MP
=
(
1
−
𝛼
PM
10
)
⋅
𝐸
tyre,total
E
PM
10
	​

tyre
	​

=α
PM
10
	​

	​

⋅E
tyre,total
	​

,E
PM
2.5
	​

tyre
	​

=α
PM
2.5
	​

	​

⋅E
tyre,total
	​

,E
runoff/soil
MP
	​

=(1−α
PM
10
	​

	​

)⋅E
tyre,total
	​


where 
𝛼
PM
10
∈
[
0.01
,
0.10
]
α
PM
10
	​

	​

∈[0.01,0.10] captures the airborne respirable fraction of Tyre and Road Wear Particles (TRWP) and 
(
1
−
𝛼
PM
10
)
(1−α
PM
10
	​

	​

) captures coarse polymer microplastics depositing onto road surfaces, stormwater runoff, aquatic sediments, and roadside soils. AutoEcoKG 2.0 treats these coefficients as first-class, provenance-tracked graph entities rather than hardcoded constants, enabling transparent sensitivity analysis as empirical road-surface and wet-weather studies evolve.

2. Existing Baseline: AutoEcoKG 1.0 Architecture & Limitations

AutoEcoKG 1.0 established the semantic and validation foundations for cross-source automotive environmental reasoning. Its verified baseline architecture consists of four tightly coupled layers:

RDF Graph Footprint: 26,822 RDF triples encoded in standard W3C RDF 1.1 (Turtle serialization), representing curated vehicle trims, laboratory WLTP ratings, ADAC Ecotest scores, and initial tyre test records.

Ontology Backbone (SOSA & PROV-O): Measurement modeling adheres strictly to the W3C SOSA (Sensor, Observation, Sample, and Actuator) ontology—representing every test score, fuel consumption reading, and emission measurement as an immutable sosa:Observation linked to a sosa:FeatureOfInterest (vehicle or tyre), a sosa:ObservableProperty, and a sosa:Procedure. Data lineage is captured via W3C PROV-O (prov:Entity, prov:Activity, prov:Agent, prov:wasDerivedFrom), preventing silent conflation of laboratory versus independent test figures.

SHACL Structural Validation: Automated W3C SHACL shape graphs enforce schema conformance prior to graph ingestion, checking mandatory provenance links, numeric range boundaries, datatype integrity (xsd:decimal, xsd:gYear), and measurement unit presence.

Competency Question Benchmark: 37/37 benchmark competency questions (CQs) pass deterministic validation, executed via 8 rigid parameterized SPARQL query templates covering single-hop lookups, WLTP-vs-ADAC deltas, and basic ranking.

Structural Bottlenecks Driving the 2.0 Redesign
Architectural Dimension	AutoEcoKG 1.0 Baseline	AutoEcoKG 2.0 Target State	Engineering Driver
Data Scale & Ingestion	26,822 triples; manual batch scripts	
>150M virtualized/materialized triples; automated RML + OBDA pipelines	Ingesting EEA Registry (
>10M rows/yr), Spritmonitor, and TÜV multi-year datasets
Emission & Lifecycle Scope	Exhaust 
CO
2
	​

/pollutants & basic tyre ratings	Full Euro 7 non-exhaust (tyre abrasion 
mg/(km⋅t), brake 
PM
10
	​

), EV battery SoH, Cradle-to-Grave LCA	Mandatory Euro 7 enforcement (Nov 2026) and UNECE WP.29 C1 abrasion rules
Decision & ESG Analytics	Single-metric sorting	5-objective Pareto TCO optimizer + audit-ready CSRD ESRS E1/E2 generator	Enterprise fleet procurement & EU statutory sustainability assurance
Query Interface	8 rigid parameterized SPARQL templates	Neuro-symbolic GraphRAG with schema-constrained Text2SPARQL & provenance binding	Handling arbitrary ad-hoc, multi-hop analytical questions without template maintenance
Interoperability & Storage	Local RDF file / single-node store	COVESA VSS + Catena-X SAMM/AAS/EDC federation over GraphDB Enterprise + Neo4j GDS + Parquet OBDA	Sovereign OEM–supplier–fleet data exchange & horizontal query scalability
3. Five Pillars for Real-World Expansion
Pillar 1: Large-Scale European Fleet & Telemetry Integration

Scaling AutoEcoKG from 26,822 triples to pan-European coverage requires ingesting three heterogeneous macro-datasets without causing catastrophic triple bloat or entity fragmentation.

1.1 EEA European Vehicle Registry (
>
10
M
>10M Rows/Year)

Published annually under Regulation (EU) 2019/631, the European Environment Agency (EEA) passenger car and van 
CO
2
CO
2
	​

 monitoring registry tracks every new vehicle registered across EU Member States, exceeding 10 million annual records and 37 million cumulative rows since 2012. Materializing every individual registration row as full SOSA/PROV-O RDF (~30 triples/row) would generate 
>
1.1
 billion
>1.1 billion redundant triples.

AutoEcoKG 2.0 solves this via a Hybrid Canonical Aggregation & Virtualization Strategy:

Canonical Type-Variant-Version (TVV) Grouping: Raw EEA records are deterministically aggregated along (RegistrationYear, MemberState, Manufacturer, CommercialName, TypeApprovalNumber, Variant, Version, FuelType, FuelMode)—compressing tens of millions of registration rows into ~250K–400K unique technical vehicle variants while preserving exact fleet volume (aekg:registrationCount), mean/median/std of mass in running order (m), WLTP 
CO
2
CO
2
	​

 (Ewltp), electric energy consumption (z), and wheelbase/axle width.

OBDA Lakehouse Virtualization: Granular row-level EEA tables remain stored in partitioned Apache Parquet queried via DuckDB/PostgreSQL and exposed on demand as virtual RDF graphs through Ontop (OBDA) using R2RML mappings for deep statistical drill-downs.

1.2 Spritmonitor Crowdsourced Real-World Consumption

To bridge Tier 1 (EEA WLTP) and Tier 2 (ADAC Ecotest) with empirical driver behavior, AutoEcoKG 2.0 ingests aggregated Spritmonitor fuel and electric consumption profiles. Because crowdsourced entries contain noisy free-text trim names and outlier fuelings, ingestion applies:

Robust Statistical Profiling: Trimmed distributions (filtering the bottom/top 2.5% data-entry errors, requiring minimum sample size 
𝑁
≥
15
N≥15 vehicles and 
≥
5,000
 km
≥5,000 km logged per vehicle) storing aekg:meanValue, aekg:medianValue, aekg:p10Value, aekg:p90Value, aekg:sampleSize, and stratified sub-profiles for driving environment (urban/rural/Autobahn) and seasonality (summer vs. winter tyre penalty).

Probabilistic Entity Resolution (ER): Cross-source linking across EEA, ADAC, and Spritmonitor uses Fellegi-Sunter probabilistic record linkage (implemented via Splink) blocking on (Manufacturer, FuelType, ModelYear ± 1) and scoring on normalized model-name token similarity, engine displacement (
±
25
 cc
±25 cc), and rated power (
±
3
 kW
±3 kW). Every cross-source link is stored as a reified aekg:EntityAlignment with confidence score 
𝜎
∈
[
0
,
1
]
σ∈[0,1], preserving auditability rather than asserting blind owl:sameAs identity.

1.3 TÜV Periodic Technical Inspection Durability

Environmental impact cannot be separated from service life: a vehicle requiring premature suspension, brake, or structural replacement incurs substantial embodied carbon and TCO penalties. AutoEcoKG 2.0 models TÜV Report inspection cohorts across five standardized vehicle age brackets (2–3, 4–5, 6–7, 8–9, and 10–11 years), capturing:

Significant Defect Rate (aekg:significantDefectRate, EM-Quote %) and cohort average odometer mileage (aekg:meanCohortMileage).

Subsystem Failure Decomposition: Disaggregated failure propensities for chassis/axles/springs, brake discs/lines, and environmental/exhaust systems, quantifying how heavier EV and SUV platforms accelerate mechanical wear relative to lighter reference segments.

Pillar 2: Euro 7 Regulatory Compliance & Particulate Modeling

AutoEcoKG 2.0 embeds executable regulatory logic aligned with Regulation (EU) 2024/1257 (Euro 7) and UNECE WP.29 technical regulations, transforming the knowledge graph into an automated compliance engine.

Euro 7 / UNECE Compliance Domain	Mandatory Regulatory Threshold / Metric	Enforcement Timeline	Knowledge Graph Representation
Exhaust Particle Number (
PN
10
	​

)	Particle counting lowered from 
23 nm (
PN
23
	​

) to 
10 nm (
PN
10
	​

) for M1/N1; stricter heavy-duty 
NO
x
	​

 (
200 mg/kWh lab / 
260 mg/kWh RDE), 
N
2
	​

O, 
HCHO	29 Nov 2026 (new M1/N1 types); 29 Nov 2027 (all new M1/N1); May 2028/2029 (HDV)	aekg:ExhaustPN10Observation linked to RDE & WLTP sosa:Procedure
Brake Dust Emissions (
PM
10
	​

)	
3 mg/km (pure BEVs); 
7 mg/km (ICE, HEV, PHEV, FCEV cars); 
11 mg/km (large ICE N1 vans); uniform 
3 mg/km from 2035	29 Nov 2026 (new M1/N1 types); 29 Nov 2027 (all new M1/N1)	aekg:BrakeDustObservation parameterized by regen-braking fraction & WLTP-Brake cycle
Tyre Abrasion & Microplastics	Abrasion rate (
mg/km), load-normalized abrasion level (
mg/(km⋅t)), and Abrasion Index 
AI
CT
	​

 vs. SRTT17S/SRTT17W via on-road convoy or indoor drum test	C1: 1 Jul 2028 (new types) / 1 Jul 2030 (ban); C2: Apr 2030/2032; C3: Apr 2032/2034	aekg:TyreAbrasionObservation + aekg:MicroplasticEmissionFraction
EV/PHEV Battery Durability & Cold Range	Minimum State-of-Health (SoH): 
80% at 5 yr / 
100,000 km and 
72% at 8 yr / 
160,000 km (M1 cars); 
75% / 
67% (N1 vans); mandatory 
−7
∘
C winter range test	29 Nov 2026 (new M1/N1 types); 29 Nov 2027 (all new M1/N1)	aekg:BatteryDurabilityObservation, aekg:ColdRangeObservation
Digital Monitoring & Passports	Mandatory Environmental Vehicle Passport (EVP) at registration & continuous quantitative On-Board Monitoring (OBM) with anti-tampering integrity	Concurrent with Euro 7 M1/N1/HDV rollouts	aekg:EnvironmentalVehiclePassport + OBM telemetry streams
Cradle-to-Grave EV Battery & Vehicle LCA Sub-Graph

To prevent narrow operational optimization that obscures upstream manufacturing impacts, Pillar 2 implements an ISO 14040/14044 Cradle-to-Grave LCA ontology module decomposing total lifecycle Global Warming Potential (
GWP
100
GWP
100
	​

, in 
kg CO
2
e
kg CO
2
	​

e) into five traceable stages:

LCA
total
(
𝑣
)
=
𝐸
glider
+
𝐸
battery_mfg
(
𝑐
,
𝑄
,
𝑔
mfg
)
+
∫
0
𝐷
life
𝑒
use
(
𝑣
,
𝑥
,
𝑔
grid
(
𝑡
)
)
𝑑
𝑥
+
𝐸
maint
(
𝑣
,
T
U
¨
V
)
−
𝐶
EoL
(
𝑐
,
𝜂
rec
)
LCA
total
	​

(v)=E
glider
	​

+E
battery_mfg
	​

(c,Q,g
mfg
	​

)+∫
0
D
life
	​

	​

e
use
	​

(v,x,g
grid
	​

(t))dx+E
maint
	​

(v,T
U
¨
V)−C
EoL
	​

(c,η
rec
	​

)

Cathode Chemistry & Capacity Parameterization (
𝑐
,
𝑄
,
𝑔
mfg
c,Q,g
mfg
	​

): Explicitly distinguishes LFP, NMC622, NMC811, NCA, and Na-ion pack chemistries, nominal energy capacity 
𝑄
Q (
kWh
kWh), and cell manufacturing region grid carbon intensity 
𝑔
mfg
g
mfg
	​

 (
g CO
2
e/kWh
g CO
2
	​

e/kWh), ingesting Catena-X Product Carbon Footprints (PCFs) when primary supplier data is available and falling back to ecoinvent/GREET secondary factors with explicit aekg:DataQualityRating.

Dynamic Use-Phase & Maintenance Integration: Multiplies real-world Spritmonitor/OBFCM consumption against Member-State hourly or annual average grid carbon intensity 
𝑔
grid
(
𝑡
)
g
grid
	​

(t), adding replacement tyre embodied carbon (driven by tread lifespan) and battery second-life / hydrometallurgical recycling credits 
𝐶
EoL
C
EoL
	​

 aligned with the EU Battery Regulation (EU) 2023/1542.

Pillar 3: Fleet Total Cost of Ownership (TCO) & CSRD ESG Reporting
3.1 Multi-Criteria Pareto Decision Engine

Fleet procurement decisions rarely hinge on a single KPI. A low-rolling-resistance tyre that cuts BEV energy consumption may sacrifice wet-braking distance or increase abrasion mass loss. AutoEcoKG 2.0 exposes a Multi-Criteria Pareto Optimization Engine evaluating every valid vehicle-tyre pairing 
𝑥
=
(
𝑣
,
𝑡
)
∈
𝐹
x=(v,t)∈F (filtered by load index, speed rating, rim diameter, and Euro 7 compliance) across a 5-dimensional objective vector:

min
⁡
𝑥
∈
𝐹
𝐹
(
𝑥
)
=
[
−
𝑓
safety
(
𝑥
)
,
𝑓
abrasion
(
𝑥
)
,
−
𝑓
lifespan
(
𝑥
)
,
𝑓
RRC
(
𝑥
)
,
𝑓
TCO
(
𝑥
)
]
𝑇
x∈F
min
	​

F(x)=[−f
safety
	​

(x),f
abrasion
	​

(x),−f
lifespan
	​

(x),f
RRC
	​

(x),f
TCO
	​

(x)]
T

Safety Score (
𝑓
safety
f
safety
	​

, maximize): Composite of EU Tyre Label wet-grip class, ADAC wet/dry braking deceleration (
m/s
2
m/s
2
), aquaplaning resistance, and Euro NCAP adult/vulnerable-road-user ratings.

Tyre Abrasion & Microplastics (
𝑓
abrasion
f
abrasion
	​

, minimize): Vehicle-load-adjusted abrasion rate 
𝐸
tyre,total
(
𝑣
,
𝑡
)
E
tyre,total
	​

(v,t) in 
mg/km
mg/km and cumulative microplastic release (kg) over the fleet holding period 
𝐻
H.

Combined Lifespan & Durability (
𝑓
lifespan
f
lifespan
	​

, maximize): Predicted tyre tread life 
𝐷
tread
(
𝑣
,
𝑡
)
D
tread
	​

(v,t) (km to 
1.6
 mm
1.6 mm legal / 
3.0
 mm
3.0 mm fleet-safety threshold) paired with TÜV cohort mechanical durability index.

Rolling Resistance (
𝑓
RRC
f
RRC
	​

, minimize): Tyre Rolling Resistance Coefficient (
kg/t
kg/t) mapped via physics-based elasticity (
≈
1.5
–
2.0
%
≈1.5–2.0% real-world energy change per 
1
 kg/t
1 kg/t RRC shift) onto Spritmonitor baseline consumption.

5-Year Real-World Fleet TCO (
𝑓
TCO
f
TCO
	​

, minimize):

TCO
(
𝑣
,
𝑡
,
𝐻
,
𝐷
ann
)
=
CAPEX
(
𝑣
)
−
RV
(
𝑣
,
𝐻
,
SoH
)
+
∑
𝑦
=
1
𝐻
𝐶
energy
,
𝑦
+
𝐶
tyres
,
𝑦
+
𝐶
maint
,
𝑦
(
T
U
¨
V
)
+
𝐶
tax/CO
2
,
𝑦
(
1
+
𝑟
)
𝑦
TCO(v,t,H,D
ann
	​

)=CAPEX(v)−RV(v,H,SoH)+
y=1
∑
H
	​

(1+r)
y
C
energy,y
	​

+C
tyres,y
	​

+C
maint,y
	​

(T
U
¨
V)+C
tax/CO
2
	​

,y
	​

	​


where residual value 
RV
RV explicitly incorporates Euro 7 battery SoH retention curves and 
𝐶
tyres
,
𝑦
C
tyres,y
	​

 models exact replacement cadence 
⌈
(
𝐻
⋅
𝐷
ann
)
/
𝐷
tread
(
𝑣
,
𝑡
)
⌉
⌈(H⋅D
ann
	​

)/D
tread
	​

(v,t)⌉.

The engine first prunes dominated pairings via exact Pareto Skyline filtering (executed directly in SPARQL 1.1 or Neo4j/Python via NSGA-II for continuous fleet-mix allocation), then ranks the non-dominated frontier using configurable TOPSIS weights so corporate fleet managers can trade off cost, safety, and microplastic reduction transparently.

3.2 Audit-Grade CSRD (ESRS E1 & E2) Reporting Pipeline

Under the EU Corporate Sustainability Reporting Directive (CSRD), large enterprises must disclose auditable climate and pollution metrics across own operations and value chains. AutoEcoKG 2.0 automates machine-readable ESRS JSON-LD / ESEF-ready disclosures directly from graph queries:

ESRS E1 (Climate Change): Aggregates absolute energy consumption in MWh disaggregated by renewable vs. non-renewable fuels and electricity, alongside Scope 1 (owned ICE fleet real-world fuel combustion), Scope 2 (location- and market-based BEV charging), and Scope 3 (Cat. 1/2 embodied vehicle & tyre production, Cat. 3 well-to-tank energy, Cat. 11/12 leased fleet & end-of-life).

ESRS E2 (Pollution): Directly satisfies Disclosure Requirement E2-4 (pollution of air, water, and soil—quantifying 
NO
𝑥
NO
x
	​

, exhaust 
PN
10
PN
10
	​

, brake 
PM
10
PM
10
	​

, and tyre-derived microplastics partitioned into atmospheric vs. soil/water loads, together with the measurement methodology) and E2-5 (Substances of Concern and SVHCs such as 6PPD antioxidants, zinc oxide vulcanization activators, and PAHs in tyre tread compounds).

Assurance-Ready Provenance: Every reported KPI binds to its underlying prov:Activity, dataset version URI, emission-factor timestamp, and uncertainty interval, giving external CSRD auditors deterministic lineage from executive summary down to individual vehicle cohorts.

Pillar 4: Production GraphRAG & Conversational AI

AutoEcoKG 1.0 relied on 8 rigid parameterized SPARQL templates—adequate for fixed dashboards, but brittle against novel regulatory, fleet-planning, or cross-domain questions. AutoEcoKG 2.0 replaces static templates with a Neuro-Symbolic Hybrid GraphRAG Engine engineered for zero-hallucination analytical querying.

4.1 Five-Stage Neuro-Symbolic Query Pipeline

Ontology-Aware Schema & Entity Linking: Incoming natural language queries are embedded and matched against two vector indices (Qdrant / GraphDB Similarity Index): (a) a TBox Schema Index over OWL classes, properties, and SHACL definitions, and (b) an ABox Entity Index resolving colloquial references (e.g., "VW ID.4 Pro on Michelin e.Primacy" or "Euro 7 BEV brake limit") into canonical URIs.

Few-Shot Schema-Constrained Text2SPARQL: A domain-tuned LLM (e.g., Qwen/Llama/Gemini class via constrained decoding) receives the pruned relevant TBox subgraph, resolved entity URIs, and top-
𝑘
k structurally similar verified SPARQL exemplars to synthesize a SPARQL 1.1 query.

Static AST & SHACL Semantic Verification Gate: Before touching the triple store, a deterministic symbolic verifier parses the generated SPARQL AST (rdflib/Apache Jena), validating:

Read-only safety (blocking INSERT/DELETE/DROP injection and unbounded SERVICE calls).

Predicate domain/range consistency against the OWL TBox (catching hallucinated predicates or inverted triples).

Query complexity and timeout bounds (enforcing LIMIT and preventing Cartesian-product joins).

Iterative Self-Correction Loop: If static verification fails or execution yields an unexpected empty result set, the verifier extracts structured error diagnostics (e.g., "Property aekg:hasAbrasionRate attaches to aekg:TyreAbrasionObservation, not aekg:TyreModel"), triggers up to 
𝑁
=
3
N=3 targeted repair iterations, or gracefully falls back to an explicit calibrated abstention explaining the exact data gap.

Provenance-Bound Answer Synthesis: Query results are returned alongside mandatory provenance bindings (?sourceAgent, ?procedure, ?testDate, ?confidenceScore). The synthesis module generates natural language responses and structured tables where every numerical assertion carries an inline clickable citation to its graph prov:Entity URI.

4.2 AutoEcoBench 2.0 Evaluation Suite

The 37 CQs from AutoEcoKG 1.0 are preserved as a mandatory regression suite and expanded into AutoEcoBench 2.0 (150+ benchmark tasks) spanning five difficulty tiers:

Tier A (37 legacy CQs): Single/two-hop WLTP & ADAC lookups.

Tier B (35 CQs): EEA–Spritmonitor–TÜV real-world divergence & cohort aggregation.

Tier C (30 CQs): Euro 7 non-exhaust compliance, 
AI
CT
AI
CT
	​

, brake 
PM
10
PM
10
	​

, and EV battery durability.

Tier D (28 CQs): Multi-criteria Pareto TCO & CSRD ESRS E1/E2 rollup queries.

Tier E (20+ adversarial CQs): Out-of-scope or missing-data probes measuring Abstention Precision (target 
≥
98
%
≥98%), Execution Accuracy (EX) (target 
≥
92
%
≥92%), and Provenance Citation Faithfulness (target 
100
%
100%).

Pillar 5: Automotive Standards & Enterprise Deployment

To operate inside real European OEM, Tier-1 supplier, and fleet ecosystems rather than as an academic silo, AutoEcoKG 2.0 natively adopts two core automotive industry standards.

5.1 COVESA Vehicle Signal Specification (VSS) Alignment

The COVESA Vehicle Signal Specification (VSS) defines the industry-standard hierarchical tree for in-vehicle telemetry attributes, sensors, and actuators. AutoEcoKG 2.0 bridges live vehicle telemetry into the semantic graph via W3C VSSo (VSS Ontology) mappings:

Static attributes (e.g., Vehicle.VehicleIdentification.VIN, Vehicle.CurrentOverallWeight, Vehicle.Powertrain.TractionBattery.GrossCapacity) map to aekg:VehicleInstance properties.

Dynamic time-series signals (Vehicle.Powertrain.TractionBattery.StateOfHealth, Vehicle.Chassis.Axle.Row1.Wheel.Left.Tire.Pressure, Vehicle.OBD.Odometer, Vehicle.Powertrain.ElectricMotor.Power) map directly to sosa:ObservableProperty instances. High-frequency telemetry (1–100 Hz) is never dumped raw into RDF; instead, edge/cloud stream processors (Apache Kafka + Flink) compute rolling trip/monthly aggregations (e.g., mean regenerative braking ratio, winter Wh/km, quarterly SoH snapshots) and commit compact sosa:ObservationCollection summaries into the Knowledge Graph.

5.2 Catena-X Data Space Integration

For sovereign B2B exchange of primary supplier data (e.g., tyre compound SVHC declarations, laboratory drum abrasion reports, and battery cell Product Carbon Footprints), AutoEcoKG 2.0 aligns with the Catena-X Data Ecosystem across all three interoperability layers:

Semantic Interoperability: Core AutoEcoKG 2.0 modules are published as SAMM (Semantic Aspect Meta Model) Aspect Models (TTL/JSON-LD) and packaged inside Asset Administration Shells (AAS) for Digital Battery Passports, Tyre Environmental Passports, and PCF exchange.

Technical Interoperability: External partner graphs connect through Tractus-X Eclipse Dataspace Components (EDC) implementing the Data Spaces Protocol (DSP) and Decentralized Claims Protocol (DCP). Federated cross-company SPARQL queries execute through Catena-X Knowledge Agents (Binding Agents) without centralizing proprietary OEM or Tier-1 test databases.

Legal & Policy Interoperability: Usage control policies (ODRL contracts enforced by EDC) restrict how sensitive supplier abrasion or battery degradation data may be used (e.g., "permitted for CSRD ESRS E2 aggregation; prohibited for public model-level benchmarking"), preserving commercial confidentiality.

5.3 Scalable Enterprise Storage Architecture
Storage Tier	Recommended Engine	Workload Role	Scaling & Performance Strategy
Primary Semantic Core	Ontotext GraphDB Enterprise (Cluster)	Authoritative OWL 2 / RDF-star / SHACL triple store, SPARQL 1.1 federation, provenance graphs	High-availability Raft cluster; named-graph partitioning by source & year; built-in Lucene/vector connectors for GraphRAG
High-Speed Analytical Projection	Neo4j Enterprise (via n10s / Neosemantics)	Optional synchronized LPG projection for sub-second Graph Data Science (GDS) similarity, clustering, and fleet Pareto routing	Incremental CDC sync from GraphDB; dedicated read replicas for Fleet TCO SaaS UI
Cold Raw & Time-Series Lakehouse	Apache Parquet / TimescaleDB + Ontop OBDA	Raw 37M+ EEA registration rows, granular Spritmonitor refueling logs, and raw COVESA VSS telemetry streams	Columnar compression; virtualized via R2RML/Ontop only when deep row-level drill-down is requested
4. Concrete Ontology Extensions & Sample SPARQL 1.1 Queries
4.1 Modular Ontology Extensions (Turtle / OWL 2 + SOSA + PROV-O + SAMM/VSS)
Code snippet
@prefix aekg:  <https://w3id.org/autoecokg/ontology#> .
@prefix sosa:  <http://www.w3.org/ns/sosa/> .
@prefix prov:  <http://www.w3.org/ns/prov#> .
@prefix qudt:  <http://qudt.org/schema/qudt/> .
@prefix unit:  <http://qudt.org/vocab/unit/> .
@prefix owl:   <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix skos:  <http://www.w3.org/2004/02/skos/core#> .
@prefix vsso:  <https://github.com/w3c/vsso#> .
@prefix samm:  <urn:samm:org.eclipse.esmf.samm:meta-model:2.1.0#> .

<https://w3id.org/autoecokg/ontology/2.0> a owl:Ontology ;
    owl:versionIRI <https://w3id.org/autoecokg/ontology/2.0.0> ;
    rdfs:label "AutoEcoKG 2.0 Automotive & Environmental Ontology"@en ;
    owl:imports <http://www.w3.org/ns/sosa/> ,
                <http://www.w3.org/ns/prov-o#> .

# =====================================================================
# 1. CANONICAL FLEET, ENTITY ALIGNMENT & DURABILITY CLASSES (Pillar 1)
# =====================================================================

aekg:VehicleModelVariant a owl:Class ;
    rdfs:subClassOf sosa:FeatureOfInterest , prov:Entity ;
    rdfs:comment "Canonical EU Type-Variant-Version (TVV) vehicle specification aggregated from EEA CoC data."@en .

aekg:TyreModel a owl:Class ;
    rdfs:subClassOf sosa:FeatureOfInterest , prov:Entity ;
    rdfs:comment "Pneumatic tyre SKU classified under UNECE Class C1, C2, or C3."@en .

aekg:VehicleTyreConfiguration a owl:Class ;
    rdfs:subClassOf sosa:FeatureOfInterest ;
    rdfs:comment "Valid operational pairing of a VehicleModelVariant and TyreModel for compliance and Pareto TCO."@en .

aekg:RealWorldConsumptionDistribution a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "Statistically aggregated real-world fuel/energy consumption (e.g., Spritmonitor or OBFCM cohort)."@en .

aekg:TUVInspectionCohort a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "Age-bracketed periodic technical inspection (HU) defect rate and mileage cohort."@en .

aekg:EntityAlignment a owl:Class ;
    rdfs:subClassOf prov:Entity ;
    rdfs:comment "Probabilistic cross-dataset entity match with explicit linkage confidence score."@en .

# =====================================================================
# 2. EURO 7 NON-EXHAUST, BATTERY DURABILITY & LCA CLASSES (Pillar 2)
# =====================================================================

aekg:TyreAbrasionObservation a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "UNECE WP.29 / Euro 7 tyre abrasion measurement capturing rate (mg/km), level (mg/km/t), and AI_CT."@en .

aekg:BrakeDustObservation a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "Euro 7 WLTP-Brake PM10 mass emission observation (mg/km)."@en .

aekg:BatteryDurabilityObservation a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "EV/PHEV traction battery State-of-Health (SoH %) observation at milestone age/mileage."@en ;
    skos:relatedMatch vsso:TractionBatteryStateOfHealth .

aekg:EnvironmentalVehiclePassport a owl:Class ;
    rdfs:subClassOf prov:Entity ;
    rdfs:comment "Digital Euro 7 Environmental Vehicle Passport (EVP) aligned with Catena-X AAS/SAMM."@en .

aekg:LifecycleStageImpact a owl:Class ;
    rdfs:subClassOf sosa:Observation , prov:Entity ;
    rdfs:comment "ISO 14040/14044 Cradle-to-Grave GWP100 impact for a specific lifecycle stage (Production, Use, EoL)."@en .

# =====================================================================
# 3. FLEET TCO & CSRD ESRS E1/E2 CLASSES (Pillar 3)
# =====================================================================

aekg:TCOCalculation a owl:Class ;
    rdfs:subClassOf prov:Entity ;
    rdfs:comment "Discounted multi-year Fleet Total Cost of Ownership calculation bound to operational parameters."@en .

aekg:ESRSE2PollutionDisclosure a owl:Class ;
    rdfs:subClassOf prov:Entity ;
    rdfs:comment "Audit-ready CSRD ESRS E2-4 / E2-5 air, soil, and water particulate/microplastic disclosure."@en .

# =====================================================================
# 4. CORE OBJECT & DATATYPE PROPERTIES
# =====================================================================

aekg:hasVehicleVariant a owl:ObjectProperty ;
    rdfs:domain aekg:VehicleTyreConfiguration ;
    rdfs:range aekg:VehicleModelVariant .

aekg:hasTyreModel a owl:ObjectProperty ;
    rdfs:domain aekg:VehicleTyreConfiguration ;
    rdfs:range aekg:TyreModel .

aekg:referenceSRTT a owl:ObjectProperty ;
    rdfs:domain aekg:TyreAbrasionObservation ;
    rdfs:range aekg:TyreModel ;
    rdfs:comment "Reference ASTM Standard Reference Test Tyre (SRTT17S or SRTT17W) used for AI_CT normalization."@en .

aekg:vssSignalPath a owl:DatatypeProperty ;
    rdfs:domain sosa:ObservableProperty ;
    rdfs:range xsd:string ;
    rdfs:comment "Canonical COVESA VSS dot-notation path (e.g., Vehicle.Powertrain.TractionBattery.StateOfHealth)."@en .

aekg:sammAspectUrn a owl:DatatypeProperty ;
    rdfs:domain owl:Class ;
    rdfs:range xsd:anyURI ;
    rdfs:comment "Corresponding Catena-X SAMM Aspect Model URN."@en .

aekg:abrasionRateMgKm a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreAbrasionObservation ; rdfs:range xsd:decimal .

aekg:abrasionLevelMgKmTonne a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreAbrasionObservation ; rdfs:range xsd:decimal .

aekg:abrasionIndexAICT a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreAbrasionObservation ; rdfs:range xsd:decimal .

aekg:airbornePM10Fraction a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreAbrasionObservation ; rdfs:range xsd:decimal .

aekg:brakePM10MgKm a owl:DatatypeProperty ;
    rdfs:domain aekg:BrakeDustObservation ; rdfs:range xsd:decimal .

aekg:batterySoHPercent a owl:DatatypeProperty ;
    rdfs:domain aekg:BatteryDurabilityObservation ; rdfs:range xsd:decimal .

aekg:milestoneYears a owl:DatatypeProperty ;
    rdfs:domain aekg:BatteryDurabilityObservation ; rdfs:range xsd:integer .

aekg:milestoneKm a owl:DatatypeProperty ;
    rdfs:domain aekg:BatteryDurabilityObservation ; rdfs:range xsd:integer .

aekg:wetGripScore a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreModel ; rdfs:range xsd:decimal .

aekg:rollingResistanceCoeff a owl:DatatypeProperty ;
    rdfs:domain aekg:TyreModel ; rdfs:range xsd:decimal .

aekg:predictedTreadLifespanKm a owl:DatatypeProperty ;
    rdfs:domain aekg:VehicleTyreConfiguration ; rdfs:range xsd:integer .

aekg:fiveYearTCOEur a owl:DatatypeProperty ;
    rdfs:domain aekg:TCOCalculation ; rdfs:range xsd:decimal .

aekg:significantDefectRatePct a owl:DatatypeProperty ;
    rdfs:domain aekg:TUVInspectionCohort ; rdfs:range xsd:decimal .

aekg:confidenceScore a owl:DatatypeProperty ;
    rdfs:domain aekg:EntityAlignment ; rdfs:range xsd:decimal .

4.2 SHACL Validation Shapes (Euro 7 & Provenance Gatekeeper)

Every ETL pipeline and Catena-X partner ingestion must pass pySHACL / GraphDB SHACL validation prior to graph commit:

Code snippet
@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix aekg: <https://w3id.org/autoecokg/ontology#> .
@prefix sosa: <http://www.w3.org/ns/sosa/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

aekg:TyreAbrasionObservationShape a sh:NodeShape ;
    sh:targetClass aekg:TyreAbrasionObservation ;
    sh:property [
        sh:path sosa:hasFeatureOfInterest ;
        sh:class aekg:TyreModel ;
        sh:minCount 1 ; sh:maxCount 1 ;
        sh:message "TyreAbrasionObservation must reference exactly one TyreModel."@en ;
    ] ;
    sh:property [
        sh:path aekg:abrasionLevelMgKmTonne ;
        sh:datatype xsd:decimal ;
        sh:minExclusive 0.0 ; sh:maxInclusive 500.0 ;
        sh:minCount 1 ;
        sh:message "Abrasion level (mg/km/t) must be within physically valid bounds (0, 500]."@en ;
    ] ;
    sh:property [
        sh:path aekg:referenceSRTT ;
        sh:class aekg:TyreModel ;
        sh:minCount 1 ;
        sh:message "UNECE WP.29 compliance requires linking the Standard Reference Test Tyre (SRTT17S/SRTT17W)."@en ;
    ] ;
    sh:property [
        sh:path sosa:usedProcedure ;
        sh:minCount 1 ;
        sh:message "Test method (on-road convoy or indoor drum) must be declared via sosa:usedProcedure."@en ;
    ] ;
    sh:property [
        sh:path prov:wasAttributedTo ;
        sh:minCount 1 ;
        sh:message "Every observation requires explicit PROV-O source attribution."@en ;
    ] .

aekg:BatteryDurabilityShape a sh:NodeShape ;
    sh:targetClass aekg:BatteryDurabilityObservation ;
    sh:property [
        sh:path aekg:batterySoHPercent ;
        sh:datatype xsd:decimal ;
        sh:minInclusive 0.0 ; sh:maxInclusive 100.0 ;
        sh:minCount 1 ;
    ] ;
    sh:property [
        sh:path aekg:milestoneYears ;
        sh:datatype xsd:integer ;
        sh:in ( 5 8 ) ;
        sh:severity sh:Warning ;
        sh:message "Euro 7 M1/N1 durability compliance milestones are defined at 5 years (100k km) and 8 years (160k km)."@en ;
    ] .

4.3 Sample Production SPARQL 1.1 Queries
Query 1: Three-Tier Epistemic Divergence (EEA WLTP vs. ADAC Ecotest vs. Spritmonitor)

Quantifies the real-world energy consumption gap across European BEV variants weighted by EEA registration volume, returning full provenance citations for GraphRAG synthesis.

Code snippet
PREFIX aekg: <https://w3id.org/autoecokg/ontology#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?modelName ?regCount
       ?wltpKwh ?adacKwh ?realWorldMeanKwh
       (ROUND(((?realWorldMeanKwh - ?wltpKwh) / ?wltpKwh) * 1000) / 10.0 AS ?realVsWltpGapPct)
       (ROUND(((?realWorldMeanKwh - ?adacKwh) / ?adacKwh) * 1000) / 10.0 AS ?realVsAdacGapPct)
       ?sampleSize ?eeaSource ?smSource
WHERE {
  ?vehicle a aekg:VehicleModelVariant ;
           rdfs:label ?modelName ;
           aekg:powertrainType "BEV" ;
           aekg:registrationCount ?regCount .

  # Tier 1: EEA WLTP Homologation Observation
  ?wltpObs a sosa:Observation ;
           sosa:hasFeatureOfInterest ?vehicle ;
           sosa:observedProperty aekg:ElectricEnergyConsumptionWLTP ;
           sosa:hasSimpleResult ?wltpKwh ;
           prov:wasAttributedTo ?eeaSource .

  # Tier 2: ADAC Ecotest Independent Measurement
  ?adacObs a sosa:Observation ;
           sosa:hasFeatureOfInterest ?vehicle ;
           sosa:observedProperty aekg:ElectricEnergyConsumptionADAC ;
           sosa:hasSimpleResult ?adacKwh .

  # Tier 3: Spritmonitor Crowdsourced Distribution (linked via verified EntityAlignment)
  ?alignment a aekg:EntityAlignment ;
             aekg:canonicalEntity ?vehicle ;
             aekg:externalEntity ?smVehicle ;
             aekg:confidenceScore ?conf .
  FILTER (?conf >= 0.90)

  ?smObs a aekg:RealWorldConsumptionDistribution ;
         sosa:hasFeatureOfInterest ?smVehicle ;
         aekg:meanValue ?realWorldMeanKwh ;
         aekg:sampleSize ?sampleSize ;
         prov:wasAttributedTo ?smSource .
  FILTER (?sampleSize >= 30 && ?regCount >= 5000)
}
ORDER BY DESC(?realVsWltpGapPct)
LIMIT 25

Query 2: Euro 7 Brake Dust Compliance & Annual Tyre Microplastic Load (Pillar 2)

Screens vehicle-tyre pairings against Euro 7 M1 brake 
PM
10
PM
10
	​

 limits (
3
 mg/km
3 mg/km BEV; 
7
 mg/km
7 mg/km ICE/HEV) and computes annual fleet-level tyre microplastic runoff (kg/yr) and airborne 
PM
10
PM
10
	​

 (g/yr) for a 100-vehicle fleet driving 
25,000
 km/yr
25,000 km/yr.

Code snippet
PREFIX aekg: <https://w3id.org/autoecokg/ontology#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?vehicleName ?powertrain ?tyreName ?abrasionLevel ?aiCT ?brakePM10 ?brakeCompliant
       (ROUND(?annualMicroplasticSoilWaterKg * 100) / 100.0 AS ?fleetSoilWaterMicroplasticsKgYr)
       (ROUND(?annualAirbornePM10Grams * 10) / 10.0 AS ?fleetAirborneTyrePM10GramsYr)
WHERE {
  BIND(100 AS ?fleetSize)
  BIND(25000 AS ?annualKmPerVehicle)

  ?cfg a aekg:VehicleTyreConfiguration ;
       aekg:hasVehicleVariant ?vehicle ;
       aekg:hasTyreModel ?tyre .

  ?vehicle rdfs:label ?vehicleName ;
           aekg:powertrainType ?powertrain ;
           aekg:massInRunningOrderKg ?massKg .
  ?tyre rdfs:label ?tyreName ;
        aekg:tyreClass "C1" .

  # Tyre Abrasion Observation (load-normalized mg/km/t)
  ?abrObs a aekg:TyreAbrasionObservation ;
          sosa:hasFeatureOfInterest ?tyre ;
          aekg:abrasionLevelMgKmTonne ?abrasionLevel ;
          aekg:abrasionIndexAICT ?aiCT ;
          aekg:airbornePM10Fraction ?alphaPM10 .

  # Brake Dust Observation (PM10 mg/km)
  ?brakeObs a aekg:BrakeDustObservation ;
            sosa:hasFeatureOfInterest ?vehicle ;
            aekg:brakePM10MgKm ?brakePM10 .

  # Euro 7 M1 Brake Dust Limit Logic (3 mg/km BEV, 7 mg/km ICE/HEV/PHEV)
  BIND(IF(?powertrain = "BEV", 3.0, 7.0) AS ?euro7BrakeLimit)
  BIND(?brakePM10 <= ?euro7BrakeLimit AS ?brakeCompliant)

  # Total vehicle tyre abrasion rate (mg/km) = abrasionLevel (mg/km/t) * vehicle mass (t)
  BIND(?abrasionLevel * (?massKg / 1000.0) AS ?vehAbrasionMgKm)
  # Convert mg -> kg (divide by 1e6) for soil/water microplastic fraction (1 - alpha)
  BIND((?vehAbrasionMgKm * (1.0 - ?alphaPM10) * ?annualKmPerVehicle * ?fleetSize) / 1000000.0
       AS ?annualMicroplasticSoilWaterKg)
  # Convert mg -> g (divide by 1e3) for airborne PM10 fraction
  BIND((?vehAbrasionMgKm * ?alphaPM10 * ?annualKmPerVehicle * ?fleetSize) / 1000.0
       AS ?annualAirbornePM10Grams)
}
ORDER BY ASC(?fleetSoilWaterMicroplasticsKgYr)

Query 3: Exact Pareto Skyline Query for Fleet Vehicle-Tyre Selection (Pillar 3)

Returns strictly non-dominated vehicle-tyre configurations across five criteria—maximizing wet safety and tread lifespan while minimizing tyre abrasion, rolling resistance, and 5-year TCO—using pure SPARQL 1.1 FILTER NOT EXISTS skyline semantics.

Code snippet
PREFIX aekg: <https://w3id.org/autoecokg/ontology#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?vehicleName ?tyreName ?safety ?abrasion ?lifespanKm ?rrc ?tcoEur
WHERE {
  ?cfg a aekg:VehicleTyreConfiguration ;
       aekg:hasVehicleVariant ?v ;
       aekg:hasTyreModel ?t ;
       aekg:predictedTreadLifespanKm ?lifespanKm ;
       aekg:hasTCOCalculation/aekg:fiveYearTCOEur ?tcoEur .

  ?v rdfs:label ?vehicleName ; aekg:segment "C-SUV" .
  ?t rdfs:label ?tyreName ;
     aekg:wetGripScore ?safety ;
     aekg:rollingResistanceCoeff ?rrc .
  ?abrObs a aekg:TyreAbrasionObservation ;
          sosa:hasFeatureOfInterest ?t ;
          aekg:abrasionLevelMgKmTonne ?abrasion .

  # Pareto Skyline condition: No alternative configuration ?cfg2 dominates ?cfg
  FILTER NOT EXISTS {
    ?cfg2 a aekg:VehicleTyreConfiguration ;
          aekg:hasVehicleVariant/aekg:segment "C-SUV" ;
          aekg:hasTyreModel ?t2 ;
          aekg:predictedTreadLifespanKm ?lifespan2 ;
          aekg:hasTCOCalculation/aekg:fiveYearTCOEur ?tco2 .
    ?t2 aekg:wetGripScore ?safety2 ;
        aekg:rollingResistanceCoeff ?rrc2 .
    ?abrObs2 a aekg:TyreAbrasionObservation ;
             sosa:hasFeatureOfInterest ?t2 ;
             aekg:abrasionLevelMgKmTonne ?abrasion2 .

    FILTER (
      ?safety2   >= ?safety     &&
      ?lifespan2 >= ?lifespanKm &&
      ?abrasion2 <= ?abrasion   &&
      ?rrc2      <= ?rrc        &&
      ?tco2      <= ?tcoEur     &&
      ( ?safety2 > ?safety || ?lifespan2 > ?lifespanKm ||
        ?abrasion2 < ?abrasion || ?rrc2 < ?rrc || ?tco2 < ?tcoEur )
    )
  }
}
ORDER BY ASC(?tcoEur)

Query 4: Federated Catena-X Battery LCA & COVESA VSS Euro 7 Durability Audit (Pillars 4 & 5)

Demonstrates cross-organizational sovereign federation via a Catena-X Knowledge Agent endpoint, joining live VSS fleet State-of-Health observations against Euro 7 5-year/100,000 km (
80
%
80%) thresholds and primary supplier cradle-to-gate battery PCFs.

Code snippet
PREFIX aekg: <https://w3id.org/autoecokg/ontology#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX cx:   <https://w3id.org/catenax/ontology/pcf#>

SELECT ?vehicleModel ?cathodeChem ?soh5yr ?euro7SoHCompliant
       ?batteryMfgCO2eKg ?supplierAgent ?vssObsURI
WHERE {
  # Local AutoEcoKG 2.0 Graph: Aggregated COVESA VSS Fleet Telemetry
  ?vssObsURI a aekg:BatteryDurabilityObservation ;
             sosa:hasFeatureOfInterest ?vehicle ;
             aekg:milestoneYears 5 ;
             aekg:batterySoHPercent ?soh5yr ;
             sosa:observedProperty ?prop .
  ?prop aekg:vssSignalPath "Vehicle.Powertrain.TractionBattery.StateOfHealth" .

  ?vehicle a aekg:VehicleModelVariant ;
           rdfs:label ?vehicleModel ;
           aekg:batteryPackPartId ?partId ;
           aekg:cathodeChemistry ?cathodeChem .

  BIND(?soh5yr >= 80.0 AS ?euro7SoHCompliant)

  # Sovereign Catena-X EDC / Knowledge Agent Federated Subquery
  SERVICE <https://edc-agent.catena-x.internal/sparql/pcf> {
    ?pcfEntity a cx:ProductCarbonFootprint ;
               cx:materialPartId ?partId ;
               cx:fossilGhgEmissionsKgCO2e ?batteryMfgCO2eKg ;
               prov:wasAttributedTo ?supplierAgent .
  }
}
ORDER BY DESC(?soh5yr)

5. Implementation Architecture & Phased Roadmap
5.1 Layered Production System Architecture
Plaintext
+=========================================================================================+
|  LAYER 6: CONSUMERS, GOVERNANCE & OBSERVABILITY                                         |
|  [Fleet TCO & Pareto UI]  [CSRD ESRS E1/E2 Auditor]  [GraphRAG Chat]  [AutoEcoBench CI] |
+=========================================================================================+
                                          ^
                                          | REST / GraphQL / SPARQL / JSON-LD
+=========================================================================================+
|  LAYER 5: NEURO-SYMBOLIC GRAPHRAG & ANALYTICS ENGINE                                    |
|  +------------------------------------------+  +--------------------------------------+ |
|  | Hybrid GraphRAG Pipeline                 |  | Domain Decision & Compliance Engines | |
|  | - Vector TBox/ABox Linker (Qdrant)       |  | - Euro 7 Compliance Evaluator        | |
|  | - Schema-Constrained Text2SPARQL LLM     |  | - Cradle-to-Grave Battery LCA Engine | |
|  | - AST + SHACL Verifier & Repair Loop     |  | - NSGA-II / TOPSIS Pareto Optimizer  | |
|  | - PROV-O Citation Binder (Zero-Halluc.)  |  | - CSRD ESRS E1/E2 XBRL/JSON Exporter | |
|  +------------------------------------------+  +--------------------------------------+ |
+=========================================================================================+
                                          ^
                                          | SPARQL 1.1 / Cypher / SQL-OBDA
+=========================================================================================+
|  LAYER 4: FEDERATED SEMANTIC STORAGE & REASONING CORE                                   |
|  +----------------------------+  +------------------------+  +------------------------+ |
|  | Ontotext GraphDB Cluster   |  | Neo4j Enterprise (GDS) |  | Ontop OBDA Lakehouse   | |
|  | - OWL 2 RL/QL Reasoner     |<-| - n10s RDF Sync        |  | - Apache Parquet (EEA) | |
|  | - Native SHACL Gatekeeper  |  | - Fleet Graph Analytics|  | - TimescaleDB (VSS)    | |
|  | - Named Graphs & RDF-star  |  |                        |  | - R2RML Virtual Views  | |
|  +----------------------------+  +------------------------+  +------------------------+ |
+=========================================================================================+
                                          ^
                                          | Validated RDF / SAMM Aspect Streams
+=========================================================================================+
|  LAYER 3: ETL, ENTITY RESOLUTION & QUALITY PIPELINE                                     |
|  [RML / YARRRML Mapper] -> [Splink Probabilistic ER] -> [pySHACL / ROBOT Quality Gate]  |
+=========================================================================================+
                                          ^
+=========================================================================================+
|  LAYER 2: STANDARDS & DATASPACE CONNECTIVITY                                            |
|  [COVESA VSS Kafka/Flink Stream Aggregator]   [Catena-X Tractus-X EDC + AAS/SAMM Agent] |
+=========================================================================================+
                                          ^
+=========================================================================================+
|  LAYER 1: HETEROGENEOUS DATA SOURCES                                                    |
|  [EEA Registry >10M/yr] [ADAC Ecotest] [Spritmonitor] [TÜV Reports] [OEM EVP / OEM PCF] |
+=========================================================================================+

5.2 Phased Implementation Roadmap (18 Months)
Phase & Timeline	Core Deliverables	Key Engineering Activities	Quantitative Exit Criteria
Phase 1: Scale-Up & Semantic Backbone (Months 1–4)	AutoEcoKG 2.0 Core Ontology (v2.0); GraphDB + Ontop OBDA cluster; EEA, Spritmonitor & TÜV ingestion	Migrate 26,822 legacy triples; automate RML/YARRRML pipelines; deploy Splink probabilistic ER across EEA/ADAC/Spritmonitor; integrate pySHACL & ROBOT into GitLab/GitHub CI	
>10M annual EEA rows virtualized & canonically aggregated; ER precision 
≥96%; 37/37 legacy CQs passing; 0 SHACL errors
Phase 2: Euro 7 & LCA Compliance Core (Months 5–9)	Non-Exhaust Particulate Engine (Tyre Abrasion & Brake 
PM
10
	​

); EV Battery Durability & Cradle-to-Grave LCA module	Implement UNECE ECE/TRANS/WP.29/2026/138 SRTT/
AI
CT
	​

 schema; ingest Euro 7 EVP specs & brake 
PM
10
	​

 curves; connect ecoinvent/GREET LCA factors + EU grid intensities	100% automated Euro 7 M1/N1 compliance screening; validated microplastic mass-balance equations; full ISO 14040/44 provenance tracking
Phase 3: Fleet Pareto TCO, CSRD & GraphRAG (Months 10–14)	5-Objective Pareto TCO Optimizer; CSRD ESRS E1/E2 Report Generator; Production Neuro-Symbolic GraphRAG	Build NSGA-II/skyline optimizer + TOPSIS UI; map graph KPIs to ESRS E1 & E2-4/E2-5 schemas; retire 8 rigid templates; deploy Text2SPARQL + AST verifier + AutoEcoBench 2.0 (150+ CQs)	Text2SPARQL Execution Accuracy 
≥92% on AutoEcoBench 2.0; 
100% provenance citation faithfulness; 
<3s P95 Pareto query latency
Phase 4: COVESA VSS, Catena-X & Enterprise GA (Months 15–18)	COVESA VSS Telemetry Bridge; Catena-X SAMM/AAS/EDC Federation; Enterprise Multi-Tenant Release	Deploy Kafka/Flink VSSo aggregators; publish SAMM Aspect Models & AAS templates; configure Tractus-X EDC + ODRL usage policies & Knowledge Agent federation; SOC 2 / ISO 27001 hardening	Live federated SPARQL PCF/abrasion exchange across 
≥2 Catena-X pilot partners; 99.9% cluster SLA; external CSRD pilot audit sign-off
5.3 Risk Register & Architectural Mitigations
Risk Category	Specific Failure Mode	Concrete Technical Mitigation
Triple Bloat & Query Latency	Materializing 37M+ raw EEA rows or 10 Hz VSS telemetry collapses triple-store join performance	Enforce Canonical TVV aggregation in GraphDB; keep raw rows in Parquet/TimescaleDB behind Ontop OBDA; pre-aggregate VSS signals into monthly sosa:ObservationCollection summaries
Cross-Source Entity Mismatch	Erroneous owl:sameAs merges across European trim naming variants corrupt real-world divergence metrics	Replace owl:sameAs with reified aekg:EntityAlignment nodes carrying Splink confidence scores; enforce human-in-the-loop review for 
0.75≤σ<0.90 matches
LLM Hallucination in Text2SPARQL	Conversational AI invents non-existent predicates, drops provenance filters, or fabricates regulatory thresholds	Enforce grammar/schema-constrained decoding, mandatory AST/TBox static verification prior to execution, and strict zero-citation blocking (responses fail closed if numeric claims lack prov:Entity bindings)
Data Licensing & Privacy (GDPR)	Crowdsourced driver logs (Spritmonitor), proprietary test publishers (ADAC/TÜV), and VIN-linked VSS telemetry carry strict legal constraints	Strip all PII/VINs at ingestion edge (k-anonymity 
k≥15 for real-world cohorts); enforce ODRL usage policies inside Tractus-X EDC and named-graph RBAC in GraphDB so licensed commercial feeds never leak into public exports
Regulatory Drift (C2/C3 & Phase 2 Limits)	UNECE WP.29 updates to C2/C3 tyre abrasion thresholds (2030–2034) or Euro 7 delegated acts invalidate hardcoded rules	Externalize all regulatory limits as versioned, time-stamped OWL/SHACL Policy Graphs (aekg:effectiveFrom, aekg:supersededBy), enabling historical back-testing and seamless rule updates without code redeployment

By grounding every real-world observation, regulatory threshold, lifecycle inventory factor, and Pareto trade-off in W3C SOSA, PROV-O, SHACL, COVESA VSS, and Catena-X SAMM standards, AutoEcoKG 2.0 establishes a verifiable semantic infrastructure capable of bridging European environmental law, automotive engineering, and corporate climate accountability at continental scale.