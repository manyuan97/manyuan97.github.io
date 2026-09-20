(() => {
  const controls = document.querySelector('.publication-filters');
  const publications = [...document.querySelectorAll('.publication')];
  const list = document.querySelector('.publication-list');
  const buttons = [...controls.querySelectorAll('button')];
  const status = document.querySelector('#publication-status');

  function filterPublications(filter) {
    let count = 0;
    for (const paper of publications) {
      const visible = filter === 'all'
        || (filter === 'earlier' && Number(paper.dataset.year) < 2025)
        || paper.dataset.year === filter;
      paper.hidden = !visible;
      if (visible) count++;
    }
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === filter)));
    status.textContent = `${count} publications shown.`;
  }

  controls.hidden = false;
  filterPublications('all');
  buttons.forEach(button => button.addEventListener('click', () => filterPublications(button.dataset.filter)));


  // Preserve direct links to individual papers, including those outside the selection.
  function revealLinkedPaper() {
    let id;
    try { id = decodeURIComponent(window.location.hash.slice(1)); } catch { return; }
    const paper = document.getElementById(id);
    if (paper?.classList.contains('publication')) {
      filterPublications('all');
      paper.scrollIntoView();
    }
  }
  revealLinkedPaper();
  window.addEventListener('hashchange', revealLinkedPaper);

})();
