window.initPortfolioReader = function initPortfolioReader() {
  const dialog = document.getElementById('portfolio-reader');
  if (!dialog || typeof dialog.showModal !== 'function') return false;

  const recordSelector = 'details.case, details.program-story, details.strategy-case, #project-archive, #portfolio-context';
  const title = dialog.querySelector('#reader-title');
  const category = dialog.querySelector('.portfolio-reader-category');
  const scroller = dialog.querySelector('.portfolio-reader-scroll');
  const brief = dialog.querySelector('.portfolio-reader-brief');
  const evidence = dialog.querySelector('.portfolio-reader-evidence');
  const evidenceDisclosure = evidence.querySelector('details');
  const source = evidence.querySelector('.portfolio-reader-source');
  const role = brief.querySelector('[data-brief-role]');
  const resultLabel = brief.querySelector('[data-brief-result-label]');
  const result = brief.querySelector('[data-brief-result]');
  const strategy = brief.querySelector('[data-brief-strategy]');
  const execution = brief.querySelector('[data-brief-execution]');
  const closeButton = dialog.querySelector('[data-reader-close]');
  const backButton = dialog.querySelector('[data-reader-back]');
  const archive = document.getElementById('project-archive');
  const records = new Map();
  const labels = [
    ['.case', 'Case study'], ['.program-story', 'Product program'],
    ['.strategy-case', 'Strategy & research'], ['#project-archive', 'Project archive'],
    ['#portfolio-context', 'Career figures']
  ];

  for (const item of document.querySelectorAll(recordSelector)) {
    const summary = item.querySelector(':scope > summary');
    const content = item.querySelector(':scope > .case-body, :scope > .program-body, :scope > .strategy-body, :scope > .archive-body, :scope > .portfolio-context-body');
    const label = summary?.querySelector('h3,h4,strong');
    if (!summary || !content || !label) continue;
    const type = labels.find(([selector]) => item.matches(selector))[1];
    records.set(item, {item, summary, content, type, title: label.textContent.trim()});
    summary.setAttribute('aria-haspopup', 'dialog');
    summary.setAttribute('aria-controls', dialog.id);
    const marker = summary.querySelector('.program-expand span,.strategy-expand span');
    if (marker) marker.textContent = '↗';
    summary.addEventListener('click', event => {
      event.preventDefault();
      navigate(item, summary);
    });
  }
  document.documentElement.classList.add('has-portfolio-reader');

  let current = null;
  let opener = null;
  let closing = false;
  let visibleDepth = 0;
  const readingPositions = new Map();

  function depth() {
    return history.state?.portfolioReaderDepth || 0;
  }

  function recordFor(target) {
    return records.get(target?.closest(recordSelector)) ||
      (current?.content.contains(target) ? current : null);
  }

  function fromHash(hash) {
    if (!hash) return null;
    try { return document.getElementById(decodeURIComponent(hash.slice(1))); }
    catch { return null; }
  }

  function restoreContent() {
    if (!current) return;
    current.item.append(current.content);
    current = null;
  }

  function dismiss(restoreFocus = true) {
    restoreContent();
    if (dialog.open) dialog.close();
    if (restoreFocus && opener?.isConnected) opener.focus({preventScroll: true});
    opener = null;
    readingPositions.clear();
  }

  function render(target, trigger, restorePosition = false) {
    const record = recordFor(target);
    if (!record) return;
    if (!dialog.open) {
      const archiveSummary = archive.querySelector(':scope > summary');
      opener = trigger || (archive.contains(record.item) && record.item !== archive ? archiveSummary : record.summary);
    }
    if (current && current !== record) {
      current.item.append(current.content);
      current = null;
    }
    current = record;
    const summary = window.portfolioBriefs?.[record.item.id];
    brief.hidden = evidence.hidden = !summary;
    evidenceDisclosure.open = false;
    if (summary) {
      const [roleText, resultText, strategyText, executionText, label = 'Result'] = summary;
      role.textContent = roleText;
      resultLabel.textContent = label;
      result.textContent = resultText;
      strategy.textContent = strategyText;
      execution.textContent = executionText;
      source.append(record.content);
    } else {
      scroller.append(record.content);
    }
    category.textContent = record.type;
    title.textContent = record.title;
    backButton.hidden = !history.state?.portfolioReaderHasParent;
    if (!dialog.open) dialog.showModal();
    closeButton.focus({preventScroll: true});
    scroller.scrollTop = 0;

    const position = restorePosition ? readingPositions.get(depth()) : null;
    if (position) {
      evidenceDisclosure.open = position.evidenceOpen;
      scroller.scrollTop = position.top;
    } else if (target !== record.item && record.content.contains(target)) {
      if (summary) evidenceDisclosure.open = true;
      for (let node = target.parentElement; node && node !== scroller; node = node.parentElement) {
        if (node.tagName === 'DETAILS') node.open = true;
      }
      const top = target.getBoundingClientRect().top - scroller.getBoundingClientRect().top;
      scroller.scrollTop += top - 18;
    }
    visibleDepth = depth();
  }

  function rememberPosition() {
    if (current) readingPositions.set(visibleDepth, {
      top: scroller.scrollTop,
      evidenceOpen: evidenceDisclosure.open
    });
  }

  function navigate(target, trigger) {
    rememberPosition();
    if (location.hash !== '#' + target.id || !dialog.open) {
      history.pushState({...history.state, portfolioReaderDepth: depth() + 1, portfolioReaderHasParent: Boolean(current)}, '', '#' + target.id);
    }
    render(target, trigger);
  }

  function removeReadingHash() {
    const url = new URL(location.href);
    url.hash = '';
    const state = {...history.state};
    delete state.portfolioReaderDepth;
    delete state.portfolioReaderHasParent;
    history.replaceState(state, '', url);
  }

  function requestClose() {
    const count = depth();
    if (count) {
      closing = true;
      history.go(-count);
    } else {
      removeReadingHash();
      dismiss();
    }
  }

  function syncLocation() {
    const target = fromHash(location.hash);
    rememberPosition();
    if (closing) {
      closing = false;
      if (recordFor(target)) removeReadingHash();
      dismiss();
    } else if (recordFor(target)) {
      render(target, null, true);
    } else if (dialog.open) {
      dismiss();
    }
  }

  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (!link || event.defaultPrevented || event.button !== 0 ||
      event.metaKey || event.ctrlKey || event.shiftKey || event.altKey ||
      (link.target && link.target !== '_self')) return;
    const target = fromHash(link.hash);
    if (recordFor(target)) {
      event.preventDefault();
      navigate(target, link);
    } else if (dialog.open && dialog.contains(link) && target) {
      dismiss(false);
    }
  });
  closeButton.addEventListener('click', requestClose);
  backButton.addEventListener('click', () => history.back());
  dialog.addEventListener('cancel', event => {
    event.preventDefault();
    requestClose();
  });
  window.addEventListener('hashchange', syncLocation);
  requestAnimationFrame(syncLocation);
  return true;
};
