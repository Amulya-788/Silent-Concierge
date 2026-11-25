import os
import json
import time
import urllib.parse
import pandas as pd
import numpy as np

# Clean data directory for CSV tables and runtime state packet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Lock seed for 100% deterministic DevFest demos
np.random.seed(42)

# Module-level in-memory cache for sub-5ms edge latency
_EDGE_RAM_CACHE = None

# ==============================================================================
# 1. ZERO-FAIL LUXURY IMAGE URL ENGINE (Offline-Safe SVG Data URIs)
# ==============================================================================
def build_luxury_image_url(style_code, item_name, category, finish, climate, origin, hex_bg, hex_accent):
    """
    Generates an unbreakable, zero-latency data:image/svg+xml URL for each Master Style Code.
    Never throws a 404/403 error and renders instantly inside HTML/Streamlit <img> tags.
    """
    short_title = item_name[:28] + ("..." if len(item_name) > 28 else "")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 260" width="100%" height="100%">
        <rect width="400" height="260" fill="{hex_bg}"/>
        <rect x="12" y="12" width="376" height="236" fill="none" stroke="{hex_accent}" stroke-width="1.2" opacity="0.6"/>
        <text x="28" y="38" fill="{hex_accent}" font-family="Georgia, serif" font-size="10" letter-spacing="2">
            {style_code} • {origin.upper()}
        </text>
        <circle cx="200" cy="115" r="42" fill="none" stroke="{hex_accent}" stroke-width="1" stroke-dasharray="3,3"/>
        <text x="200" y="119" fill="{hex_accent}" font-family="Georgia, serif" font-size="13" text-anchor="middle" letter-spacing="3">
            {category.upper()}
        </text>
        <text x="200" y="192" fill="#FFFFFF" font-family="Georgia, serif" font-size="14" text-anchor="middle" letter-spacing="1">
            {short_title}
        </text>
        <text x="200" y="218" fill="{hex_accent}" font-family=" monospace" font-size="11" text-anchor="middle" letter-spacing="1.5">
            [{climate.upper()} // {finish.upper()}]
        </text>
    </svg>"""
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)


def _build_vip_profiles():
    client_ids = [f"VIP_{str(i).zfill(3)}" for i in range(1, 51)]
    real_names = [
        "Mme. Camille Laurent", "Lady Eleanor Vance", "Dr.Amulya C A", "Sig.ra Sofia Conti",
        "Mme. Chloé Dubois", "Ms. Mei-Ling Zhou", "Princess Layla Al-Mansoor", "Mme. Isabelle Moreau"
    ]
    rtw_sizes = ["FR 34", "FR 36", "FR 38", "FR 40"]
    shoe_sizes = ["EU 36", "EU 37", "EU 38", "EU 39"]
    sa_notes = [
        "Prefers private salon seating; loves structured shoulders & Florence leathercraft. Never show loud logos on coats.",
        "Collects high-shine evening clutches and Rainy-season trenches. Travels frequently between Paris and Bengaluru.",
        "Strict quiet-luxury purist for Winter/Formal office wear, but loves high-glamour Place Vendôme jewelry for Galas.",
        "Appreciates Scottish cashmere and simple matte textures; occasionally buys oversized men's/large sizes as family gifts."
    ]

    vip_profiles = {}
    for idx, cid in enumerate(client_ids):
        # Notice: Even-indexed VIPs (quiet luxury) own 005 & 007 in RTW, leaving 008 (Bar Jacket) as an UNOWNED 88%+ quiet-luxury discovery!
        # Odd-indexed VIPs (glamour/statement) own 006 & 009 in RTW, leaving 010 (Silk Kaftan) as an UNOWNED discovery!
        vip_profiles[cid] = {
            "client_id": cid,
            "decrypted_name": f"{real_names[idx % len(real_names)]} ({cid})",
            "home_boutique": ["Paris Avenue Montaigne", "Milan Via Montenapoleone", "London New Bond St", "Tokyo Ginza"][idx % 4],
            "core_rtw_size": rtw_sizes[idx % len(rtw_sizes)],
            "core_shoe_size": shoe_sizes[idx % len(shoe_sizes)],
            "paris_sa_handoff_note": sa_notes[idx % len(sa_notes)],
            "preferred_styles": (
                ["STYLE_CD_001", "STYLE_CD_005", "STYLE_CD_007", "STYLE_CD_011", "STYLE_CD_012"]
                if idx % 2 == 0 else
                ["STYLE_CD_002", "STYLE_CD_006", "STYLE_CD_009", "STYLE_CD_011", "STYLE_CD_012"]
            )
        }
    return vip_profiles, rtw_sizes, shoe_sizes


# ==============================================================================
# 2. STORAGE LAYER: MASTER PIM CATALOG, VIP HISTORY & LOCAL RFID INVENTORY
# ==============================================================================
def initialize_storage_databases(force_rebuild=False):
    """
    Creates or loads from RAM cache the 3 core relational CSV tables:
    1. master_product_catalog.csv (Paris PIM: Style Codes, 1-5 Scores, Climate, Shiny/Simple, Image URL)
    2. vip_global_history.csv     (Global purchases with Buyer Size & Gift detection)
    3. local_rfid_inventory.csv   (Bengaluru Stockroom: Only holds RFID_SKU, Style Code, Size, Aging)
    """
    global _EDGE_RAM_CACHE
    if not force_rebuild and _EDGE_RAM_CACHE is not None:
        return _EDGE_RAM_CACHE

    vip_profiles, rtw_sizes, shoe_sizes = _build_vip_profiles()

    if not force_rebuild and all(
        os.path.exists(f) for f in (os.path.join(DATA_DIR, "master_product_catalog.csv"), os.path.join(DATA_DIR, "vip_global_history.csv"), os.path.join(DATA_DIR, "local_rfid_inventory.csv"))
    ):
        catalog_df = pd.read_csv(os.path.join(DATA_DIR, "master_product_catalog.csv"))
        vip_history_df = pd.read_csv(os.path.join(DATA_DIR, "vip_global_history.csv"))
        rfid_df = pd.read_csv(os.path.join(DATA_DIR, "local_rfid_inventory.csv"))
        _EDGE_RAM_CACHE = (catalog_df, vip_history_df, rfid_df, vip_profiles)
        return _EDGE_RAM_CACHE

    np.random.seed(42)

    # --- TABLE 1: PARIS MASTER PRODUCT CATALOG (12 Grounded Luxury Templates) ---
    pim_templates = [
        # HANDBAGS
        ("STYLE_CD_001", "Lady Crocodile Mini Bag", "Handbags", "Grand", "Shiny", "Florence Leathercraft", [5, 2, 5, 1, 1, 5], 19500, "#141414", "#D4AF37"),
        ("STYLE_CD_002", "Satin Crystal Minaudière Clutch", "Handbags", "Grand", "Shiny", "Paris Atelier", [5, 1, 5, 1, 5, 5], 7800, "#2A0818", "#F3E5AB"),
        ("STYLE_CD_003", "Matte Calfskin Quiet Tote", "Handbags", "Formal", "Simple", "Florence Leathercraft", [5, 1, 1, 3, 1, 1], 6400, "#1C1C1C", "#A8A8A8"),
        ("STYLE_CD_004", "Oblique Monogram Weekender", "Handbags", "Summer", "Simple", "Florence Leathercraft", [3, 5, 3, 4, 3, 2], 4200, "#1B263B", "#E0E1DD"),

        # READY-TO-WEAR (Summer, Winter, Rainy/Monsoon, Formal, Grand)
        ("STYLE_CD_005", "Hydro-Treated Gabardine Trench", "Ready-to-Wear", "Rainy", "Simple", "Paris Atelier", [5, 1, 2, 5, 2, 1], 5900, "#1F2421", "#C5C392"),
        ("STYLE_CD_006", "Patent Monogram Rain Anorak", "Ready-to-Wear", "Rainy", "Shiny", "Milanese Tailoring", [4, 4, 3, 2, 1, 5], 4600, "#0D1B2A", "#90E0EF"),
        ("STYLE_CD_007", "Double-Face Cashmere Coat", "Ready-to-Wear", "Winter", "Simple", "Scottish Highlands", [5, 1, 1, 5, 1, 1], 11200, "#1A1817", "#D6CCC2"),
        ("STYLE_CD_008", "Tailored Silk-Wool Bar Jacket", "Ready-to-Wear", "Formal", "Simple", "Paris Atelier", [5, 1, 3, 3, 1, 2], 5400, "#161616", "#E5E5E5"),
        ("STYLE_CD_009", "Sequined Gold Bouclé Cropped Jacket", "Ready-to-Wear", "Grand", "Shiny", "Paris Atelier", [5, 3, 5, 1, 4, 5], 9200, "#23190F", "#FFD166"),
        ("STYLE_CD_010", "Pleated Silk Chiffon Resort Kaftan", "Ready-to-Wear", "Summer", "Shiny", "Milanese Tailoring", [4, 2, 3, 5, 5, 4], 4900, "#2B192E", "#FF9F1C"),

        # SHOES & JEWELRY
        ("STYLE_CD_011", "Patent Leather Slingback Pump", "Shoes", "Formal", "Shiny", "Florence Leathercraft", [4, 2, 2, 2, 1, 4], 1450, "#1A1A1D", "#C3073F"),
        ("STYLE_CD_012", "Place Vendôme Diamond Choker", "Jewelry", "Grand", "Shiny", "Place Vendôme Jeweler", [5, 1, 5, 1, 1, 5], 23500, "#0B0C10", "#66FCF1"),
    ]

    catalog_rows = []
    for row in pim_templates:
        s_code, name, cat, clim, fin, orig, traits, price, bg, acc = row
        img_url = build_luxury_image_url(s_code, name, cat, fin, clim, orig, bg, acc)
        catalog_rows.append({
            "style_code": s_code,
            "item_name": name,
            "item_category": cat,
            "climate_tag": clim,
            "surface_finish": fin,
            "craftsmanship_origin": orig,
            "material_tier": traits[0],
            "logo_prominence": traits[1],
            "detail_complexity": traits[2],
            "silhouette_length": traits[3],
            "color_palette": traits[4],
            "shiny_index": traits[5],
            "base_price_usd": price,
            "image_url": img_url
        })

    catalog_df = pd.DataFrame(catalog_rows)
    catalog_df.to_csv(os.path.join(DATA_DIR, "master_product_catalog.csv"), index=False)

    # --- TABLE 2: VIP METADATA & GLOBAL PURCHASE HISTORY (With Size-Delta Gift Detection) ---
    client_ids = sorted(list(vip_profiles.keys()))
    history_rows = []
    for i in range(2500):
        cid = np.random.choice(client_ids)
        prof = vip_profiles[cid]
        is_gift_scenario = np.random.choice([0, 1], p=[0.85, 0.15])

        if is_gift_scenario == 0:
            s_code = np.random.choice(prof["preferred_styles"])
            cat = catalog_df.loc[catalog_df["style_code"] == s_code, "item_category"].values[0]
            purchased_size = prof["core_rtw_size"] if cat == "Ready-to-Wear" else (
                prof["core_shoe_size"] if cat == "Shoes" else "ONE_SIZE"
            )
            gift_box_flag = 0
        else:
            s_code = np.random.choice(catalog_df["style_code"].values)
            cat = catalog_df.loc[catalog_df["style_code"] == s_code, "item_category"].values[0]
            purchased_size = "FR 44 (GIFT)" if cat == "Ready-to-Wear" else (
                "EU 41 (GIFT)" if cat == "Shoes" else "ONE_SIZE"
            )
            gift_box_flag = 1

        history_rows.append({
            "transaction_id": f"TXN_{20000 + i}",
            "client_id": cid,
            "style_code": s_code,
            "purchased_size": purchased_size,
            "core_rtw_size": prof["core_rtw_size"],
            "core_shoe_size": prof["core_shoe_size"],
            "gift_receipt_flag": gift_box_flag,
            "purchase_city": np.random.choice(["Paris", "Milan", "Tokyo", "London"])
        })

    vip_history_df = pd.DataFrame(history_rows)
    vip_history_df.to_csv(os.path.join(DATA_DIR, "vip_global_history.csv"), index=False)

    # --- TABLE 3: BENGALURU BACKROOM PASSIVE RFID INVENTORY (60 Physical Units) ---
    # Use (i // len(catalog_df)) % 4 for size assignment so every style_code has all 4 size variants in stock
    rfid_rows = []
    for i in range(60):
        s_code = catalog_df["style_code"].iloc[i % len(catalog_df)]
        cat = catalog_df.loc[catalog_df["style_code"] == s_code, "item_category"].values[0]
        size_cycle_idx = (i // len(catalog_df)) % 4
        stock_size = rtw_sizes[size_cycle_idx] if cat == "Ready-to-Wear" else (
            shoe_sizes[size_cycle_idx] if cat == "Shoes" else "ONE_SIZE"
        )
        rfid_rows.append({
            "rfid_sku": f"DIOR_BLR_{600 + i}",
            "style_code": s_code,
            "stock_size": stock_size,
            "days_on_floor": int(np.random.randint(7, 140))
        })

    rfid_df = pd.DataFrame(rfid_rows)
    rfid_df.to_csv(os.path.join(DATA_DIR, "local_rfid_inventory.csv"), index=False)

    _EDGE_RAM_CACHE = (catalog_df, vip_history_df, rfid_df, vip_profiles)
    return _EDGE_RAM_CACHE


# ==============================================================================
# 3. CORE EDGE ENGINE: BLE PRIVACY UNLOCK, SIZE-DELTA FILTER & CATEGORY MATH
# ==============================================================================
def execute_silent_concierge_scan(
    target_vip="VIP_007",
    trigger_mode="LAYER_1_DOORWAY_BLE",   # "LOCKED_AT_REST", "LAYER_1_DOORWAY_BLE", "TOMORROW_24H_APPOINTMENT_KEY"
    selected_category="Ready-to-Wear",    # "Handbags", "Ready-to-Wear", "Shoes", "Jewelry"
    climate_filter="All",                 # "All", "Summer", "Winter", "Rainy", "Formal", "Grand"
    finish_filter="All",                  # "All", "Simple", "Shiny"
    prioritize_dead_stock=False
):
    catalog_df, vip_history_df, rfid_df, vip_profiles = initialize_storage_databases()
    start_ts = time.perf_counter()
    prof = vip_profiles[target_vip]

    # --- STEP A: PRIVACY PROTOCOL (Locked Code vs. BLE Arrival / 24h Tomorrow Token) ---
    if trigger_mode == "LOCKED_AT_REST":
        latency_ms = round((time.perf_counter() - start_ts) * 1000, 2)
        privacy_state = {
            "is_unlocked": False,
            "display_identity": f"{target_vip} [PII ENCRYPTED - NO ACTIVE BLE OR 24H TOKEN]",
            "home_boutique": "REDACTED (GDPR LOCK)",
            "paris_sa_note": "🔒 Locked. Requires Physical Doorway BLE Handshake or 24-Hour Tomorrow Appointment Key.",
            "ble_telemetry": [
                f"[0.1ms] Edge Storage Status: {target_vip} vector stored at rest (Zero-PII GDPR Mode).",
                "[0.2ms] Identity Decryption BLOCKED: Client is not in store and no 24h Appointment Key is active."
            ]
        }
        state_packet = {
            "client_id": target_vip,
            "trigger_mode": trigger_mode,
            "selected_category": selected_category,
            "latency_ms": latency_ms,
            "gifts_filtered_out": 0,
            "core_sizes": {"rtw": "REDACTED", "shoe": "REDACTED"},
            "privacy": privacy_state,
            "category_style_dna": {},
            "past_wardrobe_items": [],
            "present_rfid_recommendations": []
        }
        with open(os.path.join(DATA_DIR, "edge_live_state.json"), "w", encoding="utf-8") as f:
            json.dump(state_packet, f, indent=2)
        return state_packet

    elif trigger_mode == "TOMORROW_24H_APPOINTMENT_KEY":
        privacy_state = {
            "is_unlocked": True,
            "display_identity": prof["decrypted_name"],
            "home_boutique": prof["home_boutique"],
            "paris_sa_note": f"🗝️ [24H PRE-ARRIVAL KEY ACTIVE] Old SA Note ({prof['home_boutique']}): \"{prof['paris_sa_handoff_note']}\"",
            "ble_telemetry": [
                f"[0.4ms] Ephemeral 24-Hour Appointment Token verified from {prof['home_boutique']}.",
                f"[1.1ms] Temporary PII Decryption granted for {prof['decrypted_name']} (Expires in 23h 59m)."
            ]
        }
    else:  # LAYER_1_DOORWAY_BLE
        privacy_state = {
            "is_unlocked": True,
            "display_identity": prof["decrypted_name"],
            "home_boutique": prof["home_boutique"],
            "paris_sa_note": f"📡 [LIVE BLE ARRIVAL UNLOCK] Sister-Boutique Brief ({prof['home_boutique']}): \"{prof['paris_sa_handoff_note']}\"",
            "ble_telemetry": [
                "[0.3ms] Doorway Ceiling iBeacon (UUID: DIOR-BLR-DOOR01) detected Apple Wallet PassKit wake-up.",
                f"[1.2ms] Encrypted PassKit Token matched to {target_vip} -> In-Store Arrival Verified.",
                f"[1.8ms] Ephemeral PII Unlocked: {prof['decrypted_name']} | Core Size: {prof['core_rtw_size']} / {prof['core_shoe_size']}."
            ]
        }

    # --- STEP B: RELATIONAL JOIN (Zero-Typing PIM Merge) & SIZE-DELTA GIFT FILTER ---
    vip_raw = vip_history_df.loc[vip_history_df["client_id"] == target_vip].merge(
        catalog_df, on="style_code", how="left"
    )

    personal_mask = (
        ((vip_raw["item_category"] == "Ready-to-Wear") & (vip_raw["purchased_size"] == vip_raw["core_rtw_size"])) |
        ((vip_raw["item_category"] == "Shoes") & (vip_raw["purchased_size"] == vip_raw["core_shoe_size"])) |
        (~vip_raw["item_category"].isin(["Ready-to-Wear", "Shoes"]) & (vip_raw["gift_receipt_flag"] == 0))
    )
    personal_purchases = vip_raw.loc[personal_mask].copy()
    gifts_filtered_count = int(len(vip_raw) - len(personal_purchases))

    # --- STEP C: CATEGORY-SPECIFIC PAST WARDROBE (So Bags & Coats Never Blur!) ---
    cat_past = personal_purchases.loc[personal_purchases["item_category"] == selected_category].copy()
    if cat_past.empty:
        cat_past = personal_purchases.copy()

    style_features = [
        "material_tier", "logo_prominence", "detail_complexity",
        "silhouette_length", "color_palette", "shiny_index"
    ]
    all_features = style_features + ["base_price_usd"]

    vip_category_dna = {trait: int(cat_past[trait].mode().iloc[0]) for trait in style_features}
    vip_category_dna["base_price_usd"] = int(cat_past["base_price_usd"].median())

    past_wardrobe_cards = (
        cat_past.groupby(["style_code", "item_name", "climate_tag", "surface_finish", "craftsmanship_origin", "base_price_usd", "image_url", "purchased_size"])
        .size()
        .reset_index(name="times_purchased")
        .sort_values(by="times_purchased", ascending=False)
        .head(3)
        .to_dict(orient="records")
    )
    owned_style_codes = {item["style_code"] for item in past_wardrobe_cards}

    # --- STEP D: JOIN LOCAL RFID STOCK WITH MASTER CATALOG, EXACT SIZE FILTER & MATCH ---
    live_stock = rfid_df.merge(catalog_df, on="style_code", how="left")
    cat_stock = live_stock.loc[live_stock["item_category"] == selected_category].copy()

    # Exact VIP Size Match Filter for live backroom RFID stock
    target_stock_size = (
        prof["core_rtw_size"] if selected_category == "Ready-to-Wear" else (
            prof["core_shoe_size"] if selected_category == "Shoes" else "ONE_SIZE"
        )
    )
    size_matched_stock = cat_stock.loc[cat_stock["stock_size"] == target_stock_size]
    if not size_matched_stock.empty:
        cat_stock = size_matched_stock.copy()

    if climate_filter != "All":
        sub = cat_stock.loc[cat_stock["climate_tag"] == climate_filter]
        if not sub.empty:
            cat_stock = sub.copy()

    if finish_filter != "All":
        sub = cat_stock.loc[cat_stock["surface_finish"] == finish_filter]
        if not sub.empty:
            cat_stock = sub.copy()

    if prioritize_dead_stock:
        sub = cat_stock.loc[cat_stock["days_on_floor"] >= 90]
        if not sub.empty:
            cat_stock = sub.copy()

    # Pure-NumPy Domain-locked MinMaxScaler + Sqrt-Weighted Euclidean Distance
    min_bounds = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1200.0])
    max_bounds = np.array([5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 25000.0])
    denom = max_bounds - min_bounds

    weights = np.array([0.30, 0.20, 0.15, 0.10, 0.10, 0.10, 0.05])
    sqrt_w = np.sqrt(weights)

    stock_matrix = cat_stock[all_features].to_numpy(dtype=float)
    vip_vector = np.array([[vip_category_dna[f] for f in all_features]], dtype=float)

    scaled_stock = ((stock_matrix - min_bounds) / denom) * sqrt_w
    scaled_vip = ((vip_vector - min_bounds) / denom) * sqrt_w

    distances = np.linalg.norm(scaled_stock - scaled_vip, axis=1)
    cat_stock["style_distance"] = distances
    cat_stock["match_pct"] = np.clip(np.round((1.0 - (cat_stock["style_distance"] / 0.85)) * 100, 1), 65.0, 99.8)

    # Rank strictly by true Style DNA distance, then place NEW unowned items within the top matches at Rank #1
    top_present_matches = (
        cat_stock.sort_values(by="style_distance", ascending=True)
        .drop_duplicates(subset=["style_code"])
        .head(3)
        .to_dict(orient="records")
    )
    top_present_matches.sort(key=lambda r: (r["style_code"] in owned_style_codes, r["style_distance"]))

    latency_ms = round((time.perf_counter() - start_ts) * 1000, 2)
    privacy_state["ble_telemetry"].append(
        f"[{latency_ms}ms] Filtered {gifts_filtered_count} Size-Delta Gifts | Matched '{selected_category}' ({target_stock_size}) RFID Stock."
    )

    # --- STEP E: WRITE SYNC PACKET TO edge_live_state.json ---
    state_packet = {
        "client_id": target_vip,
        "trigger_mode": trigger_mode,
        "selected_category": selected_category,
        "latency_ms": latency_ms,
        "gifts_filtered_out": gifts_filtered_count,
        "core_sizes": {"rtw": prof["core_rtw_size"], "shoe": prof["core_shoe_size"]},
        "privacy": privacy_state,
        "category_style_dna": vip_category_dna,
        "past_wardrobe_items": past_wardrobe_cards,
        "present_rfid_recommendations": top_present_matches
    }

    with open(os.path.join(DATA_DIR, "edge_live_state.json"), "w", encoding="utf-8") as f:
        json.dump(state_packet, f, indent=2)

    return state_packet


# ==============================================================================
# 4. TERMINAL TEST RUNNER (Verify Backend Standalone Before Connecting UI)
# ==============================================================================
if __name__ == "__main__":
    initialize_storage_databases(force_rebuild=True)
    state = execute_silent_concierge_scan(
        target_vip="VIP_007",
        trigger_mode="LAYER_1_DOORWAY_BLE",
        selected_category="Ready-to-Wear",
        climate_filter="All",
        finish_filter="All"
    )
    print("=" * 68)
    print(f"SILENT CONCIERGE BACKEND SYNC COMPLETE -> edge_live_state.json ({state['latency_ms']} ms)")
    print("=" * 68)
    for log in state["privacy"]["ble_telemetry"]:
        print(" •", log)
    print(f"\nUnlocked Identity : {state['privacy']['display_identity']}")
    print(f"Paris SA Handoff  : {state['privacy']['paris_sa_note']}")
    print(f"\n[PAST '{state['selected_category'].upper()}' WARDROBE OWNED BY {state['client_id']}]")
    for p in state["past_wardrobe_items"]:
        print(f"  - {p['style_code']} | {p['item_name']} ({p['climate_tag']} / {p['surface_finish']}) | Size: {p['purchased_size']} | Image URL Ready")
    print(f"\n[PRESENT BENGALURU RFID MATCHES IN '{state['selected_category'].upper()}']")
    for m in state["present_rfid_recommendations"]:
        print(f"  -> {m['rfid_sku']} ({m['style_code']}) | {m['item_name']} | Size: {m['stock_size']} | Match: {m['match_pct']}% | ${m['base_price_usd']:,}")
