const dialog = document.getElementById("loginDialog");
const showButton = document.getElementById("login");
const closeButton = document.getElementById("closeDialog");

const popupForm = document.getElementById("popupForm");
const codeForm = document.getElementById("codeForm");
const result = document.getElementById("result");

// id_generator = koodi joka on siellä tietokannassa joka on tullut app.pyn kautta



showButton.addEventListener("click", () => {
    dialog.showModal();
});

closeButton.addEventListener("click", () => {
    dialog.close();
});

popupForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = popupForm.email.value;

    if (!email.endsWith("@student.kpedu.fi")) {
        alert("Syötä kpedu-sähköposti");
        return;
    }

    const res = await fetch("/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
    });

    const data = await res.json();

    if (!res.ok) {
    alert("Palvelinvirhe");
    return;
    }



    if (data.status === "sent") {
        popupForm.hidden = true;
        codeForm.hidden = false;
    }
});


codeForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const userCode = codeForm.code.value;

    const res = await fetch("/verify", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ code: userCode }),
    });

    const data = await res.json();

    if (data.status === "ok") {
        codeForm.hidden = true;
        result.hidden = false;
        result.textContent = "Kirjautuminen onnistui 🎉";
    } else {
        alert("Väärä koodi");
    }
});

