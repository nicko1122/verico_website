document.addEventListener('DOMContentLoaded', function() {
  // Handle select language switchers
  const selects = document.querySelectorAll('select');
  selects.forEach(select => {
    select.addEventListener('change', function() {
      const lang = this.value;
      
      // Set cookie
      const expiryDate = new Date();
      expiryDate.setDate(expiryDate.getDate() + 30);
      document.cookie = `preferred_language=${lang}; expires=${expiryDate.toUTCString()}; path=/`;
      
      // Redirect directly to language path
      window.location.href = `/${lang}/`;
    });
  });
}); 