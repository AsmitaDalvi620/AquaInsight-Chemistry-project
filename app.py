import streamlit as st
import pandas as pd
import joblib
import os
from tab3_3d import render_tab3

st.set_page_config(page_title="AquaInsight | AI Water Intelligence", page_icon="💧", layout="wide")

st.markdown("""
<style>
[data-testid="stStatusWidget"],
    .viewerBadge_container__r5tak,
    .styles_viewerBadge__CvC9N,
    div[class^="viewerBadge_"],
    a[href*="streamlit.io/cloud"] {
        display: none !important;
        visibility: hidden !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent;}
.hero-banner {background: linear-gradient(120deg, #005f73, #0a9396, #94d2bd); padding: 22px 28px; border-radius: 16px; color: white; margin-bottom: 16px;}
.chem-card {background: #f8fbfc; border-top: 4px solid #0a9396; border-radius: 12px; padding: 14px; margin-bottom: 12px; box-shadow: 0 3px 10px rgba(0,0,0,0.06); height: 225px;}
.chem-title {font-size: 17px; font-weight: 700; color: #005f73; margin-bottom: 4px;}
.limit-badge {display: inline-block; background: #e0fbfc; color: #005f73; font-weight: 600; font-size: 12px; padding: 2px 10px; border-radius: 20px; margin-bottom: 8px;}
.story-box {background: #f0f9ff; border-left: 5px solid #0284c7; padding: 14px 18px; border-radius: 8px; margin-bottom: 16px;}
</style>
""", unsafe_allow_html=True)

def load_table(base_name):
    for ext in [".csv", ".xlsx", ".xls"]:
        if os.path.exists(f"{base_name}{ext}"):
            return pd.read_csv(f"{base_name}{ext}") if ext == ".csv" else pd.read_excel(f"{base_name}{ext}")
    return None

def find_image(base_name):
    for ext in [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]:
        if os.path.exists(f"{base_name}{ext}"):
            return f"{base_name}{ext}"
    return None

st.markdown("""
<div class="hero-banner">
    <h1 style="margin:0; font-size:30px;">💧 AquaInsight: AI-Based Water Quality & Pollution Fingerprinting</h1>
    <p style="margin:5px 0 0 0; font-size:15px;"><b>First-Year ChemTech Research Project</b> • Analytical Chemistry • 3D Pollution Fingerprinting • Explainable AI</p>
</div>
""", unsafe_allow_html=True)

p1, p2, p3, p4 = st.columns(4)
p1.info("**Step 1: Chemistry**\n9 physicochemical parameters & WHO/BIS limits.")
p2.info("**Step 2: Screening**\nAudit 3,276 samples & catch extreme spikes.")
p3.info("**Step 3: 3D Fingerprinting**\nInspect any sample in 3D & diagnose pollution.")
p4.info("**Step 4: AI Prediction**\nPredict Safe vs. Unsafe & explain why.")

df = load_table("cleaned_water_data")
tab1, tab2, tab3, tab4 = st.tabs(["🧪 1. Chemistry Guide", "🔬 2. Sample Explorer & Spikes", "🧬 3. 3D Pollution Fingerprints", "🤖 4. Live AI Simulator"])

