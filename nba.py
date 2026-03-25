import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="nuvora | Next Best Action",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Palette ────────────────────────────────────────────────────────────────────
BG = "#0B1622"
CARD = "#0F1E2E"
BORDER = "#1A2E42"
ORANGE = "#F5A623"
BLUE = "#3A8EBF"
MUTED = "#4A7A9B"
TEXT = "#D8E6F2"
WHITE = "#FFFFFF"
GREEN = "#4CAF50"
RED = "#EF5350"
GRID = "#1A2E42"

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
  html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
  .stApp {{ background-color: {BG}; }}
  #MainMenu, footer, header {{ visibility: hidden; }}
  [data-testid="stSidebar"] {{ display: none; }}
  section[data-testid="stSidebarContent"] {{ display: none; }}
  h1,h2,h3,p,label {{ color: {TEXT}; }}

  /* ── Scrollbar ── */
  ::-webkit-scrollbar {{ width: 4px; height: 4px; }}
  ::-webkit-scrollbar-track {{ background: {BG}; }}
  ::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 2px; }}

  /* ── Top nav ── */
  .nv-nav {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 40px;
    background: #050E1F;
    border-bottom: 1px solid {BORDER};
    margin-bottom: 32px;
  }}
  .nv-logo {{ font-size: 24px; font-weight: 800; color: {WHITE}; letter-spacing: -0.5px; }}
  .nv-logo span {{ color: {ORANGE}; }}
  .nv-nav-right {{ font-size: 11px; font-weight: 600; color: {MUTED}; text-transform: uppercase; letter-spacing: 1.5px; }}
  .nv-nav-pill {{
    background: rgba(245,166,35,0.12);
    border: 1px solid rgba(245,166,35,0.3);
    color: {ORANGE} !important;
    padding: 5px 14px; border-radius: 20px;
    font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;
  }}

  /* ── Filter bar ── */
  .nv-filterbar {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 16px 24px;
    margin-bottom: 28px;
    display: flex; align-items: center; gap: 24px; flex-wrap: wrap;
  }}
  .nv-filter-label {{
    font-size: 10px; font-weight: 700; color: {MUTED};
    text-transform: uppercase; letter-spacing: 1.5px;
    white-space: nowrap;
  }}

  /* Dropdowns in filter bar */
  div[data-baseweb="select"] > div {{
    background-color: {BG} !important;
    border-color: {BORDER} !important;
    color: {TEXT} !important;
    min-height: 36px !important;
  }}
  div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {{
    background-color: {CARD} !important;
    border: 1px solid {BORDER} !important;
  }}
  div[data-baseweb="option"] {{ background-color: {CARD} !important; color: {TEXT} !important; }}
  div[data-baseweb="option"]:hover {{ background-color: {BORDER} !important; }}
  span[data-baseweb="tag"] {{ background-color: #1A3A55 !important; color: {TEXT} !important; }}
  span[data-baseweb="tag"] span {{ color: {TEXT} !important; }}
  input, textarea, select {{ color: {TEXT} !important; background: {BG} !important; }}

  /* ── KPI cards — wide, airy ── */
  .kpi-row {{ display: flex; gap: 16px; margin-bottom: 28px; }}
  .kpi-card {{
    flex: 1;
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 28px 28px 24px 28px;
    position: relative;
    overflow: hidden;
  }}
  .kpi-card::before {{
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: {ORANGE};
  }}
  .kpi-card.blue::before {{ background: {BLUE}; }}
  .kpi-card.green::before {{ background: {GREEN}; }}
  .kpi-label {{ font-size: 10px; font-weight: 700; color: {MUTED}; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px; }}
  .kpi-value {{ font-size: 32px; font-weight: 800; color: {ORANGE}; line-height: 1; }}
  .kpi-value.blue {{ color: {BLUE}; }}
  .kpi-value.green {{ color: {GREEN}; }}
  .kpi-sub {{ font-size: 12px; color: {MUTED}; margin-top: 8px; }}

  /* ── Section header ── */
  .nv-section-hdr {{
    font-size: 11px; font-weight: 700; color: {ORANGE};
    text-transform: uppercase; letter-spacing: 2px;
    border-left: 3px solid {ORANGE};
    padding-left: 12px;
    margin-bottom: 18px;
    line-height: 1.4;
  }}

  /* ── Chart wrapper ── */
  .chart-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 24px;
  }}

  /* ── Rec cards ── */
  .rec-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-left: 3px solid {ORANGE};
    border-radius: 8px;
    padding: 18px 22px;
    margin-bottom: 12px;
  }}
  .rec-badge {{ font-size: 9px; font-weight: 700; color: {ORANGE}; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px; }}
  .rec-action {{ font-size: 14px; font-weight: 600; color: {WHITE}; }}
  .rec-reason {{ font-size: 12px; color: {MUTED}; margin-top: 5px; line-height: 1.6; }}
  .rec-impact {{ font-size: 11px; font-weight: 600; color: {ORANGE}; margin-top: 8px; }}

  /* ── Profile ── */
  .profile-card {{
    background: {CARD}; border: 1px solid {BORDER};
    border-radius: 10px; padding: 22px 24px;
  }}
  .prow {{ display: flex; justify-content: space-between; padding: 7px 0; border-bottom: 1px solid {BORDER}; }}
  .pkey {{ font-size: 10px; color: {MUTED}; text-transform: uppercase; letter-spacing: 0.8px; }}
  .pval {{ font-size: 12px; color: {WHITE}; font-weight: 600; }}

  /* ── Divider ── */
  .nv-divider {{ border: none; border-top: 1px solid {BORDER}; margin: 28px 0; }}

  /* ── Expand/collapse account selector ── */
  .stExpander {{ background: {CARD} !important; border: 1px solid {BORDER} !important; border-radius: 8px !important; }}
  .stExpander summary {{ color: {TEXT} !important; }}
