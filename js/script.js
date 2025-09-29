// Scroll animation for feature cards
document.addEventListener('DOMContentLoaded', function() {
   const featureCards = document.querySelectorAll(
      '.feature-card');

   const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
         if(entry.isIntersecting) {
            entry.target.classList.add('visible');
         }
      });
   }, {
      threshold: 0.1
   });

   featureCards.forEach(card => {
      observer.observe(card);

      // Staggered animation
      const index = Array.from(featureCards).indexOf(card);
      card.style.transitionDelay = `${index * 0.1}s`;
   });

   // Smooth scroll for anchor links
   document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
         e.preventDefault();

         const targetId = this.getAttribute('href');
         const targetElement = document.querySelector(
            targetId);

         if(targetElement) {
            window.scrollTo({
               top: targetElement.offsetTop -
                  20,
               behavior: 'smooth'
            });

            // Close drawer if open
            if(sideDrawer.classList.contains('open')) {
               toggleDrawer();
            }
         }
      });
   });

   // Drawer functionality
   const menuToggle = document.getElementById('menuToggle');
   const sideDrawer = document.getElementById('sideDrawer');
   const overlay = document.getElementById('overlay');

   function toggleDrawer() {
      sideDrawer.classList.toggle('open');
      overlay.classList.toggle('open');
      document.body.style.overflow = sideDrawer.classList.contains(
         'open') ? 'hidden' : '';
   }

   menuToggle.addEventListener('click', toggleDrawer);
   overlay.addEventListener('click', toggleDrawer);

   // Screenshot slider functionality
   const slider = document.getElementById('screenshotsSlider');
   const prevBtn = document.getElementById('prevBtn');
   const nextBtn = document.getElementById('nextBtn');

   if(slider && prevBtn && nextBtn) {
      // Improved slider with proper item width calculation
      const scrollAmount = 100; // Fixed scroll amount

      prevBtn.addEventListener('click', () => {
         slider.scrollBy({
            left: -scrollAmount,
            behavior: 'smooth'
         });
      });

      nextBtn.addEventListener('click', () => {
         slider.scrollBy({
            left: scrollAmount,
            behavior: 'smooth'
         });
      });

      // Add keyboard navigation
      document.addEventListener('keydown', (e) => {
         if(e.key === 'ArrowLeft') {
            slider.scrollBy({
               left: -scrollAmount,
               behavior: 'smooth'
            });
         } else if(e.key === 'ArrowRight') {
            slider.scrollBy({
               left: scrollAmount,
               behavior: 'smooth'
            });
         }
      });
   }

   // Video modal functionality
   const videoTrigger = document.getElementById('videoTrigger');
   const videoModal = document.getElementById('videoModal');
   const closeModal = document.getElementById('closeModal');
   const youtubeVideo = document.getElementById('youtubeVideo');

   if(videoTrigger && videoModal) {
      videoTrigger.addEventListener('click', () => {
         // Set YouTube video URL (replace with your actual video ID)
         youtubeVideo.src =
            'https://www.youtube.com/embed/QAlA3VU-sTw?si=y23HVsE2jDkf7RU9';
         videoModal.classList.add('open');
         document.body.style.overflow = 'hidden';
      });

      closeModal.addEventListener('click', () => {
         videoModal.classList.remove('open');
         youtubeVideo.src = '';
         document.body.style.overflow = '';
      });

      videoModal.addEventListener('click', (e) => {
         if(e.target === videoModal) {
            videoModal.classList.remove('open');
            youtubeVideo.src = '';
            document.body.style.overflow = '';
         }
      });
   }

   // Screenshot modal functionality
   const screenshots = document.querySelectorAll('.screenshot');
   const screenshotModal = document.getElementById(
      'screenshotModal');
   const closeScreenshotModal = document.getElementById(
      'closeScreenshotModal');
   const screenshotModalImg = document.getElementById(
      'screenshotModalImg');

   screenshots.forEach(screenshot => {
      screenshot.addEventListener('click', () => {
         const imgSrc = screenshot.getAttribute(
            'data-src');
         screenshotModalImg.src = imgSrc;
         screenshotModal.classList.add('open');
         document.body.style.overflow = 'hidden';
      });
   });

   closeScreenshotModal.addEventListener('click', () => {
      screenshotModal.classList.remove('open');
      document.body.style.overflow = '';
   });

   screenshotModal.addEventListener('click', (e) => {
      if(e.target === screenshotModal) {
         screenshotModal.classList.remove('open');
         document.body.style.overflow = '';
      }
   });
});
