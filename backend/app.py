import sys
from pathlib import Path
import base64
import io
from nicegui import ui, app

# ==========================================
# 1. BACKEND SETUP
# ==========================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from backend.pdf_reader import extract_pdf
    from backend.analyze import analyze_document
    from backend.text_extract import extract_text_from_image
    _BACKEND_AVAILABLE = True
except Exception as exc:
    _BACKEND_AVAILABLE = False
    
    def extract_pdf(_file):
        return "Mock PDF text extracted."

    def analyze_document(_info, _question, _language):
        return f"**Mock Analysis:** Here is the analysis in {_language} answering: '{_question}' based on the document."

    def extract_text_from_image(_image):
        return "Mock Image text extracted."

# ==========================================
# 2. ASSETS & GLOBAL STYLES
# ==========================================
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return "" # Fallback if icon missing

BASE_DIR = PROJECT_ROOT
icon_base64 = get_base64_image(BASE_DIR / "icons" / "AmicusIcon.png")
icon_src = f"data:image/png;base64,{icon_base64}" if icon_base64 else ""

# We inject your custom CSS globally. (We removed Streamlit-specific overrides)
ui.add_head_html(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,700;0,9..144,900;1,9..144,700;1,9..144,900&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

    body {{
        background-color: #FCFAF5;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #0F1D38;
        margin: 0;
    }}
    
    /* --- HERO CARD (Keep your existing hero styles here) --- */
    .hero {{
        position: relative; 
        margin: 6rem auto 2.6rem; 
        padding: 3.4rem 2rem 2.8rem;  
        border-radius: 38px; 
        text-align: center; 
        overflow: hidden;
        background: linear-gradient(155deg, rgba(255, 255, 255, 0.65), rgba(255, 255, 255, 0.3));
        backdrop-filter: blur(40px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.7);
        max-width: 900px; 
    }}

    .amicus-content h1, .amicus-content h2, .amicus-content h3 {{
        font-family: 'Fraunces', serif !important;
        color: #041428 !important; /* Slightly darker navy for high contrast */
        font-weight: 900 !important; /* Maximum thickness */
        font-size: 2.8rem !important; /* Large, impactful size */
        margin-top: 1.5em !important;
        margin-bottom: 0.6em !important;
        line-height: 1.1 !important;
        letter-spacing: -0.03em !important; /* Tighter letter spacing like the image */
    }}
    
    .amicus-content p, .amicus-content li {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #3E4F6D !important;
        line-height: 1.6 !important;
        font-size: 1.15rem !important; /* Slightly larger for easier reading */
        margin-bottom: 1.2em !important;
    }}
    
    .amicus-content ul {{
        list-style-type: disc !important;
        padding-left: 1.5em !important;
        margin-bottom: 1.5em !important;
    }}
    
    .amicus-content strong, .amicus-content b {{
        color: #0F1D38 !important;
        font-weight: 700 !important;
    }}
    </style>
    </style>
