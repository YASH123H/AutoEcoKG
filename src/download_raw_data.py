"""Download all ADAC vehicle and tyre source PDFs for AutoEcoKG."""
import argparse
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / 'data' / 'raw'

SOURCES = {
    'tyres': {
        'adac_summer_tyres_2025.pdf': 'https://assets.adac.de/image/upload/v1740570807/ADAC-eV/KOR/Text/PDF/ADAC_BRO_Reifenratgeber_Sommer_2025_148x210mm_rz_web_gfo2ap.pdf',
        'adac_tyre_abrasion_2023_2025.pdf': 'https://assets.adac.de/image/upload/v1749035559/ADAC-eV/KOR/Text/PDF/33477_fnoizf.pdf',
    },
    'adac': {
        'Audi A3 Sportback1.5TFSIe.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6453-audi-a3-sportback-40-tfsi-e-s-line-s-tronic/audi-a3-sportback-40-tfsi-e-s-line-s-tronic.pdf',
        'AudiA3Sportback_Autotest2.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6355-audi-a3-sportback-35-tfsi-s-line-s-tronic/audi-a3-sportback-35-tfsi-s-line-s-tronic.pdf',
        'BMW 520i M Sportpaket.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6406-bmw-520i-m-sportpaket-steptronic/bmw-520i-m-sportpaket-steptronic.pdf',
        'BYDAtto3EvoDesign.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6534-byd-atto-3-design/byd-atto-3-design.pdf',
        'HondaCivic2.0i.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6241-honda-civic-20-i-mmd-advance-ecvt/honda-civic-20-i-mmd-advance-ecvt.pdf',
        'Hyundai Tucson 1.6 CRDi.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6467-hyundai-tucson-16-crdi-prime-2wd-dct/hyundai-tucson-16-crdi-prime-2wd-dct.pdf',
        'Hyundai i30 1.5 T-GDI.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6473-hyundai-i30-15-t-gdi-mhev-n-line-dct/hyundai-i30-15-t-gdi-mhev-n-line-dct.pdf',
        'Kia EV3 (58.3 kWh) Earth.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6498-kia-ev3-583-kwh-earth/kia-ev3-583-kwh-earth.pdf',
        'Mazda 3 2.5 e-Skyactiv G 140 Takumi.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6493-mazda-3-25-e-skyactiv-g-140-takumi/mazda-3-25-e-skyactiv-g-140-takumi.pdf',
        'Mercedes-Benz CLA 250+.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6581-mercedes-benz-cla-coupe-250-eq-progressive/mercedes-benz-cla-coupe-250-eq-progressive.pdf',
        'Nissan Micra 52 kWh Evolve.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6617-nissan-micra-52-kwh-evolve/nissan-micra-52-kwh-evolve.pdf',
        'Renault Espace E-Tech Full Hybrid 200.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6568-renault-espace-e-tech-full-hybrid-200-iconic-multi-mode-automatik-7-sitzer/renault-espace-e-tech-full-hybrid-200-iconic-multi-mode-automatik-7-sitzer.pdf',
        'Renault R4 E-Tech Electric 150 Comfort Range.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6550-renault-r4-e-tech-electric-150-comfort-range-52-kwh-iconic/renault-r4-e-tech-electric-150-comfort-range-52-kwh-iconic.pdf',
        'Renault R5 E-Tech Electric 150 Comfort Range.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6482-renault-r5-e-tech-electric-150-comfort-range-52-kwh-techno/renault-r5-e-tech-electric-150-comfort-range-52-kwh-techno.pdf',
        'Tesla Model 3.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6351-tesla-model-3-maximale-reichweite-allradantrieb/tesla-model-3-maximale-reichweite-allradantrieb.pdf',
        'Tesla Model Y Maximum Range.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6477-tesla-model-y-maximale-reichweite-hinterradantrieb/tesla-model-y-maximale-reichweite-hinterradantrieb.pdf',
        'Toyota Yaris 1.5 Hybrid 130 Style PLUS CVT.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6389-toyota-yaris-15-hybrid-130-style-plus-cvt/toyota-yaris-15-hybrid-130-style-plus-cvt.pdf',
        'Volkswagen Golf 1.5 TSI Life.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6417-volkswagen-golf-15-tsi-life/volkswagen-golf-15-tsi-life.pdf',
        'Volkswagen Golf 1.5 eHybrid Style DSG.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6460-volkswagen-golf-15-ehybrid-style-dsg/volkswagen-golf-15-ehybrid-style-dsg.pdf',
        'Volvo XC60 T6 Ultra Dark AWD.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6475-volvo-xc60-t6-ultra-dark-awd-geartronic/volvo-xc60-t6-ultra-dark-awd-geartronic.pdf',
        'Škoda Kodiaq 2.0 TDI Selection DSG.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6459-skoda-kodiaq-20-tdi-selection-dsg/skoda-kodiaq-20-tdi-selection-dsg.pdf',
        'Škoda Octavia Combi 1.5 TSI mHEV Selection DSG.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6419-skoda-octavia-combi-15-tsi-mhev-selection-dsg/skoda-octavia-combi-15-tsi-mhev-selection-dsg.pdf',
        'Škoda Octavia Combi 2.0 TDI SCR Selection DSG.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6442-skoda-octavia-combi-20-tdi-scr-selection-dsg/skoda-octavia-combi-20-tdi-scr-selection-dsg.pdf',
        'Škoda Superb 2.0 TDI SCR L&K 4x4 DSG.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6485-skoda-superb-20-tdi-scr-lk-4x4-dsg/skoda-superb-20-tdi-scr-lk-4x4-dsg.pdf',
        'Škoda Superb Combi 2.0 TDI SCR Selection 4x4 DSG.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6447-skoda-superb-combi-20-tdi-scr-selection-4x4-dsg/skoda-superb-combi-20-tdi-scr-selection-4x4-dsg.pdf',
        'Škoda Superb Combi 2.0 TDI SCR Selection DSG.pdf': 'https://assets.adac.de/image/upload/Autodatenbank/Autotest/at6420-skoda-superb-combi-20-tdi-scr-selection-dsg/skoda-superb-combi-20-tdi-scr-selection-dsg.pdf',
    }
}


def download_file(url: str, dest: Path, force: bool = False):
    if dest.exists() and not force:
        print(f"[EXISTS] {dest.name}")
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; AutoEcoKG/1.0)'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read()
            if not content.startswith(b'%PDF'):
                print(f"[FAIL] {dest.name} - response is not a valid PDF")
                return False
            dest.write_bytes(content)
            print(f"[DOWNLOADED] {dest.name} ({len(content)} bytes)")
            return True
    except Exception as e:
        print(f"[ERROR] {dest.name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--force', action='store_true', help='Force re-download even if files already exist')
    args = parser.parse_args()

    total = 0
    success = 0
    for category, files in SOURCES.items():
        target_dir = DATA_RAW / category
        for filename, url in files.items():
            total += 1
            dest = target_dir / filename
            if download_file(url, dest, force=args.force):
                success += 1

    print(f"\nDownload summary: {success}/{total} files present and valid.")
    return 0 if success == total else 1


if __name__ == '__main__':
    sys.exit(main())
