// Lightbox for gallery images (anchors inside .tig-gallery linking to .jpg)
(function(){
  var links = Array.prototype.slice.call(document.querySelectorAll('.tig-gallery a[href$=".jpg"]'));
  if (!links.length) return;
  var overlay = document.createElement('div');
  overlay.className = 'tig-lb';
  overlay.innerHTML = '<button class="tig-lb__close" aria-label="Close">&times;</button>'+
    '<button class="tig-lb__nav tig-lb__prev" aria-label="Previous"><i class="fa-solid fa-chevron-left"></i></button>'+
    '<figure class="tig-lb__figure"><img alt=""><figcaption></figcaption></figure>'+
    '<button class="tig-lb__nav tig-lb__next" aria-label="Next"><i class="fa-solid fa-chevron-right"></i></button>';
  document.body.appendChild(overlay);
  var imgEl = overlay.querySelector('img'), capEl = overlay.querySelector('figcaption'), idx = 0;

  function show(i){
    idx = (i + links.length) % links.length;
    var a = links[idx];
    imgEl.src = a.getAttribute('href');
    var cap = a.querySelector('span');
    capEl.textContent = cap ? cap.textContent : (a.querySelector('img') ? a.querySelector('img').alt : '');
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function close(){
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }
  links.forEach(function(a, i){
    a.removeAttribute('target');
    a.addEventListener('click', function(e){ e.preventDefault(); show(i); });
  });
  overlay.querySelector('.tig-lb__close').addEventListener('click', close);
  overlay.querySelector('.tig-lb__prev').addEventListener('click', function(){ show(idx-1); });
  overlay.querySelector('.tig-lb__next').addEventListener('click', function(){ show(idx+1); });
  overlay.addEventListener('click', function(e){ if (e.target === overlay) close(); });
  document.addEventListener('keydown', function(e){
    if (!overlay.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(idx-1);
    if (e.key === 'ArrowRight') show(idx+1);
  });
})();
