(function () {
  const dropdowns = Array.from(document.querySelectorAll(".nav-account-dropdown"));

  if (dropdowns.length === 0) {
    return;
  }

  const closeAll = (except = null) => {
    dropdowns.forEach((dropdown) => {
      if (dropdown !== except) {
        dropdown.removeAttribute("open");
      }
    });
  };

  document.addEventListener("click", (event) => {
    dropdowns.forEach((dropdown) => {
      if (!dropdown.hasAttribute("open")) {
        return;
      }
      if (dropdown.contains(event.target)) {
        return;
      }
      dropdown.removeAttribute("open");
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") {
      return;
    }
    closeAll();
  });

  dropdowns.forEach((dropdown) => {
    dropdown.addEventListener("toggle", () => {
      if (dropdown.hasAttribute("open")) {
        closeAll(dropdown);
      }
    });
  });
})();
