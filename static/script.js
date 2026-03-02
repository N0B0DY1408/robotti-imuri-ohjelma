const signupForm = document.getElementById("signupForm");
const codeForm = document.getElementById("codeForm");

const emailView = document.getElementById("emailView");
const codeView = document.getElementById("codeView");
const successView = document.getElementById("successView");

const modalTitle = document.getElementById("modalTitle");


// EMAIL SUBMIT
signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = signupForm.email.value;

    try {
        const res = await fetch("/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email }),
        });

        const data = await res.json();

        if (data.success) {
            emailView.style.display = "none";
            codeView.style.display = "block";
            modalTitle.innerText = "Syötä vahvistuskoodi";
        } else {
            alert(data.message || "Virhe");
        }

    } catch (err) {
        console.error(err);
        alert("Tapahtui virhe");
    }
});


// CODE SUBMIT
codeForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const code = codeForm.code.value;

    try {
        const res = await fetch("/verify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ code }),
        });

        const data = await res.json();

        if (data.success) {
            codeView.style.display = "none";
            successView.style.display = "block";
            modalTitle.innerText = "Valmis!";
        } else {
            alert("Väärä koodi");
        }

    } catch (err) {
        console.error(err);
        alert("Virhe vahvistuksessa");
    }
});