</style>
""", unsafe_allow_html=True)

# ── Data ───────────────────────────────────────────────────────────────────────


@st.cache_data
def generate_data(n=140, seed=7):
    np.random.seed(seed)
    regions = ["North", "South", "East", "West", "Central"]
    grades = ["Grade A", "Grade B", "Grade C"]
    segments = ["High Value", "Growth", "At-Risk", "Dormant"]
    channels = ["Direct", "Distributor", "Online", "Partner"]
    df = pd.DataFrame({
        "Account ID":          [f"ACC-{2000+i}" for i in range(n)],
        "Account Name":        [f"Account {chr(65+i%26)}{i//26+1:02d}" for i in range(n)],
        "Region":              np.random.choice(regions, n),
        "Grade":               np.random.choice(grades, n, p=[0.20, 0.45, 0.35]),
        "Segment":             np.random.choice(segments, n, p=[0.25, 0.35, 0.25, 0.15]),
        "Channel":             np.random.choice(channels, n),
        "Monthly Revenue ($)": np.random.lognormal(9.5, 0.8, n).round(0).astype(int),
        "Engagement Score":    np.random.randint(1, 12, n),
        "Days Since Contact":  np.random.randint(7, 180, n),
        "Products Active":     np.random.randint(2, 18, n),
        "Growth (MoM %)":      np.round(np.random.normal(3.5, 12, n), 1),
    })
    score = (
        0.30*(df["Monthly Revenue ($)"]/df["Monthly Revenue ($)"].max()) +
        0.25*(df["Products Active"]/18) +
        0.20*(df["Engagement Score"]/12) +
        0.15*(1-df["Days Since Contact"]/180) +
        0.10*(df["Growth (MoM %)"].clip(-20, 20)/40+0.5)
    )
    df["Priority Score"] = (score*100).clip(10, 99).round(1)

    def get_nba(row):
        if row["Products Active"] < 5:
            return "Expand Product Portfolio", "Low activation — distribution opportunity exists.", f"+${int(row['Monthly Revenue ($)']*0.18):,} est. uplift"
        elif row["Days Since Contact"] > 90:
            return "Re-Engagement Outreach", "No contact in 90+ days — disengagement risk.", "Retention — immediate outreach"
        elif row["Segment"] == "Growth" and row["Engagement Score"] < 4:
            return "Strategic Review Session", "Growth account with low engagement.", f"+{np.random.randint(8,22)}% retention probability"
        elif row["Growth (MoM %)"] < -5:
            return "Targeted Incentive Offer", "Declining revenue — targeted offer recommended.", f"Arrest {abs(row['Growth (MoM %)']):.1f}% decline"
        elif row["Grade"] == "Grade A" and row["Products Active"] < 12:
            return "Premium Activation Campaign", "Grade A with untapped product lines.", f"+${int(row['Monthly Revenue ($)']*0.12):,} est. uplift"
        else:
            return "Account Check-In", "Maintain relationship and gather feedback.", "Relationship & retention"

    nba = df.apply(get_nba, axis=1, result_type="expand")
    df["Next Best Action"] = nba[0]
    df["Recommendation Reason"] = nba[1]
    df["Expected Impact"] = nba[2]
    df["Priority"] = pd.cut(df["Priority Score"], bins=[
                            0, 40, 70, 100], labels=["Low", "Medium", "High"])
    return df.sort_values("Priority Score", ascending=False).reset_index(drop=True)


df = generate_data()

PBG = CARD
PF = dict(family="Inter", size=11, color=MUTED)
PL = dict(paper_bgcolor=PBG, plot_bgcolor=PBG,
          font=PF, margin=dict(t=44, b=10, l=10, r=10))

# ── Top nav ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="nv-nav">
  <div><img src="data:image/png;base64,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" style="height:44px;object-fit:contain;display:block;" alt="Nuvora"/></div>
  <div><span class="nv-nav-pill">Next Best Action Engine</span></div>
  <div class="nv-nav-right">Commercial Analytics · Synthetic Demo</div>
</div>
""", unsafe_allow_html=True)

