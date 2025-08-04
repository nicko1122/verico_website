class Carousel {
  constructor(element) {
    this.element = element;
    this.currentSlide = 0;
    this.slides = element.querySelectorAll('.carousel-slide');
    this.totalSlides = this.slides.length;
    
    if (this.totalSlides > 1) {
      this.createControls();
      this.showSlide(0);
    }
  }
  
  createControls() {
    // Create navigation dots
    const dotsContainer = document.createElement('div');
    dotsContainer.className = 'carousel-dots flex justify-center space-x-2 mt-4';
    
    for (let i = 0; i < this.totalSlides; i++) {
      const dot = document.createElement('button');
      dot.className = 'w-3 h-3 rounded-full bg-gray-300 hover:bg-gray-400 transition-colors';
      dot.addEventListener('click', () => this.showSlide(i));
      dotsContainer.appendChild(dot);
    }
    
    this.element.appendChild(dotsContainer);
    
    // Create prev/next buttons
    const prevButton = document.createElement('button');
    prevButton.className = 'carousel-prev absolute left-4 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-75 hover:bg-opacity-100 rounded-full p-2 transition-all';
    prevButton.innerHTML = '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>';
    prevButton.addEventListener('click', () => this.prevSlide());
    
    const nextButton = document.createElement('button');
    nextButton.className = 'carousel-next absolute right-4 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-75 hover:bg-opacity-100 rounded-full p-2 transition-all';
    nextButton.innerHTML = '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>';
    nextButton.addEventListener('click', () => this.nextSlide());
    
    this.element.appendChild(prevButton);
    this.element.appendChild(nextButton);
  }
  
  showSlide(index) {
    this.slides.forEach((slide, i) => {
      slide.style.display = i === index ? 'block' : 'none';
    });
    
    // Update dots
    const dots = this.element.querySelectorAll('.carousel-dots button');
    dots.forEach((dot, i) => {
      dot.className = i === index 
        ? 'w-3 h-3 rounded-full bg-blue-600 transition-colors'
        : 'w-3 h-3 rounded-full bg-gray-300 hover:bg-gray-400 transition-colors';
    });
    
    this.currentSlide = index;
  }
  
  nextSlide() {
    const next = (this.currentSlide + 1) % this.totalSlides;
    this.showSlide(next);
  }
  
  prevSlide() {
    const prev = (this.currentSlide - 1 + this.totalSlides) % this.totalSlides;
    this.showSlide(prev);
  }
}

// Initialize carousels
document.addEventListener('DOMContentLoaded', function() {
  const carousels = document.querySelectorAll('.carousel');
  carousels.forEach(carousel => new Carousel(carousel));
}); 