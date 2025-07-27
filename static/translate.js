window.addEventListener('DOMContentLoaded', () => {
  const container = document.createElement("div");
  container.style.position = "fixed";
  container.style.top = "10px";
  container.style.right = "10px";
  container.style.zIndex = "9999";
  container.style.display = "flex";
  container.style.flexDirection = "column";
  container.style.alignItems = "flex-end";
  container.style.backgroundColor = "white";
  container.style.padding = "8px 10px";
  container.style.borderRadius = "5px";
  container.style.boxShadow = "0 0 10px rgba(0,0,0,0.15)";
  container.style.fontFamily = "Arial, sans-serif";

  const modelDropdown = document.createElement("select");
  modelDropdown.id = "modelDropdown";
  modelDropdown.innerHTML = `
    <option value="helsinki">Helsinki-NLP</option>
    <option value="mbart">mBART</option>
    <option value="m2m100">M2M100</option>
    <option value="nllb">NLLB</option>
  `;
  modelDropdown.style.marginBottom = "5px";
  modelDropdown.style.padding = "5px";

  const langDropdown = document.createElement("select");
  langDropdown.id = "languageDropdown";
  langDropdown.innerHTML = `
    <option value="en_XX">English</option>
    <option value="hi_IN">Hindi</option>
    <option value="fr_XX">French</option>
    <option value="de_DE">German</option>
    <option value="ja_XX">Japanese</option>
  `;
  langDropdown.style.marginBottom = "5px";
  langDropdown.style.padding = "5px";

  const spinner = document.createElement("div");
  spinner.id = "spinner";
  spinner.innerText = "🔄 Translating...";
  spinner.style.display = "none";
  spinner.style.fontSize = "12px";
  spinner.style.color = "#333";
  container.appendChild(modelDropdown);
  container.appendChild(langDropdown);
  container.appendChild(spinner);
  document.body.appendChild(container);

  const translatable = Array.from(document.querySelectorAll(
    "h1,h2,h3,h4,h5,h6,p,span,a,button,label,td,th,li,strong,b,u,i"
  )).filter(el => el.innerText.trim().length > 0 && !container.contains(el));

  const placeholders = Array.from(document.querySelectorAll("input[placeholder],textarea[placeholder]"))
    .filter(el => !container.contains(el));

  const options = Array.from(document.querySelectorAll("option"))
    .filter(el => !container.contains(el));

  [...translatable, ...placeholders, ...options].forEach(el => {
    if (!el.hasAttribute("data-original")) {
      el.setAttribute("data-original", el.innerText || el.placeholder);
    }
  });

  async function applyTranslation(modelType, targetLang) {
    spinner.style.display = "block";

    await fetch("/set_model", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model_type: modelType, target_lang: targetLang })
    });

    const translateElement = async (el, original) => {
      const res = await fetch("/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: original, target_lang: targetLang })
      });
      const data = await res.json();
      return data.translation || original;
    };

    const tasks = translatable.map(async el => {
      const original = el.getAttribute("data-original");
      const translated = await translateElement(el, original);
      el.innerText = translated;
    });

    const placeholderTasks = placeholders.map(async el => {
      const original = el.getAttribute("data-original");
      const translated = await translateElement(el, original);
      el.placeholder = translated;
    });

    const optionTasks = options.map(async el => {
      const original = el.getAttribute("data-original");
      const translated = await translateElement(el, original);
      el.innerText = translated;
    });

    await Promise.all([...tasks, ...placeholderTasks, ...optionTasks]);
    spinner.style.display = "none";
  }

  langDropdown.addEventListener("change", () => {
    const selectedLang = langDropdown.value;
    if (selectedLang === "en_XX") {
      [...translatable, ...placeholders, ...options].forEach(el => {
        const original = el.getAttribute("data-original");
        if (el.placeholder !== undefined) el.placeholder = original;
        else el.innerText = original;
      });
    } else {
      applyTranslation(modelDropdown.value, selectedLang);
    }
  });
});