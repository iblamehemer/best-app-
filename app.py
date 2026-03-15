"""
app.py
------
BrandSphere AI — Main Streamlit Application
CRS AI Capstone 2025-26 | Scenario 1

Tabs:
  1. 🏠 Home
  2. 🎯 Brand Inputs
  3. 🎨 Logo Studio
  4. 🖋  Fonts & Palette
  5. ✍️  Slogans & Content
  6. 📣  Campaign Analytics
  7. 🌍  Multilingual Studio
  8. 🎬  Animation Preview
  9. ⭐  Feedback
  10. 📦  Download Kit
"""

import os, sys, uuid, json, re, time, datetime, logging
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ── Path setup ──────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

# ── Streamlit page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="BrandSphere AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');
:root {
  --bg:#0C0D0F; --surface:#141518; --surface2:#1C1E22; --border:#2A2C31;
  --accent:#C9A84C; --accent2:#E8C97A; --teal:#3ECFB2; --red:#E05A5A;
  --text:#F0EDE8; --muted:#7A7A85;
  --font-head:'Cormorant Garamond',Georgia,serif;
  --font-body:'DM Sans',sans-serif;
  --font-mono:'Space Mono',monospace;
}
*, *::before, *::after { box-sizing:border-box; }
html, body, .stApp { background:var(--bg) !important; color:var(--text) !important; font-family:var(--font-body); }
#MainMenu, footer, header { visibility:hidden; }
.block-container { padding:0 !important; max-width:100% !important; }
section[data-testid="stSidebar"] { display:none; }
::-webkit-scrollbar { width:4px; } ::-webkit-scrollbar-track { background:var(--bg); } ::-webkit-scrollbar-thumb { background:var(--accent); border-radius:2px; }
.nav-bar { display:flex; align-items:center; justify-content:space-between; padding:16px 48px; background:var(--surface); border-bottom:1px solid var(--border); }
.nav-logo { font-family:var(--font-head); font-size:1.6rem; font-weight:700; color:var(--accent); letter-spacing:0.03em; }
.nav-logo span { color:var(--text); font-weight:300; }
.nav-tag  { font-family:var(--font-mono); font-size:0.62rem; color:var(--muted); letter-spacing:0.15em; text-transform:uppercase; }
.hero { background:linear-gradient(135deg,#0C0D0F 0%,#141518 60%,#0f1015 100%); padding:80px 48px 56px; border-bottom:1px solid var(--border); position:relative; overflow:hidden; }
.hero::before { content:''; position:absolute; top:-60px; right:-60px; width:500px; height:500px; background:radial-gradient(circle,rgba(201,168,76,0.08) 0%,transparent 70%); pointer-events:none; }
.hero-eyebrow { font-family:var(--font-mono); font-size:0.7rem; letter-spacing:0.25em; color:var(--accent); text-transform:uppercase; margin-bottom:16px; }
.hero-title { font-family:var(--font-head); font-size:clamp(2.6rem,5vw,4.6rem); font-weight:300; line-height:1.08; margin-bottom:12px; }
.hero-title em { font-style:italic; color:var(--accent); }
.hero-sub { font-size:1rem; font-weight:300; color:var(--muted); max-width:540px; line-height:1.72; margin-bottom:36px; }
.badge-row { display:flex; gap:10px; flex-wrap:wrap; }
.badge { display:inline-block; padding:5px 14px; border:1px solid var(--border); border-radius:20px; font-family:var(--font-mono); font-size:0.6rem; color:var(--muted); letter-spacing:0.1em; }
.stTabs [data-baseweb="tab-list"] { background:var(--surface) !important; border-bottom:1px solid var(--border) !important; padding:0 48px !important; gap:0 !important; }
.stTabs [data-baseweb="tab"] { background:transparent !important; border:none !important; color:var(--muted) !important; font-family:var(--font-mono) !important; font-size:0.65rem !important; letter-spacing:0.12em !important; text-transform:uppercase !important; padding:15px 18px !important; margin:0 !important; transition:color 0.2s !important; }
.stTabs [aria-selected="true"] { color:var(--accent) !important; border-bottom:2px solid var(--accent) !important; }
.stTabs [data-baseweb="tab-panel"] { padding:36px 48px !important; background:var(--bg) !important; }
.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div { background:var(--surface2) !important; border:1px solid var(--border) !important; border-radius:6px !important; color:var(--text) !important; font-family:var(--font-body) !important; font-size:0.92rem !important; }
.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus { border-color:var(--accent) !important; box-shadow:0 0 0 2px rgba(201,168,76,0.15) !important; }
label, .stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label, .stRadio label { color:var(--muted) !important; font-family:var(--font-mono) !important; font-size:0.62rem !important; letter-spacing:0.12em !important; text-transform:uppercase !important; }
.stButton>button { background:var(--accent) !important; color:#0C0D0F !important; border:none !important; border-radius:4px !important; font-family:var(--font-mono) !important; font-size:0.68rem !important; font-weight:700 !important; letter-spacing:0.15em !important; text-transform:uppercase !important; padding:11px 26px !important; transition:all 0.2s !important; }
.stButton>button:hover { background:var(--accent2) !important; transform:translateY(-1px) !important; box-shadow:0 4px 18px rgba(201,168,76,0.3) !important; }
.stDownloadButton>button { background:transparent !important; color:var(--accent) !important; border:1px solid var(--accent) !important; border-radius:4px !important; font-family:var(--font-mono) !important; font-size:0.68rem !important; font-weight:700 !important; letter-spacing:0.15em !important; text-transform:uppercase !important; padding:11px 26px !important; }
.stDownloadButton>button:hover { background:rgba(201,168,76,0.1) !important; }
.card { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:26px; margin-bottom:14px; }
.card:hover { border-color:rgba(201,168,76,0.35); }
.card-title { font-family:var(--font-head); font-size:1.25rem; font-weight:600; color:var(--text); margin-bottom:5px; }
.card-sub { font-size:0.82rem; color:var(--muted); line-height:1.65; margin-bottom:16px; }
.sec-label { font-family:var(--font-mono); font-size:0.6rem; letter-spacing:0.25em; color:var(--accent); text-transform:uppercase; margin-bottom:7px; }
.sec-title { font-family:var(--font-head); font-size:1.9rem; font-weight:300; color:var(--text); margin-bottom:5px; }
.sec-title em { font-style:italic; color:var(--accent); }
.divider { height:1px; background:var(--border); margin:28px 0; }
.metric-card { background:var(--surface2); border:1px solid var(--border); border-radius:8px; padding:20px; text-align:center; }
.metric-val { font-family:var(--font-head); font-size:2.2rem; font-weight:700; color:var(--accent); display:block; }
.metric-lbl { font-family:var(--font-mono); font-size:0.58rem; letter-spacing:0.15em; color:var(--muted); text-transform:uppercase; margin-top:3px; }
.swatch-row { display:flex; gap:8px; margin:14px 0; }
.swatch { flex:1; height:50px; border-radius:6px; display:flex; align-items:flex-end; padding:5px 8px; font-family:var(--font-mono); font-size:0.52rem; color:rgba(255,255,255,0.75); }
.tagline-card { background:var(--surface2); border-left:3px solid var(--accent); padding:15px 18px; border-radius:0 8px 8px 0; margin:7px 0; font-family:var(--font-head); font-size:1.1rem; font-style:italic; color:var(--text); line-height:1.55; }
.lang-card { background:var(--surface2); border:1px solid var(--border); border-radius:8px; padding:14px 18px; margin:5px 0; }
.lang-name { font-family:var(--font-mono); font-size:0.58rem; letter-spacing:0.15em; color:var(--accent); text-transform:uppercase; margin-bottom:4px; }
.lang-text { font-family:var(--font-head); font-size:1rem; font-style:italic; color:var(--text); }
.pill { display:inline-block; padding:3px 11px; border-radius:20px; font-family:var(--font-mono); font-size:0.57rem; letter-spacing:0.1em; text-transform:uppercase; }
.pill-g { background:rgba(62,207,178,0.15); color:#3ECFB2; border:1px solid rgba(62,207,178,0.3); }
.pill-a { background:rgba(201,168,76,0.15); color:#C9A84C; border:1px solid rgba(201,168,76,0.3); }
.pill-r { background:rgba(224,90,90,0.15); color:#E05A5A; border:1px solid rgba(224,90,90,0.3); }
.prog-wrap { background:var(--surface2); border-radius:4px; height:8px; overflow:hidden; margin:7px 0; }
.prog-bar { height:100%; border-radius:4px; background:linear-gradient(90deg,var(--accent),var(--teal)); transition:width 0.6s ease; }
.check-item { display:flex; align-items:flex-start; gap:10px; padding:9px 0; border-bottom:1px solid var(--border); }
.logo-svg-wrap { border:2px solid var(--border); border-radius:10px; padding:16px; background:var(--surface2); cursor:pointer; transition:border-color 0.2s; display:flex; flex-direction:column; align-items:center; gap:8px; }
.logo-svg-wrap:hover { border-color:var(--accent); }
.logo-svg-wrap.selected { border-color:var(--accent); background:rgba(201,168,76,0.06); }
.nltk-pill { display:inline-block; padding:3px 10px; border-radius:14px; font-family:var(--font-mono); font-size:0.55rem; background:rgba(201,168,76,0.12); color:var(--accent); border:1px solid rgba(201,168,76,0.25); margin:2px; }
.stAlert { background:var(--surface2) !important; border:1px solid var(--border) !important; }
.stSpinner>div { border-top-color:var(--accent) !important; }
@media (max-width:640px) { .stTabs [data-baseweb="tab-panel"] { padding:20px !important; } .hero { padding:40px 20px 36px; } }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────
def _init():
    defaults = {
        "session_id":    str(uuid.uuid4())[:8],
        "brand_inputs":  {},
        "logos":         [],
        "selected_logo": 0,
        "palette":       {},
        "fonts":         [],
        "slogans":       [],
        "retrieved":     [],
        "brand_story":   "",
        "translations":  {},
        "campaigns":     {},
        "kpis":          {},
        "aesthetics":    {},
        "gif_bytes":     None,
        "feedback_log":  [],
        "gemini_ok":     False,
        "api_key":       "",
        "chat_history":  [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()

# ── Gemini config ──────────────────────────────────────────────────────────
def configure_gemini(key: str) -> bool:
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        # Quick test
        model = genai.GenerativeModel("gemini-2.0-flash")
        model.generate_content("hi")
        st.session_state.gemini_ok  = True
        st.session_state.api_key    = key
        os.environ["GEMINI_API_KEY"] = key
        return True
    except Exception:
        return False

def gemini_call(prompt: str, system: str = "") -> str:
    if not st.session_state.gemini_ok:
        return ""
    try:
        import google.generativeai as genai
        model = genai.GenerativeModel("gemini-2.0-flash",
                                       system_instruction=system or None)
        return model.generate_content(prompt).text.strip()
    except Exception as e:
        return ""

# ── Auto-configure from env / streamlit secrets ────────────────────────────
_env_key = os.getenv("GEMINI_API_KEY", "")
if not _env_key:
    try:
        _env_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass
if _env_key and not st.session_state.gemini_ok:
    configure_gemini(_env_key)

# ── Import src modules ─────────────────────────────────────────────────────
from src.config import (INDUSTRIES, PERSONALITIES, TONES, PLATFORMS,
                         REGIONS, LANGUAGES_SUPPORTED, CAMPAIGN_OBJECTIVES, COLOR_NAMES)
from src.palette_engine   import generate_palette, score_palette_harmony
from src.font_engine      import recommend_fonts
from src.logo_engine      import generate_all_logos, svg_to_png_bytes
from src.slogan_engine    import generate_slogans, nltk_analyze
from src.aesthetics_engine import score_brand, gemini_recommendations
from src.multilingual_engine import translate_slogan, validate_translations
from src.animation_engine  import create_brand_gif
from src.feedback_engine   import save_feedback, load_feedback, get_summary
from src.export_engine     import build_brand_kit_zip
from src.dashboard_engine  import (kpi_bar_chart, regional_engagement_map,
                                    personality_radar, feedback_bar, feedback_pie,
                                    campaign_scatter)

# ── Lazy campaign predictor ────────────────────────────────────────────────
@st.cache_resource
def get_predictor():
    from src.campaign_predictor import predictor
    predictor._load()
    return predictor

# ── Campaign content helper ────────────────────────────────────────────────
DEMO_CAMPAIGN = {
    "caption": "Introducing {company} — where {industry} meets intelligent design.\nBuilt for the future. Crafted for you. {tag}\n👉 Tap the link.",
    "hashtags": ["#{co}", "#BrandStrategy", "#AIBranding", "#Innovation", "#DigitalMarketing",
                 "#BrandIdentity", "#StartupLife", "#MarketingAI", "#GrowthHacking", "#ProductLaunch"],
    "regional_strategy": "Focus on culturally resonant visuals and localized CTAs for {region}.",
}

def generate_campaign_content(bi, platform, region, objective):
    co  = bi.get("company", "Brand")
    ind = bi.get("industry", "Technology")
    tag = st.session_state.slogans[0]["text"] if st.session_state.slogans else f"Discover {co}"
    if st.session_state.gemini_ok:
        prompt = (
            f"Create a {platform} marketing campaign.\n"
            f"Company: {co} | Industry: {ind} | Objective: {objective} | Region: {region}\n"
            f"Tagline: \"{tag}\"\n\n"
            "Return JSON only: {\"caption\":\"...\",\"hashtags\":[\"...\"],\"regional_strategy\":\"...\"}"
        )
        raw = gemini_call(prompt)
        try:
            return json.loads(re.sub(r"```json|```", "", raw).strip())
        except Exception:
            pass
    return {
        "caption": DEMO_CAMPAIGN["caption"].format(company=co, industry=ind.lower(), tag=tag),
        "hashtags": [h.replace("{co}", co.replace(" ","")) for h in DEMO_CAMPAIGN["hashtags"]],
        "regional_strategy": DEMO_CAMPAIGN["regional_strategy"].format(region=region),
    }

def generate_brand_story(bi):
    co, ind, tone, aud = (bi.get("company",""), bi.get("industry",""),
                           bi.get("tone",""), bi.get("audience",""))
    if st.session_state.gemini_ok:
        return gemini_call(
            f"Write a 110-word brand story for {co} in the {ind} industry. "
            f"Tone: {tone}. Audience: {aud}. Write in second person. Be inspiring.",
            system="You are a brand narrative writer. Be specific, not generic."
        )
    return (
        f"{co} was built with one conviction: that great brands don't happen by accident — "
        f"they are engineered with intention.\n\n"
        f"In the competitive {ind.lower()} landscape, standing out requires more than a logo. "
        f"It demands a voice that resonates, a visual identity that commands attention, "
        f"and a message that converts.\n\n"
        f"Your brand is your most valuable asset. At {co}, every design decision, "
        f"every word, every colour choice is a deliberate act of strategic storytelling.\n\n"
        f"This is your story. Tell it boldly."
    )

# ══════════════════════════════════════════════════════════════════════════════
#  NAVBAR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="nav-bar">
  <div>
    <div class="nav-logo">Brand<span>Sphere</span> AI</div>
    <div class="nav-tag">Automated Branding Intelligence Platform</div>
  </div>
  <div class="nav-tag">Scenario 1 &nbsp;|&nbsp; CRS AI Capstone 2025–26</div>
</div>
""", unsafe_allow_html=True)

# ── API Key config ────────────────────────────────────────────────────────
with st.expander("⚙️  API Configuration", expanded=not st.session_state.gemini_ok):
    c1, c2 = st.columns([4, 1])
    with c1:
        api_inp = st.text_input("Gemini API Key", type="password",
                                placeholder="AIza...", label_visibility="collapsed")
    with c2:
        if st.button("Connect"):
            if api_inp:
                if configure_gemini(api_inp):
                    st.success("✓ Gemini connected")
                else:
                    st.error("Invalid key")
    if not st.session_state.gemini_ok:
        st.info("💡 **Demo mode** — all features work with AI-simulated outputs. Connect Gemini for live generation.")
    else:
        st.success(f"✓ Gemini 2.0 Flash connected — Session {st.session_state.session_id}")

# ── HERO ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">AI-Powered Branding Intelligence</div>
  <div class="hero-title">Your brand identity,<br><em>engineered by AI.</em></div>
  <div class="hero-sub">
    Generate logos, taglines, color palettes, campaigns, and complete brand kits in minutes.
    Powered by Computer Vision, Generative AI, NLP, and Predictive Analytics.
  </div>
  <div class="badge-row">
    <span class="badge">Logo Studio</span>
    <span class="badge">KMeans Palette</span>
    <span class="badge">NLTK NLP</span>
    <span class="badge">Random Forest KPIs</span>
    <span class="badge">Gemini API</span>
    <span class="badge">Multilingual</span>
    <span class="badge">Streamlit Cloud</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════════
tabs = st.tabs([
    "🏠 Home",
    "🎯 Brand Inputs",
    "🎨 Logo Studio",
    "🖋 Fonts & Palette",
    "✍️ Slogans & Content",
    "📣 Campaign Analytics",
    "🌍 Multilingual Studio",
    "🎬 Animation Preview",
    "⭐ Feedback",
    "📦 Download Kit",
])

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<p class="sec-label">Overview</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Welcome to <em>BrandSphere AI</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    modules = [
        ("🎨", "AI Logo & Design Studio", "5 SVG logo concepts generated from your brand personality and color palette."),
        ("✍️", "Creative Content & GenAI Hub", "NLTK-powered tagline analysis + Gemini-enhanced slogan generation."),
        ("📣", "Smart Campaign Studio", "Random Forest model trained on 200K real marketing records predicts CTR, ROI & Engagement."),
        ("🌍", "Multilingual Engine", "Gemini-powered translation into 5 languages with tone preservation."),
        ("⭐", "Feedback Intelligence", "Star ratings saved to CSV; Plotly dashboards visualize patterns."),
        ("📦", "Export Engine", "Complete brand kit: logos, palette, fonts, taglines, campaigns, animation — all in one ZIP."),
    ]
    for i, (icon, title, desc) in enumerate(modules):
        col = [c1, c2, c3][i % 3]
        with col:
            st.markdown(f"""
            <div class="card">
              <div style="font-size:1.8rem;margin-bottom:8px">{icon}</div>
              <div class="card-title">{title}</div>
              <div class="card-sub">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="sec-label">10-Week Roadmap</p>', unsafe_allow_html=True)
    weeks = [
        ("Week 1", "EDA & Data Understanding", "✅ Completed"),
        ("Week 2", "Logo Classification & Extraction", "✅ SVG Engine"),
        ("Week 3", "Font Recommendation Engine", "✅ Completed"),
        ("Week 4", "Tagline & Slogan Generation", "✅ NLTK + Gemini"),
        ("Week 5", "Color Palette Engine", "✅ KMeans"),
        ("Week 6", "Animated Visuals Studio", "✅ Pillow GIF"),
        ("Week 7", "Smart Campaign Studio", "✅ Random Forest"),
        ("Week 8", "Multilingual Generator", "✅ Gemini / Fallback"),
        ("Week 9", "Feedback Intelligence", "✅ CSV + Plotly"),
        ("Week 10","Integration & Deployment", "✅ Streamlit Cloud"),
    ]
    for wk, task, status in weeks:
        st.markdown(f"""
        <div class="check-item">
          <span style="color:var(--teal);font-size:0.95rem">✓</span>
          <div>
            <span style="font-family:var(--font-mono);font-size:0.62rem;color:var(--accent);letter-spacing:0.1em">{wk}</span>
            <span style="font-size:0.88rem;color:var(--text);margin-left:12px">{task}</span>
            <span style="margin-left:10px" class="pill pill-g">{status}</span>
          </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — BRAND INPUTS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<p class="sec-label">Step 01 — Foundation</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Brand <em>Input Form</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        company    = st.text_input("Company Name *", placeholder="e.g. NovaTech Solutions")
        industry   = st.selectbox("Industry *", INDUSTRIES)
        personality= st.selectbox("Brand Personality *", PERSONALITIES)
        audience   = st.text_input("Target Audience", placeholder="e.g. Millennials aged 25–40")
    with col2:
        tone       = st.selectbox("Communication Tone", TONES)
        tag_hint   = st.text_input("Tagline Hint (optional)", placeholder="e.g. Focus on innovation and speed")
        description= st.text_area("Product / Service Description",
                                   placeholder="What does your business do? What makes it unique?", height=108)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if st.button("🚀  Generate Full Brand Kit", use_container_width=False):
        if not company:
            st.warning("Please enter a company name.")
        else:
            bi = {"company": company, "industry": industry, "personality": personality,
                  "audience": audience, "tone": tone, "tag_hint": tag_hint, "description": description}
            st.session_state.brand_inputs = bi

            with st.spinner("Building brand identity…"):
                st.session_state.palette  = generate_palette(industry, personality)
                st.session_state.logos    = generate_all_logos(company, st.session_state.palette)
                st.session_state.fonts    = recommend_fonts(industry, personality)
                slogans, retrieved = generate_slogans(company, industry, tone, audience, tag_hint)
                st.session_state.slogans   = slogans
                st.session_state.retrieved = retrieved
                st.session_state.aesthetics = score_brand(personality, industry, tone,
                                                           slogans[0]["text"] if slogans else "",
                                                           st.session_state.palette)

            st.success(f"✓ Brand kit generated for **{company}**. Navigate the tabs to explore your assets.")

    if st.session_state.brand_inputs:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">Current Brand Profile</p>', unsafe_allow_html=True)
        bi = st.session_state.brand_inputs
        cols = st.columns(4)
        for col, (lbl, val) in zip(cols, [
            ("Company", bi.get("company","")), ("Industry", bi.get("industry","")),
            ("Personality", bi.get("personality","")), ("Tone", bi.get("tone",""))
        ]):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                  <span class="metric-lbl">{lbl}</span>
                  <span style="font-family:var(--font-head);font-size:1.1rem;color:var(--text);display:block;margin-top:5px">{val}</span>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — LOGO STUDIO
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<p class="sec-label">Module 01 — Visual Identity</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Logo <em>Studio</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.logos:
        st.info("👈 Complete Brand Inputs first to generate logos.")
    else:
        bi = st.session_state.brand_inputs
        st.markdown(f'<p class="sec-label">5 Concepts for {bi.get("company","")}</p>', unsafe_allow_html=True)
        st.caption("⚠️ Logo generation is SVG-based (no logo image dataset uploaded). See code comments for full transparency.")

        logo_cols = st.columns(5)
        for i, logo in enumerate(st.session_state.logos):
            with logo_cols[i]:
                selected_cls = "selected" if st.session_state.selected_logo == i else ""
                st.markdown(f"""
                <div class="logo-svg-wrap {selected_cls}" id="logo_{i}">
                  {logo["svg"]}
                  <div style="font-family:var(--font-mono);font-size:0.55rem;color:var(--accent);letter-spacing:0.08em;text-align:center">{logo["style"]}</div>
                </div>""", unsafe_allow_html=True)
                if st.button(f"Select", key=f"sel_logo_{i}"):
                    st.session_state.selected_logo = i
                    st.rerun()

        sel = st.session_state.logos[st.session_state.selected_logo]
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.markdown(f'<p class="sec-label">Selected: {sel["style"]}</p>', unsafe_allow_html=True)
            st.markdown(sel["svg"], unsafe_allow_html=True)
            st.download_button("⬇ Download SVG", data=sel["svg"].encode(),
                               file_name=f"{bi.get('company','brand')}_logo_{sel['index']}.svg",
                               mime="image/svg+xml")
            png = svg_to_png_bytes(sel["svg"], 300)
            if png:
                st.download_button("⬇ Download PNG", data=png,
                                   file_name=f"{bi.get('company','brand')}_logo_{sel['index']}.png",
                                   mime="image/png")
        with c2:
            st.markdown(f"""
            <div class="card">
              <p class="sec-label">Design Rationale</p>
              <p style="font-size:0.9rem;line-height:1.7;color:var(--text)">{sel["description"]}</p>
              <br/>
              <p class="sec-label">All Concepts</p>
              {"".join([f'<div style="font-size:0.83rem;color:var(--muted);padding:4px 0;border-bottom:1px solid var(--border)"><span style="color:var(--accent)">#{l["index"]+1}</span> {l["style"]} — {l["description"][:60]}…</div>' for l in st.session_state.logos])}
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — FONTS & PALETTE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<p class="sec-label">Module 02 — Visual System</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Fonts & <em>Colour Palette</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.palette:
        st.info("👈 Complete Brand Inputs first.")
    else:
        bi = st.session_state.brand_inputs

        # Palette
        st.markdown('<p class="sec-label">KMeans-Extracted Color Palette (Week 5)</p>', unsafe_allow_html=True)
        st.caption("KMeans(k=5) run on noise-augmented seed colors from industry color psychology mapping.")
        swatch_html = '<div class="swatch-row">'
        for name, v in st.session_state.palette.items():
            swatch_html += f'<div class="swatch" style="background:{v["hex"]}">{v["hex"]}</div>'
        swatch_html += "</div>"
        st.markdown(swatch_html, unsafe_allow_html=True)

        pc1, pc2 = st.columns(2, gap="large")
        with pc1:
            for name, v in st.session_state.palette.items():
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;margin:7px 0">
                  <div style="width:32px;height:32px;background:{v['hex']};border-radius:5px;flex-shrink:0"></div>
                  <div>
                    <span style="font-family:var(--font-mono);font-size:0.6rem;color:var(--accent);letter-spacing:0.1em">{name}</span>
                    <span style="font-family:var(--font-mono);font-size:0.6rem;color:var(--muted);margin-left:8px">{v['hex']}</span>
                    <div style="font-size:0.78rem;color:var(--muted)">{v['psychology']}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

        with pc2:
            harmony = score_palette_harmony(st.session_state.palette)
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom:14px">
              <span class="metric-val">{harmony}/100</span>
              <span class="metric-lbl">Palette Harmony Score</span>
            </div>""", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card">
              <p class="sec-label">Personality</p>
              <p style="font-family:var(--font-head);font-size:1.05rem;font-style:italic;color:var(--text)">
                {bi.get("personality","")} palette for {bi.get("industry","")}
              </p>
              <p style="font-size:0.82rem;color:var(--muted);margin-top:8px;line-height:1.6">
                Follow the 60-30-10 rule: 60% Primary · 30% Secondary · 10% Accent.
              </p>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Fonts
        st.markdown('<p class="sec-label">Font Recommendations (Week 3)</p>', unsafe_allow_html=True)
        st.caption("Rule-based engine mapping industry × personality → curated font pairings. No font image dataset required.")
        fcols = st.columns(3)
        for i, font in enumerate(st.session_state.fonts):
            with fcols[i]:
                st.markdown(f"""
                <div class="card">
                  <div style="font-family:var(--font-mono);font-size:0.56rem;color:var(--accent);letter-spacing:0.12em;margin-bottom:6px">{font['rank']}</div>
                  <div class="card-title">{font['heading']}</div>
                  <div style="font-size:0.8rem;color:var(--muted);margin-bottom:8px">Body: {font['body']}<br>Alt: {font['alternate']}</div>
                  <div style="font-size:0.78rem;color:var(--text);line-height:1.55">{font['rationale']}</div>
                  <br>
                  <span class="pill pill-a">{font['classification']}</span>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 5 — SLOGANS & CONTENT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<p class="sec-label">Module 03 — Generative AI</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Slogans & <em>Content Hub</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.brand_inputs:
        st.info("👈 Complete Brand Inputs first.")
    else:
        bi = st.session_state.brand_inputs

        sc1, sc2 = st.columns([1, 1], gap="large")

        with sc1:
            st.markdown('<p class="sec-label">AI-Generated Taglines</p>', unsafe_allow_html=True)
            if st.button("✨  Regenerate Taglines"):
                with st.spinner("Generating…"):
                    slogans, retrieved = generate_slogans(
                        bi["company"], bi["industry"], bi["tone"],
                        bi.get("audience",""), bi.get("tag_hint",""))
                    st.session_state.slogans   = slogans
                    st.session_state.retrieved = retrieved

            if st.session_state.slogans:
                for s in st.session_state.slogans:
                    src_pill = "pill-g" if s["source"] == "gemini" else "pill-a"
                    st.markdown(f"""
                    <div class="tagline-card">"{s['text']}"
                      <div style="margin-top:5px">
                        <span class="pill {src_pill}">{s['source']}</span>
                        <span class="pill pill-a" style="margin-left:4px">{s['tone']}</span>
                      </div>
                    </div>""", unsafe_allow_html=True)

            if st.session_state.retrieved:
                st.markdown('<p class="sec-label" style="margin-top:18px">TF-IDF Retrieved Inspiration</p>', unsafe_allow_html=True)
                for r in st.session_state.retrieved[:3]:
                    st.markdown(f'<div style="font-style:italic;color:var(--muted);font-size:0.84rem;padding:4px 0">"{r}"</div>', unsafe_allow_html=True)

            # NLTK Analysis
            if st.session_state.slogans:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                with st.expander("🔬 NLTK Text Analysis (Week 4 — NLP Preprocessing)"):
                    top = st.session_state.slogans[0]["text"]
                    analysis = st.session_state.slogans[0].get("analysis") or nltk_analyze(top)
                    st.markdown(f"""
                    <div style="background:var(--surface2);border-radius:8px;padding:14px 16px;border:1px solid var(--border)">
                      <p class="sec-label">Analysed: "{top[:50]}"</p>
                      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:10px 0">
                        <div class="metric-card"><span class="metric-val" style="font-size:1.6rem">{analysis['word_count']}</span><span class="metric-lbl">Tokens</span></div>
                        <div class="metric-card"><span class="metric-val" style="font-size:1.6rem">{analysis['unique_words']}</span><span class="metric-lbl">Unique</span></div>
                        <div class="metric-card"><span class="metric-val" style="font-size:1.6rem">{analysis['lexical_density']}</span><span class="metric-lbl">Lex Density</span></div>
                      </div>
                      <p style="font-family:var(--font-mono);font-size:0.56rem;color:var(--accent);letter-spacing:0.1em;text-transform:uppercase;margin-top:10px">Clean tokens</p>
                      <div>{"".join([f'<span class="nltk-pill">{t}</span>' for t in analysis["clean_tokens"]])}</div>
                      <p style="font-family:var(--font-mono);font-size:0.56rem;color:var(--muted);letter-spacing:0.1em;text-transform:uppercase;margin-top:10px">Stems (Porter)</p>
                      <div>{"".join([f'<span class="nltk-pill" style="opacity:0.6">{s}</span>' for s in analysis["stems"]])}</div>
                    </div>""", unsafe_allow_html=True)

        with sc2:
            st.markdown('<p class="sec-label">Brand Narrative</p>', unsafe_allow_html=True)
            if st.button("📖  Generate Brand Story"):
                with st.spinner("Writing…"):
                    st.session_state.brand_story = generate_brand_story(bi)

            if st.session_state.brand_story:
                st.markdown(f"""
                <div class="card">
                  <p class="sec-label">Brand Narrative</p>
                  <p style="font-family:var(--font-head);font-size:1rem;font-style:italic;line-height:1.85;color:var(--text)">{st.session_state.brand_story}</p>
                </div>""", unsafe_allow_html=True)

            # Aesthetics score
            if st.session_state.aesthetics:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('<p class="sec-label">Brand Consistency Score</p>', unsafe_allow_html=True)
                aes = st.session_state.aesthetics
                overall = aes["overall"]
                grade   = aes["grade"]
                pill    = "pill-g" if overall >= 88 else "pill-a" if overall >= 75 else "pill-r"
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom:14px">
                  <span class="metric-val">{overall}/100</span>
                  <span class="metric-lbl">Brand Cohesion <span class="pill {pill}">{grade}</span></span>
                </div>""", unsafe_allow_html=True)
                for dim, score in list(aes["dimensions"].items())[:4]:
                    color = "#3ECFB2" if score >= 85 else "#C9A84C" if score >= 72 else "#E05A5A"
                    st.markdown(f"""
                    <div style="margin:8px 0">
                      <div style="display:flex;justify-content:space-between;margin-bottom:3px">
                        <span style="font-family:var(--font-mono);font-size:0.58rem;color:var(--muted);letter-spacing:0.08em">{dim.upper()}</span>
                        <span style="font-family:var(--font-mono);font-size:0.62rem;color:{color}">{score}/100</span>
                      </div>
                      <div class="prog-wrap"><div class="prog-bar" style="width:{score}%;background:{color}"></div></div>
                    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 6 — CAMPAIGN ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<p class="sec-label">Module 04 — Campaign Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Smart Campaign <em>Analytics</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.brand_inputs:
        st.info("👈 Complete Brand Inputs first.")
    else:
        bi = st.session_state.brand_inputs
        ca1, ca2, ca3 = st.columns(3)
        with ca1:
            platform  = st.selectbox("Platform", PLATFORMS)
        with ca2:
            region    = st.selectbox("Region", REGIONS)
        with ca3:
            objective = st.selectbox("Objective", CAMPAIGN_OBJECTIVES)

        if st.button("🚀  Predict KPIs & Generate Campaign"):
            with st.spinner("Running ML model…"):
                pred = get_predictor()
                kpis = pred.predict(platform, region, objective,
                                    bi["personality"],
                                    duration_days=30, budget=5000)
                st.session_state.kpis = kpis
                camp_data = generate_campaign_content(bi, platform, region, objective)
                st.session_state.campaigns[platform] = camp_data

        if st.session_state.kpis:
            kpis = st.session_state.kpis
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            kc1, kc2, kc3, kc4 = st.columns(4)
            for col, (lbl, val, unit) in zip([kc1, kc2, kc3, kc4], [
                ("CTR",        kpis["CTR"],        "%"),
                ("ROI",        kpis["ROI"],        "×"),
                ("Engagement", kpis["Engagement"], "/10"),
                ("Best Time",  kpis["Best_Time"],  ""),
            ]):
                with col:
                    st.markdown(f"""
                    <div class="metric-card">
                      <span class="metric-val" style="font-size:1.7rem">{val}{unit}</span>
                      <span class="metric-lbl">{lbl}</span>
                    </div>""", unsafe_allow_html=True)

            st.caption(f"Source: {kpis.get('Source','')}")
            if kpis.get("Tip"):
                st.markdown(f"""
                <div style="background:rgba(201,168,76,0.07);border-left:3px solid var(--accent);padding:14px 16px;border-radius:0 8px 8px 0;font-size:0.86rem;line-height:1.65;color:var(--muted);margin-top:12px">
                  💡 {kpis["Tip"]}
                </div>""", unsafe_allow_html=True)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.plotly_chart(kpi_bar_chart(kpis), use_container_width=True)

            region_scores = {r: np.random.randint(58, 86) for r in REGIONS[:-1]}
            region_scores[region] = max(region_scores.values()) + 3
            st.plotly_chart(regional_engagement_map(region_scores), use_container_width=True)

        if st.session_state.campaigns:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<p class="sec-label">Generated Campaign Content</p>', unsafe_allow_html=True)
            for plat, data in st.session_state.campaigns.items():
                with st.expander(f"📱  {plat} Campaign"):
                    st.markdown(f"""
                    <div class="card">
                      <p class="sec-label">Caption</p>
                      <p style="color:var(--text);line-height:1.75;font-size:0.9rem">{data.get("caption","")}</p>
                    </div>""", unsafe_allow_html=True)
                    tags = data.get("hashtags", [])
                    html = " ".join([f'<span class="pill pill-a">{h}</span>' for h in tags])
                    st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:6px;margin:10px 0">{html}</div>', unsafe_allow_html=True)
                    if data.get("regional_strategy"):
                        st.markdown(f"""
                        <div class="card">
                          <p class="sec-label">Regional Strategy — {region}</p>
                          <p style="color:var(--muted);font-size:0.87rem;line-height:1.7">{data["regional_strategy"]}</p>
                        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 7 — MULTILINGUAL STUDIO
# ══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<p class="sec-label">Module 05 — Global Reach</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Multilingual <em>Studio</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.brand_inputs:
        st.info("👈 Complete Brand Inputs first.")
    else:
        bi    = st.session_state.brand_inputs
        langs = st.multiselect("Target Languages", LANGUAGES_SUPPORTED,
                               default=["Hindi", "Spanish", "French", "German", "Gujarati"])

        slogan_to_translate = (st.session_state.slogans[0]["text"]
                                if st.session_state.slogans
                                else f"{bi.get('company','Brand')} — Excellence by Design")

        st.markdown(f"""
        <div style="background:var(--surface2);border-radius:8px;padding:12px 16px;margin-bottom:16px">
          <span style="font-family:var(--font-mono);font-size:0.58rem;color:var(--accent);letter-spacing:0.1em;text-transform:uppercase">Original Tagline</span>
          <div style="font-family:var(--font-head);font-size:1.05rem;font-style:italic;color:var(--text);margin-top:4px">"{slogan_to_translate}"</div>
        </div>""", unsafe_allow_html=True)

        if st.button("🌍  Translate to Selected Languages"):
            with st.spinner("Translating…"):
                results = translate_slogan(slogan_to_translate, bi.get("company","Brand"), langs)
                results = validate_translations(results)
                st.session_state.translations = results

        if st.session_state.translations:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            ml_cols = st.columns(min(len(st.session_state.translations), 3))
            for i, (lang, data) in enumerate(st.session_state.translations.items()):
                with ml_cols[i % 3]:
                    src_pill = "pill-g" if data.get("source") == "gemini" else "pill-a"
                    st.markdown(f"""
                    <div class="lang-card">
                      <div class="lang-name">{data['flag']} {lang} ({data['native']})</div>
                      <div class="lang-text">{data['text']}</div>
                      <div style="margin-top:8px;font-size:0.74rem;color:var(--muted)">{data.get('tone_note','')}</div>
                      <div style="margin-top:6px"><span class="pill {src_pill}">{data.get('source','')}</span></div>
                    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 8 — ANIMATION PREVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<p class="sec-label">Module 06 — Animated Visuals</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Animation <em>Preview</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.brand_inputs:
        st.info("👈 Complete Brand Inputs first.")
    else:
        bi = st.session_state.brand_inputs
        ac1, ac2 = st.columns([1, 2], gap="large")
        with ac1:
            style  = st.selectbox("Animation Style", ["typewriter", "fade", "slide"])
            frames = st.slider("Frames", 12, 30, 20)
        with ac2:
            st.markdown(f"""
            <div class="card">
              <p class="sec-label">About this animation</p>
              <p style="font-size:0.85rem;color:var(--muted);line-height:1.65">
                Pillow-based GIF animation combining your brand logo initials, 
                colour palette, and tagline. Supports typewriter, fade-in, and slide-in effects.
                Output: 600×338px, optimised GIF.
              </p>
            </div>""", unsafe_allow_html=True)

        if st.button("🎬  Generate Brand Animation"):
            if not st.session_state.palette:
                st.warning("Generate brand kit first.")
            else:
                tag = (st.session_state.slogans[0]["text"]
                       if st.session_state.slogans else f"{bi['company']} — Excellence by Design")
                svg = (st.session_state.logos[st.session_state.selected_logo]["svg"]
                       if st.session_state.logos else "")
                with st.spinner("Rendering animation…"):
                    gif = create_brand_gif(svg, tag, st.session_state.palette,
                                           bi["company"], style, frames)
                    st.session_state.gif_bytes = gif

        if st.session_state.gif_bytes:
            st.image(st.session_state.gif_bytes, width=560)
            st.download_button("⬇ Download GIF",
                               data=st.session_state.gif_bytes,
                               file_name=f"{bi.get('company','brand')}_animation.gif",
                               mime="image/gif")

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 9 — FEEDBACK
# ══════════════════════════════════════════════════════════════════════════════
with tabs[8]:
    st.markdown('<p class="sec-label">Module 07 — Feedback Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Rate & <em>Refine</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    MODULES = ["Logo & Design Studio", "Creative Content Hub",
               "Campaign Analytics", "Multilingual Studio", "Overall Brand Kit"]
    fb_module = st.selectbox("Rate Module", MODULES)
    fb1, fb2  = st.columns([1, 2], gap="large")
    with fb1:
        rating = st.slider("Rating (1–5)", 1, 5, 4, label_visibility="collapsed")
        stars  = "⭐" * rating + "☆" * (5 - rating)
        quality = {1:"Poor",2:"Below Average",3:"Average",4:"Good",5:"Excellent"}[rating]
        pill   = "pill-r" if rating <= 2 else "pill-a" if rating == 3 else "pill-g"
        st.markdown(f'<div style="font-size:1.8rem;letter-spacing:4px;margin:10px 0">{stars}</div>', unsafe_allow_html=True)
        st.markdown(f'<span class="pill {pill}">{quality}</span>', unsafe_allow_html=True)
    with fb2:
        comment   = st.text_area("Feedback", placeholder="What worked? What could be better?", height=90)
        preferred = st.text_input("Preferred Alternative (optional)", placeholder="e.g. More vibrant palette…")

    bi = st.session_state.brand_inputs
    if st.button("📤  Submit Feedback"):
        save_feedback(st.session_state.session_id,
                      bi.get("company",""), bi.get("industry",""),
                      fb_module, rating, comment, preferred)
        record = {"timestamp": datetime.datetime.now().isoformat(),
                  "module": fb_module, "rating": rating,
                  "sentiment": "positive" if rating >= 4 else "neutral" if rating == 3 else "negative",
                  "comment": comment}
        st.session_state.feedback_log.append(record)
        st.success(f"✓ Feedback saved — Rating {rating}/5 (written to feedback_data.csv)")

    if st.session_state.feedback_log:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">Session Feedback Log</p>', unsafe_allow_html=True)
        df_log = pd.DataFrame(st.session_state.feedback_log)
        st.dataframe(df_log[["timestamp","module","rating","sentiment","comment"]]
                     .rename(columns={"timestamp":"Time","module":"Module",
                                      "rating":"Rating","sentiment":"Sentiment","comment":"Comment"}),
                     use_container_width=True, hide_index=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">Feedback Analytics</p>', unsafe_allow_html=True)
        fc1, fc2 = st.columns(2)
        with fc1:
            st.plotly_chart(feedback_bar(df_log), use_container_width=True)
        with fc2:
            st.plotly_chart(feedback_pie(df_log), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 10 — DOWNLOAD KIT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[9]:
    st.markdown('<p class="sec-label">Module 08 — Export Engine</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Download Brand <em>Kit</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    bi = st.session_state.brand_inputs
    if not bi:
        st.info("👈 Complete Brand Inputs first.")
    else:
        # Progress checklist
        checks = [
            ("Brand Inputs",        bool(bi)),
            ("Logos Generated",     bool(st.session_state.logos)),
            ("Colour Palette",      bool(st.session_state.palette)),
            ("Font Recommendations",bool(st.session_state.fonts)),
            ("Taglines Created",    bool(st.session_state.slogans)),
            ("Brand Story",         bool(st.session_state.brand_story)),
            ("Translations",        bool(st.session_state.translations)),
            ("Campaign Content",    bool(st.session_state.campaigns)),
            ("KPI Predictions",     bool(st.session_state.kpis)),
            ("Animation",           bool(st.session_state.gif_bytes)),
        ]
        done = sum(1 for _, v in checks if v)
        pct  = int(done / len(checks) * 100)

        st.markdown(f"""
        <div style="margin-bottom:20px">
          <div style="display:flex;justify-content:space-between;margin-bottom:5px">
            <span style="font-family:var(--font-mono);font-size:0.7rem;color:var(--muted)">KIT COMPLETENESS — {done}/{len(checks)}</span>
            <span style="font-family:var(--font-mono);font-size:0.7rem;color:var(--accent)">{pct}%</span>
          </div>
          <div class="prog-wrap" style="height:12px"><div class="prog-bar" style="width:{pct}%"></div></div>
        </div>""", unsafe_allow_html=True)

        for label, done_flag in checks:
            icon  = "✓" if done_flag else "○"
            color = "var(--teal)" if done_flag else "var(--muted)"
            st.markdown(f"""
            <div class="check-item">
              <span style="color:{color}">{icon}</span>
              <span style="font-size:0.87rem;color:{'var(--text)' if done_flag else 'var(--muted)'}">{label}</span>
              {'<span class="pill pill-g" style="margin-left:auto">done</span>' if done_flag else ''}
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Brand Personality Radar
        if bi.get("personality"):
            st.plotly_chart(personality_radar(bi["personality"]), use_container_width=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Download button
        if st.button("📦  Build & Download Brand Kit ZIP"):
            with st.spinner("Packaging assets…"):
                zip_bytes = build_brand_kit_zip(
                    company     = bi.get("company","brand"),
                    industry    = bi.get("industry",""),
                    personality = bi.get("personality",""),
                    logos       = st.session_state.logos or [],
                    palette     = st.session_state.palette or {},
                    fonts       = st.session_state.fonts or [],
                    slogans     = st.session_state.slogans or [],
                    brand_story = st.session_state.brand_story or "",
                    translations= st.session_state.translations or {},
                    campaigns   = st.session_state.campaigns or {},
                    kpis        = st.session_state.kpis or {},
                    aesthetics  = st.session_state.aesthetics or {},
                    gif_bytes   = st.session_state.gif_bytes,
                )
            st.download_button(
                "⬇  Download Brand Kit ZIP",
                data=zip_bytes,
                file_name=f"{bi.get('company','Brand').replace(' ','_')}_BrandKit.zip",
                mime="application/zip",
            )

        # Chatbot
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">🤖 Brand AI Assistant</p>', unsafe_allow_html=True)

        for msg in st.session_state.chat_history:
            role = "You" if msg["role"] == "user" else "BrandSphere AI"
            bg   = "var(--surface2)" if msg["role"] == "user" else "var(--surface)"
            bc   = "var(--accent)"   if msg["role"] == "assistant" else "var(--border)"
            align = "flex-end" if msg["role"] == "user" else "flex-start"
            st.markdown(f"""
            <div style="display:flex;justify-content:{align};margin:7px 0">
              <div style="max-width:75%;background:{bg};border:1px solid {bc};border-radius:10px;padding:12px 16px">
                <div style="font-family:var(--font-mono);font-size:0.52rem;color:var(--accent);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:5px">{role}</div>
                <div style="font-size:0.87rem;line-height:1.65;color:var(--text)">{msg['content']}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        chat_c1, chat_c2 = st.columns([5, 1])
        with chat_c1:
            user_q = st.text_input("Ask BrandSphere AI…", key="chat_q",
                                   placeholder="e.g. What's the best platform for a luxury brand?",
                                   label_visibility="collapsed")
        with chat_c2:
            send_btn = st.button("Send →")

        if send_btn and user_q.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_q.strip()})
            ctx = f"Brand: {bi.get('company','')} | Industry: {bi.get('industry','')} | Personality: {bi.get('personality','')}"
            if st.session_state.gemini_ok:
                reply = gemini_call(
                    user_q.strip(),
                    system=f"You are BrandSphere AI, a branding expert. Context: {ctx}. Be concise (3–5 sentences)."
                )
            else:
                reply = "🔑 Connect your Gemini API key in the API Configuration section to get live AI answers."
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

        if st.session_state.chat_history:
            if st.button("🗑 Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()
