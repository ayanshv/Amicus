import sys
from pathlib import Path

from nicegui import ui, app


ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


app.add_static_files(
    '/images',
    str(ROOT_DIR / 'assets')
)

app.add_static_files(
    '/icons',
    str(ROOT_DIR / 'icons')
)

app.add_static_files(
    '/styles',
    str(ROOT_DIR / 'styles')
)


ui.add_head_html("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link
        rel="preconnect"
        href="https://fonts.gstatic.com"
        crossorigin
    >
    <link
        rel="stylesheet"
        href="/styles/styles.css"
    >
""", shared=True)


ui.add_head_html("""
    <script>
    (function () {

        function clamp(value, min, max) {
            return Math.min(Math.max(value, min), max);
        }

        function easeOut(value) {
            return 1 - Math.pow(1 - value, 3);
        }

        function updateScrollCards() {

            const cards = document.querySelectorAll('.scroll-card');

            if (!cards.length) {
                return;
            }

            const viewportHeight = window.innerHeight;
            const focusPoint = viewportHeight * 0.58;

            cards.forEach((card) => {

                const rect = card.getBoundingClientRect();

                const cardCenter =
                    rect.top + rect.height / 2;

                const distance =
                    (cardCenter - focusPoint) /
                    (viewportHeight * 0.65);

                const normalized =
                    clamp(distance, -1, 1);

                const magnitude =
                    Math.abs(normalized);

                const eased =
                    easeOut(magnitude);

                const floatAmount =
                    Math.sin(eased * Math.PI) * -14;

                const scale =
                    1 - (eased * 0.025);

                card.style.setProperty(
                    '--scroll-y',
                    `${floatAmount.toFixed(2)}px`
                );

                card.style.setProperty(
                    '--scroll-scale',
                    scale.toFixed(4)
                );

                card.style.opacity =
                    (1 - eased * 0.08).toFixed(3);
            });
        }

        let scrollFramePending = false;

        function requestScrollUpdate() {

            if (scrollFramePending) {
                return;
            }

            scrollFramePending = true;

            requestAnimationFrame(() => {
                updateScrollCards();
                scrollFramePending = false;
            });
        }

        function bindScrollEffects() {

            updateScrollCards();

            window.addEventListener(
                'scroll',
                requestScrollUpdate,
                { passive: true }
            );

            window.addEventListener(
                'resize',
                requestScrollUpdate
            );
        }

        if (document.readyState === 'loading') {

            document.addEventListener(
                'DOMContentLoaded',
                bindScrollEffects
            );

        } else {

            bindScrollEffects();

        }

    })();
    </script>
""", shared=True)


from screens.home import home
from screens.analysis import analyze
from screens.info import info


ui.run(
    title="Amicus — Understand any legal document",
    favicon="/icons/AmicusIcon.ico"
)