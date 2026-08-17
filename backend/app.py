import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import base64


from backend.pdf_reader import extract_pdf
from backend.analyze import analyze_document
from backend.text_extract import extract_text_from_image


def extract_pdf(_file):
        return ""

def analyze_document(_info, _question, _language):
        return ""

def extract_text_from_image(_image):
        return ""

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

icon_base64 = get_base64_image("icons/AmicusIcon.png")
icon_src = f"data:image/png;base64,{icon_base64}"


st.set_page_config(
    page_title="Amicus — Understand any legal document",
    page_icon="icons/AmicusIcon.ico",
    layout="centered",
    initial_sidebar_state="collapsed",
)

if "show_camera" not in st.session_state:
    st.session_state.show_camera = False
if "saved_question" not in st.session_state:
    st.session_state.saved_question = ""
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "processed_file_id" not in st.session_state:
    st.session_state.processed_file_id = None
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = ""

def go_to_analyze():
    st.session_state.current_page = "analyze"

def go_to_home():
    st.session_state.current_page = "home"

def go_to_info():
    st.session_state.current_page = "info"

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500;1,9..144,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

    :root {
        --bg: #FCFAF5;
        --bg-2: #F3EFE6;
        --ink: #0F1D38;
        --slate: #3E4F6D;
        --muted: #8290A6;
        --accent: #16305C;
        --accent-2: #2C508D;
        --line: rgba(15, 29, 56, 0.08);
        --glass: linear-gradient(155deg, rgba(255, 255, 255, 0.65), rgba(255, 255, 255, 0.3));
        --glass-strong: linear-gradient(155deg, rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.5));
        --glass-border: rgba(255, 255, 255, 0.7);
        --glass-hi: inset 0 2px 0 rgba(255, 255, 255, 0.9);
        --glass-shadow: 0 30px 60px -20px rgba(15, 29, 56, 0.12);
        --blur: blur(40px) saturate(180%);
        --blur-nav: blur(52px) saturate(190%);
    }

    #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
    [data-testid="stHeader"] { background: transparent !important; height: 0 !important; }
    [data-testid="stDecoration"] { display: none !important; }

    .stApp,
    [data-testid="stAppViewContainer"] {
        background-color: var(--bg) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: var(--ink) !important;
    }

    [data-testid="stAppViewContainer"]::before {
        content: ""; position: fixed; inset: -20% -10% -10% -10%; z-index: 0; pointer-events: none;
        background:
            radial-gradient(42% 38% at 14% 8%, rgba(22, 48, 92, 0.05) 0%, transparent 60%),
            radial-gradient(40% 40% at 88% 2%, rgba(200, 180, 140, 0.08) 0%, transparent 62%),
            radial-gradient(48% 44% at 78% 92%, rgba(22, 48, 92, 0.06) 0%, transparent 60%),
            radial-gradient(60% 50% at 10% 100%, rgba(200, 180, 140, 0.06) 0%, transparent 60%);
        filter: blur(20px);
        animation: aurora 26s ease-in-out infinite alternate;
    }
    @keyframes aurora {
        0%   { transform: translate3d(0, 0, 0) scale(1); }
        50%  { transform: translate3d(-2.5%, 2%, 0) scale(1.08); }
        100% { transform: translate3d(2.5%, -1.5%, 0) scale(1.04); }
    }

    .block-container {
        position: relative; z-index: 1;
        padding-top: 6.6rem !important;
        padding-bottom: 8rem !important;
        max-width: 968px !important;
    }

    h1, h2, h3, h4 { font-family: 'Fraunces', serif !important; color: var(--ink) !important; letter-spacing: -0.02em; }
    p, li, label, .stMarkdown { font-family: 'Plus Jakarta Sans', sans-serif !important; color: var(--slate) !important; line-height: 1.65; }
    strong, b { color: var(--ink) !important; }

    .rai-nav {
        position: fixed; top: 16px; left: 50%; transform: translateX(-50%);
        width: min(1120px, calc(100% - 26px)); z-index: 1000;
        display: flex; align-items: center; justify-content: space-between;
        padding: 10px 12px 10px 20px; border-radius: 999px;
        background: var(--glass-strong);
        backdrop-filter: var(--blur-nav); -webkit-backdrop-filter: var(--blur-nav);
        border: 1px solid var(--glass-border);
        box-shadow: var(--glass-shadow), var(--glass-hi);
    }
    .rai-brand { display: flex; align-items: center; gap: 12px; cursor: pointer; }
    .rai-brand .mark {
        width: 38px; height: 38px; border-radius: 12px;
        background: linear-gradient(150deg, var(--accent), #bf9a55);
        display: flex; align-items: center; justify-content: center; color: #241a06; font-size: 1rem;
        box-shadow: 0 12px 24px -10px rgba(231, 198, 142, 0.8), inset 0 1px 0 rgba(255,255,255,0.55);
    }
    .rai-brand .name { font-family: 'Fraunces', serif; font-weight: 700; font-size: 1.3rem; color: var(--ink); letter-spacing: -0.01em; }
    
    .hero {
        position: relative; margin: 0.2rem auto 2.6rem; padding: 3.4rem 2rem 2.8rem;
        border-radius: 38px; text-align: center; overflow: hidden;
        background: var(--glass);
        backdrop-filter: var(--blur); -webkit-backdrop-filter: var(--blur);
        border: 1px solid var(--glass-border);
        box-shadow: var(--glass-shadow), var(--glass-hi);
    }
    .hero::before {
        content: ""; position: absolute; inset: -60% -20% auto -20%; height: 90%;
        background: radial-gradient(50% 60% at 26% 0%, rgba(231,198,142,0.28), transparent 70%),
                    radial-gradient(48% 60% at 82% 4%, rgba(210,224,255,0.22), transparent 70%);
        pointer-events: none; animation: aurora 22s ease-in-out infinite alternate;
    }
    .hero-inner { position: relative; z-index: 1; }
    .glass-badge {
        display: inline-flex; align-items: center; gap: 9px; padding: 8px 18px; border-radius: 999px;
        background: var(--glass-strong); backdrop-filter: var(--blur);
        border: 1px solid var(--glass-border); color: var(--ink); font-weight: 700; font-size: 0.84rem;
        margin-bottom: 1.7rem; box-shadow: 0 14px 30px -20px rgba(0,0,0,0.7), var(--glass-hi);
    }
    .glass-badge i { color: var(--accent); }
    .hero h1 { font-size: clamp(2.6rem, 6vw, 4.3rem) !important; line-height: 1.02 !important; font-weight: 700 !important; margin: 0 0 1.1rem !important; color: var(--ink) !important; }
    .hero h1 .soft {
        font-style: italic;
        background: linear-gradient(120deg, var(--accent-2), var(--accent));
        -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero-sub { 
        font-size: 1.16rem !important; 
        color: var(--slate) !important; 
        max-width: 660px !important; 
        margin: 0 auto 2rem !important; 
        text-align: center !important;  
        line-height: 1.62 !important; 
    }

    .hero-stats { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; margin-top: 0.4rem; }
    .stat {
        display: flex; flex-direction: column; gap: 2px; padding: 15px 26px; border-radius: 20px; min-width: 132px;
        background: var(--glass-strong); backdrop-filter: var(--blur);
        border: 1px solid var(--glass-border); box-shadow: 0 20px 44px -30px rgba(0,0,0,0.8), var(--glass-hi);
    }
    .stat .n { font-family: 'Fraunces', serif; font-weight: 700; font-size: 1.6rem; color: var(--ink); }
    .stat .l { font-size: 0.8rem; color: var(--muted); font-weight: 600; letter-spacing: 0.02em; }

    .marquee { position: relative; margin: 2.4rem 0 0; padding: 0.3rem 0; overflow: hidden; border-radius: 16px; -webkit-mask-image: linear-gradient(90deg, transparent 0%, #000 14%, #000 86%, transparent 100%); mask-image: linear-gradient(90deg, transparent 0%, #000 14%, #000 86%, transparent 100%); }
    .marquee-track { display: flex; gap: 14px; width: max-content; animation: scrollx 30s linear infinite; }
    .marquee:hover .marquee-track { animation-play-state: paused; }
    .chip {
        display: inline-flex; align-items: center; gap: 9px; padding: 10px 18px; border-radius: 999px; white-space: nowrap;
        background: var(--glass-strong); backdrop-filter: var(--blur); border: 1px solid var(--glass-border);
        color: var(--ink); font-weight: 600; font-size: 0.9rem; box-shadow: var(--glass-hi);
    }
    .chip i { color: var(--accent); }
    @keyframes scrollx { from { transform: translateX(0); } to { transform: translateX(-50%); } }

    .eyebrow { text-transform: uppercase; letter-spacing: 0.18em; font-size: 0.75rem; font-weight: 800; color: var(--accent); font-family: 'Plus Jakarta Sans', sans-serif; margin-bottom: 0.4rem; }
    .sec-title { font-family: 'Fraunces', serif; font-size: 2.35rem; color: var(--ink); font-weight: 700; margin: 0 0 0.4rem; }
    .sec-sub { color: var(--slate); font-size: 1.05rem; margin-bottom: 1.4rem; }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--glass) !important;
        backdrop-filter: var(--blur); -webkit-backdrop-filter: var(--blur);
        border: 1px solid var(--glass-border) !important;
        border-radius: 34px !important;
        box-shadow: var(--glass-shadow), var(--glass-hi) !important;
        padding: 2rem 2rem 1.8rem !important;
    }

    .card-head { display: flex; align-items: center; gap: 12px; }
    .card-head .icon {
        width: 44px; height: 44px; border-radius: 14px; background: var(--glass-strong); backdrop-filter: var(--blur);
        border: 1px solid var(--glass-border); color: var(--accent); display: flex; align-items: center; justify-content: center; font-size: 1.1rem;
    }
    .card-head .t { font-family: 'Fraunces', serif; font-weight: 700; font-size: 1.5rem; color: var(--ink); }

    [data-baseweb="select"] > div {
        border-radius: 999px !important; border: 1px solid var(--glass-border) !important;
        background: var(--glass-strong) !important; backdrop-filter: var(--blur); min-height: 48px;
        box-shadow: var(--glass-hi);
    }
    [data-baseweb="select"] div { color: var(--ink) !important; }
    [data-baseweb="popover"] { backdrop-filter: var(--blur); }
    label[data-testid="stWidgetLabel"] { display: none !important; }

    [data-testid="stFileUploader"] { margin-top: 0.5rem; }
    [data-testid="stFileUploaderDropzone"], [data-testid="stFileUploadDropzone"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 280px !important;
        border-radius: 28px !important;
        border: 2px dashed rgba(255, 255, 255, 0.22) !important;
        background: linear-gradient(155deg, rgba(255,255,255,0.06), rgba(255,255,255,0.015)) !important; 
        backdrop-filter: var(--blur);
        padding: 2rem !important; 
        transition: all 0.25s ease !important;
        box-shadow: var(--glass-hi) !important;
    }
    
    [data-testid="stFileUploaderDropzone"]:hover, [data-testid="stFileUploadDropzone"]:hover {
        border-color: var(--accent) !important; transform: translateY(-2px);
        box-shadow: 0 34px 66px -34px rgba(0, 0, 0, 0.85), var(--glass-hi) !important;
    }

    [data-testid="stFileUploaderDropzone"] > div, 
    [data-testid="stFileUploadDropzone"] > div {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 0.6rem !important;
        width: 100% !important;
    }

    [data-testid="stFileUploaderDropzone"]::before, [data-testid="stFileUploadDropzone"]::before {
        content: "\\f0ee"; font-family: "Font Awesome 6 Free"; font-weight: 900;
        display: flex; align-items: center; justify-content: center;
        width: 74px; height: 74px; margin-bottom: 0.8rem; border-radius: 999px;
        background: var(--glass-strong); backdrop-filter: var(--blur);
        border: 1px solid var(--glass-border); color: var(--accent); font-size: 1.8rem;
        box-shadow: 0 18px 34px -18px rgba(0, 0, 0, 0.8), var(--glass-hi);
    }
    
    [data-testid="stFileUploaderDropzone"] svg,
    [data-testid="stFileUploadDropzone"] svg { display: none !important; }
    
    [data-testid="stFileUploaderDropzoneInstructions"],
    [data-testid="stFileDropzoneInstructions"] { 
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        text-align: center !important; 
        gap: 0.3rem !important;
    }
    
    [data-testid="stFileUploaderDropzoneInstructions"] span,
    [data-testid="stFileDropzoneInstructions"] span { 
        font-family: 'Fraunces', serif !important; font-weight: 700 !important; font-size: 1.5rem !important; color: var(--ink) !important; 
        display: block !important;
    }
    
    [data-testid="stFileUploaderDropzoneInstructions"] small,
    [data-testid="stFileDropzoneInstructions"] small { 
        font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.98rem !important; color: var(--muted) !important; 
        display: block !important;
    }
    
    [data-testid="stFileUploaderDropzone"] button, [data-testid="stFileUploadDropzone"] button {
        position: relative !important;
        margin-top: 1rem !important; border-radius: 999px !important; border: none !important;
        background: #F6F4EF !important; color: #14141a !important;
        font-family: 'Inter', sans-serif !important; font-weight: 800 !important; padding: 0.74rem 2rem !important;
        box-shadow: 0 18px 34px -14px rgba(0, 0, 0, 0.75), inset 0 1px 0 rgba(255,255,255,0.95) !important; transition: transform 0.15s ease !important;
        z-index: 10 !important;
    }
    
    [data-testid="stFileUploaderDropzone"] button:hover, [data-testid="stFileUploadDropzone"] button:hover { transform: translateY(-1px); }
    [data-testid="stFileUploaderDropzone"] button p, [data-testid="stFileUploadDropzone"] button p { color: #14141a !important; font-family: 'Inter', sans-serif !important; font-weight: 800 !important; }

    .stButton { display: flex; justify-content: center; }
    .stButton > button, .stButton > button p {
        font-family: 'Inter', sans-serif !important; font-weight: 700 !important; letter-spacing: 0.02em !important;
    }
    .stButton > button {
        border-radius: 999px !important;
        padding: 0.84rem 2rem !important; border: 1px solid var(--glass-border) !important;
        background: var(--glass-strong) !important; backdrop-filter: var(--blur);
        color: var(--ink) !important; transition: all 0.2s ease !important; width: auto; min-width: 260px;
        box-shadow: var(--glass-hi) !important;
    }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 22px 40px -20px rgba(0,0,0,0.75), var(--glass-hi) !important; border-color: var(--accent) !important; }
    .stButton > button[kind="primary"] {
        background: linear-gradient(150deg, var(--accent-2), var(--accent)) !important; 
        border-color: transparent !important; 
        color: var(--bg) !important; 
        box-shadow: 0 20px 38px -16px rgba(22, 48, 92, 0.4), inset 0 1px 0 rgba(255,255,255,0.2) !important;
    }
    .stButton > button[kind="primary"] p { color: var(--bg) !important; } 
    .stButton > button[kind="primary"]:hover { filter: brightness(1.04); }

    .or-divider { display: flex; align-items: center; gap: 16px; color: var(--muted); font-size: 0.82rem; font-weight: 700; letter-spacing: 0.12em; margin: 1.5rem 0; text-transform: uppercase; }
    .or-divider::before, .or-divider::after { content: ""; flex: 1; height: 1px; background: var(--line); }

    [data-testid="stAlert"] {
        border-radius: 18px !important; border: 1px solid var(--glass-border) !important;
        background: var(--glass-strong) !important; backdrop-filter: var(--blur);
        box-shadow: var(--glass-hi) !important; color: var(--ink) !important;
    }
    [data-testid="stAlert"] p { color: var(--ink) !important; }

    [data-testid="stExpander"] {
        border-radius: 18px !important; border: 1px solid var(--glass-border) !important;
        background: var(--glass) !important; backdrop-filter: var(--blur);
        margin-bottom: 0.7rem; overflow: hidden; box-shadow: var(--glass-hi);
    }
    [data-testid="stExpander"] summary { font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 700 !important; color: var(--ink) !important; padding: 0.5rem 0.3rem; }
    [data-testid="stExpander"] summary:hover { color: var(--accent) !important; }

    [data-testid="stBottom"] {
        background: linear-gradient(to top, var(--bg) 40%, rgba(245, 242, 235, 0.8) 80%, transparent 100%) !important;
        backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
    }
    [data-testid="stBottom"] > div { background: transparent !important; }
    [data-testid="stBottomBlockContainer"] { max-width: 760px !important; margin: 0 auto !important; padding-bottom: 1.4rem !important; padding-top: 0.6rem !important; }
    [data-testid="stChatInput"] {
        background: var(--glass-strong) !important; backdrop-filter: var(--blur); -webkit-backdrop-filter: var(--blur);
        border: 1px solid var(--glass-border) !important; border-radius: 999px !important;
        box-shadow: var(--glass-shadow), var(--glass-hi) !important;
    }
    [data-testid="stChatInput"] textarea { color: var(--ink) !important; }
    [data-testid="stChatInput"] textarea::placeholder { color: var(--muted) !important; }
    [data-testid="stChatInput"] button { background: linear-gradient(150deg, var(--accent-2), var(--accent)) !important; border: none !important; }
    [data-testid="stChatInput"] button svg { color: #241a06 !important; fill: #241a06 !important; }

    .trust-pill {
        display: flex; align-items: center; justify-content: center; gap: 12px; text-align: center;
        color: var(--slate); background: var(--glass); backdrop-filter: var(--blur);
        border: 1px solid var(--glass-border); border-radius: 18px; padding: 16px 22px;
        margin: 1.5rem auto 0.4rem; max-width: 720px; font-size: 0.95rem;
        box-shadow: var(--glass-hi);
    }
    .trust-pill b { color: var(--ink); }
    .trust-pill i { color: var(--accent); font-size: 1.1rem; }

    .uc-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 0.5rem 0 1rem; }
    @media (max-width: 720px) { .uc-grid { grid-template-columns: 1fr; } }
    .uc-card {
        background: var(--glass); backdrop-filter: var(--blur); border: 1px solid var(--glass-border); border-radius: 22px;
        padding: 1.6rem; box-shadow: var(--glass-shadow), var(--glass-hi); transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .uc-card:hover { transform: translateY(-4px); box-shadow: 0 34px 60px -32px rgba(0, 0, 0, 0.9), var(--glass-hi); }
    .uc-card .uc-ic { width: 46px; height: 46px; border-radius: 14px; background: var(--glass-strong); backdrop-filter: var(--blur); border: 1px solid var(--glass-border); color: var(--accent); display: flex; align-items: center; justify-content: center; font-size: 1.1rem; margin-bottom: 0.9rem; }
    .uc-card h4 { font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 800; color: var(--ink) !important; font-size: 1.05rem; margin: 0 0 0.4rem; }
    .uc-card p { font-size: 0.92rem; color: var(--slate); margin: 0; }

    .rai-section { margin-top: 3.8rem; }
    .site-footer { text-align: center; color: var(--muted); font-size: 0.84rem; margin-top: 3.8rem; line-height: 1.7; }

    @keyframes floatUp { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
    .hero, .rai-section { animation: floatUp 0.7s cubic-bezier(0.22, 1, 0.36, 1) both; }
    @media (prefers-reduced-motion: reduce) { .hero, .rai-section, .marquee-track, [data-testid="stAppViewContainer"]::before, .hero::before { animation: none; } }

    .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a, 
    [data-testid="stHeaderActionElements"] {
        display: none !important;
    }

    
    /* --- HIDE GLOBE ON DESKTOP --- */
    .rai-mobile-right { display: none; }

    /* TIGHTER MOBILE OPTIMIZATION */
    @media (max-width: 640px) {
        /* 1. Make the Top Bar Taller & Add the Globe */
        .rai-nav { 
            padding: 12px 18px !important; 
            top: 12px !important; 
            width: calc(100% - 24px) !important; 
            justify-content: space-between !important;
        }
        .rai-brand .mark { width: 34px !important; height: 34px !important; font-size: 0.9rem !important; }
        .rai-brand .name { font-size: 1.15rem !important; }
        
        .rai-mobile-right { 
            display: flex; 
            align-items: center; 
            color: var(--slate); 
            font-size: 1.1rem; 
        }

        /* 2. Kill the Extra Scroll Space */
        .block-container { 
            padding-top: 5.5rem !important; 
            padding-bottom: 0.5rem !important; 
        }
        .site-footer { margin-top: 1.5rem !important; } 
        
        .hero { 
            padding: 2rem 1rem 2rem !important; 
            border-radius: 24px !important; 
            margin: 0 auto 0.5rem !important; 
        }
        .hero h1 { font-family: 'Fraunces', serif !important; font-size: 1.9rem !important; margin: 0 0 0.5rem !important; }
        .hero-sub { font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.9rem !important; margin: 0 auto 1rem !important; line-height: 1.4 !important; }
        .glass-badge { margin-bottom: 0.8rem !important; padding: 5px 12px !important; font-size: 0.75rem !important; }

        .hero-stats { display: grid !important; grid-template-columns: repeat(3, 1fr) !important; gap: 6px !important; }
        .stat { min-width: unset !important; padding: 8px 4px !important; border-radius: 14px !important; }
        .stat .n { font-size: 1.1rem !important; }
        .stat .l { font-size: 0.6rem !important; }

        .stButton > button { padding: 0.75rem 1rem !important; font-size: 1rem !important; min-width: 240px !important; }
        
        .marquee { margin: 0.5rem 0 0 !important; }
        .chip { padding: 6px 12px !important; font-size: 0.8rem !important; }

        /* THESE MUST BE INSIDE THE MEDIA QUERY! */
        [data-testid="stVerticalBlockBorderWrapper"] {
            padding: 1.2rem 1rem 1rem !important; 
            border-radius: 28px !important;
        }
        .card-head .t { font-size: 1.2rem !important; }
        [data-testid="stFileUploaderDropzone"], 
        [data-testid="stFileUploadDropzone"] {
            min-height: 220px !important;
            padding: 1.2rem 1rem !important;
        }
        [data-testid="stFileUploaderDropzoneInstructions"] span,
        [data-testid="stFileDropzoneInstructions"] span { 
            font-size: 1.15rem !important; 
        } 
    } 
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    f"""
    <div class="rai-nav">
        <div class="rai-brand" onclick="window.parent.postMessage('go_home', '*');" style="cursor: pointer;">
            <img src="{icon_src}" style="width: 38px; height: 38px; border-radius: 12px; object-fit: cover;" />
            <div class="name">Amicus</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Handle Chat Input globally when on analyze page
if st.session_state.current_page == "analyze":
    user_question = st.chat_input("Ask a question about your document…")
    if user_question:
        st.session_state.saved_question = user_question

# ==========================================
# SCREEN 1: THE HOME PAGE
# ==========================================
if st.session_state.current_page == "home":
    st.markdown(
        """
        <section class="hero">
            <div class="hero-inner">
                <div class="glass-badge"><i class="fa-solid fa-globe"></i> Understand your rights in 65+ languages</div>
                <h1>Your companion<br><span class="soft">in the legal world.</span></h1>
                <p class="hero-sub">Amicus turns confusing legal documents into clear, plain-language guidance — so language is never a barrier.</p>
                <div class="hero-stats">
                    <div class="stat"><span class="n">65+</span><span class="l">Languages</span></div>
                    <div class="stat"><span class="n">20 MB</span><span class="l">PDF or photo</span></div>
                    <div class="stat"><span class="n">0</span><span class="l">Files stored</span></div>
                </div>
            </div>
            <div class="marquee">
                <div class="marquee-track">
                    <span class="chip"><i class="fa-solid fa-house-chimney"></i> Lease agreements</span>
                    <span class="chip"><i class="fa-solid fa-briefcase"></i> Employment contracts</span>
                    <span class="chip"><i class="fa-solid fa-passport"></i> Immigration forms</span>
                    <span class="chip"><i class="fa-solid fa-file-signature"></i> Terms of service</span>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    with col2:
        st.button(
            "Go to Analysis Tool →", 
            on_click=go_to_analyze, 
            type="primary", 
            use_container_width=True
        )
        st.button(
            "Use Cases & FAQ", 
            on_click=go_to_info, 
            use_container_width=True
        )

    st.markdown(
        """
        <div class="site-footer">
            © 2026 Amicus. All rights reserved.<br>
            <i>Disclaimer: Amicus provides informational insights and does not constitute official legal advice.</i>
        </div>
        """,
        unsafe_allow_html=True,
    )


elif st.session_state.current_page == "analyze":
    st.button("← Back to Home", on_click=go_to_home)
    components.html(
        """
        <script>
            var mainContainer = window.parent.document.querySelector('.main');
            if (mainContainer) {
                mainContainer.scrollTop = 0;
            }
        </script>
        """,
        height=0
    )

    tab1, tab2 = st.tabs(["Analyze", "About us"])

    with tab1:
        st.markdown('<div id="analyze"></div>', unsafe_allow_html=True)
        
        if not _BACKEND_AVAILABLE:
            st.error("Backend modules failed to load. Analysis will not be available.", icon="⚠️")

        with st.container(border=True):
            head_left, head_right = st.columns([1.4, 1], vertical_alignment="center")
            with head_left:
                st.markdown(
                    f"""
                    <div class="card-head">
                        <img src="{icon_src}" style="width: 44px; height: 44px; border-radius: 14px; object-fit: cover;" />
                        <div class="t">Plain-language analysis</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with head_right:
                user_language = st.selectbox(
                    "Your preferred language",
                    (
                        "English", "Spanish (Español)", "French (Français)", "Chinese (中文)",
                        "Arabic (العربية)", "Russian (Русский)", "Portuguese (Português)",
                        "Hindi (हिन्दी)", "Bengali (বাংলা)", "Japanese (日本語)", "German (Deutsch)",
                        "Korean (한국어)", "Italian (Italiano)", "Dutch (Nederlands)", "Turkish (Türkçe)",
                        "Vietnamese (Tiếng Việt)", "Polish (Polski)", "Ukrainian (Українська)",
                        "Romanian (Română)", "Greek (Ελληνικά)", "Czech (Čeština)", "Swedish (Svenska)",
                        "Hungarian (Magyar)", "Finnish (Suomi)", "Dansk (Danish)", "Norwegian (Norsk)",
                        "Catalan (Català)", "Indonesian (Bahasa Indonesia)", "Malay (Bahasa Melayu)",
                        "Thai (ไทย)", "Hebrew (עברית)", "Bulgarian (Български)", "Croatian (Hrvatski)",
                        "Estonian (Eesti)", "Gujarati (ગુજરાતી)", "Kannada (ಕನ್ನಡ)", "Latvian (Latviešu)",
                        "Lithuanian (Lietuvių)", "Malayalam (മലയാളം)", "Marathi (मराठी)",
                        "Slovak (Slovenčina)", "Slovenian (Slovenščina)", "Swahili (Kiswahili)",
                        "Tamil (தமிழ்)", "Telugu (తెలుగు)", "Urdu (اردو)", "Serbian (Српски)",
                        "Filipino (Filipino)", "Icelandic (Íslenska)", "Amharic (አማርኛ)",
                        "Armenian (Հայերեն)", "Azerbaijani (Azərbaycan dili)", "Basque (Euskara)",
                        "Galician (Galego)", "Georgian (ქართული)", "Kazakh (Қазақ тілі)",
                        "Khmer (ខ្Khmer)", "Lao (ລາວ)", "Macedonian (Македонски)", "Mongolian (Монгол)",
                        "Nepali (नेपाली)", "Sinhala (සිංහල)", "Albanian (Shqip)", "Bosnian (Bosanski)",
                        "Uzbek (Oʻzbekcha)", "Zulu (isiZulu)", "Afrikaans (Afrikaans)",
                    ),
                    label_visibility="collapsed",
                )

            uploaded_pdf = st.file_uploader(
                "Drop your legal document here",
                type="pdf",
                help="PDF up to 20 MB. Your file is analyzed in real time and never stored.",
            )

            if uploaded_pdf is not None:
                    with st.spinner("Analyzing Document…"):
                        text = extract_pdf(uploaded_pdf)
                        if text and text.strip():
                            result = analyze_document(text, st.session_state.saved_question, user_language)
                            st.success("Analysis complete!")
                            st.markdown(result)
                        else:
                            st.error("No readable text found in this PDF. Please ensure it is a real PDF")

            st.markdown('<div class="or-divider">or</div>', unsafe_allow_html=True)

            def open_camera():
                st.session_state.show_camera = True

            left_col, center_col, right_col = st.columns([1, 2, 1])
            with center_col:
                st.button(
                    "Take a photo of your document",
                    on_click=open_camera,
                    type="primary",
                    use_container_width=True
                )

            if st.session_state.show_camera:
                uploaded_camera_image = st.camera_input("Capture your document")
                if uploaded_camera_image is not None:
                    with st.spinner("Analyzing Document…"):
                        text = extract_text_from_image(uploaded_camera_image)
                        if text and text.strip():
                            image_analysis = analyze_document(text, st.session_state.saved_question, user_language)
                            st.success("Analysis complete!")
                            st.markdown(image_analysis)
                        else:
                            st.error("No readable text found in the image. Please ensure the document is clear and well-lit.")

            st.markdown(
                """
                <div id="security"></div>
                <div class="trust-pill">
                    <i class="fa-solid fa-shield-halved"></i>
                    <span><b>Bank-grade encryption</b> · documents deleted after analysis</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="site-footer">
                    © 2026 Amicus. All rights reserved.<br>
                    <i>Disclaimer: Amicus provides informational insights and does not constitute official legal advice.</i>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab2:
        st.markdown(
            """
            <div class="rai-section" style="margin-top:1.4rem;">
                <div class="eyebrow">Our mission</div>
                <div class="sec-title">Language should never stand between you and justice.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            Navigating the American legal system can be overwhelming, especially when
            language barriers stand in the way of justice.

            For residents with Limited English Proficiency, a simple misunderstanding of
            legal documents or complex political jargon can lead to unintended legal trouble
            and compromised due process.

            Our platform bridges this critical gap by empowering you to:
            * **Fully understand** your rights.
            * **Easily decode** complicated legal language.
            * **Confidently plan** your next steps.
            """
        )

# ==========================================
# SCREEN 3: USE CASES & FAQ PAGE
# ==========================================
elif st.session_state.current_page == "info":
    st.button("← Back to Home", on_click=go_to_home)

    st.markdown(
        """
        <div id="usecases" class="rai-section" style="margin-top: 1rem;">
            <div class="eyebrow">Use cases</div>
            <div class="sec-title">Not sure where to start?</div>
            <div class="sec-sub">Upload or snap a photo of any of these to see plain-language guidance.</div>
            <div class="uc-grid">
                <div class="uc-card">
                    <div class="uc-ic"><i class="fa-solid fa-house-chimney"></i></div>
                    <h4>Lease agreements</h4>
                    <p>Understand your renting rights, deposit terms, and hidden fees.</p>
                </div>
                <div class="uc-card">
                    <div class="uc-ic"><i class="fa-solid fa-briefcase"></i></div>
                    <h4>Employment contracts</h4>
                    <p>Decode non-competes, termination clauses, and benefits.</p>
                </div>
                <div class="uc-card">
                    <div class="uc-ic"><i class="fa-solid fa-passport"></i></div>
                    <h4>Immigration forms</h4>
                    <p>Clarify confusing government jargon and your next steps.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div id="faq" class="rai-section">
            <div class="eyebrow">FAQ</div>
            <div class="sec-title">Frequently asked questions</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("How accurate is the AI analysis?"):
        st.write(
            "Our AI is trained on vast amounts of legal data to provide accurate summaries. "
            "However, it is an informational companion, not a replacement for a certified lawyer."
        )
    with st.expander("Do you save my legal documents?"):
        st.write(
            "No. Your privacy is our top priority. Documents are analyzed in real time and "
            "immediately deleted from our servers once the analysis is complete."
        )
    with st.expander("What languages are supported?"):
        st.write(
            "We currently support over 65 languages. Just select your preferred language "
            "from the dropdown above."
        )

    st.markdown(
        """
        <div class="site-footer">
            © 2026 Amicus. All rights reserved.<br>
            <i>Disclaimer: Amicus provides informational insights and does not constitute official legal advice.</i>
        </div>
        """,
        unsafe_allow_html=True,
    )