import sys
from pathlib import Path
import base64
import io
from nicegui import ui, app, run
ROOT_DIR = Path(__file__).resolve().parent.parent # <-- Added an extra .parent here!
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
from backend.pdf_reader import extract_pdf
from backend.analyze import analyze_document
from backend.text_extract import extract_text_from_image
_BACKEND_AVAILABLE = True
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""  # Fallback if icon missing

BASE_DIR = ROOT_DIR
icon_base64 = get_base64_image(BASE_DIR / "icons" / "AmicusIcon.png")
icon_src = f"data:image/png;base64,{icon_base64}" if icon_base64 else ""

LOCAL_IMAGE_PATH = ROOT_DIR / "assets" / "bg.jpg"

app.add_static_files('/images', str(ROOT_DIR / "assets"))

BG_IMAGE_URL = "/images/bg.jpg"

ui.add_head_html(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    <style>
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Silkscreen:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,100..900;1,9..144,100..900&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

    .q-field__native::placeholder,
    .q-field__input::placeholder,
    .q-field__label {{
        color: rgba(255, 255, 255, 0.7) !important;
    }}

    :root {{
        --bg:         #FCFAF5; 
        --ink:        #0F1D38; 
        --text-90:    rgba(15,29,56,0.90);
        --text-70:    rgba(62,79,109,0.80); 
        --text-60:    rgba(62,79,109,0.65);
        --text-45:    rgba(62,79,109,0.45);
        --glass:      rgba(255,255,255,0.75); 
        --glass-2:    rgba(255,255,255,0.50);
        --glass-brd:  rgba(255,255,255,0.90);
        --cta-grad:   linear-gradient(to bottom, #000000, #000000); 
        --accent:     #253b85;
        --radius:     22px;
        --shadow-md:  0 20px 40px -20px rgba(0,0,0,0.08);
        --shadow-lg:  0 30px 60px -25px rgba(0,0,0,0.12);
    }}

    .q-field__native, 
    .q-field__input, 
    .q-field__prefix, 
    .q-field__suffix {{
        color: #ffffff !important;
    }}

    html {{ background-color: var(--bg); }}
    
    body {{
        background-color: transparent;
        font-family: 'Geist', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--ink);
        margin: 0;
        scroll-behavior: smooth;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}
    .q-layout, .q-page-container, .q-page, .nicegui-content {{
        background: transparent !important;
    }}

    .amicus-img-bg {{
        position: fixed; inset: 0;
        width: 100%; height: 100%;
        object-fit: cover; z-index: -2;
    }}
    
    .nicegui-content {{ padding: 0 !important; }}

    .font-display, .font-serif {{ font-family: 'Geist', sans-serif !important; letter-spacing: -0.02em; }}
    .eyebrow {{
        font-weight: 600; font-size: 0.76rem; letter-spacing: 0.24em;
        text-transform: uppercase; color: var(--text-60);
    }}

    .rai-nav {{
        position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
        z-index: 1000; width: min(1160px, calc(100% - 32px));
        display: flex; align-items: center; justify-content: space-between;
        padding: 10px 10px 10px 18px;
        cursor: pointer;
    }}
    .rai-nav .brand {{ display: flex; align-items: center; gap: 10px; }}
    .rai-nav .brand-name {{
        font-family: 'Geist', sans-serif; font-weight: 600; font-size: 1.15rem;
        color: #fff; letter-spacing: -0.01em;
    }}
    .rai-nav .nav-links {{
        display: flex; align-items: center; gap: 6px;
        padding: 6px; border-radius: 999px;
        background: var(--glass);
        border: 1px solid var(--glass-brd);
        backdrop-filter: blur(18px) saturate(160%);
        -webkit-backdrop-filter: blur(18px) saturate(160%);
    }}
    .rai-nav .nav-links a {{
        text-decoration: none; color: var(--text-70); font-weight: 500;
        font-size: 0.9rem; padding: 8px 16px; border-radius: 999px;
        transition: all .2s ease;
    }}
    .rai-nav .nav-links a:hover {{ color: #fff; background: rgba(255,255,255,0.10); }}
    .rai-nav .nav-cta {{
        background: var(--cta-grad); color: #fff !important; font-weight: 500;
        border: 1px solid rgba(255,255,255,0.10);
    }}
    .rai-nav .nav-cta:hover {{ opacity: 0.9; background: var(--cta-grad); }}
    @media (max-width: 720px) {{ .rai-nav .nav-links a.hide-sm {{ display: none; }} }}

    .hero {{
        position: relative;
        min-height: 100vh;
        display: flex; flex-direction: column; justify-content: flex-end;
        padding: 7rem 3rem 3.5rem;
        max-width: 1200px; margin: 0 auto; width: 100%;
    }}
    .hero-inner {{
        display: flex; flex-direction: column; gap: 2.5rem;
        align-items: flex-start; justify-content: space-between;
    }}
    @media (min-width: 1024px) {{
        .hero-inner {{ flex-direction: row; align-items: flex-end; }}
    }}
    .hero-copy {{ max-width: 36rem; }}
    .hero-badge {{
        display: inline-flex; align-items: center; gap: 9px;
        padding: 7px 15px; border-radius: 999px;
        background: var(--glass); border: 1px solid var(--glass-brd);
        backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
        font-weight: 500; font-size: 0.8rem; color: var(--text-90);
        margin-bottom: 1.4rem;
    }}
    .hero h1 {{
        font-family: 'Geist', sans-serif; font-weight: 600;
        font-size: clamp(2.2rem, 5vw, 3.5rem);
        margin: 0; color: #fff;
        line-height: 1.08; letter-spacing: -0.03em;
    }}
    .hero h1 .accent {{ color: var(--text-45); }}
    .hero .lead {{
        color: var(--text-70); font-size: 1.1rem; max-width: 34rem;
        margin: 1.3rem 0 0; line-height: 1.6;
    }}

    .glass-cards {{ display: flex; flex-direction: column; gap: 16px; }}
    @media (min-width: 640px) {{ .glass-cards {{ flex-direction: row; }} }}
    .glass-card {{
        border-radius: 20px; background: var(--glass);
        border: 1px solid var(--glass-brd);
        backdrop-filter: blur(18px) saturate(160%);
        -webkit-backdrop-filter: blur(18px) saturate(160%);
        padding: 22px; width: 100%;
    }}
    @media (min-width: 640px) {{ .glass-card {{ width: 16rem; }} }}
    .glass-card.stat {{ display: flex; flex-direction: column; justify-content: space-between; }}
    .glass-card .num {{
        font-family: 'Silkscreen', cursive; font-weight: 400;
        font-size: clamp(1.8rem, 4vw, 2.2rem); letter-spacing: -0.02em; color: #fff;
    }}
    .glass-card .stat-body {{ color: var(--text-70); font-size: 0.9rem; line-height: 1.55; margin-top: 1rem; }}
    .glass-card .t-head {{ display: flex; align-items: center; gap: 8px; margin-bottom: 1rem; }}
    .glass-card .t-badge {{
        width: 24px; height: 24px; border-radius: 7px; display: grid; place-items: center;
        background: #000; color: #fff; font-weight: 700; font-size: 0.85rem;
    }}
    .glass-card .t-name {{ font-size: 0.9rem; font-weight: 600; color: #fff; }}
    .glass-card .quote {{ color: var(--text-70); font-size: 0.9rem; line-height: 1.6; margin: 0; }}
    .glass-card .t-foot {{ display: flex; align-items: center; gap: 12px; margin-top: 1.25rem; }}
    .glass-card .t-foot img {{ width: 36px; height: 36px; border-radius: 999px; object-fit: cover; background: rgba(255,255,255,0.2); }}
    .glass-card .t-foot .n {{ font-size: 0.9rem; font-weight: 600; color: #fff; }}
    .glass-card .t-foot .r {{ font-size: 0.75rem; color: var(--text-60); }}

    .scroll-cue {{
        margin-top: 2.5rem; display: flex; align-items: center; gap: 8px;
        color: var(--text-45); font-size: 0.8rem; letter-spacing: 0.12em; text-transform: uppercase;
    }}
    .scroll-cue i {{ animation: bob 1.8s ease-in-out infinite; }}
    @keyframes bob {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(5px); }} }}

    .section {{ max-width: 1120px; margin: 0 auto; padding: 0 24px; }}
    .section-head {{ text-align: center; max-width: 640px; margin: 0 auto 3rem; }}
    .section-head h2 {{
        font-family: 'Geist', sans-serif; font-weight: 600;
        font-size: clamp(1.9rem, 4vw, 2.7rem); color: #fff;
        letter-spacing: -0.03em; margin: 0.6rem 0 0.8rem; line-height: 1.1;
    }}
    .section-head p {{ color: var(--text-70); font-size: 1.05rem; line-height: 1.6; margin: 0; }}

    .feature-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }}
    @media (max-width: 820px) {{ .feature-grid {{ grid-template-columns: 1fr; }} }}
    .feature-card {{
        background: var(--glass-2); border: 1px solid var(--glass-brd);
        border-radius: var(--radius); padding: 28px 24px;
        backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
        transition: transform .25s ease, background .25s ease, border-color .25s ease;
    }}
    .feature-card:hover {{ transform: translateY(-4px); background: var(--glass); border-color: rgba(255,255,255,0.28); }}
    .feature-icon {{
        width: 50px; height: 50px; border-radius: 14px;
        display: grid; place-items: center; margin-bottom: 18px;
        background: var(--cta-grad); border: 1px solid rgba(255,255,255,0.14);
        color: #fff; font-size: 1.2rem;
    }}
    .feature-card h3 {{
        font-family: 'Geist', sans-serif; font-size: 1.2rem; color: #fff;
        margin: 0 0 8px; font-weight: 600; letter-spacing: -0.01em;
    }}
    .feature-card p {{ color: var(--text-70); line-height: 1.6; margin: 0; font-size: 0.98rem; }}
    .step-index {{
        font-family: 'Silkscreen', cursive; font-weight: 400; color: var(--text-45);
        font-size: 0.8rem; letter-spacing: 0.02em; margin-bottom: 4px;
    }}

    .cta-band {{
        position: relative; overflow: hidden;
        max-width: 1120px; margin: 0 auto; padding: 3.4rem 2rem;
        border-radius: 28px; text-align: center;
        background: var(--glass); border: 1px solid var(--glass-brd);
        backdrop-filter: blur(20px) saturate(150%);
        -webkit-backdrop-filter: blur(20px) saturate(150%);
        box-shadow: var(--shadow-lg);
    }}
    .cta-band h2 {{
        font-family: 'Geist', sans-serif; color: #fff; font-weight: 600;
        font-size: clamp(1.8rem, 4vw, 2.5rem); margin: 0 0 0.7rem; letter-spacing: -0.03em;
    }}
    .cta-band p {{
        color: var(--text-70); font-size: 1.05rem; max-width: 520px;
        margin: 0 auto; line-height: 1.6;
    }}

    .site-footer {{
        max-width: 1120px; 
        margin: 5rem auto 0; 
        padding: 2.4rem 24px 3rem;
        border-top: 1px solid var(--glass-brd); 
        text-align: center;
        color: rgba(255, 255, 255, 0.75) !important;
        font-size: 0.9rem; 
        line-height: 1.7;
    }}
    .site-footer i {{ color: #8AB4FF !important; }}
    .site-footer strong {{ color: #ffffff !important; }}
    .site-footer em {{ color: rgba(255, 255, 255, 0.6) !important; }}

    .amicus-content h1, .amicus-content h2, .amicus-content h3,
    .amicus-markdown h1, .amicus-markdown h2, .amicus-markdown h3 {{
        font-family: 'Geist', sans-serif !important;
        color: #fff !important; font-weight: 600 !important;
        font-size: 1.7rem !important; margin-top: 1.2em !important;
        margin-bottom: 0.5em !important; line-height: 1.2 !important;
        letter-spacing: -0.02em !important;
    }}
    .amicus-content p, .amicus-content li,
    .amicus-markdown p, .amicus-markdown li {{
        font-family: 'Geist', sans-serif !important;
        color: rgba(255, 255, 255, 0.85) !important;
        line-height: 1.65 !important;
        font-size: 1.05rem !important;
        margin-bottom: 0.9em !important;
    }}
    .amicus-content ul, .amicus-markdown ul {{
        list-style-type: disc !important; padding-left: 1.4em !important; margin-bottom: 1.2em !important;
    }}
    .amicus-content strong, .amicus-content b,
    .amicus-markdown strong, .amicus-markdown b {{ color: #fff !important; font-weight: 600 !important; }}

    .amicus-primary-btn {{
        background: var(--cta-grad) !important; color: #fff !important;
        border-radius: 999px !important; border: 1px solid rgba(255,255,255,0.12) !important;
        box-shadow: 0 20px 40px -22px rgba(0,0,0,0.9) !important;
        transition: opacity .2s ease, transform .2s ease !important;
    }}
    .amicus-primary-btn:hover {{ opacity: 0.9; transform: translateY(-2px); }}
    .amicus-ghost-btn {{
        background: var(--glass) !important; color: #fff !important;
        border: 1px solid var(--glass-brd) !important; border-radius: 999px !important;
        backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
        transition: transform .2s ease, background .2s ease !important;
    }}
    .amicus-ghost-btn:hover {{ transform: translateY(-2px); background: rgba(255,255,255,0.16) !important; }}

    .amicus-card {{
    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.18),
            rgba(255,255,255,0.07) 48%,
            rgba(255,255,255,0.10)
        ),
        rgba(16, 24, 42, 0.30) !important;

    backdrop-filter: blur(28px) saturate(145%) !important;
    -webkit-backdrop-filter: blur(28px) saturate(145%) !important;

    border: 1px solid rgba(255,255,255,0.30) !important;

    box-shadow:
        0 40px 100px -42px rgba(0,0,0,0.72),
        0 10px 30px -18px rgba(0,0,0,0.42),
        inset 0 1px 0 rgba(255,255,255,0.26),
        inset 0 -1px 0 rgba(255,255,255,0.07) !important;
}}
    .amicus-card .q-field__native, .amicus-card .text-2xl {{ color: #fff !important; }}

    .q-tabs {{ background: var(--glass); border: 1px solid var(--glass-brd); border-radius: 999px; padding: 4px; backdrop-filter: blur(14px); }}
    .q-tab {{ border-radius: 999px !important; text-transform: none !important; font-weight: 600 !important; color: var(--text-60) !important; min-height: 42px !important; }}
    .q-tab--active {{ color: #04060d !important; background: #fff !important; }}
    .q-tabs .q-tab__indicator {{ display: none !important; }}

    .q-field--outlined .q-field__control {{ border-radius: 16px !important; background: rgba(255,255,255,0.06) !important; }}
    .q-field--outlined .q-field__control:before {{ border-color: var(--glass-brd) !important; }}
    .q-field__native, .q-field__input {{ color: #fff !important; }}
    .q-field__label {{ color: var(--text-60) !important; }}
    .amicus-select .q-field__control {{ background: rgba(255,255,255,0.08) !important; }}

    .q-uploader {{ border-radius: 18px !important; box-shadow: none !important; background: rgba(255,255,255,0.04) !important; }}
    .q-uploader__header {{ background: var(--cta-grad) !important; color: #fff !important; border-radius: 14px 14px 0 0 !important; }}
    .q-uploader__list {{ background: transparent !important; color: #fff !important; }}

    .amicus-glass {{ background: var(--glass) !important; border: 1px solid var(--glass-brd) !important; backdrop-filter: blur(16px); border-radius: 16px !important; color: #fff !important; }}
    .q-expansion-item .q-item {{ font-weight: 600 !important; color: #fff !important; }}
    .q-expansion-item .q-item__section--side .q-icon {{ color: var(--text-70) !important; }}

    .amicus-back {{ color: var(--text-60) !important; text-transform: none !important; font-weight: 500 !important; }}
    .amicus-back:hover {{ color: #fff !important; }}

    .spin-card {{ opacity: 0; will-change: transform, opacity; }}
    .spin-card.in-view {{ opacity: 1; animation: cardSpinIn 0.95s cubic-bezier(0.22, 1, 0.36, 1); }}
    @keyframes cardSpinIn {{
        0%   {{ opacity: 0; transform: rotate(-215deg) scale(0.55); }}
        45%  {{ opacity: 1; }}
        100% {{ opacity: 1; transform: rotate(0deg) scale(1); }}
    }}
    @media (prefers-reduced-motion: reduce) {{
        .spin-card, .spin-card.in-view {{ opacity: 1 !important; transform: none !important; animation: none !important; }}
    }}

    .amicus-img-bg {{ z-index: -3; transform: scale(1.01); }}
    .amicus-scrim {{
        position: fixed; inset: 0; z-index: -2; pointer-events: none;
        background: radial-gradient(circle at 50% 35%, rgba(5,12,28,0.10) 0%, rgba(5,12,28,0.28) 52%, rgba(2,6,16,0.48) 100%), linear-gradient(180deg, rgba(2,6,16,0.06) 0%, rgba(2,6,16,0.20) 60%, rgba(2,6,16,0.48) 100%);
    }}
    .hero {{
        min-height: 0; width: min(980px, calc(100% - 32px)); margin: 8.5rem auto 5rem;
        padding: clamp(2rem, 5vw, 4rem); box-sizing: border-box; border-radius: 32px;
        align-items: stretch; justify-content: center; position: relative; overflow: hidden;
        background: linear-gradient(135deg, rgba(255,255,255,0.17), rgba(255,255,255,0.07) 48%, rgba(255,255,255,0.10)), rgba(12,20,38,0.28);
        border: 1px solid rgba(255,255,255,0.27);
        box-shadow: 0 42px 100px -42px rgba(0,0,0,0.78), 0 16px 38px -24px rgba(0,0,0,0.48), inset 0 1px 0 rgba(255,255,255,0.24), inset 0 -1px 0 rgba(255,255,255,0.06);
        backdrop-filter: blur(30px) saturate(150%); -webkit-backdrop-filter: blur(30px) saturate(150%);
    }}
    .hero::before {{
        content: ''; position: absolute; inset: 0; pointer-events: none;
        background: radial-gradient(circle at 12% 6%, rgba(255,255,255,0.16), transparent 28%), radial-gradient(circle at 90% 95%, rgba(138,180,255,0.10), transparent 32%);
    }}
    .hero-inner {{ position: relative; z-index: 1; flex-direction: column !important; align-items: stretch !important; gap: 2rem; }}
    .hero-copy {{ max-width: 46rem; margin: 0 auto; align-items: center; text-align: center; }}
    .hero-badge {{ background: rgba(255,255,255,0.10); border-color: rgba(255,255,255,0.20); color: rgba(255,255,255,0.92); box-shadow: inset 0 1px 0 rgba(255,255,255,0.15); }}
    .hero h1 {{ font-family: 'Fraunces', serif; font-weight: 500; font-size: clamp(3rem, 7vw, 5.7rem); line-height: 0.98; letter-spacing: -0.045em; text-wrap: balance; }}
    .hero h1 span {{ color: rgba(255,255,255,0.70) !important; }}
    .hero .lead {{ max-width: 39rem; margin-left: auto; margin-right: auto; color: rgba(255,255,255,0.78) !important; text-wrap: balance; }}
    .hero .gap-3 {{ justify-content: center; flex-wrap: wrap; }}
    .glass-cards {{ display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 12px; width: 100%; max-width: 720px; margin: 0 auto; }}
    .glass-card {{ width: auto !important; min-height: 140px; box-sizing: border-box; background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.05)); border: 1px solid rgba(255,255,255,0.19); box-shadow: inset 0 1px 0 rgba(255,255,255,0.14), 0 18px 42px -26px rgba(0,0,0,0.56); backdrop-filter: blur(22px) saturate(145%); -webkit-backdrop-filter: blur(22px) saturate(145%); }}
    .scroll-cue {{ position: relative; z-index: 1; margin-top: 0.25rem; justify-content: center; }}
    @media (max-width: 640px) {{
        .hero {{ width: min(calc(100% - 20px), 980px); margin-top: 7rem; padding: 1.5rem; border-radius: 26px; }}
        .glass-cards {{ grid-template-columns: 1fr; }}
        .glass-card {{ min-height: 0; }}
    }}
    </style>
    <script>
    (function () {{
        function bindSpinCards() {{
            var cards = document.querySelectorAll('.spin-card:not([data-spin-bound])');
            if (!cards.length) return;
            if (!('IntersectionObserver' in window)) {{
                cards.forEach(function (c) {{ c.setAttribute('data-spin-bound', '1'); c.classList.add('in-view'); }});
                return;
            }}
            var io = new IntersectionObserver(function (entries) {{
                entries.forEach(function (e) {{
                    if (e.isIntersecting) {{
                        e.target.classList.add('in-view');
                        io.unobserve(e.target);
                    }}
                }});
            }}, {{ threshold: 0.2 }});
            cards.forEach(function (c) {{ c.setAttribute('data-spin-bound', '1'); io.observe(c); }});
        }}
        document.addEventListener('DOMContentLoaded', bindSpinCards);
        setInterval(bindSpinCards, 400);

        function forcePlay() {{
            var v = document.querySelector('.amicus-video-bg');
            if (!v) return;
            v.muted = true;
            v.defaultMuted = true;
            v.setAttribute('muted', '');
            var p = v.play();
            if (p && p.catch) {{ p.catch(function () {{ }}); }}
        }}
        document.addEventListener('DOMContentLoaded', forcePlay);
        setInterval(forcePlay, 800);
        document.addEventListener('click', forcePlay, {{ once: true }});
        document.addEventListener('touchstart', forcePlay, {{ once: true }});
    }})();
    </script>
""", shared=True)
def image_bg():
    ui.html(f"""
        <img class="amicus-img-bg" src="{BG_IMAGE_URL}" alt="Background">
        <div class="amicus-scrim"></div>
    """, sanitize=False)

def navbar():
    with ui.html(f"""
        <div class="rai-nav">
            <div class="brand" onclick="window.location.href='/'">
                <img src="{icon_src}" style="width: 34px; height: 34px; border-radius: 10px; object-fit: cover; background: #101010;" />
                <div class="brand-name">Amicus</div>
            </div>
            <div class="nav-links">
                <a class="hide-sm" href="/info">Use cases</a>
                <a class="hide-sm" href="/info">FAQ</a>
                <a class="nav-cta" href="/analyze">Analyze a document</a>
            </div>
        </div>
    """, sanitize=False):
        pass

def footer():
    with ui.column().classes('w-full flex justify-center items-center'):
        ui.html("""
            <div style="width: 100%; max-width: 1120px; margin: 5rem 0 3rem 0; padding: 2.4rem 24px; border-top: 1px solid rgba(255,255,255,0.16); text-align: center; color: rgba(255, 255, 255, 0.75);">
                <i class="fa-solid fa-scale-balanced" style="color: #8AB4FF;"></i> &nbsp;<strong style="color: #ffffff;">Amicus</strong><br><br>
                <span style="color: rgba(255,255,255,0.85);">© 2026 Amicus. All rights reserved.</span><br><br>
                <em style="color: rgba(255, 255, 255, 0.6);">Disclaimer: Amicus provides informational insights and does not constitute official legal advice.</em>
            </div>
        """, sanitize=False)
@ui.page('/')
def home():
    image_bg()
    navbar()

    with ui.element('section').classes('hero'):
        with ui.element('div').classes('hero-inner'):
            with ui.column().classes('hero-copy gap-0'):
                ui.html("""
                    <div class="hero-badge">
                        <i class="fa-solid fa-globe"></i> Understand your rights in 65+ languages
                    </div>
                    <h1 style="font-family: 'Fraunces', serif; font-weight: 500; font-style: italic;">
                        Your companion<br>
                        <span style="color: #FFFFFF; font-style: normal;">in the legal world.</span>
                    </h1>
                    <p class="lead" style="color: rgba(255, 255, 255, 0.85);">
                        Amicus turns confusing legal documents into clear, plain-language
                        guidance — so language is never a barrier.
                    </p>
                """, sanitize=False)
                with ui.row().classes('gap-3 mt-8'):
                    ui.button('Go to Analysis Tool →', color=None, on_click=lambda: ui.navigate.to('/analyze')).classes('amicus-primary-btn px-7 py-3 text-base font-medium cursor-pointer')
                    ui.button('Use Cases & FAQ', color=None, on_click=lambda: ui.navigate.to('/info')).classes('amicus-ghost-btn px-7 py-3 text-base font-medium cursor-pointer')

            ui.html("""
    <div class="glass-cards">
        <div class="glass-card stat">
            <div class="num">65+</div>
            <div class="stat-body text-white">Languages supported, so guidance always reads the way you think.</div>
        </div>
        <div class="glass-card">
            <div class="t-head">
                <div class="t-badge">A</div>
                <div class="t-name">Amicus</div>
            </div>
            <p class="stat-body text-white">Untangling the fine print so you always know where you stand, what your rights are, how to take your next steps, all from the comfort of your preferred language.</p>
            <div class="t-foot">
                <div>
                    <div class="t-foot-text text-white">Your trusted legal companion</div>
                </div>
            </div>
        </div>
    </div>
""", sanitize=False)

        ui.html("""
    <div class="scroll-cue text-white" style="margin-top: 45px;"><i class="fa-solid fa-chevron-down"></i> Scroll to explore</div>
""", sanitize=False)

    with ui.column().classes('w-full items-center pb-10 gap-24 mt-24'):
        ui.html("""
                <section class="section">
                    <div class="section-head">
                        <div class="eyebrow text-white">How it works</div>
                        <h2>Clarity in three simple steps</h2>
                        <p class="text-white">No accounts, no legal jargon, no stored files — just upload and understand.</p>
                    </div>
                <div class="feature-grid">
                    <div class="feature-card spin-card">
                        <div class="feature-icon"><i class="fa-solid fa-file-arrow-up"></i></div>
                        <div class="step-index text-white">Step 01</div>
                        <h3>Upload or snap a photo</h3>
                        <p class="text-white">Drop in a PDF or take a picture of any legal document, up to 20&nbsp;MB.</p>
                    </div>
                    <div class="feature-card spin-card">
                        <div class="feature-icon"><i class="fa-solid fa-language"></i></div>
                        <div class="step-index text-white">Step 02</div>
                        <h3>Choose your language</h3>
                        <p class="text-white">Pick from 65+ languages so guidance reads the way you think.</p>
                    </div>
                    <div class="feature-card spin-card">
                        <div class="feature-icon"><i class="fa-solid fa-wand-magic-sparkles"></i></div>
                        <div class="step-index text-white">Step 03</div>
                        <h3>Read plain-language guidance</h3>
                        <p class="text-white">Get a clear summary of your rights and next steps in seconds.</p>
                    </div>
                </div>
            </section>
        """, sanitize=False).classes('w-full')

        ui.html("""
            <section class="section">
                <div class="section-head">
                    <div class="eyebrow text-white">Why Amicus</div>
                    <h2>Built for trust, privacy, and understanding</h2>
                </div>
                <div class="feature-grid">
                    <div class="feature-card spin-card">
                        <div class="feature-icon"><i class="fa-solid fa-shield-halved"></i></div>
                        <h3>Private by design</h3>
                        <p class="text-white">Bank-grade encryption and zero storage — documents are deleted right after analysis.</p>
                    </div>
                    <div class="feature-card spin-card">
                        <div class="feature-icon"><i class="fa-solid fa-scale-balanced"></i></div>
                        <h3>Plain-language first</h3>
                        <p class="text-white">Dense legal jargon becomes clear, actionable guidance anyone can follow.</p>
                    </div>
                    <div class="feature-card spin-card">
                        <div class="feature-icon"><i class="fa-solid fa-earth-americas"></i></div>
                        <h3>Truly multilingual</h3>
                        <p class="text-white">65+ languages ensure that a language barrier never stands between you and justice.</p>
                    </div>
                </div>
            </section>
        """, sanitize=False).classes('w-full')

        ui.html("""
            <section class="cta-band">
                <h2>Understand any legal document today</h2>
                <p class="text-white">Upload a file or snap a photo and get clear, plain-language guidance in your language.</p>
            </section>
        """, sanitize=False).classes('w-full')

        with ui.row().classes('w-full justify-center -mt-14'):
            ui.button('Start free analysis →', color=None, on_click=lambda: ui.navigate.to('/analyze')).classes('amicus-primary-btn px-8 py-3 text-lg font-medium cursor-pointer mt-16').style("font-weight: bold;")

        footer()

@ui.page('/analyze')
def analyze():
    image_bg()
    navbar()

    with ui.column().classes('max-w-4xl mx-auto mt-40 w-full px-4'):
        ui.button('← Back to Home', on_click=lambda: ui.navigate.to('/')).props('flat').classes('amicus-back mb-4 self-start px-5 py-2 rounded-full text-white font-medium transition-all duration-300').style('background-color: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2);')
        ui.html("""
            <div style="text-align:center; margin-bottom: 1.8rem;">
                <div class="eyebrow text-white">Analysis tool</div>
                <h2 style="font-family: 'Fraunces', serif; font-weight: 500; font-size: clamp(2rem,4vw,2.8rem); color: #ffffff; letter-spacing:-0.03em; margin:0.4rem 0 0.4rem;">Decode your document</h2>
                <p class="text-white">Ask a question, choose a language, and upload to begin.</p>
            </div>
        """, sanitize=False)
        with ui.tabs().classes('w-full justify-center') as tabs:
            tab_analyze = ui.tab('Analyze')
            tab_about = ui.tab('About us')

        with ui.tab_panels(tabs, value=tab_analyze).classes('w-full bg-transparent'):

            with ui.tab_panel(tab_analyze):
                question_input = ui.input('Ask a specific question about your document (optional)').classes('w-full mb-6').props('rounded outlined dark label-color="white" input-class="text-white" color="white"')

                with ui.card().classes('amicus-card w-full p-8'):
                    with ui.row().classes('w-full justify-between items-center mb-6'):
                        with ui.row().classes('items-center gap-4'):
                            ui.image(icon_src).classes('w-12 h-12 rounded-xl')
                            ui.label('Plain-language analysis').classes('text-2xl font-bold font-serif text-white')

                        language_select = ui.select(
                            options=["English", "Spanish (Español)", "French (Français)", "Chinese (中文)",
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
                        "Uzbek (Oʻzbekcha)", "Zulu (isiZulu)", "Afrikaans (Afrikaans)"],
                            value="English",
                            label="Language"
                        ).props('outlined label-color="white"').classes('w-48 amicus-select rounded-xl')

                    upload_container = ui.column().classes('w-full')
                    with upload_container:
                        ui.label('Upload Document (PDF) or take a Photo').classes(
                            'font-bold text-white/70 mt-4'
                        )

                        with ui.card().classes(
                            'w-full p-8 border-2 border-dashed border-white/30 rounded-2xl '
                            'bg-white/5 backdrop-blur-md flex flex-col items-center justify-center '
                            'text-center cursor-pointer hover:border-white/60 hover:bg-white/10 '
                            'transition-all group'
                        ):
                            ui.html(
                                '<div style="font-size: 2.5rem; color: #ffffff; margin-bottom: 1rem;" '
                                'class="group-hover:scale-110 transition-transform">'
                                '<i class="fa-solid fa-cloud-arrow-up"></i></div>',
                                sanitize=False
                            )

                            ui.label('Drop your legal document here').classes(
                                'text-xl font-bold text-white mb-1'
                            ).style("font-family: 'Fraunces', serif;")

                            ui.label('Supports PDF and images up to 20MB').classes(
                                'text-sm text-white/70 mb-4'
                            )

                            ui.upload(
                                on_upload=lambda e: process_file(e),
                                auto_upload=True,
                                max_file_size=20_000_000,
                            ).props(
                                'accept=".pdf, image/*" flat bordered hide-upload-btn'
                            ).classes(
                                'w-full'
                            )
                    loading_container = ui.column().classes('w-full items-center justify-center py-12').style('display: none;')
                    with loading_container:
                        ui.spinner('dots', size='4em', color='#8AB4FF')
                        ui.label('Analyzing document...').classes('text-lg font-bold text-white mt-4 font-serif')
                        ui.label('This usually takes a few seconds.').classes('text-white/60 text-sm mt-1')

                    result_container = ui.column().classes('w-full mt-2 p-2 bg-transparent').style('display: none;')
                    with result_container:
                        result_markdown = ui.markdown().classes('amicus-markdown w-full')
                        ui.button('Analyze another document', on_click=lambda: reset_ui()).props('outline rounded').classes('mt-8 amicus-ghost-btn')

                    def reset_ui():
                        result_container.style('display: none;')
                        upload_container.style('display: flex;')
                        result_markdown.set_content('')

                    async def process_file(e):
                        try:
                            upload_container.style('display: none;')
                            loading_container.style('display: flex;')

                            file_content = await e.file.read()
                            is_pdf = e.file.name.lower().endswith('.pdf')
                            file_obj = io.BytesIO(file_content)

                            if is_pdf:
                                extracted_text = await run.io_bound(extract_pdf, file_obj)
                            else:
                                extracted_text = await run.io_bound(extract_text_from_image, file_obj)

                            if extracted_text and extracted_text.strip():
                                final_result = await run.io_bound(
                                    analyze_document,
                                    extracted_text,
                                    question_input.value,
                                    language_select.value
                                )
                                result_markdown.set_content(final_result)
                            else:
                                ui.notify('No readable text found in this file.', type='negative')
                                result_markdown.set_content("❌ No readable text found.")

                        except Exception as exc:
                            error_message = str(exc)

                            if '503' in error_message and 'UNAVAILABLE' in error_message:
                                friendly_message = """
                        ### Amicus is a little busy right now

                        Our AI is experiencing unusually high demand.

                        Please wait a moment and try uploading your document again.

                        Your document was not successfully analyzed.
                        """
                                ui.notify(
                                    'Amicus is temporarily busy. Please try again in a moment.',
                                    type='warning'
                                )
                                result_markdown.set_content(friendly_message)

                            else:
                                ui.notify(
                                    'Something went wrong while analyzing your document.',
                                    type='negative'
                                )
                                result_markdown.set_content(
                                    "**We couldn't analyze your document right now.**\n\n"
                                    "Please try again in a moment."
                                )
                        finally:
                            loading_container.style('display: none;')
                            result_container.style('display: flex;')

                    ui.html("""
                        <div style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-top: 2rem; color: #ffffff; background: rgba(255,255,255,0.12); border-radius: 18px; padding: 16px 22px; font-size: 0.95rem; border: 1px solid rgba(255,255,255,0.25);">
                            <i class="fa-solid fa-shield-halved" style="color: #8AB4FF;"></i>
                            <span><b style="color:#ffffff;">Bank-grade encryption</b> · documents deleted after analysis</span>
                        </div>
                    """, sanitize=False)

            with ui.tab_panel(tab_about):
                with ui.column().classes('max-w-2xl mx-auto text-center mt-8'):
                    ui.label('Our mission').classes('eyebrow text-white')
                    ui.label('Language should never stand between you and justice.').classes('text-4xl font-bold text-white mt-2 mb-6').style("font-family: 'Fraunces', serif;")
                    ui.markdown("""
                        Navigating the American legal system can be overwhelming, especially when
                        language barriers stand in the way of justice.

                        For residents with Limited English Proficiency, a simple misunderstanding of
                        legal documents or complex political jargon can lead to unintended legal trouble
                        and compromised due process.

                        Our platform bridges this critical gap by empowering you to:
                        * **Fully understand** your rights.
                        * **Easily decode** complicated legal language.
                        * **Confidently plan** your next steps.
                    """).classes('amicus-markdown text-lg leading-relaxed text-left')

    footer()

@ui.page('/info')
def info():
    image_bg()
    navbar()

    with ui.column().classes('max-w-4xl mx-auto mt-40 w-full px-4'):
        ui.button('← Back to Home', on_click=lambda: ui.navigate.to('/')).props('flat').classes('amicus-back mb-4 self-start px-5 py-2 rounded-full text-white font-medium transition-all duration-300').style('background-color: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2);')

        ui.label('Use cases').classes('eyebrow text-white')
        ui.label('Not sure where to start?').classes('text-4xl font-bold text-white mt-2').style("font-family: 'Fraunces', serif;")
        ui.label('Upload or snap a photo of any of these to see plain-language guidance.').classes('text-lg text-white/70 mb-8')

        with ui.row().classes('w-full grid grid-cols-1 md:grid-cols-3 gap-6'):
            with ui.card().classes('feature-card rounded-2xl p-6'):
                ui.html('<div class="feature-icon"><i class="fa-solid fa-house"></i></div>', sanitize=False)
                ui.label('Lease agreements').classes('text-xl font-bold mb-2 font-serif text-white')
                ui.label('Understand your renting rights, deposit terms, and hidden fees.').classes('text-white/70')

            with ui.card().classes('feature-card rounded-2xl p-6'):
                ui.html('<div class="feature-icon"><i class="fa-solid fa-briefcase"></i></div>', sanitize=False)
                ui.label('Employment contracts').classes('text-xl font-bold mb-2 font-serif text-white')
                ui.label('Decode non-competes, termination clauses, and benefits.').classes('text-white/70')

            with ui.card().classes('feature-card rounded-2xl p-6'):
                ui.html('<div class="feature-icon"><i class="fa-solid fa-plane-departure"></i></div>', sanitize=False)
                ui.label('Immigration forms').classes('text-xl font-bold mb-2 font-serif text-white')
                ui.label('Clarify confusing government jargon and your next steps.').classes('text-white/70')

        ui.label('FAQ').classes('eyebrow mt-16')
        ui.label('Frequently asked questions').classes('text-4xl font-serif font-bold text-white mt-2').style("font-family: 'Fraunces', serif;")

        with ui.expansion('How accurate is the AI analysis?', icon='help_outline').classes('w-full amicus-glass mb-4 text-lg'):
            ui.label("Our AI is trained on vast amounts of legal data to provide accurate summaries. However, it is an informational companion, not a replacement for a certified lawyer.").classes('p-4 text-white/70')

        with ui.expansion('Do you save my legal documents?', icon='lock').classes('w-full amicus-glass mb-4 text-lg'):
            ui.label("No. Your privacy is our top priority. Documents are analyzed in real time and immediately deleted from our servers once the analysis is complete.").classes('p-4 text-white/70')

        with ui.expansion('What languages are supported?', icon='language').classes('w-full amicus-glass mb-4 text-lg'):
            ui.label("We currently support over 65 languages. Just select your preferred language from the dropdown in the Analyze tool.").classes('p-4 text-white/70')

    footer()
ui.run(title="Amicus — Understand any legal document", favicon=str(BASE_DIR / "icons" / "AmicusIcon.ico"))