// Landing page carousel controls (if present)
(() => {
  const carousel = document.querySelector(".carousel");
  const nextBtn = document.querySelector(".next");
  const prevBtn = document.querySelector(".prev");
  if (!carousel || !nextBtn || !prevBtn) return;

  let scrollAmount = 0;

  nextBtn.onclick = () => {
    scrollAmount += 300;
    carousel.style.transform = `translateX(-${scrollAmount}px)`;
  };

  prevBtn.onclick = () => {
    scrollAmount -= 300;
    if (scrollAmount < 0) scrollAmount = 0;
    carousel.style.transform = `translateX(-${scrollAmount}px)`;
  };
})();
