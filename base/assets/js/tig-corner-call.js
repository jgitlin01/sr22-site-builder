(function () {
  // Read the number off the header CTA rather than hardcoding it, so this
  // widget can never drift from config.py (the template this site was built
  // from had the previous client's number baked in right here).
  var navPhone = document.querySelector('.tig-nav-phone');
  if (!navPhone) return;
  var href = navPhone.getAttribute('href') || '';
  var label = (navPhone.querySelector('span') || {}).textContent || '';
  if (!href || href.indexOf('tel:') !== 0) return;

  var a = document.createElement('a');
  a.href = href;
  a.className = 'tig-corner-call';
  a.setAttribute('aria-label', 'Call ' + label + ' for a quote');
  a.innerHTML =
    '<span class="tig-corner-call__label">Speak to us today</span>' +
    '<span class="tig-corner-call__number"><i class="fa-solid fa-phone"></i> ' +
    label + '</span>';
  document.body.appendChild(a);

  function toggle() {
    a.classList.toggle('show', window.scrollY > 420);
  }
  window.addEventListener('scroll', toggle, { passive: true });
  toggle();
})();
