timer = document.getElementById("timer")

// ottaa ajan viime varauksesta, sitten päivittää sitä

function stop_watch(time_since) {
    if (time_since == "vapaa") {
        timer.innerHTML = "vapaa"
    } else {
        var countDownDate = new Date(time_since).getTime();

        // Update the count down every 1 second
        var x = setInterval(function() {

        // Get today's date and time
        var now = new Date().getTime();

        var distance = now - countDownDate;

        // Time calculations for days, hours, minutes and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        if (days != 0) {
            timer.innerHTML = days + " päivää";
        } else if (hours != 0) {
            timer.innerHTML = hours + " tuntia";
        } else if (minutes != 0) {
            timer.innerHTML = minutes + " minuuttia";
        } else {
            timer.innerHTML = seconds + " sekunttia";
        }
        },200);
    }
}
