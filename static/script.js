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



// EMAIL SUBMIT
signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    // jos signupformista tulee submit tämä aktivoi

    const email = document.getElementById("select-email").value;
    const number = document.getElementById("roomSelect").value;
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
            body: JSON.stringify({ email: email, number: number }),
            // vetää sivulta käyttäjän paneman emailin ja huonenumeron
            // kohdista joinka idt ovat "roomSelect" ja "select-email"
        });
        const data = await res.json();
        // odottaa että app.py palauttaa jsonify({"success": True})

        if (data.success) {
            emailView.style.display = "none";
            codeView.style.display = "block";
            modalTitle.innerText = "Syötä vahvistuskoodi";
            // näyttää käyttäjälle kohdan jossa voi panna koodin
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
    const code = codeForm.code.value;

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

new TomSelect("#roomSelect", {
    create: true,
    no_results:false,
    sortField: {
        field: "text",
        direction: "asc"
        
        
    },
    render: {
    option_create: function(data, escape) {
        return '<div class="create">lisää huone "<strong>' + 
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


Varaus.addEventListener("click", async () => {
    // jos painaa "varaa" nappia tämä aktivoi
    const room = document.getElementById("huonedropdown").value;
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

new TomSelect("#huonedropdown", {
    create: true,
    persist: false,
    sortField: {
        field: "text",
        direction: "asc"
    },
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
