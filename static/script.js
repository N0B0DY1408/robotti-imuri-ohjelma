const dialog = document.getElementById("loginDialog");
const showButton = document.getElementById("login");
const closeButton = document.getElementById("closeDialog");
const signupForm = document.getElementById("signupForm");
const codeForm = document.getElementById("codeForm");
const worked = document.getElementById("onnistui");


showButton.addEventListener("click", () => {
    dialog.showModal();
});

closeButton.addEventListener("click", () => {
    dialog.close();
});

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

        const text = await res.text();
        console.log("Raw response:", text);
        const data = JSON.parse(text);
        console.log(data); // debug

        if (data.success) {
            signupForm.hidden = true;
            codeForm.hidden = false;
        } else {
            alert(data.message || "Virhe");
        }

        if (data.success && data.ok) {
            codeForm.hidden = true;
            onnistui.hidden = false;
        }

    } catch (err) {
        console.error(err);
        alert("Tapahtui virhe");
    }
});
