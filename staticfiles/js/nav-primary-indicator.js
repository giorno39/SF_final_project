/**
 * Full-height primary nav: positions sliding highlight under .site-nav-primary links.
 */
(function () {
  const nav = document.querySelector('.site-nav-primary');
  if (!nav) return;

  const inner = nav.querySelector('.site-nav-primary-inner');
  const indicator = nav.querySelector('.site-nav-active-indicator');
  if (!inner || !indicator) return;

  const NAV_TRANSITION_MS = window.matchMedia('(prefers-reduced-motion: reduce)')
    .matches
    ? 0
    : 320;

  function activeLink() {
    return (
      nav.querySelector('.site-nav-link[aria-current="page"]') ||
      nav.querySelector('.site-nav-link.is-active') ||
      nav.querySelector('.site-nav-link')
    );
  }

  function moveTo(link, instant) {
    if (!link) return;
    const ir = inner.getBoundingClientRect();
    const lr = link.getBoundingClientRect();
    const left = lr.left - ir.left + inner.scrollLeft;
    const width = lr.width;
    if (instant) {
      indicator.style.transition = 'none';
    } else {
      indicator.style.transition = '';
    }
    indicator.style.left = `${left}px`;
    indicator.style.width = `${width}px`;
    if (instant) {
      void indicator.offsetWidth;
      requestAnimationFrame(() => {
        indicator.style.transition = '';
      });
    }
  }

  function sync(instant) {
    moveTo(activeLink(), instant);
  }

  sync(true);
  window.addEventListener('resize', () => sync(true));

  nav.querySelectorAll('a.site-nav-link').forEach((a) => {
    a.addEventListener('click', (e) => {
      if (e.defaultPrevented) return;
      if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      if (a.hasAttribute('download')) return;
      const href = a.getAttribute('href');
      if (!href || href.startsWith('#')) return;
      if (a.getAttribute('aria-current') === 'page') return;

      e.preventDefault();
      moveTo(a, false);
      window.setTimeout(() => {
        window.location.assign(a.href);
      }, NAV_TRANSITION_MS);
    });
  });
})();
