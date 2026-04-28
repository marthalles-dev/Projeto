/* IA Advocacia Empresarial — Scroll Animations, UX & Mobile Menu */
(function () {
  'use strict';

  /* ── Scroll Animation via IntersectionObserver ───────────── */
  function initAnimations() {
    var SELECTORS = [
      '.elementor-widget-heading',
      '.elementor-widget-text-editor',
      '.elementor-widget-button',
      '.elementor-widget-image',
      '.elementor-widget-icon-list',
      '.elementor-widget-divider',
      '.jet-posts__inner-box',
      '.jet-listing-grid__item',
      '.jet-testimonials__item',
      '.elementor-accordion-item',
      '.elementor-widget-shortcode',
    ];

    var elements = document.querySelectorAll(SELECTORS.join(', '));
    var skip = function (el) {
      return el.closest('.elementor-location-header') ||
             el.closest('.elementor-location-footer') ||
             el.closest('[data-no-animate]');
    };

    var grouped = {};
    elements.forEach(function (el, i) {
      if (skip(el)) return;

      el.classList.add('ia-animate');

      /* stagger siblings inside the same parent column */
      var key = el.parentElement ? el.parentElement.dataset.id || i : i;
      grouped[key] = (grouped[key] || 0);
      var delay = grouped[key];
      grouped[key]++;

      if (delay === 1) el.classList.add('ia-d1');
      if (delay === 2) el.classList.add('ia-d2');
      if (delay >= 3) el.classList.add('ia-d3');
    });

    if (!('IntersectionObserver' in window)) {
      /* Fallback for very old browsers */
      document.querySelectorAll('.ia-animate').forEach(function (el) {
        el.classList.add('ia-visible');
      });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('ia-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.ia-animate').forEach(function (el) {
      io.observe(el);
    });
  }

  /* ── Header shadow on scroll ─────────────────────────────── */
  function initHeaderScroll() {
    var header = document.querySelector('.elementor-location-header');
    if (!header) return;
    var onScroll = function () {
      if (window.pageYOffset > 50) {
        header.classList.add('ia-scrolled');
      } else {
        header.classList.remove('ia-scrolled');
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── Smooth scroll for in-page anchors ───────────────────── */
  function initSmoothScroll() {
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href^="#"]');
      if (!a) return;
      var id = a.getAttribute('href');
      var target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        var offset = 80; /* header height */
        var top = target.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }
    });
  }

  /* ── Mobile hamburger menu fix ───────────────────────────── */
  function initMobileMenu() {
    document.querySelectorAll('.elementor-nav-menu__toggle').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var widget  = btn.closest('.elementor-widget-nav-menu');
        if (!widget) return;
        var dropdown = widget.querySelector('.elementor-nav-menu--dropdown');
        if (!dropdown) return;

        var isOpen = dropdown.getAttribute('aria-hidden') === 'false' ||
                     dropdown.style.display === 'block';

        dropdown.style.display = isOpen ? 'none' : 'block';
        dropdown.setAttribute('aria-hidden', isOpen ? 'true' : 'false');
        btn.setAttribute('aria-expanded', isOpen ? 'false' : 'true');
      });
    });

    /* Close on outside click */
    document.addEventListener('click', function () {
      document.querySelectorAll('.elementor-nav-menu--dropdown').forEach(function (d) {
        d.style.display = 'none';
        d.setAttribute('aria-hidden', 'true');
      });
    });
  }

  /* ── Back to top button ──────────────────────────────────── */
  function initBackToTop() {
    var btn = document.createElement('button');
    btn.id = 'ia-back-top';
    btn.setAttribute('aria-label', 'Voltar ao topo');
    btn.innerHTML = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>';
    btn.style.cssText = [
      'position:fixed',
      'bottom:100px',
      'right:24px',
      'width:44px',
      'height:44px',
      'border-radius:50%',
      'background:#1B2A4A',
      'color:#C3A84C',
      'border:2px solid #C3A84C',
      'display:flex',
      'align-items:center',
      'justify-content:center',
      'cursor:pointer',
      'opacity:0',
      'transform:translateY(12px)',
      'transition:all 0.3s ease',
      'z-index:999',
      'box-shadow:0 4px 16px rgba(27,42,74,0.25)',
    ].join(';');

    document.body.appendChild(btn);

    window.addEventListener('scroll', function () {
      if (window.pageYOffset > 400) {
        btn.style.opacity = '1';
        btn.style.transform = 'translateY(0)';
      } else {
        btn.style.opacity = '0';
        btn.style.transform = 'translateY(12px)';
      }
    }, { passive: true });

    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ── Card image lazy hover effect ────────────────────────── */
  function initCardHover() {
    document.querySelectorAll('.jet-posts__inner-box').forEach(function (card) {
      var img = card.querySelector('.post-thumbnail img');
      if (!img) return;
      card.addEventListener('mouseenter', function () {
        img.style.transform = 'scale(1.06)';
      });
      card.addEventListener('mouseleave', function () {
        img.style.transform = 'scale(1)';
      });
    });
  }

  /* ── Init ────────────────────────────────────────────────── */
  function boot() {
    initAnimations();
    initHeaderScroll();
    initSmoothScroll();
    initMobileMenu();
    initBackToTop();
    initCardHover();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    /* Delay slightly to avoid fighting with Elementor's own init */
    setTimeout(boot, 180);
  }

})();
