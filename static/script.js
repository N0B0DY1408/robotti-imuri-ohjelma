const dialog = document.getElementById("loginDialog");
const showButton = document.getElementById("login");
const closeButton = document.getElementById("closeDialog");
const signupForm = document.getElementById("signupForm");
const worked = document.getElementById("onnistui");


showButton.addEventListener("click", () => {
    dialog.showModal();
});

closeButton.addEventListener("click", () => {
    dialog.close();
});

popupForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = popupForm.email.value;

    try {
        const res = await fetch("/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email }),
        });

        const data = await res.json();
        console.log(data); // debug

        if (data.success) {
            popupForm.hidden = true;
            worked.hidden = false;
        } else {
            alert(data.message || "Virhe");
        }

    } catch (err) {
        console.error(err);
        alert("Jokin meni pieleen");
    }
});
