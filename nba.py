import streamlit as st

st.markdown(
    '<div class="nv-section-hdr">Account Prioritization Table</div>',
    unsafe_allow_html=True
)

disp = fdf[[
    "Account ID",
    "Account Name",
    "Region",
    "Grade",
    "Monthly Revenue ($)",
    "Products Active",
    "Priority Score",
    "Growth (MoM %)",
    "Priority",
    "Next Best Action"
]].copy()


def sp(v):
    return {
        "High": f"background-color:#FEF3C7;color:#92400E;font-weight:700",
        "Medium": f"background-color:#DBEAFE;color:#1E40AF;font-weight:700",
        "Low": f"background-color:#F3F4F6;color:#6B7280;font-weight:700"
    }.get(v, "")


def ss(v):
    return (
        f"color:{ORANGE};font-weight:700"
        if v >= 70
        else f"color:{BLUE};font-weight:600"
    )


def sg(v): return f"color:{GREEN};font-weight:600" if v > 5 else (
    f"color:{RED};font-weight:600" if v < -5 else f"color:{MUTED}")


# st.dataframe(
#     disp.style.applymap(sp, subset=["Priority"]).applymap(ss, subset=["Priority Score"]).applymap(sg, subset=[
#         "Growth (MoM %)"]).format({"Monthly Revenue ($)": "${:,.0f}", "Priority Score": "{:.1f}", "Growth (MoM %)": "{:+.1f}%"}),
#     use_container_width=True, height=420
# )

styled_disp = (
    disp.style
    .map(sp, subset=["Priority"])
    .map(ss, subset=["Priority Score"])
    .map(sg, subset=["Growth (MoM %)"])
    .format({
        "Monthly Revenue ($)": "${:,.0f}",
        "Priority Score": "{:.1f}",
        "Growth (MoM %)": "{:+.1f}%"
    })
)

st.dataframe(
    styled_disp,
    use_container_width=True,
    height=420
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
