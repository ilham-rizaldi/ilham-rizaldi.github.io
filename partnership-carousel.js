(() => {
  const section = document.getElementById('partnerships');
  if (!section) return;

  const rails = new Map();
  const resizeObserver = new ResizeObserver(entries => {
    for (const entry of entries) rails.get(entry.target)?.();
  });
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  for (const rail of section.querySelectorAll('.partner-rail')) {
    const track = rail.querySelector('.partner-rail-track');
    const controls = rail.querySelector('.partner-rail-controls');
    const previous = controls.querySelector('[data-partner-prev]');
    const next = controls.querySelector('[data-partner-next]');

    function updateControls() {
      const maxScroll = track.scrollWidth - track.clientWidth;
      controls.hidden = maxScroll <= 2;
      previous.setAttribute('aria-disabled', String(track.scrollLeft <= 2));
      next.setAttribute('aria-disabled', String(track.scrollLeft >= maxScroll - 2));
    }

    function move(direction, button) {
      if (button.getAttribute('aria-disabled') === 'true') return;
      const [first, second] = track.children;
      if (!second) return;
      const step = second.offsetLeft - first.offsetLeft;
      track.scrollBy({left: direction * step, behavior: reducedMotion.matches ? 'auto' : 'smooth'});
    }

    previous.addEventListener('click', () => move(-1, previous));
    next.addEventListener('click', () => move(1, next));
    track.addEventListener('scroll', updateControls, {passive: true});
    rails.set(track, updateControls);
    resizeObserver.observe(track);
    updateControls();
  }

  const filters = section.querySelector('.partner-filters');
  const buttons = [...filters.querySelectorAll('[data-partner-filter]')];
  const panels = [...section.querySelectorAll('[data-partner-panel]')];

  function showPanel(id) {
    for (const button of buttons) {
      button.setAttribute('aria-pressed', String(button.getAttribute('aria-controls') === id));
    }
    for (const panel of panels) {
      panel.hidden = panel.id !== id;
    }
  }

  function showHashPanel() {
    const target = document.getElementById(location.hash.slice(1));
    const panel = target?.closest('[data-partner-panel]');
    if (!panels.includes(panel)) return false;
    showPanel(panel.id);
    requestAnimationFrame(() => target.scrollIntoView({block: 'start', inline: 'nearest', behavior: 'instant'}));
    return true;
  }

  for (const button of buttons) {
    button.addEventListener('click', () => showPanel(button.getAttribute('aria-controls')));
  }
  filters.hidden = false;
  if (!showHashPanel()) showPanel(panels[0].id);
  window.addEventListener('hashchange', showHashPanel);
})();