# ── Filter bar ─────────────────────────────────────────────────────────────────
with st.container():
    fc1, fc2, fc3, fc4, fc5 = st.columns([0.5, 1.5, 1.5, 1.5, 1.5])
    with fc1:
        st.markdown(
            '<div class="nv-filter-label" style="padding-top:8px;">Filters</div>', unsafe_allow_html=True)
    with fc2:
        sel_region = st.multiselect("Region", sorted(df["Region"].unique()), default=sorted(
            df["Region"].unique()), label_visibility="collapsed", placeholder="All Regions")
    with fc3:
        sel_grade = st.multiselect("Grade", sorted(df["Grade"].unique()), default=sorted(
            df["Grade"].unique()), label_visibility="collapsed", placeholder="All Grades")
    with fc4:
        sel_segment = st.multiselect("Segment", sorted(df["Segment"].unique()), default=sorted(
            df["Segment"].unique()), label_visibility="collapsed", placeholder="All Segments")
    with fc5:
        sel_priority = st.multiselect("Priority", ["High", "Medium", "Low"], default=[
                                      "High", "Medium", "Low"], label_visibility="collapsed", placeholder="All Priorities")

fdf = df[
    df["Region"].isin(sel_region if sel_region else df["Region"].unique()) &
    df["Grade"].isin(sel_grade if sel_grade else df["Grade"].unique()) &
    df["Segment"].isin(sel_segment if sel_segment else df["Segment"].unique()) &
    df["Priority"].isin(sel_priority if sel_priority else [
                        "High", "Medium", "Low"])
].reset_index(drop=True)

