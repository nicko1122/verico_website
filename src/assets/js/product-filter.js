// Product Filter Script
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.product-filter-btn');
    const productCards = document.querySelectorAll('.product-card');
    
    if (!filterButtons.length || !productCards.length) return;

    // Filter function
    function filterProducts(category) {
        productCards.forEach(card => {
            const cardCategory = card.getAttribute('data-category');
            
            if (category === 'all' || cardCategory === category) {
                card.style.display = 'block';
                card.style.opacity = '0';
                setTimeout(() => {
                    card.style.opacity = '1';
                }, 50);
            } else {
                card.style.opacity = '0';
                setTimeout(() => {
                    card.style.display = 'none';
                }, 300);
            }
        });
    }

    // Update active button
    function updateActiveButton(activeButton) {
        filterButtons.forEach(btn => {
            btn.classList.remove('bg-gray-800', 'text-white');
            btn.classList.add('bg-white', 'text-gray-700', 'border-gray-200');
        });
        
        activeButton.classList.remove('bg-white', 'text-gray-700', 'border-gray-200');
        activeButton.classList.add('bg-gray-800', 'text-white');
    }

    // Add click event to filter buttons
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            
            // Update active button
            updateActiveButton(this);
            
            // Filter products
            filterProducts(category);
            
            // Update URL hash (optional)
            if (category !== 'all') {
                window.location.hash = `category=${category}`;
            } else {
                window.location.hash = '';
            }
        });
    });

    // Initialize with 'all' category or hash-based category
    const hash = window.location.hash;
    if (hash && hash.includes('category=')) {
        const category = hash.split('=')[1];
        const targetButton = document.querySelector(`[data-category="${category}"]`);
        if (targetButton) {
            updateActiveButton(targetButton);
            filterProducts(category);
        } else {
            // Default to 'all' if category not found
            const allButton = document.querySelector('[data-category="all"]');
            if (allButton) {
                updateActiveButton(allButton);
                filterProducts('all');
            }
        }
    } else {
        // Default to 'all' category
        const allButton = document.querySelector('[data-category="all"]');
        if (allButton) {
            updateActiveButton(allButton);
            filterProducts('all');
        }
    }

    // Add animation classes to product cards
    productCards.forEach((card, index) => {
        card.style.transition = 'opacity 0.3s ease-in-out';
        card.style.opacity = '1';
    });
}); 