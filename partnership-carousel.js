(() => {
  const section = document.getElementById('partnerships');
  if (!section) return;

  const toolbar = section.querySelector('.partnership-toolbar');
  const controls = toolbar.querySelector('.partner-rail-controls');
  const previous = controls.querySelector('[data-partner-prev]');
  const next = controls.querySelector('[data-partner-next]');
  const filters = toolbar.querySelector('.partner-filters');
  const buttons = [...filters.querySelectorAll('[data-partner-filter]')];
  const panels = [...section.querySelectorAll('[data-partner-panel]')];
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const resizeObserver = new ResizeObserver(updateControls);
  let track;

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
    const distance = second.offsetLeft - first.offsetLeft;
    track.scrollBy({left: direction * distance, behavior: reducedMotion.matches ? 'auto' : 'smooth'});
  }

  function showPanel(panel) {
    const selectedTrack = panel.querySelector('.partner-rail-track');
    if (track === selectedTrack) return;
    if (track) {
      track.removeEventListener('scroll', updateControls);
      resizeObserver.unobserve(track);
    }

    for (const button of buttons) {
      button.setAttribute('aria-pressed', String(button.getAttribute('aria-controls') === panel.id));
    }
    for (const item of panels) {
      item.hidden = item !== panel;
    }

    track = selectedTrack;
    previous.setAttribute('aria-controls', track.id);
    next.setAttribute('aria-controls', track.id);
    track.addEventListener('scroll', updateControls, {passive: true});
    resizeObserver.observe(track);
    updateControls();

    const selectedButton = buttons.find(button => button.getAttribute('aria-pressed') === 'true');
    if (filters.scrollWidth > filters.clientWidth) {
      const bounds = filters.getBoundingClientRect();
      const chip = selectedButton.getBoundingClientRect();
      const inset = 3;
      if (chip.left < bounds.left + inset) filters.scrollLeft += chip.left - bounds.left - inset;
      if (chip.right > bounds.right - inset) filters.scrollLeft += chip.right - bounds.right + inset;
    }
  }

  function showHashPanel() {
    const target = document.getElementById(location.hash.slice(1));
    const panel = target?.closest('[data-partner-panel]');
    if (!panels.includes(panel)) return false;
    showPanel(panel);
    requestAnimationFrame(() => target.scrollIntoView({block: 'start', inline: 'nearest', behavior: 'instant'}));
    return true;
  }

  previous.addEventListener('click', () => move(-1, previous));
  next.addEventListener('click', () => move(1, next));
  for (const button of buttons) {
    button.addEventListener('click', () => showPanel(document.getElementById(button.getAttribute('aria-controls'))));
  }
  for (const heading of section.querySelectorAll('.partner-panel-title')) {
    heading.classList.add('sr-only');
  }
  toolbar.hidden = false;
  if (!showHashPanel()) showPanel(panels[0]);
  window.addEventListener('hashchange', showHashPanel);
})();
