const signupForm = document.getElementById("signupForm");
// signupForm on kirjautumiselle
const codeForm = document.getElementById("codeForm");
// codeForm on minne käyttäjä laittaa koodin kirjautumiselle
const Varaus = document.getElementById("Varaus");
// varaus nappi
const checkbox = document.getElementById("check1");
// check1 on se required checkbox, tarkistetaan jos ehdot on hyväksytty tarpeettomasti

const emailView = document.getElementById("emailView");
const codeView = document.getElementById("codeView");
const successView = document.getElementById("successView"); // ei käytetä
// codeView ja emailView on ne popup kohdat johon panee emailin tai koodin

const modalTitle = document.getElementById("modalTitle"); 
// jotta voi piilottaa 2 juttua vaikka suurin osa piilottamisesta on pythonin puolella

function toggleModalMode() {
    if (emailView.style.display == "none") {
        emailView.style.display = "block";
        codeView.style.display = "none";
        modalTitle.innerText = "Kirjoita sähköpostisi";
    } else {
    emailView.style.display = "none";
    codeView.style.display = "block";
    modalTitle.innerText = "Syötä vahvistuskoodi";
    };
};

// EMAIL SUBMIT
signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    // jos signupformista tulee submit tämä aktivoi

    const email = document.getElementById("select-email").value;
    const isChecked = checkbox.checked;

    if (!isChecked) {
        alert("Sinun täytyy hyväksyä ehdot ennen jatkamista.");
        return; // Estää fetchin
        // normaalisti ei tapahdu koska checkbox on required
    }

    try {
        const res = await fetch("/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: email }),
            // vetää sivulta käyttäjän paneman emailin
            // kohdasta jonka id on "select-email"
        });
        const data = await res.json();
        // odottaa että app.py palauttaa jsonify({"success": True})

        if (data.success) {
            toggleModalMode()
        } else {
            alert(data.message || "Virhe");
            // näyttää virhe viestin, oletuksena "Virhe" mutta jos teette lisää pankaa oma virhe
            // eli siis jos on jsonify({"success": False}) pane myös "message" kohtaan jotain
        }

    } catch (err) {
        console.error(err);
        alert("Tapahtui virhe");
        // jos tulee varmaan oli js puolella ongelma
    }
});


// CODE SUBMIT
codeForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    // jos codeformista tulee submit tämä aktivoi
    const numb1 = codeForm.num1.value;
    const numb2 = codeForm.num2.value;
    const numb3 = codeForm.num3.value;
    const numb4 = codeForm.num4.value;
    const code = numb1 + numb2 + numb3 + numb4
    // se näyttää typerältä mutta se toimii
    try {
        const res = await fetch("/verify", {
            // lähettää käyttäjän verify sivulle, aktivoi python skriptin sillä
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ code }),
        });

        const data = await res.json();
        // odottaa että python on valmis

        if (data.success) {
        $('#authModal').modal('hide');
        // piilottaa kirjaudu kohdan vaikka monet muut jutut piilotetaan pythonilla
        location.reload();
        // refreshaa sivun
        } else {
            alert(data.message || "Virhe");
            // näyttää virhe viestin
            // sama kun email submitilla
        }

    } catch (err) {
        console.error(err);
        alert("Virhe vahvistuksessa");
    }
});

addRoomForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    // tämä skripti antaa käyttäjän lisätä uusia huoneita
    // voi myös automaattisesti asettaa oletushuoneena
    const num = addRoomForm.new_room_num.value;
    const new_fav = addRoomForm.new_room_as_fav.checked;
    try {
        const res = await fetch("/room_thing", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ num: num, new_fav: new_fav }),
        });

        const data = await res.json();
        // odottaa että python on valmis

        if (data.success) {
            alert(data.message || "Onnistui!")
        $('#addRoomModal').modal('hide');
        // piilottaa huone kohdan heti kun on valmis
        location.reload();
        // refreshaa sivun
        } else {
            alert(data.message || "Virhe");
            // näyttää virhe viestin
            // sama kun email submitilla
        }

    } catch (err) {
        console.error(err);
        alert("Virhe vahvistuksessa");
    }
});


varausForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    // pane nykyversio eri funktioksi jotta voi panna 2 lisää funktiota tälle :3
    // maailman paras ohjelmoija minä olen
    // jos painaa "varaa" nappia tämä aktivoi
    const room = varausForm.room_select.value;
    // käyttäjän valittu huone
    // tämä funktio on aika samanlainen kuin code submit johon panin enemmän kommentteja
    try {

        const res = await fetch("/reserve", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                room: room
            })
        });

        const data = await res.json();

        if (data.success){
            alert("Varaus tehty!");
            location.reload();
        } else {
            alert(data.message || "Varaus epäonnistui");
        }

    } catch(err){
        console.error(err);
        alert("Virhe varauksessa");
    }

});

const inputs = document.getElementById("inputs");

inputs.addEventListener("input", function (e) {
    const target = e.target;
    const val = target.value;

    if (isNaN(val)) {
        target.value = "";
        return;
    }

    if (val != "") {
        const next = target.nextElementSibling;
        if (next) {
            next.focus();
        }
    }
});

inputs.addEventListener("keyup", function (e) {
    const target = e.target;
    const key = e.key.toLowerCase();

    if (key == "backspace" || key == "delete") {
        target.value = "";
        const prev = target.previousElementSibling;
        if (prev) {
            prev.focus();
        }
        return;
    }
});

new TomSelect("#select-email", {
    create: true,
    no_results:false,
    sortField: {
        field: "text",
        direction: "asc"
        
        
    },
    render: {
    option_create: function(data, escape) {
        return '<div class="create">lisää käyttäjä "<strong>' + 
            escape(data.input) + 
            '</strong>"</div>';
    },
    no_results: function(data, escape) {
        return '<div class="create">ei tuloksia "<strong>' + 
            escape(data.input) + 
            '</strong>"</div>';
    }
}

});

new TomSelect("#new_room_num", {
    create: true,
    persist: false,
    render: {
        option_create: function(data, escape) {
            return '<div class="create">Lisää huone "<strong>' + 
                escape(data.input) +
                '</strong>"</div>';
        },
        no_results: function(data, escape) {
            return '<div class="create">Ei tuloksia "<strong>' + 
                escape(data.input) + 
                '</strong>"</div>';
        }
    }
});