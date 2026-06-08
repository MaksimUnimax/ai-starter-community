(() => {
  const STORAGE_KEY = "openscript:cabinet:local-accounts:v1";
  const ACCOUNT_TITLES = {
    chatgpt: "ChatGPT",
    server: "Сервер",
  };

  const root = document.querySelector("[data-local-accounts-root]");
  if (!root) {
    return;
  }

  const listElement = root.querySelector("[data-local-accounts-list]");
  const emptyElement = root.querySelector("[data-local-accounts-empty]");
  const noticeElement = root.querySelector("[data-local-accounts-notice]");
  const typeSelect = root.querySelector("[data-local-accounts-type]");
  const addButton = root.querySelector("[data-local-accounts-add]");

  let accounts = loadAccounts();
  let noticeTimer = null;

  function createId() {
    return `account_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 10)}`;
  }

  function normalizeType(value) {
    return value === "server" ? "server" : "chatgpt";
  }

  function normalizeAccount(raw) {
    const type = normalizeType(raw && raw.type);
    return {
      id: typeof raw?.id === "string" && raw.id ? raw.id : createId(),
      type,
      title: ACCOUNT_TITLES[type],
      login: typeof raw?.login === "string" ? raw.login : "",
      password: typeof raw?.password === "string" ? raw.password : "",
      passwordVisible: Boolean(raw?.passwordVisible),
      persisted: true,
      isEditing: false,
    };
  }

  function loadAccounts() {
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        return [];
      }
      const parsed = JSON.parse(raw);
      if (!Array.isArray(parsed)) {
        return [];
      }
      return parsed.map(normalizeAccount);
    } catch (_error) {
      return [];
    }
  }

  function persistAccounts() {
    try {
      const storedAccounts = accounts
        .filter((account) => account.persisted)
        .map(({ id, type, login, password, passwordVisible }) => ({
          id,
          type,
          login,
          password,
          passwordVisible,
        }));
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(storedAccounts));
      return true;
    } catch (_error) {
      return false;
    }
  }

  function setNotice(message) {
    if (!noticeElement) {
      return;
    }

    noticeElement.textContent = message;
    if (noticeTimer !== null) {
      window.clearTimeout(noticeTimer);
    }

    if (message) {
      noticeTimer = window.setTimeout(() => {
        noticeElement.textContent = "";
        noticeTimer = null;
      }, 2200);
    }
  }

  function findAccount(id) {
    return accounts.find((account) => account.id === id) || null;
  }

  function updateAccount(id, patch) {
    const account = findAccount(id);
    if (!account) {
      return null;
    }
    Object.assign(account, patch);
    if (account.persisted) {
      persistAccounts();
    }
    return account;
  }

  function removeAccount(id) {
    accounts = accounts.filter((account) => account.id !== id);
    persistAccounts();
    renderAccounts();
  }

  function addAccount() {
    const type = normalizeType(typeSelect?.value);
    accounts = accounts.concat({
      id: createId(),
      type,
      title: ACCOUNT_TITLES[type],
      login: "",
      password: "",
      passwordVisible: false,
      persisted: false,
      isEditing: true,
    });
    renderAccounts();

    const lastCard = listElement?.querySelector(".account-card:last-child");
    const loginInput = lastCard?.querySelector('input[data-account-field="login"]');
    if (loginInput instanceof HTMLInputElement) {
      loginInput.focus();
    }
  }

  async function copyText(text) {
    if (navigator.clipboard && typeof navigator.clipboard.writeText === "function") {
      await navigator.clipboard.writeText(text);
      return true;
    }

    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "true");
    textarea.style.position = "fixed";
    textarea.style.left = "-9999px";
    textarea.style.top = "0";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();

    let success = false;
    try {
      success = document.execCommand("copy");
    } catch (_error) {
      success = false;
    }

    document.body.removeChild(textarea);
    return success;
  }

  async function copyValue(value, successMessage) {
    try {
      const copied = await copyText(value);
      setNotice(copied ? successMessage : "Не удалось скопировать");
    } catch (_error) {
      setNotice("Не удалось скопировать");
    }
  }

  function createField(labelText, inputType, value, fieldName) {
    const field = document.createElement("label");
    field.className = "account-field";

    const label = document.createElement("span");
    label.textContent = labelText;

    const input = document.createElement("input");
    input.className = "input";
    input.type = inputType;
    input.value = value;
    input.autocomplete = "off";
    input.spellcheck = false;
    input.dataset.accountField = fieldName;

    field.append(label, input);
    return { field, input };
  }

  function renderAccountCard(account) {
    const article = document.createElement("article");
    article.className = "account-card";
    article.dataset.accountId = account.id;

    const loginField = createField("Логин", "text", account.login, "login");
    loginField.input.placeholder = "Введите логин";
    loginField.input.readOnly = !account.isEditing;
    loginField.input.setAttribute("aria-readonly", String(!account.isEditing));

    const passwordField = document.createElement("label");
    passwordField.className = "account-field";

    const passwordLabel = document.createElement("span");
    passwordLabel.textContent = "Пароль";

    const passwordRow = document.createElement("div");
    passwordRow.className = "account-password-row";

    const passwordInput = document.createElement("input");
    passwordInput.className = "input";
    passwordInput.type = account.passwordVisible ? "text" : "password";
    passwordInput.value = account.password;
    passwordInput.placeholder = "Введите пароль";
    passwordInput.autocomplete = "off";
    passwordInput.spellcheck = false;
    passwordInput.dataset.accountField = "password";
    passwordInput.readOnly = !account.isEditing;
    passwordInput.setAttribute("aria-readonly", String(!account.isEditing));

    const toggleButton = document.createElement("button");
    toggleButton.className = "button button-secondary account-password-toggle";
    toggleButton.type = "button";
    toggleButton.textContent = account.passwordVisible ? "Скрыть пароль" : "Показать пароль";
    toggleButton.setAttribute("aria-label", account.passwordVisible ? "Скрыть пароль" : "Показать пароль");
    toggleButton.setAttribute("aria-pressed", String(account.passwordVisible));

    const header = document.createElement("div");
    header.className = "account-card__header";

    const title = document.createElement("h3");
    title.className = "account-card__title";
    title.textContent = account.title;

    const deleteButton = document.createElement("button");
    deleteButton.className = "button button-danger account-card__delete";
    deleteButton.type = "button";
    deleteButton.textContent = "Удалить";
    deleteButton.addEventListener("click", () => {
      removeAccount(account.id);
    });

    header.append(title, deleteButton);
    article.append(header);
    toggleButton.addEventListener("click", () => {
      const updated = updateAccount(account.id, {
        passwordVisible: !account.passwordVisible,
      });
      if (!updated) {
        return;
      }
      passwordInput.type = updated.passwordVisible ? "text" : "password";
      toggleButton.textContent = updated.passwordVisible ? "Скрыть пароль" : "Показать пароль";
      toggleButton.setAttribute("aria-label", updated.passwordVisible ? "Скрыть пароль" : "Показать пароль");
      toggleButton.setAttribute("aria-pressed", String(updated.passwordVisible));
    });

    passwordRow.append(passwordInput, toggleButton);
    passwordField.append(passwordLabel, passwordRow);

    const actions = document.createElement("div");
    actions.className = "account-actions";

    const editButton = document.createElement("button");
    editButton.className = "button button-secondary account-card__edit";
    editButton.type = "button";
    editButton.textContent = "Редактировать";

    const saveButton = document.createElement("button");
    saveButton.className = "button button-primary account-card__save";
    saveButton.type = "button";
    saveButton.textContent = "Сохранить";

    function syncMode() {
      const editing = Boolean(account.isEditing);
      article.classList.toggle("account-card--editing", editing);
      article.classList.toggle("account-card--locked", !editing);
      loginField.input.readOnly = !editing;
      passwordInput.readOnly = !editing;
      loginField.input.setAttribute("aria-readonly", String(!editing));
      passwordInput.setAttribute("aria-readonly", String(!editing));
      editButton.disabled = editing;
      saveButton.disabled = !editing;
    }

    editButton.addEventListener("click", () => {
      account.isEditing = true;
      syncMode();
      loginField.input.focus();
      loginField.input.select();
    });

    saveButton.addEventListener("click", () => {
      account.login = loginField.input.value;
      account.password = passwordInput.value;
      account.persisted = true;
      account.isEditing = false;
      persistAccounts();
      setNotice("Сохранено");
      syncMode();
    });

    const copyLoginButton = document.createElement("button");
    copyLoginButton.className = "button button-secondary";
    copyLoginButton.type = "button";
    copyLoginButton.textContent = "Скопировать логин";
    copyLoginButton.addEventListener("click", () => {
      void copyValue(loginField.input.value, "Логин скопирован");
    });

    const copyPasswordButton = document.createElement("button");
    copyPasswordButton.className = "button button-secondary";
    copyPasswordButton.type = "button";
    copyPasswordButton.textContent = "Скопировать пароль";
    copyPasswordButton.addEventListener("click", () => {
      void copyValue(passwordInput.value, "Пароль скопирован");
    });

    actions.append(copyLoginButton, editButton, copyPasswordButton, saveButton);

    article.append(loginField.field, passwordField, actions);
    syncMode();
    return article;
  }

  function renderAccounts() {
    if (!listElement) {
      return;
    }

    listElement.textContent = "";
    accounts.forEach((account) => {
      listElement.append(renderAccountCard(account));
    });

    if (emptyElement) {
      emptyElement.hidden = accounts.length > 0;
    }
  }

  if (addButton) {
    addButton.addEventListener("click", addAccount);
  }

  renderAccounts();
})();
