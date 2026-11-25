import streamlit as st
from appy import execute_silent_concierge_scan

# ==============================================================================
# 1. PAGE CONFIG & CHRISTIAN DIOR / LVMH EDITORIAL STYLING
# ==============================================================================
st.set_page_config(
    page_title="Silent Concierge — Boutique Clienteling Terminal",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #111111;
            background-color: #FFFFFF;
        }
        .maison-header {
            border-bottom: 1px solid #111111;
            padding-bottom: 14px;
            margin-bottom: 22px;
        }
        .maison-title {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 2.15rem;
            font-weight: 600;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin: 0;
            color: #0A0A0A;
        }
        .maison-sub {
            font-size: 0.78rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: #666666;
            margin-top: 4px;
        }
        .dossier-unlocked {
            background: #FAFAFA;
            border: 1px solid #E2E2E2;
            border-left: 4px solid #111111;
            padding: 18px 22px;
            margin-bottom: 20px;
        }
        .dossier-locked {
            background: #FFF7F7;
            border: 1px solid #E5B4B4;
            border-left: 4px solid #8B1E1E;
            padding: 20px 24px;
            margin-bottom: 20px;
        }
        .dossier-label {
            font-size: 0.70rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: #777777;
            margin-bottom: 4px;
        }
        .dossier-name {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 1.65rem;
            font-weight: 600;
            color: #0A0A0A;
            margin: 0 0 8px 0;
        }
        .dossier-note {
            font-size: 0.90rem;
            line-height: 1.5;
            color: #222222;
            margin-top: 8px;
        }
        .section-heading {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 1.35rem;
            font-weight: 600;
            letter-spacing: 0.10em;
            text-transform: uppercase;
            border-bottom: 1px solid #EAEAEA;
            padding-bottom: 6px;
            margin: 22px 0 14px 0;
        }
        .sku-card {
            border: 1px solid #E6E6E6;
            background: #FFFFFF;
            padding: 14px;
            height: 100%;
        }
        .sku-badge-new {
            display: inline-block;
            background: #111111;
            color: #FFFFFF;
            font-size: 0.66rem;
            font-weight: 600;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            padding: 3px 8px;
            margin-bottom: 8px;
        }
        .sku-badge-owned {
            display: inline-block;
            background: #F0F0F0;
            color: #444444;
            font-size: 0.66rem;
            font-weight: 600;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            padding: 3px 8px;
            margin-bottom: 8px;
        }
        .sku-name {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 1.18rem;
            font-weight: 600;
            margin: 8px 0 4px 0;
            color: #0A0A0A;
        }
        .sku-meta {
            font-size: 0.80rem;
            color: #555555;
            line-height: 1.5;
        }
        .dna-box {
            border: 1px solid #EAEAEA;
            background: #FAFAFA;
            padding: 10px 12px;
            text-align: center;
        }
        .dna-label {
            font-size: 0.66rem;
            letter-spacing: 0.10em;
            text-transform: uppercase;
            color: #666666;
        }
        .dna-val {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 1.35rem;
            font-weight: 600;
            color: #0A0A0A;
            margin-top: 2px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# 2. SIDEBAR CONTROLS (VIP, PRIVACY GATE & BACKROOM FILTERS)
# ==============================================================================
with st.sidebar:
    st.markdown("### BOUTIQUE TERMINAL")
    st.caption("Tier 3 Edge Node • Bengaluru Salon")

    vip_options = [f"VIP_{str(i).zfill(3)}" for i in range(1, 51)]
    selected_vip = st.selectbox(
        "1. Client PassKit Token",
        options=vip_options,
        index=6,  # Default: VIP_007
    )

    privacy_label_map = {
        "Doorway BLE Arrival (Live Unlock)": "LAYER_1_DOORWAY_BLE",
        "24-Hour Appointment Key": "TOMORROW_24H_APPOINTMENT_KEY",
        "GDPR Vault Locked (At-Rest)": "LOCKED_AT_REST",
    }
    privacy_choice = st.radio(
        "2. Privacy & Access State",
        options=list(privacy_label_map.keys()),
        index=0,
    )
    trigger_mode = privacy_label_map[privacy_choice]

    st.divider()

    selected_category = st.selectbox(
        "3. Department",
        options=["Ready-to-Wear", "Handbags", "Shoes", "Jewelry"],
        index=0,
    )
    climate_filter = st.selectbox(
        "4. Occasion / Climate",
        options=["All", "Formal", "Rainy", "Winter", "Summer", "Grand"],
        index=0,
    )
    finish_filter = st.selectbox(
        "5. Surface Finish",
        options=["All", "Simple", "Shiny"],
        index=0,
    )
    prioritize_dead_stock = st.checkbox(
        "Prioritize Slow Stock (90+ Days)",
        value=False,
    )

# ==============================================================================
# 3. EXECUTE IN-MEMORY EDGE SCAN
# ==============================================================================
live_state = execute_silent_concierge_scan(
    target_vip=selected_vip,
    trigger_mode=trigger_mode,
    selected_category=selected_category,
    climate_filter=climate_filter,
    finish_filter=finish_filter,
    prioritize_dead_stock=prioritize_dead_stock,
)

privacy = live_state["privacy"]
is_unlocked = privacy["is_unlocked"]

# ==============================================================================
# 4. HEADER & TELEMETRY BAR
# ==============================================================================
st.markdown(
    """
    <div class="maison-header">
        <div class="maison-title">SILENT CONCIERGE</div>
        <div class="maison-sub">Edge Clienteling &amp; Passive-RFID Matchmaking • Paris ↔ Bengaluru</div>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Edge Scan Latency", f"{live_state['latency_ms']} ms")
m2.metric("Privacy Protocol", "UNLOCKED" if is_unlocked else "LOCKED (GDPR)")
m3.metric("Size-Delta Gifts Filtered", str(live_state["gifts_filtered_out"]))
m4.metric(
    "Verified Core Size",
    f"{live_state['core_sizes']['rtw']} / {live_state['core_sizes']['shoe']}",
)

with st.expander(f"Edge BLE & RFID Telemetry Log ({live_state['latency_ms']} ms)", expanded=False):
    for entry in privacy["ble_telemetry"]:
        st.code(entry, language=None)

# ==============================================================================
# 5. GDPR PRIVACY GATE (STRICTLY HIDES ALL CLIENT DATA WHEN LOCKED)
# ==============================================================================
if not is_unlocked:
    st.markdown(
        f"""
        <div class="dossier-locked">
            <div class="dossier-label">GDPR Zero-PII Vault • Encrypted At Rest</div>
            <div class="dossier-name">{privacy['display_identity']}</div>
            <div class="dossier-meta"><strong>Home Boutique:</strong> {privacy['home_boutique']}</div>
            <div class="dossier-note">{privacy['paris_sa_note']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(
        "All Style DNA vectors, owned archive history, and tailored RFID pulls are withheld "
        "until a physical Doorway BLE handshake or 24-Hour Appointment Key is active."
    )
else:
    # --- CLIENT DOSSIER BANNER ---
    st.markdown(
        f"""
        <div class="dossier-unlocked">
            <div class="dossier-label">Active Client Dossier • {privacy['home_boutique']}</div>
            <div class="dossier-name">{privacy['display_identity']}</div>
            <div class="dossier-note">{privacy['paris_sa_note']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- SECTION I: CATEGORY STYLE DNA ---
    dna = live_state.get("category_style_dna", {})
    if dna:
        st.markdown(
            f'<div class="section-heading">I. {selected_category} Style DNA (Personal Purchases Only)</div>',
            unsafe_allow_html=True,
        )
        dna_cols = st.columns(7)
        dna_fields = [
            ("Material Tier", f"{dna['material_tier']}/5"),
            ("Logo Index", f"{dna['logo_prominence']}/5"),
            ("Complexity", f"{dna['detail_complexity']}/5"),
            ("Silhouette", f"{dna['silhouette_length']}/5"),
            ("Palette", f"{dna['color_palette']}/5"),
            ("Shine Index", f"{dna['shiny_index']}/5"),
            ("Median Spend", f"${dna['base_price_usd']:,}"),
        ]
        for col, (label, value) in zip(dna_cols, dna_fields):
            col.markdown(
                f"""
                <div class="dna-box">
                    <div class="dna-label">{label}</div>
                    <div class="dna-val">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # --- SECTION II: PRESENT BENGALURU BACKROOM RFID MATCHES ---
    st.markdown(
        f'<div class="section-heading">II. Backroom RFID Curation — {selected_category}</div>',
        unsafe_allow_html=True,
    )
    past_items = live_state.get("past_wardrobe_items", [])
    owned_codes = {item["style_code"] for item in past_items}
    recs = live_state.get("present_rfid_recommendations", [])

    if not recs:
        st.warning("No matching backroom RFID units found for the selected filters.")
    else:
        rec_cols = st.columns(len(recs))
        for idx, (col, item) in enumerate(zip(rec_cols, recs), start=1):
            is_new = item["style_code"] not in owned_codes
            badge_html = (
                '<span class="sku-badge-new">NEW FOR CLIENT</span>'
                if is_new
                else '<span class="sku-badge-owned">ARCHIVE REPLENISHMENT</span>'
            )
            col.markdown(
                f"""
                <div class="sku-card">
                    {badge_html}
                    <img src="{item['image_url']}" style="width:100%; border-radius:2px;" alt="{item['item_name']}" />
                    <div class="sku-name">#{idx} {item['item_name']}</div>
                    <div class="sku-meta">
                        <strong>Match Score:</strong> {item['match_pct']}%<br/>
                        <strong>RFID SKU:</strong> {item['rfid_sku']} ({item['style_code']})<br/>
                        <strong>Verified Size:</strong> {item['stock_size']}<br/>
                        <strong>Price:</strong> ${item['base_price_usd']:,}<br/>
                        <strong>Profile:</strong> {item['climate_tag']} • {item['surface_finish']} • {item['days_on_floor']}d on floor
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # --- SECTION III: OWNED ARCHIVE WARDROBE ---
    st.markdown(
        f'<div class="section-heading">III. Owned Archive Reference — {selected_category}</div>',
        unsafe_allow_html=True,
    )
    if not past_items:
        st.caption("No personal purchase history recorded in this category.")
    else:
        past_cols = st.columns(len(past_items))
        for col, item in zip(past_cols, past_items):
            col.markdown(
                f"""
                <div class="sku-card">
                    <span class="sku-badge-owned">OWNED ×{item['times_purchased']}</span>
                    <img src="{item['image_url']}" style="width:100%; border-radius:2px;" alt="{item['item_name']}" />
                    <div class="sku-name">{item['item_name']}</div>
                    <div class="sku-meta">
                        <strong>Style Code:</strong> {item['style_code']}<br/>
                        <strong>Purchased Size:</strong> {item['purchased_size']}<br/>
                        <strong>Price:</strong> ${item['base_price_usd']:,}<br/>
                        <strong>Origin:</strong> {item['craftsmanship_origin']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
