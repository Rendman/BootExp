(() => {
  const storageKey = "bootstrap-theme";
  const root = document.documentElement;
  const systemTheme = typeof window.matchMedia === "function"
    ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  let preference;
  let toggle;

  try {
    const saved = localStorage.getItem(storageKey);
    if (saved === "light" || saved === "dark") preference = saved;
  } catch {
    // The toggle still works when browser storage is unavailable.
  }

  function applyTheme() {
    const dark = preference ? preference === "dark" : Boolean(systemTheme && systemTheme.matches);
    root.dataset.theme = dark ? "dark" : "light";
    if (toggle) {
      toggle.setAttribute("aria-pressed", String(dark));
      toggle.title = dark ? "Switch to light mode" : "Switch to dark mode";
    }
  }

  // Apply before the stylesheet loads to avoid flashing the wrong theme.
  applyTheme();
  if (systemTheme && typeof systemTheme.addEventListener === "function") {
    systemTheme.addEventListener("change", applyTheme);
  } else if (systemTheme && typeof systemTheme.addListener === "function") {
    systemTheme.addListener(applyTheme);
  }
  window.addEventListener("storage", (event) => {
    if (event.key !== storageKey && event.key !== null) return;
    preference = event.newValue === "light" || event.newValue === "dark"
      ? event.newValue : undefined;
    applyTheme();
  });

  function initializeToggle() {
    toggle = document.querySelector(".theme-toggle");
    if (!toggle) return;
    toggle.addEventListener("click", () => {
      preference = root.dataset.theme === "dark" ? "light" : "dark";
      applyTheme();
      try {
        localStorage.setItem(storageKey, preference);
      } catch {
        // Keep this page usable even when saving the preference fails.
      }
    });
    applyTheme();
    toggle.hidden = false;
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeToggle, { once: true });
  } else {
    initializeToggle();
  }
  window.addEventListener("pageshow", applyTheme);
})();
