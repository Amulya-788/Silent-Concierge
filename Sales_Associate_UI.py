import json
import urllib.parse
import streamlit as st
import pandas as pd
import numpy as np

from appy import execute_silent_concierge_scan, initialize_storage_databases

# ==============================================================================
# 1. AUTHENTIC LVMH / DIOR.COM UI DESIGN SYSTEM (STARK BLACK & WHITE COUTURE)
# ==============================================================================
st.set_page_config(page_title="LVMH Clienteling | Christian Dior Couture", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;0,6..96,600;1,6..96,400&family=Inter:wght@300;400;500;600&display=swap');

    /* Global Pure White & Stark Black LVMH Palette */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    section[data-testid="stSidebar"] {
        background-color: #F8F8F8 !important;
        border-right: 1px solid #E5E5E5;
    }
    section[data-testid="stSidebar"] * {
        font-family: 'Inter', sans-serif !important;
        color: #111111 !important;
        font-size: 12px;
    }

    /* LVMH / CHRISTIAN DIOR Header Masthead */
    .lvmh-header {
        text-align: center;
        padding: 10px 0 16px 0;
        border-bottom: 1px solid #000000;
        margin-bottom: 18px;
    }
    .lvmh-group-tag {
        font-family: 'Inter', sans-serif;
        font-size: 9px;
        font-weight: 500;
        letter-spacing: 4px;
        color: #666666;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .dior-wordmark {
        font-family: 'Bodoni Moda', 'Didot', 'Georgia', serif;
        font-size: 32px;
        font-weight: 400;
        letter-spacing: 8px;
        color: #000000;
        margin: 0;
        text-transform: uppercase;
    }
    .dior-sub {
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        font-weight: 400;
        letter-spacing: 2.5px;
        color: #444444;
        margin-top: 4px;
        text-transform: uppercase;
    }

    /* Compact Client Dossier Bar */
    .client-bar {
        background-color: #FAFAFA;
        border: 1px solid #E5E5E5;
        border-left: 3px solid #000000;
        padding: 14px 20px;
        margin-bottom: 16px;
    }
    .client-bar-locked {
        background-color: #FFF5F5;
        border: 1px solid #E5B8B8;
        border-left: 3px solid #990000;
        padding: 14px 20px;
        margin-bottom: 16px;
    }
    .client-eyebrow {
        font-family: 'Inter', sans-serif;
        font-size: 9px;
        font-weight: 600;
        letter-spacing: 2px;
        color: #666666;
        text-transform: uppercase;
    }
    .client-name {
        font-family: 'Bodoni Moda', 'Georgia', serif;
        font-size: 22px;
        font-weight: 500;
        color: #000000;
        margin: 2px 0 4px 0;
    }
    .client-meta {
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        color: #333333;
        margin-bottom: 6px;
    }
    .client-note {
        font-family: 'Inter', sans-serif;
        font-size: 11.5px;
        font-style: italic;
        color: #222222;
        background-color: #FFFFFF;
        border: 1px solid #EEEEEE;
        padding: 7px 12px;
        margin: 0;
    }

    /* Compact DNA Metrics Strip */
    .dna-grid {
        display: flex;
        justify-content: space-between;
        border-top: 1px solid #E5E5E5;
        border-bottom: 1px solid #E5E5E5;
        padding: 10px 12px;
        margin-bottom: 20px;
        background-color: #FFFFFF;
    }
    .dna-cell {
        text-align: center;
        flex: 1;
        border-right: 1px solid #F0F0F0;
    }
    .dna-cell:last-child {
        border-right: none;
    }
    .dna-k {
        font-family: 'Inter', sans-serif;
        font-size: 8.5px;
        font-weight: 500;
        letter-spacing: 1.5px;
        color: #777777;
        text-transform: uppercase;
    }
    .dna-v {
        font-family: 'Bodoni Moda', serif;
        font-size: 18px;
        font-weight: 600;
        color: #000000;
        margin-top: 2px;
    }

    /* Section Titles */
    .sec-title {
        font-family: 'Bodoni Moda', 'Georgia', serif;
        font-size: 17px;
        font-weight: 500;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #000000;
        margin: 10px 0 2px 0;
    }
    .sec-caption {
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        color: #666666;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    /* Compact E-Commerce / 24S / Dior.com Product Cards */
    .lvmh-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E5E5;
        padding: 12px;
        transition: border-color 0.2s ease;
    }
    .lvmh-badge-new {
        display: inline-block;
        font-family: 'Inter', sans-serif;
        font-size: 8.5px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 3px 8px;
        background-color: #000000;
        color: #FFFFFF;
        margin-bottom: 8px;
    }
    .lvmh-badge-owned {
        display: inline-block;
        font-family: 'Inter', sans-serif;
        font-size: 8.5px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 3px 8px;
        background-color: #EFEFEF;
        color: #333333;
        border: 1px solid #CCCCCC;
        margin-bottom: 8px;
    }
    .prod-origin {
        font-family: 'Inter', sans-serif;
        font-size: 9px;
        font-weight: 500;
        letter-spacing: 1.5px;
        color: #777777;
        text-transform: uppercase;
        margin-top: 6px;
    }
    .prod-title {
        font-family: 'Bodoni Moda', 'Georgia', serif;
        font-size: 16px;
        font-weight: 500;
        color: #000000;
        margin: 2px 0 4px 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .prod-price {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        font-weight: 600;
        color: #000000;
        margin-bottom: 6px;
    }
    .prod-meta {
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        color: #555555;
        line-height: 1.55;
        border-top: 1px solid #F0F0F0;
        padding-top: 6px;
    }
    .prod-whisper {
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        color: #111111;
        background-color: #F9F9F9;
        border-left: 2px solid #000000;
        padding: 6px 8px;
        margin-top: 8px;
        line-height: 1.4;
    }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. COMPACT E-COMMERCE PRODUCT SILHOUETTE RENDERER (175px UNIFORM THUMBNAILS)
# ==============================================================================
def render_lvmh_product_thumbnail(style_code, item_name, category, finish, climate, origin):
    """
    Renders a compact, standardized e-commerce studio thumbnail (#F6F6F6)
    with a crisp vector fashion illustration matching the exact category.
    """
    if category == "Handbags":
        icon_svg = """
        <path d="M120,78 C120,52 160,52 160,78" fill="none" stroke="#111111" stroke-width="2.2"/>
        <rect x="95" y="78" width="90" height="68" rx="3" fill="#FFFFFF" stroke="#111111" stroke-width="2"/>
        <line x1="95" y1="98" x2="185" y2="98" stroke="#111111" stroke-width="1"/>
        <circle cx="140" cy="98" r="5" fill="#111111"/>
        """
    elif category == "Ready-to-Wear":
        icon_svg = """
        <polygon points="118,56 162,56 184,88 168,96 160,78 160,148 120,148 120,78 112,96 96,88"
                 fill="#FFFFFF" stroke="#111111" stroke-width="2" stroke-linejoin="round"/>
        <line x1="140" y1="56" x2="140" y2="148" stroke="#111111" stroke-width="1"/>
        <circle cx="135" cy="95" r="2" fill="#111111"/>
        <circle cx="135" cy="112" r="2" fill="#111111"/>
        """
    elif category == "Shoes":
        icon_svg = """
        <path d="M92,132 L132,132 L158,95 L178,95 L178,142 L170,142 L170,115 L142,142 L92,142 Z"
              fill="#FFFFFF" stroke="#111111" stroke-width="2" stroke-linejoin="round"/>
        """
    else:  # Jewelry
        icon_svg = """
        <circle cx="140" cy="96" r="34" fill="none" stroke="#111111" stroke-width="2"/>
        <polygon points="140,132 132,144 140,154 148,144" fill="#FFFFFF" stroke="#111111" stroke-width="1.8"/>
        """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 185" width="100%" height="165">
        <rect width="280" height="185" fill="#F5F5F5"/>
        <text x="12" y="20" fill="#777777" font-family="Arial, sans-serif" font-size="8" letter-spacing="1.5">
            {style_code}
        </text>
        <text x="268" y="20" fill="#111111" font-family="Arial, sans-serif" font-size="8" font-weight="bold" text-anchor="end" letter-spacing="1.5">
            {climate.upper()} • {finish.upper()}
        </text>
        {icon_svg}
        <text x="140" y="172" fill="#555555" font-family="Georgia, serif" font-size="9.5" font-style="italic" text-anchor="middle" letter-spacing="1">
            {origin}
        </text>
    </svg>"""
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)


@st.cache_data
def warm_up_edge_ram():
    return initialize_storage_databases()

catalog_df, vip_history_df, rfid_df, vip_profiles = warm_up_edge_ram()

# ==============================================================================
# 3. SIDEBAR: LVMH CLIENTELING CONTROLS
# ==============================================================================
st.sidebar.markdown("### DIOR CLIENTELING PORT")
st.sidebar.caption("LVMH EDGE INTELLIGENCE // BENGALURU")

if "active_vip" not in st.session_state:
    st.session_state.active_vip = "VIP_007"
if "trigger_mode" not in st.session_state:
    st.session_state.trigger_mode = "LAYER_1_DOORWAY_BLE"

if st.sidebar.button("SIMULATE DOORWAY BLE ARRIVAL", use_container_width=True):
    st.session_state.active_vip = np.random.choice(sorted(list(vip_profiles.keys())))
    st.session_state.trigger_mode = "LAYER_1_DOORWAY_BLE"

client_list = sorted(list(vip_profiles.keys()))
selected_vip = st.sidebar.selectbox(
    "1. CLIENT ARCHIVE ID",
    client_list,
    index=client_list.index(st.session_state.active_vip)
)
st.session_state.active_vip = selected_vip

trigger_label_map = {
    "In-Boutique Arrival (BLE Unlocked)": "LAYER_1_DOORWAY_BLE",
    "24h Appointment Key (Pre-Arrival)": "TOMORROW_24H_APPOINTMENT_KEY",
    "GDPR Vault Locked (At-Rest)": "LOCKED_AT_REST"
}
chosen_trigger_label = st.sidebar.radio(
    "2. PRIVACY & ACCESS STATE",
    list(trigger_label_map.keys()),
    index=list(trigger_label_map.values()).index(st.session_state.trigger_mode)
)
st.session_state.trigger_mode = trigger_label_map[chosen_trigger_label]

st.sidebar.markdown("---")
selected_category = st.sidebar.selectbox(
    "3. PRODUCT CATEGORY",
    ["Ready-to-Wear", "Handbags", "Shoes", "Jewelry"]
)

climate_filter = st.sidebar.selectbox(
    "4. SEASON / OCCASION",
    ["All", "Grand", "Formal", "Summer", "Winter", "Rainy"]
)

finish_filter = st.sidebar.selectbox(
    "5. SURFACE FINISH",
    ["All", "Shiny", "Simple"]
)

prioritize_dead_stock = st.sidebar.checkbox("Prioritize Slow Stock (90+ Days)", value=False)

# ==============================================================================
# 4. RUN BACKEND SCAN & LOAD SYNCED JSON PACKET
# ==============================================================================
live_state = execute_silent_concierge_scan(
    target_vip=st.session_state.active_vip,
    trigger_mode=st.session_state.trigger_mode,
    selected_category=selected_category,
    climate_filter=climate_filter,
    finish_filter=finish_filter,
    prioritize_dead_stock=prioritize_dead_stock
)

# ==============================================================================
# 5. LVMH / DIOR MASTHEAD & CLIENT DOSSIER BAR
# ==============================================================================
st.markdown("""
<div class='lvmh-header'>
    <div class='lvmh-group-tag'>LVMH MOËT HENNESSY • LOUIS VUITTON — RETAIL EDGE ARCHITECTURE</div>
    <p class='dior-wordmark'>CHRISTIAN DIOR</p>
    <div class='dior-sub'>SILENT CONCIERGE CLIENTELING • PARIS — BENGALURU BOUTIQUE</div>
</div>
""", unsafe_allow_html=True)

if not live_state["privacy"]["is_unlocked"]:
    st.markdown(f"""
    <div class='client-bar-locked'>
        <div class='client-eyebrow'>GDPR ZERO-PII ENCRYPTION ACTIVE • SUB-5MS EDGE LOCK</div>
        <div class='client-name'>{live_state['privacy']['display_identity']}</div>
        <div class='client-meta'>Identity, Style DNA vector, and purchase archive are cryptographically locked at rest. Requires physical Apple Wallet BLE doorway handshake or active 24-hour pre-arrival token to decrypt.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    clean_note = live_state["privacy"]["paris_sa_note"].split(":", 1)[-1].strip()
    st.markdown(f"""
    <div class='client-bar'>
        <div class='client-eyebrow'>VERIFIED CLIENT DOSSIER • ACTIVE SESSION ({live_state['latency_ms']} MS EDGE SYNC)</div>
        <div class='client-name'>{live_state['privacy']['display_identity']}</div>
        <div class='client-meta'>
            <strong>HOME BOUTIQUE:</strong> {live_state['privacy']['home_boutique']} &nbsp;|&nbsp;
            <strong>VERIFIED SIZES:</strong> RTW {live_state['core_sizes']['rtw']} • SHOES {live_state['core_sizes']['shoe']} &nbsp;|&nbsp;
            <strong>SIZE-DELTA GIFTS FILTERED:</strong> {live_state['gifts_filtered_out']}
        </div>
        <div class='client-note'><strong>Sister-Boutique Note:</strong> {clean_note}</div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================================================================
    # 6. FREQUENCY STYLE DNA STRIP
    # ==============================================================================
    dna = live_state["category_style_dna"]
    st.markdown(f"""
    <div class='dna-grid'>
        <div class='dna-cell'><div class='dna-k'>CATEGORY</div><div class='dna-v'>{selected_category}</div></div>
        <div class='dna-cell'><div class='dna-k'>MATERIAL (30%)</div><div class='dna-v'>{dna['material_tier']}/5</div></div>
        <div class='dna-cell'><div class='dna-k'>LOGO CODE (20%)</div><div class='dna-v'>{dna['logo_prominence']}/5</div></div>
        <div class='dna-cell'><div class='dna-k'>DETAIL (15%)</div><div class='dna-v'>{dna['detail_complexity']}/5</div></div>
        <div class='dna-cell'><div class='dna-k'>SILHOUETTE (10%)</div><div class='dna-v'>{dna['silhouette_length']}/5</div></div>
        <div class='dna-cell'><div class='dna-k'>SHINE INDEX (10%)</div><div class='dna-v'>{dna['shiny_index']}/5</div></div>
        <div class='dna-cell'><div class='dna-k'>MEDIAN SPEND (5%)</div><div class='dna-v'>${dna['base_price_usd']:,}</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================================================================
    # 7. ROW I: PRESENT BENGALURU RFID RECOMMENDATIONS (SORTED: NEW ITEMS FIRST!)
    # ==============================================================================
    st.markdown(f"<div class='sec-title'>I. In-Stock Backroom Curation — {selected_category}</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-caption'>Exact Client Size Match • Prioritizing New Acquisitions Ahead of Owned Archive Styles</div>", unsafe_allow_html=True)

    owned_style_codes = {item["style_code"] for item in live_state["past_wardrobe_items"]}

    sorted_recs = sorted(
        live_state["present_rfid_recommendations"],
        key=lambda r: (r["style_code"] in owned_style_codes, r["style_distance"])
    )

    rec_cols = st.columns(3)
    for idx, rec in enumerate(sorted_recs):
        with rec_cols[idx]:
            already_owns = rec["style_code"] in owned_style_codes
            badge_html = (
                "<div class='lvmh-badge-owned'>OWNED IN ARCHIVE • REPLENISHMENT</div>"
                if already_owns else
                f"<div class='lvmh-badge-new'>NEW FOR CLIENT • {rec['match_pct']}% MATCH</div>"
            )
            thumb_url = render_lvmh_product_thumbnail(
                rec["style_code"], rec["item_name"], selected_category,
                rec["surface_finish"], rec["climate_tag"], rec["craftsmanship_origin"]
            )
            whisper = (
                f"Bring {rec['rfid_sku']} ({rec['stock_size']}): {rec['craftsmanship_origin']} piece "
                f"matched to her {rec['surface_finish'].lower()} {rec['climate_tag'].lower()} profile."
            )

            st.markdown(f"""
            <div class='lvmh-card'>
                {badge_html}
                <img src="{thumb_url}" style="width:100%; height:165px; object-fit:cover; display:block; margin-bottom:6px;" />
                <div class='prod-origin'>{rec['craftsmanship_origin']}</div>
                <div class='prod-title'>{rec['item_name']}</div>
                <div class='prod-price'>${rec['base_price_usd']:,}</div>
                <div class='prod-meta'>
                    <strong>RFID SKU:</strong> {rec['rfid_sku']} &nbsp;|&nbsp; <strong>SIZE:</strong> {rec['stock_size']}<br>
                    <strong>CLIMATE:</strong> {rec['climate_tag']} ({rec['surface_finish']}) &nbsp;|&nbsp; <strong>STOCK:</strong> {rec['days_on_floor']}d
                </div>
                <div class='prod-whisper'>“{whisper}”</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==============================================================================
    # 8. ROW II: CLIENT'S OWNED ARCHIVE WARDROBE (GUARANTEED 3-COLUMN UNIFORM GRID)
    # ==============================================================================
    st.markdown(f"<div class='sec-title'>II. Client’s Owned Archive — Past Purchases</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-caption'>Verified Personal-Size Purchases from Global Maisons (Size-Delta Gifts Excluded)</div>", unsafe_allow_html=True)

    archive_items = list(live_state["past_wardrobe_items"])

    if len(archive_items) < 3:
        vip_all = vip_history_df.loc[
            (vip_history_df["client_id"] == st.session_state.active_vip) &
            (vip_history_df["gift_receipt_flag"] == 0)
        ].merge(catalog_df, on="style_code", how="left")
        existing_codes = {x["style_code"] for x in archive_items}
        extra_pool = (
            vip_all.loc[~vip_all["style_code"].isin(existing_codes)]
            .groupby(["style_code", "item_name", "item_category", "climate_tag", "surface_finish", "craftsmanship_origin", "base_price_usd", "purchased_size"])
            .size()
            .reset_index(name="times_purchased")
            .sort_values(by="times_purchased", ascending=False)
            .to_dict(orient="records")
        )
        for extra in extra_pool:
            if len(archive_items) >= 3:
                break
            archive_items.append(extra)

    past_cols = st.columns(3)
    for idx, item in enumerate(archive_items[:3]):
        with past_cols[idx]:
            cat_label = item.get("item_category", selected_category)
            thumb_url = render_lvmh_product_thumbnail(
                item["style_code"], item["item_name"], cat_label,
                item["surface_finish"], item["climate_tag"], item["craftsmanship_origin"]
            )
            st.markdown(f"""
            <div class='lvmh-card'>
                <div class='lvmh-badge-owned'>OWNED ARCHIVE • BOUGHT {item['times_purchased']}X ({item['purchased_size']})</div>
                <img src="{thumb_url}" style="width:100%; height:165px; object-fit:cover; display:block; margin-bottom:6px;" />
                <div class='prod-origin'>{item['craftsmanship_origin']}</div>
                <div class='prod-title'>{item['item_name']}</div>
                <div class='prod-price'>${item['base_price_usd']:,}</div>
                <div class='prod-meta'>
                    <strong>STYLE CODE:</strong> {item['style_code']} &nbsp;|&nbsp; <strong>DEPT:</strong> {cat_label}<br>
                    <strong>CLIMATE:</strong> {item['climate_tag']} &nbsp;|&nbsp; <strong>FINISH:</strong> {item['surface_finish']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# 9. COLLAPSIBLE ARCHITECT TELEMETRY LOG
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("LVMH EDGE TELEMETRY // APPLE WALLET BLE & VECTOR SYNC LOG (<5MS)"):
    for line in live_state["privacy"]["ble_telemetry"]:
        st.code(line, language="text")