# ── KPI row ────────────────────────────────────────────────────────────────────
top_action = fdf["Next Best Action"].value_counts(
).index[0] if len(fdf) else "—"
high_n = int((fdf["Priority"] == "High").sum())
avg_rev = fdf["Monthly Revenue ($)"].mean() if len(fdf) else 0
avg_score = fdf["Priority Score"].mean() if len(fdf) else 0
opp_pool = int(fdf[fdf["Priority"] == "High"]
               ["Monthly Revenue ($)"].sum() * 0.15)

k1, k2, k3, k4, k5 = st.columns(5)
kpis = [
    (k1, "Accounts in View",   str(len(fdf)),
     f"of {len(df)} total", ""),
    (k2, "High Priority",      str(high_n),
     "immediate action",    ""),
    (k3, "Avg Monthly Revenue", f"${avg_rev:,.0f}",
     "across filtered",     "blue"),
    (k4, "Avg Priority Score", f"{avg_score:.1f}",
     "out of 100",          ""),
    (k5, "Opportunity Pool",   f"${opp_pool:,}",
     "est. high-pri uplift", "green"),
]
for col, label, value, sub, cls in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card {cls}">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value {cls}" style="font-size:{'22px' if len(value)>9 else '32px'}">{value}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── CHARTS ROW 1 — full width, dominating ─────────────────────────────────────
st.markdown('<div class="nv-section-hdr">Portfolio Overview</div>',
            unsafe_allow_html=True)

ch1, ch2, ch3 = st.columns([1.4, 1, 1])

with ch1:
    # Score vs Revenue — the hero chart
    fig_main = px.scatter(
        fdf, x="Priority Score", y="Monthly Revenue ($)",
        color="Priority", size="Products Active",
        color_discrete_map={"High": ORANGE, "Medium": BLUE, "Low": BORDER},
        hover_data=["Account Name", "Grade", "Segment", "Next Best Action"],
        title="Account Universe — Priority Score vs. Revenue"
    )
    fig_main.update_layout(
        **PL, height=340,
        title_font=dict(size=13, color=ORANGE, family="Inter"),
        legend=dict(orientation="h", y=-0.18, font=dict(size=10, color=MUTED)),
        xaxis=dict(showgrid=True, gridcolor=GRID,
                   title="Priority Score", color=MUTED),
        yaxis=dict(showgrid=True, gridcolor=GRID,
                   title="Monthly Revenue ($)", color=MUTED),
    )
    st.plotly_chart(fig_main, use_container_width=True)

with ch2:
    # Action distribution — donut
    ac = fdf["Next Best Action"].value_counts().reset_index()
    ac.columns = ["Action", "Count"]
    # Shorten labels
    ac["Short"] = ac["Action"].str.replace(" Portfolio", "").str.replace(" Outreach", "").str.replace(
        " Session", "").str.replace(" Campaign", "").str.replace(" Offer", "").str.replace(" Check-In", "")
    fig2 = go.Figure(go.Pie(
        labels=ac["Short"], values=ac["Count"],
        hole=0.55,
        marker=dict(colors=[ORANGE, "#C8590A", BLUE, "#1A5F8A", "#2A7A9B", "#3A6A8A"],
                    line=dict(color=BG, width=2)),
        textfont=dict(size=10, color=WHITE),
        hovertemplate="%{label}<br>%{value} accounts<extra></extra>"
    ))
    fig2.add_annotation(text=f"<b>{len(fdf)}</b><br><span style='font-size:10px'>accounts</span>",
                        x=0.5, y=0.5, showarrow=False, font=dict(size=14, color=WHITE))
    fig2.update_layout(
        paper_bgcolor=PBG, plot_bgcolor=PBG, font=PF,
        height=340,
        title="Action Mix",
        title_font=dict(size=13, color=ORANGE, family="Inter"),
        legend=dict(orientation="v", font=dict(size=9, color=MUTED), x=1.02),
        margin=dict(t=44, b=10, l=10, r=80),
        showlegend=True
    )
    st.plotly_chart(fig2, use_container_width=True)

