/* Failsafe for the entrance animations.
 *
 * script.js hides every [data-animation] element (inline opacity:0) and
 * reveals it when an IntersectionObserver fires. That is fine while you are
 * scrolling normally, but the observer can be skipped entirely when the
 * browser restores a scroll position on reload, when an anchor link jumps
 * down the page, or when a fast scroll outruns it. The result is content
 * stuck at opacity 0 with no way back except scrolling away and returning.
 *
 * On a page whose whole job is to answer questions, invisible content is a
 * correctness bug, not a cosmetic one. This reveals anything still hidden
 * after a short grace period, and again on load, so motion is a bonus rather
 * than a precondition for reading the page.
 */
(function () {
  function reveal(el) {
    el.style.opacity = '1';
    el.style.transform = 'none';
    el.style.animationPlayState = 'running';
    el.classList.add('animated');
  }

  function sweep() {
    document.querySelectorAll('[data-animation]:not(.animated)')
      .forEach(function (el) {
        var r = el.getBoundingClientRect();
        // Anything at or above the fold has had its chance; anything below
        // still gets its animation when the observer reaches it.
        if (r.top < window.innerHeight) reveal(el);
      });
  }

  // Grace period long enough for the observer to do its job normally.
  setTimeout(sweep, 1200);
  window.addEventListener('load', function () { setTimeout(sweep, 400); });

  // A restored scroll position lands after load; catch that case too.
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) setTimeout(sweep, 200);
  });

  // Last resort: nothing should stay hidden once the user has been here a
  // while, wherever they are on the page.
  setTimeout(function () {
    document.querySelectorAll('[data-animation]:not(.animated)').forEach(reveal);
  }, 6000);
})();
