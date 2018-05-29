var getFriends = function() {
    var table = document.getElementById("friendslist-input");
    table.innerHTML = "";
    for (var i = 0; i < len(friendslist); i++) {
        // Creates a row for a friend
        var row = document.createElement("tr");

        // Friend's name
        var friendN = document.createElement("td");
        friendN.innerHTML = friendslist[i][0];
        row.appendChild(friendN);

        // Friend status. Placeholder for a button with message action
        var friendS = document.createElement("td");
        friendS.innerHTML = friendslist[i][1];
        row.appendChild(friendS);

        // Message friend button placeholder
        var friendM = document.createElement("td");
        friendM.innerHTML = friendslist[i][2];
        row.appendChild(friendM);

        // Poke friend placeholder.
        var friendP = document.createElement("td");
        friendP.innerHTML = friendslist[i][3];
        row.appendChild(friendP);

        // Appends the friend row entry to the table
        table.appendChild(row);
    }
};