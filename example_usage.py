# -*- coding: utf-8 -*-
"""
Example usage of GlanceVisualLookVirtualTryOnCurator
Demonstrates outfit styling across varying aesthetic vectors and weather.
"""

from client import GlanceVisualLookVirtualTryOnCurator

def main():
    curator = GlanceVisualLookVirtualTryOnCurator()

    test_profiles = [
        {
            "name": "Profile A: Milan Autumn Business Gala (Quiet Luxury Focus)",
            "aesthetics": {"Quiet Luxury": 0.95, "Minimalist": 0.85, "Streetwear": 0.05},
            "temp": 12.0,
            "occasion": "EVENING_GALA"
        },
        {
            "name": "Profile B: Summer Weekend Coastal Casual",
            "aesthetics": {"Minimalist": 0.90, "Coastal Chic": 0.85, "Quiet Luxury": 0.60},
            "temp": 28.0,
            "occasion": "CASUAL_WEEKEND"
        }
    ]

    print("================================================================")
    print("Glance Visual Look & Virtual Try-On Curator - Live Runs")
    print("================================================================\n")

    for p in test_profiles:
        res = curator.curate_outfit_lookbook(
            user_aesthetic_vector=p["aesthetics"],
            ambient_temperature_c=p["temp"],
            target_occasion=p["occasion"]
        )
        print(f"[{p['name']}]")
        print(f"  Lookbook ID            : {res['curated_outfit_id']}")
        print(f"  Overall Compatibility  : {res['overall_compatibility_pct']}% ({res['style_coherence_tier']})")
        print(f"  Color Harmony Index    : {res['color_harmony_index']}")
        print(f"  Thermal Comfort Index  : {res['thermal_comfort_index']}")
        print(f"  Outfit Total Value     : ${res['outfit_total_price_usd']:,.2f}")
        print(f"  Hero Showcase Item     : {res['hero_item']['brand']} - {res['hero_item']['name']} (${res['hero_item']['price_usd']})")
        print("  Ensemble Breakdown:")
        for item in res["selected_apparel_ensemble"]:
            print(f"    * [{item['slot'].upper():<10}] {item['brand']:<20} {item['name']:<35} (${item['price_usd']})")
        print()

if __name__ == "__main__":
    main()
