document.addEventListener('DOMContentLoaded', function() {
  // --- 行動版導覽抽屜邏輯 ---
  const mobileMenuButton = document.getElementById('mobile-menu-button');
  const mobileNavDrawer = document.getElementById('mobile-nav-drawer');
  const mobileNavClose = document.getElementById('mobile-nav-close');
  const mobileNavOverlay = document.getElementById('mobile-nav-overlay');

  if (mobileMenuButton && mobileNavDrawer) {
    mobileMenuButton.addEventListener('click', function() {
      mobileNavDrawer.classList.remove('-translate-x-full');
      mobileNavDrawer.classList.add('translate-x-0');
      mobileNavOverlay.classList.remove('hidden');
    });
  }

  if (mobileNavClose && mobileNavDrawer) {
    mobileNavClose.addEventListener('click', function() {
      mobileNavDrawer.classList.add('-translate-x-full');
      mobileNavDrawer.classList.remove('translate-x-0');
      mobileNavOverlay.classList.add('hidden');
    });
  }

  if (mobileNavOverlay && mobileNavDrawer) {
    mobileNavOverlay.addEventListener('click', function() {
      mobileNavDrawer.classList.add('-translate-x-full');
      mobileNavDrawer.classList.remove('translate-x-0');
      mobileNavOverlay.classList.add('hidden');
    });
  }

  // --- 語言選擇器功能 ---
  const languageSelector = document.querySelector('select');
  if (languageSelector) {
    languageSelector.addEventListener('change', function() {
      const selectedLang = this.value;
      const currentUrl = window.location.pathname;
      const newUrl = currentUrl.replace(/^\/(en|de)\//, '/' + selectedLang + '/');
      window.location.href = newUrl;
    });
  }
}); 