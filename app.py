import streamlit as st
import pandas as pd
from pathlib import Path

# ------------------------------------------------------------
# ANT YODAYA FOUNDATION | PROGRAM MONITORING DASHBOARD
# Keep app.py and antyodaya_logo.png in the same folder.
# ------------------------------------------------------------

st.set_page_config(
    page_title="Antyodaya Foundation | Program Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Published Google Sheets CSV URLs
OVERVIEW_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSS8V23q0CHWD5DPOExIbNb4DgwMQcerPUAfEPa6y-GKKsuNJAYVQC66j33Ih8I1CrycQu0dug6A0bo/pub?gid=0&single=true&output=csv"
CENTERS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSS8V23q0CHWD5DPOExIbNb4DgwMQcerPUAfEPa6y-GKKsuNJAYVQC66j33Ih8I1CrycQu0dug6A0bo/pub?gid=1710079468&single=true&output=csv"
INVENTORY_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSS8V23q0CHWD5DPOExIbNb4DgwMQcerPUAfEPa6y-GKKsuNJAYVQC66j33Ih8I1CrycQu0dug6A0bo/pub?gid=1659379092&single=true&output=csv"
MEETINGS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSS8V23q0CHWD5DPOExIbNb4DgwMQcerPUAfEPa6y-GKKsuNJAYVQC66j33Ih8I1CrycQu0dug6A0bo/pub?gid=1344140243&single=true&output=csv"

# Brand palette inspired by the Antyodaya Foundation booklet:
# Burgundy + saffron/orange + warm ivory + dark charcoal.
BURGUNDY = "#710B10"
BURGUNDY_DARK = "#52070B"
ORANGE = "#F29A2E"
IVORY = "#FBF8F0"
CHARCOAL = "#352E2D"
MUTED = "#776B66"
BORDER = "#E9DED1"

st.markdown(
    f"""
    <style>
    :root {{
        --af-burgundy: {BURGUNDY};
        --af-burgundy-dark: {BURGUNDY_DARK};
        --af-orange: {ORANGE};
        --af-ivory: {IVORY};
        --af-charcoal: {CHARCOAL};
        --af-muted: {MUTED};
        --af-border: {BORDER};
    }}

    .stApp {{
        background: #FFFEFC;
        color: var(--af-charcoal);
    }}

    [data-testid="stHeader"] {{
        background: rgba(255, 254, 252, 0.94);
    }}

    .block-container {{
        max-width: 1440px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }}

    h1, h2, h3 {{
        color: var(--af-burgundy) !important;
        letter-spacing: -0.025em;
    }}

    h1 {{
        font-weight: 800 !important;
    }}

    h2 {{
        font-weight: 750 !important;
        padding-bottom: .35rem;
        border-bottom: 2px solid var(--af-orange);
    }}

    h3 {{
        font-weight: 700 !important;
    }}

    .af-hero {{
        background: linear-gradient(110deg, #FFF9EE 0%, #FFFFFF 70%);
        border: 1px solid var(--af-border);
        border-top: 5px solid var(--af-burgundy);
        border-radius: 18px;
        padding: 1.25rem 1.5rem;
        margin: .25rem 0 1.4rem 0;
        box-shadow: 0 5px 18px rgba(82, 7, 11, .055);
    }}

    .af-eyebrow {{
        color: var(--af-orange);
        text-transform: uppercase;
        font-size: .76rem;
        font-weight: 800;
        letter-spacing: .13em;
        margin-bottom: .25rem;
    }}

    .af-title {{
        color: var(--af-burgundy);
        font-size: clamp(1.6rem, 3vw, 2.3rem);
        font-weight: 850;
        line-height: 1.15;
        margin: 0;
    }}

    .af-subtitle {{
        color: var(--af-muted);
        font-size: 1rem;
        margin-top: .5rem;
        margin-bottom: 0;
    }}

    [data-testid="stMetric"] {{
        background: #FFFFFF;
        border: 1px solid var(--af-border);
        border-top: 4px solid var(--af-orange);
        border-radius: 15px;
        padding: 1rem 1.1rem;
        box-shadow: 0 4px 15px rgba(82, 7, 11, .045);
        min-height: 120px;
    }}

    [data-testid="stMetricLabel"] {{
        color: var(--af-muted) !important;
        font-weight: 650 !important;
        font-size: .91rem !important;
    }}

    [data-testid="stMetricValue"] {{
        color: var(--af-burgundy) !important;
        font-weight: 800 !important;
    }}

    [data-testid="stExpander"] {{
        background: #FFFFFF;
        border: 1px solid var(--af-border);
        border-left: 4px solid var(--af-burgundy);
        border-radius: 13px;
        margin-bottom: .7rem;
        overflow: hidden;
    }}

    [data-testid="stExpander"] summary {{
        color: var(--af-burgundy);
        font-weight: 750;
    }}

    [data-testid="stExpander"] summary:hover {{
        color: var(--af-burgundy-dark);
    }}

    [data-testid="stDataFrame"] {{
        border: 1px solid var(--af-border);
        border-radius: 10px;
        overflow: hidden;
    }}

    div.stButton > button {{
        background: var(--af-burgundy);
        color: white;
        border: 1px solid var(--af-burgundy);
        border-radius: 10px;
        font-weight: 700;
        padding: .45rem 1rem;
    }}

    div.stButton > button:hover {{
        background: var(--af-burgundy-dark);
        color: white;
        border-color: var(--af-orange);
    }}

    .af-section-note {{
        color: var(--af-muted);
        margin-top: -.45rem;
        margin-bottom: 1rem;
        font-size: .92rem;
    }}

    .af-footer {{
        border-top: 1px solid var(--af-border);
        margin-top: 2.5rem;
        padding-top: 1rem;
        color: var(--af-muted);
        font-size: .82rem;
        text-align: center;
    }}

    @media (max-width: 700px) {{
        .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}
        .af-hero {{
            padding: 1rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=300, show_spinner=False)
def load_sheet(url: str) -> pd.DataFrame:
    return pd.read_csv(url)


def get_sheet(url: str, name: str) -> pd.DataFrame:
    try:
        df = load_sheet(url).copy()
        df.columns = df.columns.astype(str).str.strip()
        return df
    except Exception as exc:
        st.error(
            f"Could not load the **{name}** sheet. Check that its CSV is published "
            f"and the URL is correct. Technical details: {exc}"
        )
        st.stop()


def clean_text(value, fallback="—") -> str:
    if pd.isna(value) or str(value).strip() == "":
        return fallback
    return str(value).strip()


def normalize_id(value) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip()
    try:
        number = float(text)
        if number.is_integer():
            return str(int(number))
    except (ValueError, TypeError):
        pass
    return text


def display_number(value) -> str:
    if pd.isna(value) or str(value).strip() == "":
        return "Not updated"
    text = str(value).strip()
    try:
        number = float(text.replace(",", ""))
        return f"{number:,.0f}" if number.is_integer() else f"{number:,.2f}".rstrip("0").rstrip(".")
    except ValueError:
        return text


def format_attendance(value) -> str:
    if pd.isna(value) or str(value).strip() == "":
        return "Not updated"
    text = str(value).strip()
    if text.endswith("%"):
        return text
    try:
        number = float(text.replace(",", ""))
        # A decimal between 0 and 1 is treated as a proportion.
        if 0 <= number <= 1:
            return f"{number:.0%}"
        return f"{number:g}%"
    except ValueError:
        return text


# Load data
overview = get_sheet(OVERVIEW_URL, "Overview")
centers = get_sheet(CENTERS_URL, "Training Center")
inventory = get_sheet(INVENTORY_URL, "Inventory")
meetings = get_sheet(MEETINGS_URL, "Meetings")

# Top banner and brand logo
logo_path = Path(__file__).resolve().parent / "antyodaya_logo.png"
hero_left, hero_right = st.columns([4.2, 1.3], vertical_alignment="center")

with hero_left:
    st.markdown(
        """
        <div class="af-hero">
            <div class="af-eyebrow">Antyodaya Foundation</div>
            <div class="af-title">Program Monitoring Dashboard</div>
            <p class="af-subtitle">
                A live view of field outreach, skill development centres,
                resources and programme meetings.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with hero_right:
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
    else:
        st.markdown(
            f"<div style='color:{BURGUNDY};font-size:1.35rem;font-weight:800;'>अंत्योदय फाउंडेशन</div>",
            unsafe_allow_html=True,
        )

refresh_col, info_col = st.columns([1, 4], vertical_alignment="center")
with refresh_col:
    if st.button("↻ Refresh dashboard", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
with info_col:
    st.caption("Data is read directly from the published Google Sheets. Automatic refresh interval: 5 minutes.")


# Overview KPI cards: show values entered in the sheet; no KPI calculations.
st.markdown("## 📊 Programme at a glance")
st.markdown(
    '<div class="af-section-note">Key programme figures maintained in the Overview sheet.</div>',
    unsafe_allow_html=True,
)

required_overview = {"Parameter", "Value"}
if not required_overview.issubset(overview.columns):
    st.error("The Overview sheet must contain columns named 'Parameter' and 'Value'.")
    st.stop()

overview_values = {
    str(parameter).strip(): clean_text(value)
    for parameter, value in zip(overview["Parameter"], overview["Value"])
}

kpi_columns = st.columns(4)
kpis = [
    ("👥", "Active Surveyors", "Active Surveyors"),
    ("📍", "Villages with Surveyors", "Villages with Surveyors"),
    ("🏫", "Training Centers", "Training Centers"),
    ("🚲", "Cycles Distributed", "Cycles Distributed"),
]

for col, (icon, label, key) in zip(kpi_columns, kpis):
    with col:
        st.metric(
            label=f"{icon}  {label}",
            value=overview_values.get(key, "—"),
        )


# Training centres
st.markdown("## 🏫 Training Centres")
st.markdown(
    '<div class="af-section-note">Select a centre to view enrolment, course dates and its inventory.</div>',
    unsafe_allow_html=True,
)

required_center_columns = {
    "Center ID",
    "District",
    "Village",
    "Students",
    "Trade",
    "Start Date",
    "End Date",
    "Student Appeared for exam",
    "Average Attendance",
}
missing_center_columns = required_center_columns - set(centers.columns)
if missing_center_columns:
    st.error(
        "Missing columns in the Training Center sheet: "
        + ", ".join(sorted(missing_center_columns))
    )
    st.stop()

required_inventory_columns = {"Center_ID", "Item_Name", "Available_Quantity"}
missing_inventory_columns = required_inventory_columns - set(inventory.columns)
if missing_inventory_columns:
    st.error(
        "Missing columns in the Inventory sheet: "
        + ", ".join(sorted(missing_inventory_columns))
    )
    st.stop()

# Show each training centre as an expandable card.
for _, center in centers.iterrows():
    center_id = normalize_id(center["Center ID"])
    village = clean_text(center["Village"], "Unnamed village")
    district = clean_text(center["District"])
    trade = clean_text(center["Trade"], "Trade not specified")
    title = f"{village} · {trade}"

    with st.expander(f"📚  {title}", expanded=False):
        st.markdown(
            f"<div style='color:{MUTED};font-size:.9rem;margin-bottom:.8rem;'>"
            f"Centre ID: <b>{center_id or '—'}</b> &nbsp; · &nbsp; "
            f"District: <b>{district}</b></div>",
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("👩‍🎓 Students enrolled", display_number(center["Students"]))
        with c2:
            st.metric("📅 Average attendance", format_attendance(center["Average Attendance"]))
        with c3:
            st.metric(
                "📝 Students appeared for exam",
                display_number(center["Student Appeared for exam"]),
            )

        date1, date2 = st.columns(2)
        with date1:
            st.markdown(
                f"<div style='background:{IVORY};border:1px solid {BORDER};"
                f"border-radius:10px;padding:.8rem 1rem;'>"
                f"<span style='color:{MUTED};font-size:.82rem;'>COURSE START DATE</span><br>"
                f"<b style='color:{BURGUNDY};'>{clean_text(center['Start Date'])}</b></div>",
                unsafe_allow_html=True,
            )
        with date2:
            st.markdown(
                f"<div style='background:{IVORY};border:1px solid {BORDER};"
                f"border-radius:10px;padding:.8rem 1rem;'>"
                f"<span style='color:{MUTED};font-size:.82rem;'>COURSE END DATE</span><br>"
                f"<b style='color:{BURGUNDY};'>{clean_text(center['End Date'])}</b></div>",
                unsafe_allow_html=True,
            )

        st.markdown("### 📦 Centre inventory")
        matched_inventory = inventory[
            inventory["Center_ID"].apply(normalize_id) == center_id
        ].copy()

        if matched_inventory.empty:
            st.info("No inventory records are currently listed for this centre.")
        else:
            matched_inventory = matched_inventory[["Item_Name", "Available_Quantity"]].rename(
                columns={
                    "Item_Name": "Inventory item",
                    "Available_Quantity": "Available quantity",
                }
            )
            st.dataframe(
                matched_inventory,
                hide_index=True,
                use_container_width=True,
            )


# Meetings and important updates
st.markdown("## 🗓️ Meetings & important updates")
st.markdown(
    '<div class="af-section-note">Meeting dates and titles maintained in the Meetings sheet.</div>',
    unsafe_allow_html=True,
)

required_meeting_columns = {"Date", "Meeting Title"}
missing_meeting_columns = required_meeting_columns - set(meetings.columns)

if missing_meeting_columns:
    st.error(
        "Missing columns in the Meetings sheet: "
        + ", ".join(sorted(missing_meeting_columns))
    )
else:
    meeting_view = meetings[["Date", "Meeting Title"]].copy()
    meeting_view.columns = ["Date", "Meeting / update"]
    st.dataframe(
        meeting_view,
        hide_index=True,
        use_container_width=True,
    )

st.markdown(
    f"""
    <div class="af-footer">
        <strong style="color:{BURGUNDY};">ANTYODAYA FOUNDATION</strong>
        <br>Programme Monitoring Dashboard · Supporting education, skills and self-reliance
    </div>
    """,
    unsafe_allow_html=True,
)
