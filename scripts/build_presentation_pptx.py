"""Build AutoEcoKG 2.0 Widescreen PowerPoint Presentation (16:9).
Strictly follows the Knowledge Graph Project Guidelines (WS26/27):
Intro -> Knowledge Graph -> Application -> Evaluation -> Conclusion / Reflection.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Widescreen 16:9 dimensions
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Color Palette
COLOR_BG = RGBColor(248, 250, 252)         # Slate 50
COLOR_NAVY = RGBColor(15, 23, 42)          # Slate 900
COLOR_DARK = RGBColor(30, 41, 59)          # Slate 800
COLOR_CYAN = RGBColor(14, 165, 233)        # Sky 500
COLOR_BLUE = RGBColor(2, 132, 199)         # Sky 600
COLOR_GREEN = RGBColor(16, 185, 129)       # Emerald 500
COLOR_CARD_BG = RGBColor(255, 255, 255)    # White
COLOR_BORDER = RGBColor(226, 232, 240)     # Slate 200
COLOR_MUTED = RGBColor(100, 116, 139)      # Slate 500
COLOR_LIGHT_ACC = RGBColor(240, 249, 255)  # Light cyan accent
COLOR_RED = RGBColor(239, 68, 68)          # Red 500


def create_deck():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6]  # Blank slide

    def add_header(slide, section_tag, title_text, subtitle_text):
        # Section Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = section_tag.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_CYAN

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_NAVY

        # Subtitle
        if subtitle_text:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.7), Inches(0.35))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle_text
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = COLOR_MUTED

    def add_footer(slide, current_slide, total_slides=12):
        # Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_BORDER
        line.line.color.rgb = COLOR_BORDER

        # Footer text
        foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(9.0), Inches(0.3))
        tf = foot_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "AutoEcoKG 2.0 | Creation and Application of Knowledge Graphs (WS26/27) | LUH · L3S · TIB"
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_MUTED

        # Page number
        num_box = slide.shapes.add_textbox(Inches(10.5), Inches(7.05), Inches(2.033), Inches(0.3))
        tf_num = num_box.text_frame
        tf_num.margin_left = tf_num.margin_top = tf_num.margin_right = tf_num.margin_bottom = 0
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"{current_slide} / {total_slides}"
        p_num.font.size = Pt(9.5)
        p_num.font.bold = True
        p_num.font.color.rgb = COLOR_MUTED

    def add_card(slide, left, top, width, height, title, items, badge_text=None, accent_color=COLOR_BLUE):
        # Background shape
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD_BG
        shape.line.color.rgb = COLOR_BORDER
        shape.line.width = Pt(1)

        # Header accent stripe
        stripe = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.08))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = accent_color
        stripe.line.fill.background()

        # Text box
        pad = Inches(0.25)
        tb = slide.shapes.add_textbox(left + pad, top + pad, width - (pad * 2), height - (pad * 2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Title
        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(14)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_DARK
        p_title.space_after = Pt(10)

        # Items
        for item in items:
            p = tf.add_paragraph()
            p.space_after = Pt(6)
            if isinstance(item, tuple):
                bold_part, regular_part = item
                run_b = p.add_run()
                run_b.text = "• " + bold_part + ": "
                run_b.font.bold = True
                run_b.font.size = Pt(11)
                run_b.font.color.rgb = COLOR_DARK

                run_r = p.add_run()
                run_r.text = regular_part
                run_r.font.size = Pt(11)
                run_r.font.color.rgb = COLOR_MUTED
            else:
                run = p.add_run()
                run.text = "• " + item
                run.font.size = Pt(11)
                run.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    # Background full dark
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.fill.background()

    # Decorative Cyan Line
    dec_line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.8), Inches(1.5), Inches(0.08))
    dec_line.fill.solid()
    dec_line.fill.fore_color.rgb = COLOR_CYAN
    dec_line.line.fill.background()

    # Title & Subtitle Box
    t_box1 = s1.shapes.add_textbox(Inches(1.2), Inches(2.1), Inches(10.9), Inches(2.6))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p_t1 = tf1.paragraphs[0]
    p_t1.text = "AutoEcoKG 2.0"
    p_t1.font.size = Pt(40)
    p_t1.font.bold = True
    p_t1.font.color.rgb = RGBColor(255, 255, 255)

    p_t2 = tf1.add_paragraph()
    p_t2.text = "Environmental Knowledge Graph for Real-World Automotive Compliance & Fleet Decision-Making"
    p_t2.font.size = Pt(20)
    p_t2.font.bold = True
    p_t2.font.color.rgb = COLOR_CYAN
    p_t2.space_before = Pt(8)

    p_t3 = tf1.add_paragraph()
    p_t3.text = "Euro 7 Non-Exhaust Particulates · Catena-X Battery Pass · 5-Criterion Pareto Skyline TCO"
    p_t3.font.size = Pt(13)
    p_t3.font.color.rgb = RGBColor(148, 163, 184)
    p_t3.space_before = Pt(12)

    # Metadata Card
    meta_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.9), Inches(10.9), Inches(1.5))
    meta_box.fill.solid()
    meta_box.fill.fore_color.rgb = COLOR_DARK
    meta_box.line.color.rgb = RGBColor(51, 65, 85)
    meta_tf = meta_box.text_frame
    meta_tf.word_wrap = True
    meta_tf.margin_left = Inches(0.3)
    meta_tf.margin_top = Inches(0.2)

    p_m1 = meta_tf.paragraphs[0]
    p_m1.text = "Author: Riddhadipta Nath  |  Course: Creation & Application of Knowledge Graphs (WS26/27)"
    p_m1.font.size = Pt(12)
    p_m1.font.bold = True
    p_m1.font.color.rgb = RGBColor(241, 245, 249)

    p_m2 = meta_tf.add_paragraph()
    p_m2.text = "Institutions: Leibniz University Hannover · L3S Research Center · TIB"
    p_m2.font.size = Pt(11)
    p_m2.font.color.rgb = RGBColor(148, 163, 184)
    p_m2.space_before = Pt(4)

    p_m3 = meta_tf.add_paragraph()
    p_m3.text = "Submission Contact: xinyue.gong@l3s.de  |  Project Repository: https://github.com/YASH123H/AutoEcoKG/pull/2"
    p_m3.font.size = Pt(10.5)
    p_m3.font.color.rgb = COLOR_CYAN
    p_m3.space_before = Pt(4)

    # =========================================================================
    # SLIDE 2: Introduction - Motivation & Automotive Dilemma
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. Introduction", "Motivation & The Real-World Automotive Gap",
               "Why official lab ratings fail to reflect modern driving impacts and regulatory shifts.")
    add_footer(s2, 2)

    add_card(s2, Inches(0.8), Inches(1.85), Inches(3.64), Inches(4.85),
             "1. Lab vs. Road Divergence",
             [("WLTP Inaccuracies", "Official homologation cycles systematically underestimate energy and fuel consumption by 15% to 30%."),
              ("Real-World EcoTest", "ADAC independent testing measures realistic mixed driving with high-speed highway and climate loads."),
              ("Epistemic Gap", "Fleet managers making purchasing decisions based purely on OEM datasheets suffer unexpected carbon costs.")],
             accent_color=COLOR_RED)

    add_card(s2, Inches(4.84), Inches(1.85), Inches(3.64), Inches(4.85),
             "2. The Euro 7 Paradigm Shift",
             [("Beyond Tailpipe CO2", "As EV adoption grows, non-exhaust emissions (brake dust and tyre abrasion) dominate particulate pollution."),
              ("Regulation EU 2024/1257", "First regulation globally mandating strict brake PM10 limits (3 mg/km BEV, 7 mg/km ICE)."),
              ("Tyre Microplastics", "Microplastic abrasion splits 90% into road runoff/water and 10% into breathable airborne PM10.")],
             accent_color=COLOR_BLUE)

    add_card(s2, Inches(8.88), Inches(1.85), Inches(3.64), Inches(4.85),
             "3. Circular Battery Mandates",
             [("Regulation EU 2023/1542", "Mandates digital Battery Passports with transparent State of Health (SoH) durability tracking."),
              ("Milestone Guarantees", "Requires >= 80% SoH at 5 yrs / 100,000 km, and >= 70% SoH at 8 yrs / 160,000 km."),
              ("Lifecycle Economics", "Battery degradation directly governs second-life residual values and long-term fleet depreciation.")],
             accent_color=COLOR_GREEN)

    # =========================================================================
    # SLIDE 3: Introduction - Role of the Knowledge Graph
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "1. Introduction", "Why a Graph-Native Knowledge Graph?",
               "Unifying multi-dimensional testing, regulatory standards, and supply-chain ontologies.")
    add_footer(s3, 3)

    add_card(s3, Inches(0.8), Inches(1.85), Inches(5.65), Inches(4.85),
             "Limitations of Conventional Approaches",
             [("Relational Database Silos", "Tabular SQL joins collapse when connecting heterogeneous observations (vehicle bench tests, tyre road wear, battery chemistry, dynamic pricing)."),
              ("Lack of Standard Semantics", "Varying OEM naming conventions lead to mismatched fitment and incompatible tyre ratings."),
              ("Vector-Only Limitations", "Pure vector search lacks formal logical guarantees; cannot verify strict regulatory constraints or perform exact dominance pruning.")],
             accent_color=COLOR_RED)

    add_card(s3, Inches(6.85), Inches(1.85), Inches(5.65), Inches(4.85),
             "Knowledge Graph Value Proposition",
             [("Ontological Unification", "Formalizes automotive systems, environmental impact, and observation provenance in OWL 2 DL."),
              ("Multi-Hop Graph Reasoning", "Seamlessly navigates from vehicle powertrain -> fitted tyre dimension -> abrasion rate -> particulate runoff via SPARQL 1.1."),
              ("SHACL Constraint Validation", "Enforces strict mathematical bounds and regulatory compliance checks during graph generation."),
              ("Industrial Alignment", "Mapped directly to COVESA Vehicle Signal Specification (VSS 4.0) and Catena-X Battery Pass standards.")],
             accent_color=COLOR_CYAN)

    # =========================================================================
    # SLIDE 4: Knowledge Graph - Pipeline & Construction
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "2. Knowledge Graph", "Data Ingestion & Graph Construction Pipeline",
               "Automated multi-source extraction, entity alignment, and provenance modeling.")
    add_footer(s4, 4)

    add_card(s4, Inches(0.8), Inches(1.85), Inches(3.64), Inches(4.85),
             "1. Multi-Source Ingestion",
             [("Automated Downloader", "Robust fetcher (src/download_raw_data.py) verifies SHA-256 hashes of all source reports."),
              ("26 Vehicle EcoTests", "ADAC multi-page PDFs parsed into 608 granular observation records covering WLTP vs EcoTest."),
              ("160 Tyre Abrasion Tests", "Extracted abrasion wear rates (mg/km/t) and safety test grades across 162 tyre variants.")],
             accent_color=COLOR_BLUE)

    add_card(s4, Inches(4.84), Inches(1.85), Inches(3.64), Inches(4.85),
             "2. Alignment & Modeling",
             [("Entity Alignment", "Disambiguated 161 vehicle-tyre configuration candidate links based on dimensional compatibility."),
              ("W3C SOSA/SSN Provenance", "Every observation reifies source document, page number, test protocol, and observation context."),
              ("Zero Manual Labelling", "Deterministic rule-based alignment with strict confidence scoring and fallback review cues.")],
             accent_color=COLOR_CYAN)

    add_card(s4, Inches(8.88), Inches(1.85), Inches(3.64), Inches(4.85),
             "3. Graph Metrics & Scale",
             [("29,739 RDF Triples", "Expanded graph scale (+1,811 triples over v1.0) serialized in Turtle format."),
              ("Rich Entity Diversity", "26 vehicles, 162 tyres, 631 vehicle observations, 1,170 tyre observations, 161 configurations."),
              ("100% SHACL Conformance", "Automated validation with pyshacl yields zero errors or violations.")],
             accent_color=COLOR_GREEN)

    # =========================================================================
    # SLIDE 5: Knowledge Graph - Ontology & Schema Architecture
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "2. Knowledge Graph", "Ontology & Schema Architecture",
               "Extending AutoEcoKG with Euro 7 non-exhaust particulates, Catena-X, and VSS 4.0.")
    add_footer(s5, 5)

    add_card(s5, Inches(0.8), Inches(1.85), Inches(5.65), Inches(4.85),
             "Core Ontological Hierarchy",
             [("aekg:VehicleVariant", "Instances of tested automobiles with powertrain types (BEV, HEV, PHEV, ICE) and curb weight."),
              ("aekg:TyreVariant", "Tyre models with dimensions (e.g., 225/40 R18), wet/dry safety ratings, and longevity."),
              ("aekg:TyreAbrasionObservation", "Captures abrasion in mg/km/t, road runoff (90%), and airborne PM10 (10%)."),
              ("aekg:BrakeDustObservation", "Reifies brake wear emissions against Euro 7 limits (3 mg/km BEV, 7 mg/km ICE)."),
              ("aekg:BatteryDurabilityObservation", "Encapsulates SoH degradation milestones, battery chemistry (LFP, NMC), and capacity."),
              ("aekg:VehicleTyreConfiguration", "Synthesizes real-world combinations for holistic fleet optimization.")],
             accent_color=COLOR_NAVY)

    add_card(s5, Inches(6.85), Inches(1.85), Inches(5.65), Inches(4.85),
             "Standards Alignment & SHACL Verification",
             [("COVESA VSS 4.0", "Embedded signal paths (vssSignalPath) mapping directly to in-vehicle telematics (e.g., Vehicle.Powertrain.TractionBattery.StateOfHealth)."),
              ("Catena-X Battery Pass", "Complies with EU 2023/1542 digital product passport specifications."),
              ("SHACL Shape Constraints", "shacl_shapes.ttl enforces range limits: tyre abrasion (0-500 mg/km/t), brake wear (>= 0), battery SoH (0-100%)."),
              ("Epistemic Reification", "Explicitly separates official laboratory ratings (WLTP) from empirical ADAC testing.")],
             accent_color=COLOR_BLUE)

    # =========================================================================
    # SLIDE 6: Application - Architecture & Core Engine
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "3. Application", "System Architecture & Analytical Modules",
               "A three-tier pipeline from RDF graph storage to interactive fleet intelligence.")
    add_footer(s6, 6)

    add_card(s6, Inches(0.8), Inches(1.85), Inches(3.64), Inches(4.85),
             "Layer 1: Semantic Storage",
             [("RDFLib Triplestore", "In-memory triplestore loading autoecokg_triples.ttl (29,739 triples) in under 1.5 seconds."),
              ("Ontology Reasoning", "Enforces RDFS subsumption across powertrain hierarchies and observation classes."),
              ("SPARQL 1.1 Cache", "Pre-compiled query templates for sub-millisecond query execution.")],
             accent_color=COLOR_NAVY)

    add_card(s6, Inches(4.84), Inches(1.85), Inches(3.64), Inches(4.85),
             "Layer 2: Analytical Core",
             [("Euro 7 Compliance Screener", "Filters vehicle-tyre combinations against brake dust and tyre abrasion thresholds."),
              ("Fleet Microplastic Calculator", "Computes annual fleet particulate releases partitioned into waterways vs. air."),
              ("5-Criterion Pareto Engine", "Calculates non-dominated skyline configurations across economic and ecological vectors.")],
             accent_color=COLOR_CYAN)

    add_card(s6, Inches(8.88), Inches(1.85), Inches(3.64), Inches(4.85),
             "Layer 3: Interactive UI",
             [("Streamlit Dashboard (app_v2.py)", "12 interactive analytical views tailored for fleet operators and environmental regulators."),
              ("Dynamic Parameter Tuning", "Live sliders for annual mileage, electricity/fuel costs, and CO2 social shadow taxes."),
              ("Visual Pareto Frontiers", "Interactive Plotly scatter plots with multi-dimensional bubble sizing.")],
             accent_color=COLOR_GREEN)

    # =========================================================================
    # SLIDE 7: Application - Euro 7 Particulates & Battery Durability
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "3. Application", "Euro 7 Non-Exhaust Particulates & Battery Lifecycle",
               "Operationalizing Regulation EU 2024/1257 and EU 2023/1542 Battery Pass.")
    add_footer(s7, 7)

    add_card(s7, Inches(0.8), Inches(1.85), Inches(5.65), Inches(4.85),
             "Euro 7 Non-Exhaust Particulate Modeling",
             [("Brake Wear Limit Screening", "BEVs benefit from regenerative braking: mandated 3 mg/km limit vs. 7 mg/km for ICE/HEVs. AutoEcoKG verifies compliance across all 26 vehicle variants."),
              ("Tyre Abrasion Microplastics", "Microplastic emissions quantified per vehicle-tonne. AutoEcoKG models environmental fate: 90% enters roadside soil/drainage runoff, 10% stays airborne as breathable PM10/PM2.5."),
              ("Fleet Impact Calculator", "A 100-vehicle fleet driving 20,000 km/yr releases ~196 kg of microplastics annually. The engine identifies low-abrasion tyre combinations that reduce this by up to 34%.")],
             accent_color=COLOR_BLUE)

    add_card(s7, Inches(6.85), Inches(1.85), Inches(5.65), Inches(4.85),
             "Catena-X Battery Pass Durability",
             [("Milestone Durability Verification", "Tracks battery State of Health (SoH) against legal EU thresholds: >= 80% at 5 years / 100,000 km; >= 70% at 8 years / 160,000 km."),
              ("Chemistry & Capacity Tracking", "Distinguishes LFP (high cycle life, low degradation) from NMC811 (high energy density, steeper degradation curves)."),
              ("Second-Life & Residual Value", "Integrates battery health with 5-year vehicle TCO to calculate post-fleet repurposing potential (BESS stationary storage).")],
             accent_color=COLOR_GREEN)

    # =========================================================================
    # SLIDE 8: Application - 5-Criterion Pareto Skyline Fleet TCO Engine
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "3. Application", "5-Criterion Pareto Skyline Fleet TCO Engine",
               "Multi-objective fleet optimization balancing economics, climate, wear, and safety.")
    add_footer(s8, 8)

    add_card(s8, Inches(0.8), Inches(1.85), Inches(3.64), Inches(4.85),
             "5 Optimization Objectives",
             [("1. 5-Year TCO (€)", "Capital acquisition + energy/fuel + maintenance + tyre replacements + CO2 shadow tax."),
              ("2. WTW CO2 (g/km)", "Well-to-Wheel greenhouse gas intensity based on grid emissions."),
              ("3. Total PM10 (mg/km)", "Sum of exhaust, brake wear, and airborne tyre microplastics."),
              ("4. Tyre Longevity (km)", "Expected tyre service lifespan before replacement."),
              ("5. Safety Score", "ADAC driving safety and wet/dry braking performance rating.")],
             accent_color=COLOR_NAVY)

    add_card(s8, Inches(4.84), Inches(1.85), Inches(3.64), Inches(4.85),
             "Skyline Dominance Pruning",
             [("Zero-Weight Optimization", "Avoids arbitrary subjective weighting; finds mathematically non-dominated solutions."),
              ("Strict Dominance Rule", "Configuration A dominates B if A is no worse than B in all 5 criteria and strictly better in at least one."),
              ("Pruning Efficiency", "Reduces 161 configurations to a concise, high-value set of ~12 optimal fleet deployment candidates.")],
             accent_color=COLOR_BLUE)

    add_card(s8, Inches(8.88), Inches(1.85), Inches(3.64), Inches(4.85),
             "Real-World Fleet Impact",
             [("Tailored Recommendations", "Allows corporate fleets to balance CSR emissions goals against strict operational budget caps."),
              ("Dynamic Sensitivity", "Instant re-computation as carbon tax varies from 0 to 300 €/tonne and energy prices fluctuate."),
              ("Verified Results", "Evaluated and verified via automated SPARQL query templates.")],
             accent_color=COLOR_GREEN)

    # =========================================================================
    # SLIDE 9: Application - Interactive Streamlit Dashboard
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "3. Application", "Interactive Streamlit Dashboard (app_v2.py)",
               "User-facing interface for exploration, compliance verification, and decision-making.")
    add_footer(s9, 9)

    add_card(s9, Inches(0.8), Inches(1.85), Inches(5.65), Inches(4.85),
             "12 Dedicated Analytical Views",
             [("Overview & Vehicle Explorer", "Holistic fleet distributions, powertrain shares, and detailed single-vehicle dossiers."),
              ("Compare Vehicles", "Side-by-side radar and bar comparisons of real EcoTest vs. WLTP divergence."),
              ("Euro 7 & Microplastics View", "Screening tables for brake dust limits, tyre microplastic runoff, and interactive fleet load calculator."),
              ("Fleet TCO & Pareto View", "Dynamic economic sliders with real-time Pareto scatter plots and recommendation tables."),
              ("Graph Explorer & SPARQL", "Direct SPARQL endpoint with pre-configured canonical query templates.")],
             accent_color=COLOR_CYAN)

    add_card(s9, Inches(6.85), Inches(1.85), Inches(5.65), Inches(4.85),
             "Verified Streamlit Performance",
             [("Zero-Crash Headless Testing", "Verified across all 12 views using Streamlit AppTest framework with 0 exceptions."),
              ("Low-Latency In-Memory Execution", "RDFLib SPARQL queries execute interactively without lag."),
              ("Interactive Visualizations", "Rich Plotly charts supporting zoom, hover tooltips, and dynamic filtering."),
              ("Production Ready", "Launched via: .venv/bin/streamlit run src/app_v2.py.")],
             accent_color=COLOR_BLUE)

    # =========================================================================
    # SLIDE 10: Evaluation - Design & Quantitative Benchmark
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "4. Evaluation", "Evaluation Design & Quantitative Benchmark",
               "Automated verification across 42 competency questions covering all functional domains.")
    add_footer(s10, 10)

    add_card(s10, Inches(0.8), Inches(1.85), Inches(3.64), Inches(4.85),
             "Benchmark Design (CQ-01..42)",
             [("Taxonomy & Ingestion (CQ 1-8)", "Verifies vehicle names, unique IDs, WLTP emissions, and fuel consumption divergence gaps."),
              ("Tyre Metrics & Joins (CQ 9-22)", "Validates abrasion observations, ascending rankings, safety-abrasion joins, and provenance."),
              ("Recommendation Logic (CQ 23-32)", "Tests balanced multi-criteria rankings, dimension filtering, and edge cases."),
              ("Input Validation (CQ 33-37)", "Enforces rejection of invalid weights, thresholds, dimensions, and unknown SPARQL queries.")],
             accent_color=COLOR_NAVY)

    add_card(s10, Inches(4.84), Inches(1.85), Inches(3.64), Inches(4.85),
             "AutoEcoKG 2.0 Tests (CQ 38-42)",
             [("CQ-38: Euro 7 Brake Limits", "Verifies presence of brake dust nodes and BEV 3 mg/km threshold compliance."),
              ("CQ-39: Microplastic Consistency", "Mathematically verifies 90/10 environmental partitioning across fleet calculations."),
              ("CQ-40: Battery Durability", "Confirms battery SoH observations conform to Euro 7 5-year/80% milestone."),
              ("CQ-41: Pareto Skyline TCO", "Validates that multi-criteria skyline query returns valid, non-dominated configurations."),
              ("CQ-42: Epistemic Divergence", "Verifies 3-tier divergence (lab vs real vs delta).")],
             accent_color=COLOR_CYAN)

    add_card(s10, Inches(8.88), Inches(1.85), Inches(3.64), Inches(4.85),
             "Quantitative Results",
             [("Total Tests", "42 Competency Questions"),
              ("Passed", "42 / 42 (100.0% Pass Rate)"),
              ("Failed", "0 Failures"),
              ("SHACL Status", "shacl_conforms: True (0 errors)"),
              ("Query Latency", "Sub-millisecond to low-millisecond execution across 29,739 triples"),
              ("Test Suite", "Automated execution via src/evaluate.py")],
             accent_color=COLOR_GREEN)

    # =========================================================================
    # SLIDE 11: Evaluation - Qualitative Findings & Insights
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "4. Evaluation", "Qualitative Findings & Automotive Insights",
               "Discoveries surfaced by querying the unified environmental knowledge graph.")
    add_footer(s11, 11)

    add_card(s11, Inches(0.8), Inches(1.85), Inches(3.64), Inches(4.85),
             "1. Epistemic Divergence",
             [("Real-World Consumption Gap", "Combustion models like Renault Espace (+26%) and Hyundai Tucson exhibit dramatic divergence above official WLTP ratings."),
              ("High-Speed & Thermal Penalty", "BEVs show significant range reduction during winter highway cycles due to cabin heating and air resistance."),
              ("Decision Value", "Provides fleet buyers with unvarnished real-world cost and emissions baselines.")],
             accent_color=COLOR_RED)

    add_card(s11, Inches(4.84), Inches(1.85), Inches(3.64), Inches(4.85),
             "2. The BEV Mass Paradox",
             [("Regenerative Brake Benefit", "Electric vehicles cut brake dust by >55%, easily beating the stringent 3 mg/km Euro 7 limit."),
              ("Tyre Abrasion Penalty", "Heavier battery mass increases tyre wear by 12% to 18%, generating more microplastics."),
              ("Mitigation Insight", "Fitting premium low-abrasion tyres (e.g. Michelin e.Primacy) resolves the paradox, achieving dual compliance.")],
             accent_color=COLOR_BLUE)

    add_card(s11, Inches(8.88), Inches(1.85), Inches(3.64), Inches(4.85),
             "3. Optimal Pareto Fleet Picks",
             [("Best Overall Compromise", "Compact BEVs paired with low-abrasion tyres dominate the Pareto frontier under €100+/t CO2 shadow tax."),
              ("Long-Distance Workhorses", "High-efficiency diesels remain Pareto-optimal only where annual mileage exceeds 45,000 km in non-LEZ corridors."),
              ("Transparent Explanations", "Every recommendation is backed by transparent graph provenance.")],
             accent_color=COLOR_GREEN)

    # =========================================================================
    # SLIDE 12: Conclusion & Reflection
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "5. Conclusion", "Project Summary, Reflection & Future Outlook",
               "Learnings from building AutoEcoKG 2.0 and future research directions.")
    add_footer(s12, 12)

    add_card(s12, Inches(0.8), Inches(1.85), Inches(3.64), Inches(4.85),
             "Project Wrap-Up",
             [("Successful Delivery", "Created a graph-native intelligence platform connecting 29,739 triples across vehicles, tyres, and regulations."),
              ("Regulatory Impact", "First KG operationalizing Euro 7 non-exhaust particulates and Catena-X Battery Pass."),
              ("Practical Utility", "Interactive Streamlit dashboard ready for corporate and municipal fleet procurement.")],
             accent_color=COLOR_GREEN)

    add_card(s12, Inches(4.84), Inches(1.85), Inches(3.64), Inches(4.85),
             "Challenges & Reflection",
             [("PDF Extraction Variance", "ADAC reports have minor layout variations across years; required resilient multi-strategy regex scrapers."),
              ("Spatial Dispersion Modeling", "Microplastic runoff modeling currently uses macro ratios (90/10); fine-grained dispersion requires GeoSPARQL."),
              ("What We'd Do Differently", "Adopt native graph ETL tooling (e.g. R2RML / YARRRML) upfront for higher throughput.")],
             accent_color=COLOR_BLUE)

    add_card(s12, Inches(8.88), Inches(1.85), Inches(3.64), Inches(4.85),
             "Future Outlook",
             [("Real-Time Telematics", "Ingest live CAN-bus and OBD-II telemetry via COVESA VSS over MQTT/Kafka into dynamic triples."),
              ("Catena-X Federation", "Connect via Eclipse Dataspace Connector (EDC) to federated OEM digital battery passports."),
              ("Graph Machine Learning", "Train Link Prediction and Node Classification models for predictive component wear.")],
             accent_color=COLOR_CYAN)

    # Save presentation
    output_path = "/Users/riddhadipta/antigravity-test/AutoEcoKG/report/AutoEcoKG_2.0_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved to: {output_path}")


if __name__ == "__main__":
    create_deck()