with tab1:
    st.subheader("🧪 The 9 Physicochemical Building Blocks of Water Quality")
    params = [
        ("⚗️ 1. pH Level", "Safe: 6.5 – 8.5", "#0a9396", "Hydrogen ion activity (-log[H⁺]) on an acidic-to-alkaline scale.", "Low pH corrodes pipes and leaches toxic metals; high pH causes scaling."),
        ("🪨 2. Hardness", "Safe: < 200 mg/L", "#0077b6", "Dissolved multivalent cations, mainly Calcium (Ca²⁺) and Magnesium (Mg²⁺).", "Forms hard CaCO₃ scale inside industrial boilers and heat exchangers."),
        ("🧂 3. Solids (TDS)", "Safe: < 500 mg/L", "#ee9b00", "Total Dissolved Solids—inorganic salts and trace organics in water.", "High TDS signals mineral dissolution or industrial effluent discharge."),
        ("🧪 4. Chloramines", "Safe: < 4.0 mg/L", "#ca6702", "Disinfectant (NH₂Cl) formed by reacting chlorine with ammonia.", "Kills pathogens in pipelines, but excess doses cause toxicity and odor."),
        ("🌋 5. Sulfate (SO₄²⁻)", "Safe: < 250 mg/L", "#bb3e03", "Anion leached from gypsum minerals or industrial chemical waste.", "Levels > 250 mg/L corrode concrete pipes and cause laxative effects."),
        ("⚡ 6. Conductivity", "Safe: < 400 µS/cm", "#ae2012", "Ability to carry electric current, driven by dissolved ion concentration.", "Fast sensor proxy for total ionic salinity and mineral contamination."),
        ("🌿 7. Organic Carbon", "Safe: < 10 mg/L", "#2a9d8f", "Total Organic Carbon (TOC) from decaying organic matter or waste.", "Reacts with chlorine during treatment to form toxic byproducts."),
        ("☣️ 8. Trihalomethanes", "Safe: < 80 µg/L", "#9b2226", "Volatile organic byproducts (e.g., chloroform) from water chlorination.", "Regulated potential carcinogens monitored in water treatment plants."),
        ("🌫️ 9. Turbidity", "Safe: < 5.0 NTU", "#5f0f40", "Cloudiness caused by suspended clay, silt, and colloidal particles.", "Shields bacteria from UV/chlorine disinfection and clogs filters.")
    ]
    for r in range(0, 9, 3):
        cols = st.columns(3)
        for i in range(3):
            title, badge, color, chem, impact = params[r + i]
            cols[i].markdown(f"""<div class="chem-card" style="border-top-color:{color};"><div class="chem-title">{title}</div><span class="limit-badge">{badge}</span><p style="font-size:13px;color:#1e293b;margin-bottom:5px;"><b>Chemistry:</b> {chem}</p><p style="font-size:12.5px;color:#475569;margin:0;"><b>Why It Matters:</b> {impact}</p></div>""", unsafe_allow_html=True)

with tab2:
    st.subheader("🔬 Dataset Audit & Extreme Chemical Spikes (3,276 Samples)")
    if df is not None:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Samples", "3,276", "100% Cleaned")
        m2.metric("Safe (Potable)", "1,278", "39.0% Pass")
        m3.metric("Unsafe (Non-Potable)", "1,998", "61.0% Unsafe")
        m4.metric("Extreme Outliers", "164", "Top 5% Spikes")
        sid = st.slider("Slide to inspect any real water sample (#0 to #3275):", 0, len(df)-1, 10, key="t2_s")
        row = df.iloc[sid]
        st.write(f"**Sample #{sid} Verdict:** {'✅ POTABLE (Safe)' if row['Potability'] == 1 else '⚠️ NON-POTABLE (Unsafe)'}")
        sc = st.columns(9)
        names = ["pH", "Hardness", "Solids", "Chloram.", "Sulfate", "Conduct.", "Org. C", "THMs", "Turbidity"]
        rcols = ["ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity"]
        for i in range(9):
            sc[i].metric(names[i], f"{row[rcols[i]]:.1f}")
    ca, cb = st.columns([1, 1.2])
    with ca:
        st.markdown("#### 📋 Safe Limit Failure Rates (%)")
        viol = load_table("regulatory_violations")
        if viol is not None: st.dataframe(viol, use_container_width=True, hide_index=True)
    with cb:
        st.markdown("#### 🚨 Normal Water (Blue) vs. Spikes (Red)")
        img_a = find_image("anomaly_plot")
        if img_a: st.image(img_a, use_container_width=True)

with tab3:
    render_tab3(df, find_image)

