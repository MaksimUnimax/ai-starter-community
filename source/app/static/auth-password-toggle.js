document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-password-field]").forEach((field) => {
    const input = field.querySelector("[data-password-input]");
    const toggle = field.querySelector("[data-password-toggle]");
    if (!input || !toggle) {
      return;
    }

    const syncToggle = () => {
      const visible = input.type === "text";
      toggle.textContent = visible ? "Скрыть пароль" : "Показать пароль";
      toggle.setAttribute("aria-label", visible ? "Скрыть пароль" : "Показать пароль");
      toggle.setAttribute("aria-pressed", String(visible));
    };

    toggle.addEventListener("click", () => {
      input.type = input.type === "password" ? "text" : "password";
      syncToggle();
    });

    syncToggle();
  });
});
