// Radius Systems - Main JavaScript Application
document.addEventListener('DOMContentLoaded', () => {
  // Sticky Header Effect
  const header = document.querySelector('.site-header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });

  // Hero Slider Initialization
  const slides = document.querySelectorAll('.slide');
  const dots = document.querySelectorAll('.dot');
  const prevBtn = document.querySelector('.slider-prev');
  const nextBtn = document.querySelector('.slider-next');
  let currentSlide = 0;
  let slideInterval;

  function goToSlide(index) {
    slides.forEach(slide => slide.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));
    
    currentSlide = (index + slides.length) % slides.length;
    slides[currentSlide].classList.add('active');
    if (dots[currentSlide]) dots[currentSlide].classList.add('active');
  }

  function startAutoplay() {
    slideInterval = setInterval(() => {
      goToSlide(currentSlide + 1);
    }, 5000);
  }

  function resetAutoplay() {
    clearInterval(slideInterval);
    startAutoplay();
  }

  if (prevBtn && nextBtn) {
    prevBtn.addEventListener('click', () => {
      goToSlide(currentSlide - 1);
      resetAutoplay();
    });

    nextBtn.addEventListener('click', () => {
      goToSlide(currentSlide + 1);
      resetAutoplay();
    });
  }

  dots.forEach((dot, idx) => {
    dot.addEventListener('click', () => {
      goToSlide(idx);
      resetAutoplay();
    });
  });

  // Pause autoplay on slider hover
  const sliderContainer = document.querySelector('.slider-container');
  if (sliderContainer) {
    sliderContainer.addEventListener('mouseenter', () => clearInterval(slideInterval));
    sliderContainer.addEventListener('mouseleave', startAutoplay);
  }

  startAutoplay();

  // Product Category Filter Tabs
  const tabBtns = document.querySelectorAll('.tab-btn');
  const productCards = document.querySelectorAll('.product-card');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const category = btn.getAttribute('data-category');

      productCards.forEach(card => {
        if (category === 'all' || card.getAttribute('data-category') === category) {
          card.style.display = 'block';
          card.style.animation = 'fadeIn 0.4s ease';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });

  // Search & Mobile Menu Overlay Controls
  const searchModal = document.getElementById('searchModal');
  const searchTrigger = document.getElementById('searchTrigger');
  const searchClose = document.getElementById('searchClose');

  if (searchTrigger && searchModal) {
    searchTrigger.addEventListener('click', () => searchModal.classList.add('active'));
  }
  if (searchClose && searchModal) {
    searchClose.addEventListener('click', () => searchModal.classList.remove('active'));
  }

  // Mobile Drawer Toggle
  const mobileToggle = document.getElementById('mobileToggle');
  const mobileDrawer = document.getElementById('mobileDrawer');
  const mobileDrawerClose = document.getElementById('mobileDrawerClose');

  if (mobileToggle && mobileDrawer) {
    mobileToggle.addEventListener('click', () => mobileDrawer.classList.add('active'));
  }
  if (mobileDrawerClose && mobileDrawer) {
    mobileDrawerClose.addEventListener('click', () => mobileDrawer.classList.remove('active'));
  }

  // Business Lead & Quote Modal
  const leadModal = document.getElementById('leadModal');
  const quoteTriggers = document.querySelectorAll('.trigger-quote-modal');
  const leadClose = document.getElementById('leadClose');
  const leadForm = document.getElementById('leadForm');
  const formSuccess = document.getElementById('formSuccess');

  quoteTriggers.forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      if (leadModal) {
        leadModal.classList.add('active');
        if (formSuccess) formSuccess.style.display = 'none';
        if (leadForm) leadForm.style.display = 'block';
      }
    });
  });

  if (leadClose && leadModal) {
    leadClose.addEventListener('click', () => leadModal.classList.remove('active'));
  }

  // Close modals on clicking outside content
  window.addEventListener('click', (e) => {
    if (e.target === searchModal) searchModal.classList.remove('active');
    if (e.target === leadModal) leadModal.classList.remove('active');
  });

  // Lead Form Submission Handler
  if (leadForm) {
    leadForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const submitBtn = leadForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerText;
      submitBtn.innerText = 'Submitting...';
      submitBtn.disabled = true;

      setTimeout(() => {
        submitBtn.innerText = originalText;
        submitBtn.disabled = false;
        leadForm.style.display = 'none';
        if (formSuccess) {
          formSuccess.style.display = 'block';
        }
        leadForm.reset();
      }, 1000);
    });
  }
});