with tab4:
    st.subheader("🤖 Live AI Water Simulator & Chemical Explainer")
    b1, b2, b3 = st.columns(3)
    if b1.button("🚰 Preset 1: Clean Tap Water", use_container_width=True):
        st.session_state.update({"ph": 7.2, "hard": 140.0, "solids": 350.0, "chlor": 2.5, "sulf": 180.0, "cond": 310.0, "org": 6.0, "tri": 45.0, "turb": 2.0})
    if b2.button("🪨 Preset 2: Hard Groundwater", use_container_width=True):
        st.session_state.update({"ph": 8.1, "hard": 290.0, "solids": 28000.0, "chlor": 7.5, "sulf": 380.0, "cond": 550.0, "org": 15.0, "tri": 75.0, "turb": 4.2})
    if b3.button("🏭 Preset 3: Industrial Runoff", use_container_width=True):
        st.session_state.update({"ph": 4.3, "hard": 260.0, "solids": 45000.0, "chlor": 10.5, "sulf": 440.0, "cond": 680.0, "org": 22.0, "tri": 95.0, "turb": 6.1})

    lc, rc = st.columns([1.15, 1])
    with lc:
        p1, p2, p3 = st.columns(3)
        ph = p1.slider("pH (6.5–8.5)", 0.0, 14.0, st.session_state.get("ph", 7.2), 0.1)
        hard = p2.slider("Hardness (<200)", 40.0, 350.0, st.session_state.get("hard", 180.0), 1.0)
        solids = p3.slider("Solids (<500)", 300.0, 60000.0, st.session_state.get("solids", 18000.0), 100.0)
        chlor = p1.slider("Chloramines (<4)", 0.0, 14.0, st.session_state.get("chlor", 6.5), 0.1)
        sulf = p2.slider("Sulfate (<250)", 120.0, 500.0, st.session_state.get("sulf", 310.0), 1.0)
        cond = p3.slider("Conductivity (<400)", 180.0, 800.0, st.session_state.get("cond", 410.0), 5.0)
        org = p1.slider("Organic C (<10)", 2.0, 30.0, st.session_state.get("org", 12.0), 0.5)
        tri = p2.slider("THMs (<80)", 0.0, 130.0, st.session_state.get("tri", 65.0), 1.0)
        turb = p3.slider("Turbidity (<5)", 1.0, 7.0, st.session_state.get("turb", 3.5), 0.1)
        img_fi = find_image("feature_importance")
        if img_fi: st.image(img_fi, use_container_width=True)

    with rc:
        if os.path.exists("rf_model.pkl"):
            model = joblib.load("rf_model.pkl")
            cols = joblib.load("model_columns.pkl") if os.path.exists("model_columns.pkl") else ["ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity"]
            inp = pd.DataFrame([[ph, hard, solids, chlor, sulf, cond, org, tri, turb]], columns=cols)
            pred = int(model.predict(inp)[0])
            probs = model.predict_proba(inp)[0]
            if pred == 1:
                st.success(f"### ✅ POTABLE (Safe to Drink)\n**AI Confidence:** {probs[1]*100:.1f}%")
            else:
                st.error(f"### ⚠️ NON-POTABLE (Unsafe)\n**AI Risk Confidence:** {probs[0]*100:.1f}%")
            st.progress(int(probs[1]*100), text=f"Safety Score: {probs[1]*100:.1f}% Safe vs. {probs[0]*100:.1f}% Unsafe")
            bad = []
            if not (6.5 <= ph <= 8.5): bad.append(f"pH ({ph}) outside 6.5–8.5")
            if sulf > 250: bad.append(f"Sulfate ({sulf} mg/L) > 250")
            if hard > 200: bad.append(f"Hardness ({hard} mg/L) > 200")
            if solids > 500: bad.append(f"Solids ({solids} mg/L) > 500")
            if chlor > 4.0: bad.append(f"Chloramines ({chlor} mg/L) > 4.0")
            if turb > 5.0: bad.append(f"Turbidity ({turb} NTU) > 5.0")
            if bad: st.warning("**🚨 Failing Safe Limits:**\n- " + "\n- ".join(bad))
            else: st.info("**✅ All major parameters are within WHO/BIS limits!**")
            img_cm = find_image("confusion_matrix")
            if img_cm:
                with st.expander("📈 View Model Confusion Matrix (66.9% Accuracy)"):
                    st.image(img_cm, use_container_width=True)

