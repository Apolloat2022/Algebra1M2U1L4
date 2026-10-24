// Multiple-choice engine shared by the bell work, homework and quiz pages.
// Each page sets window.MC = {mode: "homework" | "quiz", questions: [{q, choices, why, se?, extra?, letters?}]};
// `extra` is optional HTML (such as a data table) shown under the question; `letters` (such as "FGHJ") replaces "ABCD".
// The first choice is always the correct one; choices are shuffled on screen.
// Math goes inside [[ ]] and gets the math font, with every letter (always a variable) italic.
// Optional `accom` (IEP / 504 pages): {keep: [question indices], choices: n (drop trailing distractors),
// readAloud: true (a speech button on each question), add: [fields merged into question i, such as extra or why]}.
(function () {
  document.querySelector(".wrap").insertAdjacentHTML("afterbegin", '<a class="home" href="../index.html">← Home</a>');
  const { mode, accom = {} } = window.MC;
  const all = window.MC.questions.map((item, i) => ({ ...item, ...(accom.add || [])[i] }));
  const questions = (accom.keep ? accom.keep.map(i => all[i]) : all)
    .map(item => accom.choices ? { ...item, choices: item.choices.slice(0, accom.choices) } : item);
  const list = document.getElementById("questions");
  const result = document.getElementById("result");
  const submit = document.getElementById("submit");
  const math = s => s.replace(/\[\[(.+?)\]\]/g, (_, m) =>
    `<span class="mt">${m.replace(/[A-Za-z]/g, "<i>$&</i>")}</span>`);
  const shuffle = a => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

  function render() {
    list.innerHTML = questions.map((item, n) => {
      const order = shuffle(item.choices.map((_, i) => i));
      return `<li class="card"><fieldset>
        <legend>${math(item.q)}${item.se ? ` <span class="se">(SE p. ${item.se})</span>` : ""}</legend>${item.extra || ""}
        ${order.map((c, k) => `<label class="choice" data-c="${c}"><input type="radio" name="q${n}" value="${c}">
          <span class="letter">${(item.letters || "ABCD")[k]}</span><span>${math(item.choices[c])}</span></label>`).join("")}
        <p class="why" hidden></p></fieldset>${accom.readAloud ? '<button type="button" class="ghost say">Read aloud</button>' : ""}</li>`;
    }).join("");
    result.hidden = true;
    if (submit) submit.disabled = true;
    update();
  }

  // Marks one question: green on the right answer, red on a wrong pick, then the explanation.
  function grade(fs, n) {
    const picked = fs.querySelector("input:checked");
    const ok = picked && picked.value === "0";
    fs.querySelector('[data-c="0"]').classList.add("right");
    if (picked && !ok) picked.parentElement.classList.add("wrong");
    const why = fs.querySelector(".why");
    why.innerHTML = (ok ? '<b class="ok">Correct.</b> ' : `<b class="no">Incorrect.</b> The answer is ${math(questions[n].choices[0])}. `) + math(questions[n].why);
    why.hidden = false;
    fs.disabled = true;
    return ok;
  }

  const answered = () => list.querySelectorAll("input:checked").length;

  function update() {
    const done = answered(), total = questions.length;
    if (mode === "homework") {
      const right = list.querySelectorAll("fieldset:disabled input:checked[value='0']").length;
      result.hidden = done === 0;
      result.innerHTML = done < total
        ? `${done} of ${total} answered · ${right} correct`
        : `Finished: <b>${right} of ${total}</b> correct (${Math.round(100 * right / total)}%).`;
    } else {
      submit.disabled = done < total;
      submit.textContent = done < total ? `Submit (${done} of ${total} answered)` : "Submit quiz";
    }
  }

  list.addEventListener("change", e => {
    if (mode === "homework") grade(e.target.closest("fieldset"), +e.target.name.slice(1));
    update();
  });

  list.addEventListener("click", e => {  // read the question and its choices in on-screen order
    if (!e.target.classList.contains("say") || !window.speechSynthesis) return;
    const li = e.target.closest("li");
    const text = li.querySelector("legend").textContent + ". " +
      [...li.querySelectorAll(".choice")].map(c => c.textContent.trim().replace(/\s+/, ". ")).join(". ");
    speechSynthesis.cancel();
    speechSynthesis.speak(new SpeechSynthesisUtterance(text.replace(/−/g, " minus ")));
  });

  if (submit) submit.addEventListener("click", () => {
    const right = [...list.querySelectorAll("fieldset")].filter(grade).length;
    const name = document.getElementById("name").value.trim();
    submit.disabled = true;
    result.innerHTML = `${name ? `<b>${name.replace(/[<>&]/g, "")}</b> · ` : ""}Score: <b>${right} of ${questions.length}</b> (${Math.round(100 * right / questions.length)}%) · ${new Date().toLocaleString()}`;
    result.hidden = false;
    result.scrollIntoView({ behavior: "smooth", block: "center" });
  });

  document.getElementById("reset").addEventListener("click", () => { render(); window.scrollTo(0, 0); });
  render();
})();
