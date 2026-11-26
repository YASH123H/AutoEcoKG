"""AutoEcoKG query engine. Run: python src/engine.py --list"""
import argparse
import csv
import sys
from pathlib import Path
from rdflib import Graph, Literal, XSD

PREFIX = """
PREFIX aek: <https://w3id.org/autoecokg/ontology#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX prov: <http://www.w3.org/ns/prov#>
"""
QUERIES = {
"vehicles": """
SELECT ?vehicle ?name ?powertrain WHERE {
 ?vehicle a aek:VehicleVariant ; rdfs:label ?name ; aek:powertrain ?powertrain .
} ORDER BY ?name
""",
"vehicle_co2": """
SELECT ?vehicle ?name ?co2 WHERE {
 ?vehicle a aek:VehicleVariant ; rdfs:label ?name .
 ?obs a aek:VehicleObservation ; sosa:hasFeatureOfInterest ?vehicle ;
 aek:measurementProperty aek:wltp_co2_g_km ; aek:numericValue ?co2 .
} ORDER BY ?co2 ?name
""",
"fuel_gap": """
SELECT ?name ?wltp ?adac ?gap WHERE {
 ?vehicle a aek:VehicleVariant ; rdfs:label ?name .
 ?w sosa:hasFeatureOfInterest ?vehicle ; aek:measurementProperty aek:wltp_fuel_l_100km ; aek:numericValue ?wltp .
 ?a sosa:hasFeatureOfInterest ?vehicle ; aek:measurementProperty aek:adac_fuel_l_100km ; aek:numericValue ?adac .
 ?g sosa:hasFeatureOfInterest ?vehicle ; aek:measurementProperty aek:fuel_l_100km_gap_pct ; aek:numericValue ?gap .
} ORDER BY DESC(?gap) ?name
""",
"low_abrasion": """
SELECT ?tyre ?name ?size ?category ?abrasion WHERE {
 ?tyre a aek:TyreVariant ; rdfs:label ?name ; aek:tyreSize ?size ; aek:seasonCategory ?category .
 ?obs a aek:TyreObservation ; sosa:hasFeatureOfInterest ?tyre ;
 aek:measurementProperty aek:abrasion_mg_km_t ; aek:numericValue ?abrasion .
} ORDER BY ?abrasion ?name ?size
""",
"safe_low_abrasion": """
SELECT ?tyre ?name ?size ?abrasion ?safety WHERE {
 ?tyre a aek:TyreVariant ; rdfs:label ?name ; aek:tyreSize ?size .
 { SELECT ?tyre ?abrasion WHERE { ?a aek:measurementProperty aek:abrasion_mg_km_t ; sosa:hasFeatureOfInterest ?tyre ; aek:numericValue ?abrasion . } }
 { SELECT ?tyre ?safety WHERE { ?s aek:measurementProperty aek:safety_grade ; sosa:hasFeatureOfInterest ?tyre ; aek:numericValue ?safety . } }
 FILTER(?safety <= ?maxSafety)
} ORDER BY ?abrasion ?safety ?name
""",
"alignment": """
SELECT ?vehicleName ?tyreName ?size ?matchType ?identity ?fitment WHERE {
 ?candidate a aek:AlignmentCandidate ; aek:candidateVehicle ?v ;
 aek:candidateTyre ?t ; aek:matchType ?matchType ;
 aek:identityVerified ?identity ; aek:fitmentVerified ?fitment .
 ?v rdfs:label ?vehicleName .
 ?t rdfs:label ?tyreName ; aek:tyreSize ?size .
} ORDER BY ?matchType ?vehicleName ?tyreName ?size
""",
"matched_tyre_observations": """
SELECT ?vehicleName ?tyreName ?abrasion ?safety ?identity ?fitment WHERE {
 ?candidate a aek:AlignmentCandidate ; aek:candidateVehicle ?v ;
 aek:candidateTyre ?t ; aek:matchType "model_size_match"^^<http://www.w3.org/2001/XMLSchema#string> ;
 aek:identityVerified ?identity ; aek:fitmentVerified ?fitment .
 ?v rdfs:label ?vehicleName .
 ?t rdfs:label ?tyreName .
 ?a sosa:hasFeatureOfInterest ?t ; aek:measurementProperty aek:abrasion_mg_km_t ; aek:numericValue ?abrasion .
 OPTIONAL { ?s sosa:hasFeatureOfInterest ?t ; aek:measurementProperty aek:safety_grade ; aek:numericValue ?safety . }
} ORDER BY ?vehicleName
""",
"provenance": """
SELECT ?name ?abrasion ?file ?page WHERE {
 ?t a aek:TyreVariant ; rdfs:label ?name .
 ?obs sosa:hasFeatureOfInterest ?t ; aek:measurementProperty aek:abrasion_mg_km_t ;
 aek:numericValue ?abrasion ; prov:wasDerivedFrom ?doc ; aek:sourcePage ?page .
 ?doc a aek:SourceDocument ; aek:sourceFilename ?file .
} ORDER BY ?name ?abrasion
""",
"euro7_particulates": """
SELECT ?vehicleName ?powertrain ?tyreName ?abrasionLevel ?aiCT ?brakePM10 ?brakeCompliant
       (ROUND(?annualMicroplasticSoilWaterKg * 100) / 100.0 AS ?fleetSoilWaterMicroplasticsKgYr)
       (ROUND(?annualAirbornePM10Grams * 10) / 10.0 AS ?fleetAirborneTyrePM10GramsYr)
WHERE {
  BIND(100 AS ?fleetSize)
  BIND(25000 AS ?annualKmPerVehicle)

  ?cfg a aek:VehicleTyreConfiguration ;
       aek:hasVehicleVariant ?vehicle ;
       aek:hasTyreModel ?tyre .

  ?vehicle rdfs:label ?vehicleName ;
           aek:powertrain ?powertrain ;
           aek:massInRunningOrderKg ?massKg .
  ?tyre rdfs:label ?tyreName .

  ?abrObs a aek:TyreAbrasionObservation ;
          sosa:hasFeatureOfInterest ?tyre ;
          aek:abrasionLevelMgKmTonne ?abrasionLevel ;
          aek:abrasionIndexAICT ?aiCT ;
          aek:airbornePM10Fraction ?alphaPM10 .

  ?brakeObs a aek:BrakeDustObservation ;
            sosa:hasFeatureOfInterest ?vehicle ;
            aek:brakePM10MgKm ?brakePM10 .

  BIND(IF(?powertrain = "electric", 3.0, 7.0) AS ?euro7BrakeLimit)
  BIND(?brakePM10 <= ?euro7BrakeLimit AS ?brakeCompliant)

  BIND(?abrasionLevel * (?massKg / 1000.0) AS ?vehAbrasionMgKm)
  BIND((?vehAbrasionMgKm * (1.0 - ?alphaPM10) * ?annualKmPerVehicle * ?fleetSize) / 1000000.0
       AS ?annualMicroplasticSoilWaterKg)
  BIND((?vehAbrasionMgKm * ?alphaPM10 * ?annualKmPerVehicle * ?fleetSize) / 1000.0
       AS ?annualAirbornePM10Grams)
} ORDER BY ?vehicleName ?tyreName
""",
"battery_durability": """
SELECT ?vehicleName ?powertrain ?sohPercent ?milestoneYears ?milestoneKm ?euro7Compliant WHERE {
  ?vehicle a aek:VehicleVariant ; rdfs:label ?vehicleName ; aek:powertrain ?powertrain .
  ?obs a aek:BatteryDurabilityObservation ; sosa:hasFeatureOfInterest ?vehicle ;
       aek:batterySoHPercent ?sohPercent ; aek:milestoneYears ?milestoneYears ;
       aek:milestoneKm ?milestoneKm .
  BIND(?sohPercent >= 80.0 AS ?euro7Compliant)
} ORDER BY ?vehicleName
""",
"tco_pareto_skyline": """
SELECT ?vehicleName ?tyreName ?lifespanKm ?tcoEur WHERE {
  ?cfg a aek:VehicleTyreConfiguration ;
       aek:hasVehicleVariant ?vehicle ;
       aek:hasTyreModel ?tyre ;
       aek:predictedTreadLifespanKm ?lifespanKm ;
       aek:hasTCOCalculation ?tco .
  ?tco aek:fiveYearTCOEur ?tcoEur .
  ?vehicle rdfs:label ?vehicleName .
  ?tyre rdfs:label ?tyreName .
} ORDER BY ?tcoEur ?vehicleName
""",
"epistemic_divergence": """
SELECT ?vehicleName ?powertrain ?wltp ?adac ?gap WHERE {
  ?vehicle a aek:VehicleVariant ; rdfs:label ?vehicleName ; aek:powertrain ?powertrain .
  {
    ?w sosa:hasFeatureOfInterest ?vehicle ; aek:measurementProperty aek:wltp_fuel_l_100km ; aek:numericValue ?wltp .
    ?a sosa:hasFeatureOfInterest ?vehicle ; aek:measurementProperty aek:adac_fuel_l_100km ; aek:numericValue ?adac .
    ?g sosa:hasFeatureOfInterest ?vehicle ; aek:measurementProperty aek:fuel_l_100km_gap_pct ; aek:numericValue ?gap .
  } UNION {
    ?w sosa:hasFeatureOfInterest ?vehicle ; aek:measurementProperty aek:wltp_electric_kwh_100km ; aek:numericValue ?wltp .
    ?a sosa:hasFeatureOfInterest ?vehicle ; aek:measurementProperty aek:adac_electric_kwh_100km ; aek:numericValue ?adac .
    ?g sosa:hasFeatureOfInterest ?vehicle ; aek:measurementProperty aek:electric_kwh_100km_gap_pct ; aek:numericValue ?gap .
  }
} ORDER BY DESC(?gap) ?vehicleName
"""
}

