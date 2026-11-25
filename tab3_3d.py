import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def render_tab3(df, find_image):
    st.subheader("🧬 3D Pollution Fingerprinting & Individual Sample Detective")
    st.markdown("""
    <div class="story-box">
        <b>How to use this tab:</b> Every water sample leaves a unique chemical fingerprint. 
        Select <b>any of the 3,276 samples</b> below to see its exact location in <b>3D Chemical Space</b>, inspect its <b>9-Parameter Pollution Radar</b>, and read a plain-English diagnosis of why it is polluted and how to treat it.
    </div>
    """, unsafe_allow_html=True)

    if df is None:
        st.error("cleaned_water_data.csv not found.")
        return

    raw_cols = ["ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity"]
    features = df[raw_cols]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["Cluster_ID"] = kmeans.fit_predict(X_scaled)

    group_names = {
        0: "🔵 Group 1: Cloudy & Chlorinated Surface Water",
        1: "🟠 Group 2: High-Salt & Mineral Runoff Water",
        2: "🟢 Group 3: Hard & Alkaline Groundwater"
    }
    group_treatments = {
        0: "Coagulation, Flocculation & Sand/Carbon Filtration (to remove suspended silt & excess chloramines)",
        1: "Reverse Osmosis (RO) Desalination & Ion Exchange (to strip heavy dissolved salts & sulfates)",
        2: "Lime-Soda Softening & Zeolite Ion-Exchange (to remove Ca²⁺/Mg²⁺ hardness and prevent boiler scale)"
    }
    df["Pollution Group"] = df["Cluster_ID"].map(group_names)

    st.markdown("### 🔎 Pick Any Water Sample to Inspect (0 to 3,275)")
    sel_col1, sel_col2 = st.columns([2, 1])
    with sel_col1:
        sample_idx = st.slider("Slide to choose a water sample:", 0, len(df) - 1, 42, key="tab3_slider")
    with sel_col2:
        sample_idx = st.number_input("Or type exact Sample ID:", min_value=0, max_value=len(df) - 1, value=sample_idx, step=1)

    sample = df.iloc[sample_idx]
    cid = int(sample["Cluster_ID"])
    assigned_group = group_names[cid]

    limits = {
        "ph": ("pH Level", 6.5, 8.5, "pH units", "Controls acidity/alkalinity & pipe corrosion"),
        "Hardness": ("Hardness (Ca²⁺/Mg²⁺)", 0, 200.0, "mg/L", "Causes white scale buildup in boilers & pipes"),
        "Solids": ("Solids / TDS", 0, 500.0, "mg/L", "High dissolved salts from mineral/industrial runoff"),
        "Chloramines": ("Chloramines", 0, 4.0, "mg/L", "Excess chemical disinfectant causes odor & irritation"),
        "Sulfate": ("Sulfate (SO₄²⁻)", 0, 250.0, "mg/L", "Bitter taste, pipe corrosion & laxative effect"),
        "Conductivity": ("Conductivity", 0, 400.0, "µS/cm", "High electrical conductivity from dissolved ions"),
        "Organic_carbon": ("Organic Carbon (TOC)", 0, 10.0, "mg/L", "Decaying organic matter that reacts with chlorine"),
        "Trihalomethanes": ("Trihalomethanes", 0, 80.0, "µg/L", "Harmful chlorination byproducts"),
        "Turbidity": ("Turbidity", 0, 5.0, "NTU", "Suspended mud/colloids that shield bacteria")
    }

    breakdown_rows = []
    radar_labels = []
    radar_sample_pct = []
    unsafe_count = 0

    for col, (label, low, high, unit, reason) in limits.items():
        val = float(sample[col])
        radar_labels.append(label.split(" (")[0])
        
        if col == "ph":
            if low <= val <= high:
                status = "✅ Safe"
                level_txt = "Normal (Balanced)"
                pct_of_limit = 75.0
            elif val < low:
                status = "⚠️ Polluted (Acidic)"
                level_txt = f"{low - val:.2f} units too acidic"
                pct_of_limit = min(200.0, 100 + (low - val) * 25)
                unsafe_count += 1
            else:
                status = "⚠️ Polluted (Alkaline)"
                level_txt = f"{val - high:.2f} units too basic"
                pct_of_limit = min(200.0, 100 + (val - high) * 25)
                unsafe_count += 1
            limit_str = "6.5 – 8.5"
        else:
            ratio = (val / high) * 100
            pct_of_limit = min(220.0, ratio)
            if val <= high:
                status = "✅ Safe"
                level_txt = f"Within limit ({ratio:.0f}% of max)"
            elif ratio <= 150:
                status = "🟡 Mildly High"
                level_txt = f"{ratio/100:.1f}x above safe limit"
                unsafe_count += 1
            else:
                status = "🔴 Heavily Polluted"
                level_txt = f"{ratio/100:.1f}x above safe limit"
                unsafe_count += 1
            limit_str = f"< {high} {unit}"

        radar_sample_pct.append(pct_of_limit)
        breakdown_rows.append({
            "Chemical Parameter": label,
            "Sample Value": f"{val:.2f} {unit}",
            "WHO/BIS Safe Limit": limit_str,
            "Status": status,
            "Pollution Level": level_txt,
            "Why It Matters": reason
        })

    if unsafe_count <= 2:
        severity = "🟢 LOW POLLUTION (Mostly Clean)"
    elif unsafe_count <= 4:
        severity = "🟡 MODERATE POLLUTION (Needs Standard Filtration)"
    elif unsafe_count <= 6:
        severity = "🟠 HIGH POLLUTION (Multi-Stage Treatment Needed)"
    else:
        severity = "🔴 SEVERE POLLUTION (Heavily Contaminated)"

    m1, m2, m3 = st.columns(3)
    m1.metric("Selected Sample ID", f"Sample #{sample_idx}", "Potable" if sample["Potability"] == 1 else "Non-Potable")
    m2.metric("Assigned Fingerprint Group", assigned_group.split(": ")[1])
    m3.metric("Overall Pollution Level", f"{unsafe_count} / 9 Unsafe", severity.split(" (")[0])

    st.info(f"""
    **🧪 Plain-English Diagnosis for Sample #{sample_idx}:**
    * **Pollution Severity:** **{severity}** — {unsafe_count} out of 9 parameters exceed WHO/BIS safe limits.
    * **Chemical Family:** Belongs to **{assigned_group}**.
    * **Recommended ChemTech Treatment:** {group_treatments[cid]}
    """)

    viz1, viz2 = st.columns([1.25, 1])

    with viz1:
        st.markdown("#### 🌐 3D Chemical Space (Drag to Rotate, Scroll to Zoom)")
        fig_3d = px.scatter_3d(
            df, x="Solids", y="Hardness", z="Turbidity",
            color="Pollution Group",
            color_discrete_map={
                "🔵 Group 1: Cloudy & Chlorinated Surface Water": "#0096c7",
                "🟠 Group 2: High-Salt & Mineral Runoff Water": "#f77f00",
                "🟢 Group 3: Hard & Alkaline Groundwater": "#2a9d8f"
            },
            opacity=0.45,
            height=500
        )
        fig_3d.update_traces(marker=dict(size=3))
        fig_3d.add_trace(go.Scatter3d(
            x=[sample["Solids"]],
            y=[sample["Hardness"]],
            z=[sample["Turbidity"]],
            mode="markers+text",
            marker=dict(size=12, color="#ff0055", symbol="diamond", line=dict(color="white", width=2)),
            text=[f"⭐ Sample #{sample_idx}"],
            textposition="top center",
            name=f"Selected Sample #{sample_idx}"
        ))
        fig_3d.update_layout(margin=dict(l=0, r=0, t=10, b=0), legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig_3d, use_container_width=True)
        st.caption("The **pink diamond** shows where your chosen sample sits inside the 3D cloud of all 3,276 samples.")

    with viz2:
        st.markdown("#### 🕸️ Virtual Pollution Fingerprint Radar")
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[100] * 9,
            theta=radar_labels,
            fill="toself",
            fillcolor="rgba(42, 157, 143, 0.15)",
            line=dict(color="#2a9d8f", dash="dash", width=2),
            name="100% Safe Limit Zone"
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_sample_pct,
            theta=radar_labels,
            fill="toself",
            fillcolor="rgba(255, 0, 85, 0.25)",
            line=dict(color="#ff0055", width=2.5),
            name=f"Sample #{sample_idx}"
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 220], ticksuffix="%")),
            margin=dict(l=40, r=40, t=30, b=20),
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.caption("Any red spike poking **outside the green dashed circle** is a pollutant exceeding safe limits.")

    st.markdown(f"#### 📋 Complete 9-Parameter Pollution Breakdown for Sample #{sample_idx}")
    st.dataframe(pd.DataFrame(breakdown_rows), use_container_width=True, hide_index=True)

    with st.expander("📊 View Full Dataset Correlation Heatmap & Overall Group Chart"):
        c_left, c_right = st.columns(2)
        with c_left:
            img_corr = find_image("correlation_heatmap")
            if img_corr:
                st.image(img_corr, use_container_width=True)
        with c_right:
            img_fp = find_image("pollution_fingerprints_chart")
            if img_fp:
                st.image(img_fp, use_container_width=True)
