/* ============================================================
   Slow Burn Finance — Minimal JS
   Scroll animations + nav scroll effect
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
    // --- Scroll-triggered fade-in animations ---
    const sections = document.querySelectorAll(
        '.about, .latest-posts, .signup, .blog-listing, .post-body'
    );
    sections.forEach(el => el.classList.add('fade-in'));

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1 }
    );

    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

    // --- Nav background on scroll ---
    const nav = document.getElementById('main-nav');
    if (nav) {
        window.addEventListener('scroll', () => {
            nav.style.borderBottomColor = window.scrollY > 40
                ? 'rgba(232, 168, 76, 0.12)'
                : 'rgba(255, 255, 255, 0.06)';
        }, { passive: true });
    }
});
