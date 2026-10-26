# -*- coding: utf-8 -*-
"""
Glance Visual Look & Virtual Try-On Curator Client
Synthesizes context-aware fashion outfits and personalized editorial lookbooks matching user aesthetics, weather, and occasion.
Zero external dependencies -- Python 3.9+ standard library only.
"""

import math
from typing import Dict, Any, List

class GlanceVisualLookVirtualTryOnCurator:
    """
    Curates personalized fashion looks and simulates virtual styling compatibility
    across multi-dimensional aesthetic vectors, thermal comfort, and color harmony.
    """

    OCCASION_FORMALITY_MAP = {
        "CASUAL_WEEKEND": 0.2,
        "SMART_CASUAL": 0.5,
        "BUSINESS_FORMAL": 0.8,
        "EVENING_GALA": 0.95,
        "ATHLETIC_FITNESS": 0.1
    }

    def __init__(self):
        pass

    def calculate_cosine_similarity(self, vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
        """Computes cosine similarity between two feature weight dictionaries."""
        all_keys = set(vec_a.keys()).union(set(vec_b.keys()))
        if not all_keys:
            return 0.5
        dot_product = sum(vec_a.get(k, 0.0) * vec_b.get(k, 0.0) for k in all_keys)
        mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
        mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
        if mag_a == 0.0 or mag_b == 0.0:
            return 0.5
        return max(0.0, min(1.0, dot_product / (mag_a * mag_b)))

    def calculate_color_harmony(self, color_hues: List[float]) -> float:
        """
        Evaluates color harmony based on circular hue differences on the color wheel (0-360 deg).
        High scores for monochromatic (close angles), complementary (approx 180 deg), or triad (approx 120 deg).
        """
        if len(color_hues) < 2:
            return 0.85
        diffs = []
        for i in range(len(color_hues)):
            for j in range(i + 1, len(color_hues)):
                d = abs(color_hues[i] - color_hues[j]) % 360
                d = min(d, 360 - d)
                diffs.append(d)

        # Average harmony score across pairs
        pair_scores = []
        for d in diffs:
            if d <= 30: # Monochromatic / Analogous
                pair_scores.append(0.92)
            elif 110 <= d <= 130: # Triadic
                pair_scores.append(0.85)
            elif 165 <= d <= 195: # Complementary
                pair_scores.append(0.95)
            else: # Neutral / intermediate
                pair_scores.append(0.68)

        return sum(pair_scores) / len(pair_scores)

    def calculate_thermal_comfort(self, ambient_temp_c: float, outfit_thermal_weight: float) -> float:
        """
        Gaussian comfort curve matching outfit insulation (0=summer ultra-light to 1=heavy winter parka)
        against ambient temperature.
        """
        # Optimal thermal weight: 0.0 at 35C, 1.0 at -5C
        optimal_weight = max(0.0, min(1.0, (32.0 - ambient_temp_c) / 35.0))
        delta = abs(outfit_thermal_weight - optimal_weight)
        return math.exp(-3.5 * (delta ** 2))

    def curate_outfit_lookbook(
        self,
        user_aesthetic_vector: Dict[str, float],
        ambient_temperature_c: float = 20.0,
        target_occasion: str = "SMART_CASUAL",
        candidate_items: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Curates candidate fashion apparel items into a cohesive editorial lookbook.
        """
        if candidate_items is None:
            candidate_items = [
                {"id": "TOP-101", "name": "Cashmere Knit Turtleneck", "slot": "top", "hue": 35.0, "thermal_weight": 0.65, "formality": 0.60, "style": {"Quiet Luxury": 0.90, "Minimalist": 0.80, "Streetwear": 0.10}, "brand": "Brunello Cucinelli", "price_usd": 1250},
                {"id": "BTM-202", "name": "Tailored Pleated Wool Trousers", "slot": "bottom", "hue": 40.0, "thermal_weight": 0.55, "formality": 0.70, "style": {"Quiet Luxury": 0.85, "Minimalist": 0.85, "Streetwear": 0.20}, "brand": "Loro Piana", "price_usd": 980},
                {"id": "OUT-303", "name": "Double-Breasted Camel Hair Coat", "slot": "outerwear", "hue": 30.0, "thermal_weight": 0.80, "formality": 0.75, "style": {"Quiet Luxury": 0.95, "Minimalist": 0.75, "Streetwear": 0.15}, "brand": "Max Mara", "price_usd": 2400},
                {"id": "SHOE-404", "name": "Italian Handcrafted Leather Loafers", "slot": "footwear", "hue": 25.0, "thermal_weight": 0.40, "formality": 0.70, "style": {"Quiet Luxury": 0.80, "Minimalist": 0.70, "Streetwear": 0.10}, "brand": "Tod's", "price_usd": 750},
                {"id": "ACC-505", "name": "Titanium Minimalist Chronograph", "slot": "accessory", "hue": 210.0, "thermal_weight": 0.05, "formality": 0.80, "style": {"Quiet Luxury": 0.90, "Minimalist": 0.90, "Streetwear": 0.30}, "brand": "Cartier", "price_usd": 4200}
            ]

        # Group items by slot
        slots = {}
        for item in candidate_items:
            s = item.get("slot", "misc")
            slots.setdefault(s, []).append(item)

        target_formality = self.OCCASION_FORMALITY_MAP.get(target_occasion.upper(), 0.5)

        # Score individual items
        scored_items = []
        for item in candidate_items:
            style_sim = self.calculate_cosine_similarity(user_aesthetic_vector, item.get("style", {}))
            formality_match = 1.0 - abs(item.get("formality", 0.5) - target_formality)
            item_score = 0.65 * style_sim + 0.35 * formality_match
            scored_items.append({**item, "individual_score": round(item_score, 4)})

        # Select highest scoring item per slot
        selected_slots = {}
        hues = []
        thermal_weights = []
        total_price = 0.0
        for slot_name, items in slots.items():
            best = max(items, key=lambda x: next(s["individual_score"] for s in scored_items if s["id"] == x["id"]))
            selected_slots[slot_name] = best
            hues.append(best.get("hue", 0.0))
            thermal_weights.append(best.get("thermal_weight", 0.5))
            total_price += best.get("price_usd", 0.0)

        # Ensemble outfit scores
        color_harmony = self.calculate_color_harmony(hues)
        avg_thermal_weight = sum(thermal_weights) / len(thermal_weights) if thermal_weights else 0.5
        thermal_comfort = self.calculate_thermal_comfort(ambient_temperature_c, avg_thermal_weight)

        avg_style_sim = sum(
            self.calculate_cosine_similarity(user_aesthetic_vector, it.get("style", {}))
            for it in selected_slots.values()
        ) / max(1, len(selected_slots))

        composite_look_score = (
            0.45 * avg_style_sim +
            0.30 * color_harmony +
            0.25 * thermal_comfort
        )
        compatibility_pct = round(composite_look_score * 100.0, 1)

        hero_item = max(selected_slots.values(), key=lambda x: x.get("price_usd", 0.0))

        return {
            "curated_outfit_id": f"GLANCE-LOOK-{abs(hash(str(user_aesthetic_vector))) % 100000:05d}",
            "overall_compatibility_pct": compatibility_pct,
            "style_coherence_tier": "EDITORIAL_EXCELLENCE" if compatibility_pct >= 85 else ("HIGH_HARMONY" if compatibility_pct >= 70 else "MODERATE"),
            "color_harmony_index": round(color_harmony, 3),
            "thermal_comfort_index": round(thermal_comfort, 3),
            "target_occasion": target_occasion,
            "ambient_temp_c": ambient_temperature_c,
            "outfit_total_price_usd": round(total_price, 2),
            "hero_item": {
                "id": hero_item["id"],
                "name": hero_item["name"],
                "brand": hero_item.get("brand"),
                "price_usd": hero_item.get("price_usd")
            },
            "selected_apparel_ensemble": [
                {
                    "slot": k,
                    "item_id": v["id"],
                    "name": v["name"],
                    "brand": v.get("brand"),
                    "price_usd": v.get("price_usd"),
                    "color_hue_deg": v.get("hue")
                }
                for k, v in selected_slots.items()
            ]
        }