""", shared=True)

# ==========================================
# 3. REUSABLE COMPONENTS
# ==========================================
def navbar():
    with ui.html(f"""
        <div class="rai-nav" onclick="window.location.href='/'">
            <div style="display: flex; align-items: center; gap: 12px;">
                <img src="{icon_src}" style="width: 38px; height: 38px; border-radius: 12px; object-fit: cover; background: #16305C;" />
                <div style="font-family: 'Fraunces', serif; font-weight: 700; font-size: 1.3rem;">Amicus</div>
            </div>
        </div>
    """,sanitize=False):
        pass

def footer():
    ui.html("""
        <div class="site-footer">
            © 2026 Amicus. All rights reserved.<br>
            <i>Disclaimer: Amicus provides informational insights and does not constitute official legal advice.</i>
        </div>
    """,sanitize=False)

# ==========================================
# 4. PAGES
# ==========================================
@ui.page('/')
def home():
    navbar()
    
    # Wrap everything in a perfectly centered column
    with ui.column().classes('w-full items-center justify-center min-h-screen pt-20'):
        
        # Hero Section
        ui.html("""
            <section class="hero" style="margin: 0 auto; display: flex; flex-direction: column; align-items: center;">
                <div style="display: inline-flex; align-items: center; gap: 9px; padding: 8px 18px; border-radius: 999px; background: rgba(255,255,255,0.8); border: 1px solid white; font-weight: 700; font-size: 0.84rem; margin-bottom: 1.7rem;">
                    <i class="fa-solid fa-globe" style="color:#16305C;"></i> Understand your rights in 65+ languages
                </div>
                <h1 style="font-family: 'Fraunces', serif; font-size: clamp(2.6rem, 6vw, 4.3rem); margin: 0 0 1.1rem; color: #0F1D38; font-weight:700; line-height: 1.02; text-align: center;">
                    Your companion<br>
                    <span style="font-style: italic; background: linear-gradient(120deg, #2C508D, #16305C); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">in the legal world.</span>
                </h1>
                <p style="color: #3E4F6D; font-size: 1.16rem; max-width: 660px; margin: 0 auto 2rem; line-height: 1.62; text-align: center;">
                    Amicus turns confusing legal documents into clear, plain-language guidance — so language is never a barrier.
                </p>
                <div style="display: flex; gap: 14px; justify-content: center; flex-wrap: wrap;">
                    <div style="padding: 15px 26px; border-radius: 20px; background: rgba(255,255,255,0.8); border: 1px solid white; box-shadow: 0 20px 44px -30px rgba(0,0,0,0.8);">
                        <div style="font-family: 'Fraunces', serif; font-size: 1.6rem; font-weight: 700; color: #0F1D38;">65+</div>
                        <div style="font-size: 0.8rem; color: #8290A6; font-weight: 600; text-transform: uppercase;">Languages</div>
                    </div>
                    <div style="padding: 15px 26px; border-radius: 20px; background: rgba(255,255,255,0.8); border: 1px solid white; box-shadow: 0 20px 44px -30px rgba(0,0,0,0.8);">
                        <div style="font-family: 'Fraunces', serif; font-size: 1.6rem; font-weight: 700; color: #0F1D38;">20 MB</div>
                        <div style="font-size: 0.8rem; color: #8290A6; font-weight: 600; text-transform: uppercase;">PDF or photo</div>
                    </div>
                    <div style="padding: 15px 26px; border-radius: 20px; background: rgba(255,255,255,0.8); border: 1px solid white; box-shadow: 0 20px 44px -30px rgba(0,0,0,0.8);">
                        <div style="font-family: 'Fraunces', serif; font-size: 1.6rem; font-weight: 700; color: #0F1D38;">0</div>
                        <div style="font-size: 0.8rem; color: #8290A6; font-weight: 600; text-transform: uppercase;">Files stored</div>
                    </div>
                </div>
            </section>
        """, sanitize=False).classes('w-full flex justify-center')
        
        # Buttons
        with ui.row().classes('w-full justify-center gap-6 mt-8 max-w-3xl'):
            ui.button('Go to Analysis Tool →', color=None,  on_click=lambda: ui.navigate.to('/analyze')).classes('rounded-full bg-[#04508a] text-white px-8 py-3 text-lg font-bold shadow-xl hover:scale-105 transition-transform cursor-pointer')

            
            # The issue here was Quasar swallowing the text color. We use `style()` to force it.
            ui.button('Use Cases & FAQ', on_click=lambda: ui.navigate.to('/info')).classes('rounded-full bg-white border border-[#16305C] px-8 py-3 text-lg font-bold shadow-lg hover:scale-105 transition-transform cursor-pointer').style('color: #16305C !important;')
            
        footer()


@ui.page('/analyze')
def analyze():
    navbar()
    
    with ui.column().classes('max-w-4xl mx-auto mt-28 w-full px-4'):
        ui.button('← Back to Home', on_click=lambda: ui.navigate.to('/')).props('flat').classes('text-[#3E4F6D] mb-4')
        
        with ui.tabs().classes('w-full') as tabs:
            tab_analyze = ui.tab('Analyze')
            tab_about = ui.tab('About us')
            
        with ui.tab_panels(tabs, value=tab_analyze).classes('w-full bg-transparent'):
            
            # --- ANALYZE TAB ---
            # --- ANALYZE TAB ---
            with ui.tab_panel(tab_analyze):
                
                question_input = ui.input('Ask a specific question about your document (optional)').classes('w-full bg-white rounded-full px-4 py-2 mb-6 shadow-md').props('rounded outlined')
                
                with ui.card().classes('w-full rounded-3xl p-8 bg-white/60 backdrop-blur-md shadow-xl border border-white/80'):
                    
                    with ui.row().classes('w-full justify-between items-center mb-6'):
                        with ui.row().classes('items-center gap-4'):
                            ui.image(icon_src).classes('w-12 h-12 rounded-xl')
                            ui.label('Plain-language analysis').classes('text-2xl font-bold font-serif text-[#0F1D38]')
                        
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
                        "Uzbek (Oʻzbekcha)", "Zulu (isiZulu)", "Afrikaans (Afrikaans)",],
                            value="English",
                            label="Language"
                        ).classes('w-48 bg-white rounded-xl shadow-sm')

                    # 1. The Upload Container
                    upload_container = ui.column().classes('w-full')
                    with upload_container:
                        ui.label('Upload Document (PDF) or take a Photo').classes('font-bold text-[#3E4F6D] mt-4')
                        ui.upload(
                            on_upload=lambda e: process_file(e),
                            auto_upload=True,
                            max_file_size=20_000_000, 
                        ).props('accept=".pdf, image/*" flat bordered color="white" text-color="black"').classes('w-full border-2 border-dashed border-gray-300 rounded-xl bg-gray-50/50 hover:border-[#16305C] transition-colors')

                    # 2. The Loading Container (Hidden by default)
                    loading_container = ui.column().classes('w-full items-center justify-center py-12').style('display: none;')
                    with loading_container:
                        ui.spinner('dots', size='4em', color='#16305C')
                        ui.label('Analyzing document...').classes('text-lg font-bold text-[#16305C] mt-4 font-serif')
                        ui.label('This usually takes a few seconds.').classes('text-[#3E4F6D] text-sm mt-1')

                    # 3. The Result Container (Hidden by default)
                    result_container = ui.column().classes('w-full mt-2 p-2 bg-transparent').style('display: none;')
                    with result_container:
                        # Notice we attach the 'amicus-markdown' class here so our CSS styles it!
                        result_markdown = ui.markdown().classes('amicus-markdown w-full')
                        ui.button('Analyze another document', on_click=lambda: reset_ui()).props('outline rounded').classes('mt-8 text-[#16305C]')
                    
                    # Function to reset the UI back to the upload state
                    def reset_ui():
                        result_container.style('display: none;')
                        upload_container.style('display: flex;')
                        result_markdown.set_content('')

                    # The processing logic
                    async def process_file(e):
                        try:
                            # Hide uploader, show loading spinner
                            upload_container.style('display: none;')
                            loading_container.style('display: flex;')
                            
                            file_content = await e.file.read()
                            is_pdf = e.file.name.lower().endswith('.pdf')
                            
                            file_obj = io.BytesIO(file_content)
                            
                            if is_pdf:
                                extracted_text = extract_pdf(file_obj)
                            else:
                                extracted_text = extract_text_from_image(file_obj)
                                
                            if extracted_text and extracted_text.strip():
                                final_result = analyze_document(extracted_text, question_input.value, language_select.value)
                                result_markdown.set_content(final_result)
                            else:
                                ui.notify('No readable text found in this file.', type='negative')
                                result_markdown.set_content("❌ No readable text found.")
                                
                        except Exception as exc:
                            ui.notify(f"Analysis failed: {str(exc)}", type='negative')
                            result_markdown.set_content(f"**Error:** {str(exc)}")
                        finally:
                            # Hide loading spinner, show results
                            loading_container.style('display: none;')
                            result_container.style('display: flex;')

                    # Trust Pill
                    ui.html("""
                        <div style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-top: 2rem; color: #3E4F6D; background: rgba(255,255,255,0.5); border-radius: 18px; padding: 16px 22px; font-size: 0.95rem; border: 1px solid white;">
                            <i class="fa-solid fa-shield-halved" style="color: #16305C;"></i>
                            <span><b>Bank-grade encryption</b> · documents deleted after analysis</span>
                        </div>
                    """, sanitize=False)

            # --- ABOUT TAB ---
            with ui.tab_panel(tab_about):
                with ui.column().classes('max-w-2xl mx-auto text-center mt-8'):
                    ui.label('Our mission').classes('text-sm font-bold text-[#16305C] uppercase tracking-widest')
                    ui.label('Language should never stand between you and justice.').classes('text-4xl font-serif font-bold text-[#0F1D38] mt-2 mb-6')
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
                    """).classes('text-lg text-[#3E4F6D] leading-relaxed text-left')

    footer()

