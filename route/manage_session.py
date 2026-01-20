from flask import Flask, session
import connect
import hash

app = Flask(__name__,
template_folder="../templates")

app.secret_key = b'b7a9b343607593ce48fd351b034908c89a74c4eaf147811a8b0b8676992a0e0a'

# koodi käytetään kun session id tehdään, poistetaan, tai käytetään

@app.route("/", methods=["GET", "POST"])
def is_logged_in(email):
    if 'email' in session:
        return f'Logged in as {session["email"]}'
    else:
        session['email'] = email
        return 'You are not logged in'

def make_session_id(email):
    random_string = "testvalue"
    user_salt, user_hash = hash.save_password(random_string)
    # update the vgalues in the dee bee

    # tee pitkä string ja salt, tallenna häshätty string ja salt

if __name__ == "__main__":
    app.run(debug=True)
