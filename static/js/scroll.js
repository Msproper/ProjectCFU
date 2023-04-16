window.onload = function() {
  if (window.location.hash) {
    window.scrollTo(0, 0);
    setTimeout(function() {
      window.scrollTo(0, parseInt(window.location.hash.slice(1)) || 0);
    }, 0);
  }
}

// Сохраняем позицию прокрутки в хэш-фрагменте URL при скролле страницы
window.addEventListener('scroll', function() {
  window.location.hash = window.scrollY;
});