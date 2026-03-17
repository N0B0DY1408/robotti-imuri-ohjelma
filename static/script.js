const signupForm = document.getElementById("signupForm");
const codeForm = document.getElementById("codeForm");
const checkbox = document.getElementById("check1");

const emailView = document.getElementById("emailView");
const codeView = document.getElementById("codeView");
const successView = document.getElementById("successView");

const modalTitle = document.getElementById("modalTitle");



// EMAIL SUBMIT
signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("select-email").value;
    const number = document.getElementById("roomSelect").value;
    const isChecked = checkbox.checked;

    if (!isChecked) {
        alert("Sinun täytyy hyväksyä ehdot ennen jatkamista.");
        return; // Estää fetchin
    }

    try {
        const res = await fetch("/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: email, number: number }),
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
        $('#authModal').modal('hide');
        location.reload();
        } else {
            alert("Väärä koodi");
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

const Varaus = document.getElementById("Varaus");

Varaus.addEventListener("click", async () => {

    const room = document.getElementById("robottidropdown").value;

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

new TomSelect("#robottidropdown", {
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