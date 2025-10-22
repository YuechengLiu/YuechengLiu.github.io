// Language Toggle Script
(function() {
  'use strict';
  
  // Get current page language
  function getCurrentLang() {
    return document.documentElement.lang || 
           (window.location.pathname.includes('/zh/') || 
            window.location.pathname.includes('-zh') ? 'zh' : 'en');
  }
  
  // Store language preference
  function storeLangPreference(lang) {
    try {
      localStorage.setItem('preferred-language', lang);
    } catch (e) {
      // LocalStorage not available
    }
  }
  
  // Get stored language preference
  function getStoredLangPreference() {
    try {
      return localStorage.getItem('preferred-language');
    } catch (e) {
      return null;
    }
  }
  
  // Initialize language toggle
  function initLangToggle() {
    var langToggle = document.getElementById('lang-toggle');
    if (!langToggle) return;
    
    var link = langToggle.querySelector('a');
    if (!link) return;
    
    // Add click event to store preference
    link.addEventListener('click', function(e) {
      var currentLang = getCurrentLang();
      var newLang = currentLang === 'zh' ? 'en' : 'zh';
      storeLangPreference(newLang);
    });
  }
  
  // Auto-redirect to preferred language on home page
  function autoRedirectToPreferredLang() {
    var storedLang = getStoredLangPreference();
    var currentLang = getCurrentLang();
    var isHomePage = window.location.pathname === '/' || 
                      window.location.pathname === '/index.html';
    
    // Only redirect on home page if stored preference differs
    if (isHomePage && storedLang && storedLang !== currentLang) {
      if (storedLang === 'zh') {
        window.location.href = '/zh/';
      }
    }
  }
  
  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      initLangToggle();
      // Uncomment the next line if you want auto-redirect
      // autoRedirectToPreferredLang();
    });
  } else {
    initLangToggle();
    // Uncomment the next line if you want auto-redirect
    // autoRedirectToPreferredLang();
  }
})();
