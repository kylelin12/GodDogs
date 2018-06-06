var getFriends = function() {
    // Selects the friends table
    var table = document.getElementById("friendslist-input");

    // For each friend in the logged in user's friendslist
    // Will be stored as a variable in the javascript file
    // Database scoured through via python
    // using session['username'] as id
    for (var i = 0; i < len(friendslist); i++) {
        // Creates a row for a friend
        // Name | Status | Message | Poke
        var row = document.createElement("tr");

        // Friend's name
        // Clicking their name goes to their profile page
        var friendN = document.createElement("td");
        friendN.innerHTML = friendslist[i][0];
        row.appendChild(friendN);

        // Friend status. Placeholder for a button with unfriend action
        // Clicking button will unfriend them :(
        var friendS = document.createElement("td");
        friendS.innerHTML = friendslist[i][1];
        row.appendChild(friendS);

        // Message friend button placeholder
        // Clicking message takes you to messenger with friend highlighted
        var friendM = document.createElement("td");
        friendM.innerHTML = friendslist[i][2];
        row.appendChild(friendM);

        // Poke friend placeholder.
        // Use this to be really annoying
        // Make sure you do it at odd AM hours for best effect
        var friendP = document.createElement("td");
        friendP.innerHTML = friendslist[i][3];
        row.appendChild(friendP);

        // Appends the friend row entry to the table
        table.appendChild(row);
    }
};