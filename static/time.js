timer = document.getElementById("timer")

// ottaa ajan viime varauksesta, sitten päivittää sitä

function stop_watch(time_since) {
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

    if (hours == 0) {
        timer.innerHTML = minutes + "m " + seconds + "s ";
    } else if (days == 0) {
        timer.innerHTML = hours + "h "
        + minutes + "m " + seconds + "s ";
    } else {
        timer.innerHTML = days + "d " + hours + "h "
        + minutes + "m " + seconds + "s ";
    }
    });
}
