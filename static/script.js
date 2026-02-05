const dialog = document.getElementById("loginDialog");
const showButton = document.getElementById("login");
const closeButton = document.getElementById("closeDialog");

const popupForm = document.getElementById("popupForm");
const codeForm = document.getElementById("codeForm");
const result = document.getElementById("result");

import id_generator from "app.py";


showButton.addEventListener("click", () => {
    dialog.showModal();
});

closeButton.addEventListener("click", () => {
    dialog.close();
});

popupForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const email = popupForm.email.value;

    if (!email.endsWith("kpedu.fi")) {
        alert("Syötä kpedu-sähköposti");
        return;
    }

    popupForm.hidden = true;
    codeForm.hidden = false;
});


codeForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const userCode = codeForm.code.value;

    if (userCode !== id_generator()) {
        alert("Väärä koodi");
        return;
    }

    codeForm.hidden = true;
    result.hidden = false;
    result.textContent = "Kirjautuminen onnistui 🎉";
});
