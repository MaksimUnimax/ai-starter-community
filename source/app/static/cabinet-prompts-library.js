(() => {
  const STORAGE_KEY = "openscript:cabinet:prompts-library:v1";

  const root = document.querySelector("[data-prompts-library-root]");
  if (!root) {
    return;
  }

  const builtInList = root.querySelector("[data-prompts-built-in-list]");
  const customList = root.querySelector("[data-prompts-custom-list]");
  const emptyElement = root.querySelector("[data-prompts-empty]");
  const noticeElement = root.querySelector("[data-prompts-notice]");
  const addButton = root.querySelector("[data-prompts-add]");
  const customTemplate = root.querySelector("[data-prompts-custom-template]");

  let state = loadState();
  let noticeTimer = null;
  const builtInPrompts = collectBuiltInPrompts();

  function createId() {
    return `prompt_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 10)}`;
  }

  function slugify(value) {
    const slug = String(value || "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "");
    return slug || "custom-prompt";
  }

  function normalizeCustomTitle(value) {
    const title = typeof value === "string" ? value.trim() : "";
    return title || "Новый промпт";
  }

  function normalizeState(raw) {
    const source = raw && typeof raw === "object" ? raw : {};
    const overridesSource = source.overrides && typeof source.overrides === "object" ? source.overrides : {};
    const customSource = Array.isArray(source.custom) ? source.custom : [];

    const overrides = {};
    Object.entries(overridesSource).forEach(([id, value]) => {
      const markdown = typeof value?.markdown === "string" ? value.markdown : "";
      if (!markdown) {
        return;
      }
      overrides[id] = {
        title: typeof value?.title === "string" && value.title.trim() ? value.title.trim() : "Промпт",
        markdown,
        updatedAt: typeof value?.updatedAt === "string" ? value.updatedAt : "",
      };
    });

    const custom = customSource.map((rawPrompt) => ({
      id: typeof rawPrompt?.id === "string" && rawPrompt.id ? rawPrompt.id : createId(),
      title: normalizeCustomTitle(rawPrompt?.title),
      markdown: typeof rawPrompt?.markdown === "string" ? rawPrompt.markdown : "",
      updatedAt: typeof rawPrompt?.updatedAt === "string" ? rawPrompt.updatedAt : "",
      isEditing: false,
      isExpanded: false,
    }));

    return { overrides, custom };
  }

  function loadState() {
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        return normalizeState(null);
      }
      return normalizeState(JSON.parse(raw));
    } catch (_error) {
      return normalizeState(null);
    }
  }

  function persistState() {
    try {
      const payload = {
        overrides: state.overrides,
        custom: state.custom.map(({ id, title, markdown, updatedAt }) => ({
          id,
          title,
          markdown,
          updatedAt,
        })),
      };
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
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

  function copyValue(value, successMessage) {
    void (async () => {
      try {
        const copied = await copyText(value);
        setNotice(copied ? successMessage : "Не удалось скопировать");
      } catch (_error) {
        setNotice("Не удалось скопировать");
      }
    })();
  }

  function downloadMarkdown(markdown, filename) {
    const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    link.rel = "noopener";
    document.body.appendChild(link);
    link.click();
    window.setTimeout(() => {
      window.URL.revokeObjectURL(url);
      link.remove();
    }, 0);
  }

  function setPromptCardExpanded(card, expanded) {
    const body = card.querySelector("[data-prompt-body]");
    const toggleButton = card.querySelector("[data-prompt-toggle]");

    card.dataset.promptExpanded = String(expanded);
    card.classList.toggle("prompt-card--collapsed", !expanded);
    card.classList.toggle("prompt-card--expanded", expanded);

    if (body) {
      body.hidden = !expanded;
    }

    if (toggleButton) {
      toggleButton.setAttribute("aria-expanded", String(expanded));
      toggleButton.textContent = expanded ? "Свернуть" : "Развернуть";
    }
  }

  function collectBuiltInPrompts() {
    if (!builtInList) {
      return [];
    }

    return Array.from(builtInList.querySelectorAll(".prompt-card--built-in")).map((card) => {
      const textarea = card.querySelector("[data-prompt-textarea]");
      return {
        id: card.dataset.promptId || createId(),
        card,
        title: card.dataset.promptTitle || card.querySelector(".prompt-card__title")?.textContent?.trim() || "Промпт",
        ownerLabel: card.dataset.promptOwner || "",
        sourceLabel: card.dataset.promptSourceLabel || "",
        filename: card.dataset.promptFilename || "",
        textarea,
        editButton: card.querySelector("[data-prompt-edit]"),
        saveButton: card.querySelector("[data-prompt-save]"),
        copyButton: card.querySelector("[data-prompt-copy]"),
        downloadButton: card.querySelector("[data-prompt-download]"),
        resetButton: card.querySelector("[data-prompt-reset]"),
        toggleButton: card.querySelector("[data-prompt-toggle]"),
        body: card.querySelector("[data-prompt-body]"),
        originalMarkdown: textarea?.defaultValue || textarea?.value || "",
        isEditing: false,
        isExpanded: false,
      };
    });
  }

  function findBuiltInPrompt(id) {
    return builtInPrompts.find((prompt) => prompt.id === id) || null;
  }

  function applyBuiltInPrompt(prompt) {
    const override = state.overrides[prompt.id];
    const markdown = override ? override.markdown : prompt.originalMarkdown;
    prompt.textarea.value = markdown;
    prompt.textarea.readOnly = !prompt.isEditing;
    prompt.textarea.setAttribute("aria-readonly", String(!prompt.isEditing));
    prompt.card.classList.toggle("prompt-card--editing", prompt.isEditing);
    setPromptCardExpanded(prompt.card, prompt.isEditing || prompt.isExpanded);
    if (prompt.toggleButton) {
      prompt.toggleButton.disabled = prompt.isEditing;
    }
    if (prompt.saveButton) {
      prompt.saveButton.hidden = !prompt.isEditing;
      prompt.saveButton.disabled = !prompt.isEditing;
    }
    if (prompt.editButton) {
      prompt.editButton.disabled = prompt.isEditing;
    }
  }

  function persistBuiltInOverride(prompt) {
    state.overrides[prompt.id] = {
      title: prompt.title,
      markdown: prompt.textarea.value,
      updatedAt: new Date().toISOString(),
    };
    persistState();
  }

  function resetBuiltInOverride(prompt) {
    delete state.overrides[prompt.id];
    prompt.textarea.value = prompt.originalMarkdown;
    persistState();
  }

  function renderBuiltInPrompts() {
    builtInPrompts.forEach((prompt) => {
      applyBuiltInPrompt(prompt);

      if (prompt.toggleButton) {
        prompt.toggleButton.addEventListener("click", () => {
          if (prompt.isEditing) {
            return;
          }
          prompt.isExpanded = !prompt.isExpanded;
          applyBuiltInPrompt(prompt);
        });
      }

      if (prompt.editButton) {
        prompt.editButton.addEventListener("click", () => {
          prompt.isEditing = true;
          prompt.isExpanded = true;
          applyBuiltInPrompt(prompt);
          prompt.textarea.focus();
          prompt.textarea.select();
        });
      }

      if (prompt.saveButton) {
        prompt.saveButton.addEventListener("click", () => {
          persistBuiltInOverride(prompt);
          prompt.isEditing = false;
          prompt.isExpanded = true;
          applyBuiltInPrompt(prompt);
          setNotice("Промпт сохранён");
        });
      }

      if (prompt.copyButton) {
        prompt.copyButton.addEventListener("click", () => {
          copyValue(prompt.textarea.value, "Промпт скопирован");
        });
      }

      if (prompt.downloadButton) {
        prompt.downloadButton.addEventListener("click", () => {
          const filename = prompt.filename || `${slugify(prompt.title)}.md`;
          downloadMarkdown(prompt.textarea.value, filename);
          setNotice("Промпт скачан");
        });
      }

      if (prompt.resetButton) {
        prompt.resetButton.addEventListener("click", () => {
          prompt.isEditing = false;
          prompt.isExpanded = true;
          resetBuiltInOverride(prompt);
          applyBuiltInPrompt(prompt);
          setNotice("Версия курса восстановлена");
        });
      }
    });
  }

  function createCustomPromptCard(prompt) {
    if (!customTemplate) {
      return null;
    }

    const fragment = customTemplate.content.cloneNode(true);
    const card = fragment.querySelector("[data-prompt-custom]");
    const titleInput = card.querySelector("[data-prompt-title]");
    const textarea = card.querySelector("[data-prompt-textarea]");
    const editButton = card.querySelector("[data-prompt-edit]");
    const saveButton = card.querySelector("[data-prompt-save]");
    const copyButton = card.querySelector("[data-prompt-copy]");
    const downloadButton = card.querySelector("[data-prompt-download]");
    const deleteButton = card.querySelector("[data-prompt-delete]");
    const toggleButton = card.querySelector("[data-prompt-toggle]");
    const body = card.querySelector("[data-prompt-body]");
    const summaryTitle = card.querySelector("[data-prompt-summary-title]");

    card.dataset.promptId = prompt.id;
    titleInput.value = prompt.title;
    textarea.value = prompt.markdown;
    card.classList.toggle("prompt-card--editing", prompt.isEditing);
    titleInput.readOnly = !prompt.isEditing;
    textarea.readOnly = !prompt.isEditing;
    if (summaryTitle) {
      summaryTitle.textContent = prompt.title;
    }
    if (editButton) {
      editButton.hidden = prompt.isEditing;
      editButton.disabled = prompt.isEditing;
    }
    if (saveButton) {
      saveButton.hidden = !prompt.isEditing;
      saveButton.disabled = !prompt.isEditing;
    }
    if (toggleButton) {
      toggleButton.disabled = prompt.isEditing;
    }
    setPromptCardExpanded(card, prompt.isEditing || prompt.isExpanded);

    if (editButton) {
      editButton.addEventListener("click", () => {
        prompt.isEditing = true;
        prompt.isExpanded = true;
        renderCustomPrompts();
      });
    }

    if (saveButton) {
      saveButton.addEventListener("click", () => {
        prompt.title = normalizeCustomTitle(titleInput.value);
        prompt.markdown = textarea.value;
        prompt.updatedAt = new Date().toISOString();
        prompt.isEditing = false;
        prompt.isExpanded = true;
        persistState();
        renderCustomPrompts();
        setNotice("Промпт сохранён");
      });
    }

    if (copyButton) {
      copyButton.addEventListener("click", () => {
        copyValue(textarea.value, "Промпт скопирован");
      });
    }

    if (downloadButton) {
      downloadButton.addEventListener("click", () => {
        const filename = `${slugify(titleInput.value || prompt.title)}.md`;
        downloadMarkdown(textarea.value, filename);
        setNotice("Промпт скачан");
      });
    }

    if (deleteButton) {
      deleteButton.addEventListener("click", () => {
        state.custom = state.custom.filter((item) => item.id !== prompt.id);
        persistState();
        renderCustomPrompts();
        setNotice("Промпт удалён");
      });
    }

    if (toggleButton) {
      toggleButton.addEventListener("click", () => {
        if (prompt.isEditing) {
          return;
        }
        prompt.isExpanded = !prompt.isExpanded;
        renderCustomPrompts();
      });
    }

    titleInput.addEventListener("input", () => {
      if (prompt.isEditing) {
        prompt.title = normalizeCustomTitle(titleInput.value);
        if (summaryTitle) {
          summaryTitle.textContent = prompt.title;
        }
      }
    });

    textarea.addEventListener("input", () => {
      if (prompt.isEditing) {
        prompt.markdown = textarea.value;
      }
    });

    return card;
  }

  function renderCustomPrompts() {
    if (!customList) {
      return;
    }

    customList.textContent = "";
    state.custom.forEach((prompt) => {
      const card = createCustomPromptCard(prompt);
      if (card) {
        customList.append(card);
      }
    });

    if (emptyElement) {
      emptyElement.hidden = state.custom.length > 0;
    }
  }

  function addCustomPrompt() {
    state.custom = state.custom.concat({
      id: createId(),
      title: "Новый промпт",
      markdown: "",
      updatedAt: "",
      isEditing: true,
    });
    persistState();
    renderCustomPrompts();

    const lastCard = customList?.querySelector(".prompt-card:last-child");
    const titleInput = lastCard?.querySelector("[data-prompt-title]");
    if (titleInput instanceof HTMLInputElement) {
      titleInput.focus();
      titleInput.select();
    }
  }

  if (addButton) {
    addButton.addEventListener("click", addCustomPrompt);
  }

  renderBuiltInPrompts();
  renderCustomPrompts();
})();
