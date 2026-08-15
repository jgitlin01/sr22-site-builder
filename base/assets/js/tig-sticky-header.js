(function(){
  var header = document.querySelector('header');
  if (!header) return;

  function setHeight(){
    document.documentElement.style.setProperty('--tig-header-h', header.offsetHeight + 'px');
  }
  setHeight();
  window.addEventListener('resize', setHeight);

  function onScroll(){
    header.classList.toggle('tig-scrolled', window.scrollY > 40);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
