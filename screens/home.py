from nicegui import ui, app, run

from components.background import image_bg
from components.navbar import navbar
from components.footer import footer
from components.config import icon_src

@ui.page('/')
@ui.page('/home')
def home():
    image_bg()
    navbar()

    with ui.element('section').classes('hero'):
        with ui.element('div').classes('hero-inner'):

            with ui.column().classes('hero-copy gap-0'):
                ui.html("""
                    <div class="hero-badge">
                        <i class="fa-solid fa-globe"></i>
                        Understand your rights in 65+ languages
                    </div>

                    <h1 style="
                        font-family: 'Fraunces', serif;
                        font-weight: 500;
                        font-style: italic;
                    ">
                        Your companion<br>
                        <span style="
                            color: #FFFFFF;
                            font-style: normal;
                        ">
                            in the legal world.
                        </span>
                    </h1>

                    <p class="lead" style="color: rgba(255,255,255,0.85);">
                        Amicus turns confusing legal documents into clear,
                        plain-language guidance — so language is never a barrier.
                    </p>
                """, sanitize=False)

                with ui.row().classes('gap-3 mt-8'):
                    ui.button(
                        'Go to Analysis Tool →',
                        color=None,
                        on_click=lambda: ui.navigate.to('/analyze')
                    ).classes(
                        'amicus-primary-btn px-7 py-3 text-base font-medium cursor-pointer'
                    )

                    ui.button(
                        'Explore Amicus',
                        color=None,
                        on_click=lambda: ui.run_javascript(
                            "document.getElementById('product-demo').scrollIntoView({behavior:'smooth',block:'center'})"
                        )
                    ).classes(
                        'amicus-ghost-btn px-7 py-3 text-base font-medium cursor-pointer'
                    )

            ui.html("""
                <div class="glass-cards">
                    <div class="glass-card stat">
                        <div class="num">65+</div>

                        <div class="stat-body text-white">
                            Languages supported, so guidance always reads
                            the way you think.
                        </div>
                    </div>

                    <div class="glass-card">
                        <div class="t-head">
                            <div class="t-badge">A</div>
                            <div class="t-name">Amicus</div>
                        </div>

                        <p class="stat-body text-white">
                            Untangling the fine print so you always know
                            where you stand, what your rights are, and
                            what to consider next.
                        </p>

                        <div class="t-foot">
                            <div class="t-foot-text text-white">
                                Your trusted legal companion
                            </div>
                        </div>
                    </div>
                </div>
            """, sanitize=False)

        ui.html("""
            <div class="scroll-cue text-white" style="margin-top: 45px;">
                <i class="fa-solid fa-chevron-down"></i>
                Scroll to explore
            </div>
        """, sanitize=False)

    with ui.column().classes(
        'amicus-story w-full items-center'
    ):

        ui.html("""
            <section class="product-demo section" id="product-demo">

                <div class="section-head">
                    <div class="eyebrow text-white">
                        See Amicus in action
                    </div>

                    <h2>
                        Legal clarity, without the friction.
                    </h2>

                    <p class="text-white">
                        Watch a document move from dense legal language
                        to clear, useful understanding.
                    </p>
                </div>

                <div class="demo-frame scroll-card">

                    <div class="demo-window">

                        <div class="demo-window-bar">

                            <div class="demo-dots">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>

                            <div class="demo-window-title">
                                Amicus
                            </div>

                        </div>

                        <video
                            class="amicus-demo-video"
                            src="/images/amicus_demo.mp4"
                            autoplay
                            muted
                            loop
                            playsinline
                            preload="metadata"
                        ></video>

                    </div>

                </div>

            </section>
        """, sanitize=False).classes('w-full')

        ui.html("""
            <section class="section showcase-section">

                <div class="section-head">
                    <div class="eyebrow text-white">
                        The experience
                    </div>

                    <h2>
                        Designed to make complexity feel simple.
                    </h2>

                    <p class="text-white">
                        Every part of Amicus is built around understanding,
                        not deciphering.
                    </p>
                </div>

                <div class="showcase-grid-two">

                    <article class="showcase-card showcase-card-large scroll-card">

                        <div class="showcase-image">
                            <img
                                src="/images/amicus_languages.png"
                                alt="Amicus language selection"
                            >
                        </div>

                        <div class="showcase-copy">
                            <div class="showcase-label">
                                01 — Language
                            </div>

                            <h3>
                                Understand in your language.
                            </h3>

                            <p>
                                Choose the language that feels natural to you,
                                with support across 65+ languages.
                            </p>
                        </div>

                    </article>

                    <article class="showcase-card showcase-card-large scroll-card">

                        <div class="showcase-image">
                            <img
                                src="/images/amicus_plainlanguage.png"
                                alt="Amicus plain language explanation"
                            >
                        </div>

                        <div class="showcase-copy">
                            <div class="showcase-label">
                                02 — Clarity
                            </div>

                            <h3>
                                From legal jargon to clarity.
                            </h3>

                            <p>
                                Dense terminology becomes a clear explanation
                                you can actually understand and use.
                            </p>
                        </div>

                    </article>

                </div>

            </section>
        """, sanitize=False).classes('w-full')

        ui.html("""
            <section class="section showcase-section showcase-feature">

                <div class="section-head">
                    <div class="eyebrow text-white">
                        The core experience
                    </div>

                    <h2>
                        Know where you stand.
                    </h2>

                    <p class="text-white">
                        Everything you need to understand a document,
                        gathered into one focused analysis.
                    </p>
                </div>

                <article class="showcase-card showcase-card-hero scroll-card">

                    <div class="showcase-image showcase-image-hero">
                        <img
                            src="/images/amicus_analysis.png"
                            alt="Amicus analysis interface"
                        >
                    </div>

                    <div class="showcase-copy showcase-copy-hero">

                        <div class="showcase-label">
                            03 — Analysis
                        </div>

                        <h3>
                            See what matters first.
                        </h3>

                        <p>
                            Ask questions, choose your language, and receive
                            plain-language guidance from the document in seconds.
                        </p>

                    </div>

                </article>

            </section>
        """, sanitize=False).classes('w-full')

        ui.html("""
            <section class="section showcase-section">

                <div class="section-head">
                    <div class="eyebrow text-white">
                        Built around understanding
                    </div>

                    <h2>
                        A simpler way through the paperwork.
                    </h2>

                    <p class="text-white">
                        From the first upload to the final answer,
                        every step stays focused.
                    </p>
                </div>

                <div class="showcase-grid-three">

                    <article class="showcase-card showcase-card-small scroll-card">

                        <div class="showcase-image">
                            <img
                                src="/images/amicus_upload.png"
                                alt="Amicus document upload"
                            >
                        </div>

                        <div class="showcase-copy">
                            <div class="showcase-label">
                                04 — Upload
                            </div>

                            <h3>
                                Start anywhere.
                            </h3>

                            <p>
                                Upload a PDF or capture a document directly
                                from your device.
                            </p>
                        </div>

                    </article>

                    <article class="showcase-card showcase-card-small scroll-card">

                        <div class="showcase-image">
                            <img
                                src="/images/amicus_questions.png"
                                alt="Amicus question input"
                            >
                        </div>

                        <div class="showcase-copy">
                            <div class="showcase-label">
                                05 — Questions
                            </div>

                            <h3>
                                Ask what actually matters.
                            </h3>

                            <p>
                                Point Amicus toward the part of the document
                                you need help understanding.
                            </p>
                        </div>

                    </article>

                    <article class="showcase-card showcase-card-small scroll-card">

                        <div class="showcase-image">
                            <img
                                src="/images/amicus_guidance.png"
                                alt="Amicus guidance result"
                            >
                        </div>

                        <div class="showcase-copy">
                            <div class="showcase-label">
                                06 — Guidance
                            </div>

                            <h3>
                                Know what to do next.
                            </h3>

                            <p>
                                Turn complicated language into useful,
                                plain-language guidance.
                            </p>
                        </div>

                    </article>

                </div>

            </section>
        """, sanitize=False).classes('w-full')

        ui.html("""
            <section class="section showcase-section">

                <div class="showcase-split">

                    <article class="showcase-card showcase-card-tall scroll-card">

                        <div class="showcase-image showcase-image-tall">
                            <img
                                src="/images/amicus_privacy.png"
                                alt="Amicus privacy and trust"
                            >
                        </div>

                    </article>

                    <div class="showcase-side-copy">

                        <div class="eyebrow text-white">
                            Built for real people
                        </div>

                        <h2>
                            Legal help should feel understandable.
                        </h2>

                        <div class="showcase-points">

                            <div class="showcase-point">
                                <div class="point-number">
                                    01
                                </div>

                                <div>
                                    <h3>
                                        65+ languages
                                    </h3>

                                    <p>
                                        Understand documents naturally
                                        without language becoming another barrier.
                                    </p>
                                </div>
                            </div>

                            <div class="showcase-point">
                                <div class="point-number">
                                    02
                                </div>

                                <div>
                                    <h3>
                                        Plain-language first
                                    </h3>

                                    <p>
                                        Complexity is translated into
                                        something people can actually follow.
                                    </p>
                                </div>
                            </div>

                            <div class="showcase-point">
                                <div class="point-number">
                                    03
                                </div>

                                <div>
                                    <h3>
                                        Private by design
                                    </h3>

                                    <p>
                                        Your documents should be treated
                                        with care throughout the experience.
                                    </p>
                                </div>
                            </div>

                            <div class="showcase-point">
                                <div class="point-number">
                                    04
                                </div>

                                <div>
                                    <h3>
                                        Actionable guidance
                                    </h3>

                                    <p>
                                        Focus on what matters and what
                                        to consider next.
                                    </p>
                                </div>
                            </div>

                        </div>

                    </div>

                </div>

            </section>
        """, sanitize=False).classes('w-full')

        ui.html("""
            <section class="amicus-closing">

                <div class="amicus-closing-inner">

                    <div class="amicus-closing-eyebrow">
                        AMICUS
                    </div>

                    <h2>
                        Understand what matters.<br>
                        Before you act.
                    </h2>

                    <p>
                        Clear, plain-language guidance for the documents
                        that shape your life.
                    </p>

                    <a
                        href="/analyze"
                        class="amicus-closing-btn"
                    >
                        Analyze a document
                        <span>→</span>
                    </a>

                </div>

            </section>
        """, sanitize=False).classes('w-full')

        footer()