with ch3:
    # Regional performance
    rg = fdf.groupby("Region").agg(
        avg_rev=("Monthly Revenue ($)", "mean"),
        avg_score=("Priority Score", "mean"),
        count=("Account ID", "count")
    ).reset_index().sort_values("avg_rev", ascending=True)

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        y=rg["Region"], x=rg["avg_rev"],
        orientation="h", name="Avg Revenue",
        marker=dict(color=BLUE, opacity=0.85),
        text=rg["avg_rev"].apply(lambda v: f"${v:,.0f}"),
        textposition="outside", textfont=dict(color=MUTED, size=10),
    ))
    fig3.add_trace(go.Scatter(
        y=rg["Region"], x=rg["avg_score"] * (rg["avg_rev"].max()/100),
        mode="markers", name="Avg Score",
        marker=dict(color=ORANGE, size=10, symbol="diamond"),
        xaxis="x"
    ))
    fig3.update_layout(
        **PL, height=340,
        title="Regional Snapshot",
        title_font=dict(size=13, color=ORANGE, family="Inter"),
        legend=dict(orientation="h", y=-0.18, font=dict(size=10, color=MUTED)),
        xaxis=dict(showgrid=True, gridcolor=GRID, title="", color=MUTED),
        yaxis=dict(showgrid=False, title="", color=MUTED),
        barmode="overlay"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ── CHARTS ROW 2 ───────────────────────────────────────────────────────────────
ch4, ch5 = st.columns([1, 1])

with ch4:
    sp2 = fdf.groupby(["Segment", "Priority"]).size().reset_index(name="Count")
    fig4 = px.bar(sp2, x="Segment", y="Count", color="Priority",
                  color_discrete_map={"High": ORANGE,
                                      "Medium": BLUE, "Low": BORDER},
                  title="Priority Breakdown by Segment", barmode="stack")
    fig4.update_layout(
        **PL, height=280,
        title_font=dict(size=13, color=ORANGE, family="Inter"),
        legend=dict(orientation="h", y=-0.22, font=dict(size=10, color=MUTED)),
        xaxis=dict(showgrid=False, title="", color=MUTED),
        yaxis=dict(showgrid=True, gridcolor=GRID, title="", color=MUTED),
    )
    st.plotly_chart(fig4, use_container_width=True)

with ch5:
    grade_seg = fdf.groupby("Grade")["Monthly Revenue ($)"].mean(
    ).reset_index().sort_values("Monthly Revenue ($)", ascending=False)
    fig5 = px.bar(grade_seg, x="Grade", y="Monthly Revenue ($)",
                  color="Grade",
                  color_discrete_map={"Grade A": ORANGE,
                                      "Grade B": BLUE, "Grade C": BORDER},
                  title="Avg Revenue by Grade",
                  text="Monthly Revenue ($)")
    fig5.update_traces(texttemplate="$%{text:,.0f}", textposition="outside", textfont=dict(
        color=MUTED, size=10))
    fig5.update_layout(
        **PL, height=280, showlegend=False,
        title_font=dict(size=13, color=ORANGE, family="Inter"),
        xaxis=dict(showgrid=False, title="", color=MUTED),
        yaxis=dict(showgrid=True, gridcolor=GRID, title="", color=MUTED),
    )
    st.plotly_chart(fig5, use_container_width=True)

# ── ACCOUNT DEEP DIVE ──────────────────────────────────────────────────────────
st.markdown("<div class='nv-divider'></div>", unsafe_allow_html=True)
st.markdown('<div class="nv-section-hdr">Account Deep Dive & Recommendations</div>',
            unsafe_allow_html=True)

dd1, dd2, dd3 = st.columns([1.2, 1.2, 1.6])

with dd1:
    st.markdown("<div style='font-size:11px;color:#4A7A9B;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>Select Account</div>", unsafe_allow_html=True)
    sel = st.selectbox(
        "Account", fdf["Account ID"]+" — "+fdf["Account Name"], label_visibility="collapsed")
    acc = fdf[fdf["Account ID"] == sel.split(" — ")[0]].iloc[0]
    gc = GREEN if acc["Growth (MoM %)"] > 0 else RED
    cc = RED if acc["Days Since Contact"] > 90 else WHITE
    st.markdown(f"""
    <div class="profile-card" style="margin-top:12px;">
      <div style="font-size:18px;font-weight:700;color:{WHITE};margin-bottom:2px;">{acc['Account Name']}</div>
      <div style="font-size:11px;color:{MUTED};margin-bottom:16px;">{acc['Account ID']} · {acc['Region']} · {acc['Channel']}</div>
      <div class="prow"><span class="pkey">Grade</span><span class="pval">{acc['Grade']}</span></div>
      <div class="prow"><span class="pkey">Segment</span><span class="pval">{acc['Segment']}</span></div>
      <div class="prow"><span class="pkey">Monthly Revenue</span><span class="pval">${acc['Monthly Revenue ($)']:,}</span></div>
      <div class="prow"><span class="pkey">Growth MoM</span><span style="color:{gc};font-weight:600;">{acc['Growth (MoM %)']:+.1f}%</span></div>
      <div class="prow"><span class="pkey">Products Active</span><span class="pval">{acc['Products Active']}</span></div>
      <div class="prow" style="border:none;"><span class="pkey">Days Since Contact</span><span style="color:{cc};font-weight:600;">{acc['Days Since Contact']}</span></div>
    </div>""", unsafe_allow_html=True)

with dd2:
    st.markdown("<div style='font-size:11px;color:#4A7A9B;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>Priority Score</div>", unsafe_allow_html=True)
    score = acc["Priority Score"]
    fig_g = go.Figure(go.Indicator(
        mode="gauge+number", value=score,
        number={"font": {"size": 44, "color": ORANGE,
                         "family": "Inter"}, "suffix": ""},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": BORDER, "tickfont": {"size": 9, "color": MUTED}},
            "bar": {"color": ORANGE, "thickness": 0.24},
            "bgcolor": CARD, "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "#1A2E42"},
                {"range": [40, 70], "color": "#1A3A52"},
                {"range": [70, 100], "color": "#1A4A6A"}
            ],
            "threshold": {"line": {"color": ORANGE, "width": 3}, "thickness": 0.8, "value": score}
        }
    ))
    fig_g.update_layout(height=220, margin=dict(
        t=10, b=0, l=20, r=20), paper_bgcolor=CARD, font={"family": "Inter"})
    st.plotly_chart(fig_g, use_container_width=True)

    # Mini stats under gauge
    pri_color = {"High": ORANGE, "Medium": BLUE,
                 "Low": MUTED}.get(str(acc["Priority"]), MUTED)
    st.markdown(f"""
    <div style="display:flex;gap:12px;margin-top:4px;">
      <div style="flex:1;background:{BG};border:1px solid {BORDER};border-radius:6px;padding:10px 14px;text-align:center;">
        <div style="font-size:9px;color:{MUTED};text-transform:uppercase;letter-spacing:1px;">Priority</div>
        <div style="font-size:16px;font-weight:700;color:{pri_color};margin-top:4px;">{acc['Priority']}</div>
      </div>
      <div style="flex:1;background:{BG};border:1px solid {BORDER};border-radius:6px;padding:10px 14px;text-align:center;">
        <div style="font-size:9px;color:{MUTED};text-transform:uppercase;letter-spacing:1px;">Engagement</div>
        <div style="font-size:16px;font-weight:700;color:{WHITE};margin-top:4px;">{acc['Engagement Score']}/12</div>
      </div>
    </div>""", unsafe_allow_html=True)