@ui.page('/info')
def info():
    navbar()
    
    with ui.column().classes('max-w-4xl mx-auto mt-28 w-full px-4'):
        ui.button('← Back to Home', on_click=lambda: ui.navigate.to('/')).props('flat').classes('text-[#3E4F6D] mb-4 self-start ml-4 md:ml-0')
        
        # Use Cases Section
        ui.label('Use cases').classes('text-sm font-bold text-[#16305C] uppercase tracking-widest')
        ui.label('Not sure where to start?').classes('text-4xl font-serif font-bold text-[#0F1D38] mt-2')
        ui.label('Upload or snap a photo of any of these to see plain-language guidance.').classes('text-lg text-[#3E4F6D] mb-8')
        
        with ui.row().classes('w-full grid grid-cols-1 md:grid-cols-3 gap-6'):
            # Card 1
            with ui.card().classes('rounded-2xl p-6 bg-white shadow-lg border border-gray-100'):
                ui.icon('home', size='2rem', color='#16305C').classes('mb-4')
                ui.label('Lease agreements').classes('text-xl font'
                '-bold mb-2')
                ui.label('Understand your renting rights, deposit terms, and hidden fees.').classes('text-[#3E4F6D]')
            
            # Card 2
            with ui.card().classes('rounded-2xl p-6 bg-white shadow-lg border border-gray-100'):
                ui.icon('work', size='2rem', color='#16305C').classes('mb-4')
                ui.label('Employment contracts').classes('text-xl font-bold mb-2')
                ui.label('Decode non-competes, termination clauses, and benefits.').classes('text-[#3E4F6D]')
                
            # Card 3
            with ui.card().classes('rounded-2xl p-6 bg-white shadow-lg border border-gray-100'):
                ui.icon('flight_takeoff', size='2rem', color='#16305C').classes('mb-4')
                ui.label('Immigration forms').classes('text-xl font-bold mb-2')
                ui.label('Clarify confusing government jargon and your next steps.').classes('text-[#3E4F6D]')
                
        # FAQ Section
        ui.label('FAQ').classes('text-sm font-bold text-[#16305C] uppercase tracking-widest mt-16')
        ui.label('Frequently asked questions').classes('text-4xl font-serif font-bold text-[#0F1D38] mt-2 mb-8')
        
        with ui.expansion('How accurate is the AI analysis?', icon='help_outline').classes('w-full bg-white rounded-xl shadow-sm mb-4 text-lg'):
            ui.label("Our AI is trained on vast amounts of legal data to provide accurate summaries. However, it is an informational companion, not a replacement for a certified lawyer.").classes('p-4 text-[#3E4F6D]')
            
        with ui.expansion('Do you save my legal documents?', icon='lock').classes('w-full bg-white rounded-xl shadow-sm mb-4 text-lg'):
            ui.label("No. Your privacy is our top priority. Documents are analyzed in real time and immediately deleted from our servers once the analysis is complete.").classes('p-4 text-[#3E4F6D]')
            
        with ui.expansion('What languages are supported?', icon='language').classes('w-full bg-white rounded-xl shadow-sm mb-4 text-lg'):
            ui.label("We currently support over 65 languages. Just select your preferred language from the dropdown in the Analyze tool.").classes('p-4 text-[#3E4F6D]')

    footer()

# ==========================================
# 5. APP EXECUTION
# ==========================================
# This starts the local server. By default, it will be on port 8080.
ui.run(title="Amicus — Understand any legal document", favicon="⚖️")