(function(){
  var btn = document.createElement('button');
  btn.className = 'tig-scrolltop';
  btn.setAttribute('aria-label', 'Scroll to top');
  btn.innerHTML = '<i class="fa-solid fa-arrow-up"></i>';
  document.body.appendChild(btn);

  function toggle(){
    if (window.scrollY > 420) btn.classList.add('show');
    else btn.classList.remove('show');
  }
  window.addEventListener('scroll', toggle, { passive: true });
  toggle();

  btn.addEventListener('click', function(){
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();