with dd3:
    st.markdown("<div style='font-size:11px;color:#4A7A9B;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>Recommended Actions</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="rec-card">
      <div class="rec-badge">◈ Primary</div>
      <div class="rec-action">{acc['Next Best Action']}</div>
      <div class="rec-reason">{acc['Recommendation Reason']}</div>
      <div class="rec-impact">Expected impact: {acc['Expected Impact']}</div>
    </div>""", unsafe_allow_html=True)

    secondary = []
    if acc["Products Active"] < 8:
        secondary.append(("Review Assortment Coverage",
                         "Below-average product range — expansion opportunity.", "Assortment"))
    if acc["Days Since Contact"] > 60:
        secondary.append(
            ("Schedule Follow-Up", "Contact cadence below target for this grade.", "Relationship"))
    if acc["Growth (MoM %)"] > 10:
        secondary.append(
            ("Upsell Premium Tier", "Strong growth — receptive to premium introductions.", "Revenue"))
    if acc["Segment"] == "At-Risk":
        secondary.append(("Retention Intervention",
                         "At-risk — early action reduces churn probability.", "Churn prevention"))
    for action, reason, impact in secondary[:3]:
        st.markdown(f"""
        <div class="rec-card" style="border-left-color:{BLUE};">
          <div class="rec-badge" style="color:{BLUE};">◈ Secondary</div>
          <div class="rec-action" style="color:#7ABEDE;">{action}</div>
          <div class="rec-reason">{reason}</div>
          <div class="rec-impact" style="color:{BLUE};">Context: {impact}</div>
        </div>""", unsafe_allow_html=True)

# ── ACCOUNT TABLE ──────────────────────────────────────────────────────────────
st.markdown("<div class='nv-divider'></div>", unsafe_allow_html=True)
tl, tr = st.columns([3, 1])
with tl:
    st.markdown('<div class="nv-section-hdr">Account Prioritization Table</div>',
                unsafe_allow_html=True)
with tr:
    sort_by = st.selectbox("Sort", [
                           "Priority Score", "Monthly Revenue ($)", "Growth (MoM %)"], label_visibility="collapsed")

disp = fdf.sort_values(sort_by, ascending=False)[[
    "Account ID", "Account Name", "Region", "Grade", "Segment", "Channel",
    "Priority Score", "Monthly Revenue ($)", "Products Active",
    "Growth (MoM %)", "Days Since Contact", "Priority", "Next Best Action"
]].copy()


def sp(v): return {"High": f"background-color:#7A3800;color:{ORANGE}",
                   "Medium": f"background-color:#0A2A4A;color:{BLUE}", "Low": f"background-color:{BORDER};color:{MUTED}"}.get(v, "")


def ss(v): return f"color:{ORANGE};font-weight:700" if v >= 70 else (
    f"color:{BLUE};font-weight:600" if v >= 40 else f"color:{MUTED}")


def sg(v): return f"color:{GREEN};font-weight:600" if v > 5 else (
    f"color:{RED};font-weight:600" if v < -5 else f"color:{MUTED}")


st.dataframe(
    disp.style.applymap(sp, subset=["Priority"]).applymap(ss, subset=["Priority Score"]).applymap(sg, subset=[
        "Growth (MoM %)"]).format({"Monthly Revenue ($)": "${:,.0f}", "Priority Score": "{:.1f}", "Growth (MoM %)": "{:+.1f}%"}),
    use_container_width=True, height=420
)
st.markdown(
    f"<div style='font-size:11px;color:{MUTED};margin-top:6px;'>{len(disp)} accounts</div>", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;font-size:11px;color:#2A4A62;
  padding:20px 0;border-top:1px solid {BORDER};margin-top:32px;">
  nuv◉ra Analytics &nbsp;·&nbsp; Next Best Action Demo
  &nbsp;·&nbsp; Synthetic data — illustrative purposes only
</div>""", unsafe_allow_html=True)