class QueryEngine:
    def __init__(self, graph_path):
        self.graph = Graph().parse(graph_path, format="turtle")

    def run(self, name, max_safety=2.5):
        if name not in QUERIES:
            raise ValueError(f"Unknown query: {name}")
        bindings = {"maxSafety": Literal(str(max_safety), datatype=XSD.decimal)} if name == "safe_low_abrasion" else {}
        result = self.graph.query(PREFIX + QUERIES[name], initBindings=bindings)
        columns = [str(v) for v in result.vars]
        return columns, [{c: str(v) if v is not None else "" for c,v in zip(columns,row)} for row in result]

def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, default=root/"data/autoecokg_triples.ttl")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--query", choices=QUERIES)
    parser.add_argument("--limit", type=int, default=10, help="Displayed rows; 0 shows all")
    parser.add_argument("--max-safety", type=float, default=2.5)
    parser.add_argument("--output", type=Path, help="Optional CSV containing all results")
    args = parser.parse_args()
    if args.list:
        print("\n".join(QUERIES)); return
    if not args.query: parser.error("Use --query NAME or --list")
    if args.limit < 0 or not 0.6 <= args.max_safety <= 5.5: parser.error("Invalid limit or safety grade")
    engine = QueryEngine(args.graph)
    columns, rows = engine.run(args.query, args.max_safety)
    print(f"Query: {args.query} | RDF triples: {len(engine.graph)} | Results: {len(rows)}")
    writer = csv.DictWriter(sys.stdout, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows[:args.limit] if args.limit else rows)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader(); writer.writerows(rows)
        print(f"Saved: {args.output}")

if __name__ == "__main__":
    main()
