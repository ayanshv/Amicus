# Amicus
A civic tech web app that translates confusing legal documents into clear, 
plain-language guidance in 65+ languages, ensuring language is never a barrier 
to your safety, protection, and peace of mind.

## 🌐 Live Demo
[Click here to try it](https://amicusai.streamlit.app)

---

## 📸 Screenshots

### Home — Your Legal Companion
![Home](screenshots/screenshot_home.png)

### ⚖️ Document Upload — PDF & Camera Input
![Upload](screenshots/screenshot_upload.png)

### 🌐 Plain-Language Analysis
![Analysis](screenshots/screenshot_analysis.png)

### 🗣️ Multi-Language Analysis
![Multilingual Analysis](screenshots/screenshot_multilingual.png)

### 💡 Use Cases & FAQ
![Use Cases](screenshots/screenshot_info.png)

---

## Why I Built This
Navigating the legal system can be overwhelming, especially when language 
barriers stand in the way of justice. For residents with Limited English 
Proficiency, a simple misunderstanding of legal documents — like lease 
agreements, employment contracts, or immigration forms — can lead to 
unintended legal trouble or compromised due process.

I wanted to build a tool that bridges this gap, allowing anyone to fully 
understand their rights and confidently plan their next steps without 
needing a law degree or fluency in English. Along the way I learned more 
than I expected — how to integrate OCR, handle PDF text extraction, design 
a mobile-responsive UI in Streamlit, and securely leverage Gemini AI to 
simplify complex legal text.

---

## Tech Stack
- Python — core language
- Streamlit — interactive web app
- Gemini API — plain-language document analysis and translation
- pdfplumber — PDF text extraction
- EasyOCR & Pillow — image processing and OCR for photo uploads
- python-dotenv — environment variable management

---

## How to Run Locally
1. Clone the repo
```bash
   git clone [https://github.com/yourusername/amicus.git](https://github.com/yourusername/amicus.git)
```
2. Install dependencies
```bash
   pip install -r requirements.txt
```
3. Add your Gemini API key to a `.env` file
GEMINI_API_KEY=your_key_here
4. Run the app
```bash
   streamlit run app.py
```

---

## Project Structure
- `app.py` — Streamlit web app UI, custom CSS styling, and page routing
- `analyze.py` — structured AI prompt handling and Gemini API integration
- `pdf_reader.py` — extracts text from uploaded PDF documents
- `text_extract.py` — OCR engine for extracting text from image/camera uploads