let roomCount = 1; // Initial number of rooms
const maxRooms = {{ data.available_rooms }}; // Maximum number of rooms allowed
const maxPeoplePerRoom = {{ room.space_adult}} + {{ room.space_child}};
const maxChildrenWithOneAdult = {{room.space_child}};

function updateRoomCount(delta) {
    const roomInput = document.getElementById("room-count");
    let currentRooms = parseInt(roomInput.value);
    let newRoomCount = currentRooms + delta;

    if (newRoomCount > maxRooms) {
        alert(`We have only ${maxRooms} rooms left.`);
        return;
    }

    if (newRoomCount < 1) {
        alert(`You must book at least 1 room.`);
        return;
    }

    // Update the room count
    roomInput.value = newRoomCount;

    if (delta > 0) {
        addNewRoom();
    } else if (delta < 0) {
        removeRoom(roomCount); // Remove the last room
    }
}

function addNewRoom() {
    if (roomCount >= maxRooms) {
        alert(`You can only add up to ${maxRooms} rooms.`);
        return;
    }

    roomCount++;
    const roomContainer = document.getElementById("room-container1");

    const newRoom = document.createElement("div");
    newRoom.classList.add("room"); // Add the "room" class
    newRoom.id = `room-${roomCount}`; // Set the ID for the room

    // Set the inner HTML with proper structure and classes
    newRoom.innerHTML = `
        <div class="room-header">
            <span>Room ${roomCount}</span>
            <button class="remove-room-btn" onclick="removeRoom(${roomCount})">REMOVE</button>
        </div>
        <div class="capacity">
            <div class="control-group">
                <label>Nº of adults</label>
                <div class="control-buttons">
                    <button onclick="updateAdults(${roomCount}, -1)">-</button>
                    <input type="text" id="adult-count-${roomCount}" value="2" readonly>
                    <button onclick="updateAdults(${roomCount}, 1)">+</button>
                </div>
            </div>
            <div class="control-group">
                <label>Nº of children <span>(Up to 12 years old)</span></label>
                <div class="control-buttons">
                    <button onclick="updateChildren(${roomCount}, -1)">-</button>
                    <input type="text" id="child-count-${roomCount}" value="0" readonly>
                    <button onclick="updateChildren(${roomCount}, 1)">+</button>
                </div>
            </div>
        </div>
    `;

    // Append the new room to the container
    roomContainer.appendChild(newRoom);

    // Update the room count in the input field
    document.getElementById("room-count").value = roomCount;
}

function removeRoom(roomId) {
    if (roomCount <= 1) {
        alert("You must have at least one room.");
        return;
    }

    const roomToRemove = document.getElementById(`room-${roomId}`);
    if (roomToRemove) {
        roomToRemove.remove();
        roomCount--;

        // Update room numbers for all remaining rooms
        const remainingRooms = document.querySelectorAll(".room");
        let index = 0;
        remainingRooms.forEach((room) => {
            index++;
            room.id = `room-${index}`;
            room.querySelector(".room-header span").textContent = `Room ${index}`;
            room.querySelector(".remove-room-btn").setAttribute("onclick", `removeRoom(${index})`);
            room.querySelectorAll("button").forEach((btn) => {
                btn.setAttribute("onclick", btn.getAttribute("onclick").replace(/\d+/, index));
            });
        });

        // Update the room count display
        document.getElementById("room-count").value = index;
        roomCount = index;
    }
}

function updateAdults(roomId, delta) {
    const adultInput = document.getElementById(`adult-count-${roomId}`);
    const childInput = document.getElementById(`child-count-${roomId}`);
    const currentAdults = parseInt(adultInput.value);
    const currentChildren = parseInt(childInput.value);

    let newAdults = Math.max(1, currentAdults + delta);
    let totalPeople = newAdults + currentChildren;

    if (totalPeople > maxPeoplePerRoom) {
        newAdults -= 1;
        alert(`Maximum ${maxPeoplePerRoom} people per room.`);
    }

    adultInput.value = newAdults;

    // Restrict children when adults are 1
    if (newAdults === 1 && currentChildren > maxChildrenWithOneAdult) {
        childInput.value = maxChildrenWithOneAdult;
        alert(`Only ${maxChildrenWithOneAdult} children allowed when 1 adult.`);
    }
}

function updateChildren(roomId, delta) {
    const adultInput = document.getElementById(`adult-count-${roomId}`);
    const childInput = document.getElementById(`child-count-${roomId}`);
    const currentAdults = parseInt(adultInput.value);
    const currentChildren = parseInt(childInput.value);

    let newChildren = Math.max(0, currentChildren + delta);
    let totalPeople = currentAdults + newChildren;

    if (totalPeople > maxPeoplePerRoom) {
        newChildren -= 1;
        alert(`Maximum ${maxPeoplePerRoom} people per room.`);
    }

    if (currentAdults === 1 && newChildren > maxChildrenWithOneAdult) {
        newChildren = maxChildrenWithOneAdult;
        alert(`Only ${maxChildrenWithOneAdult} children allowed.`);
    }

    childInput.value = newChildren;
}
function submitBooking() {
    // Gather personal details
    const title = document.querySelector('input[name="title"]:checked')?.value;
    const firstName = document.getElementById("first-name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const country = document.getElementById("country").value;

    // Validate personal details
    if (!title || !firstName  || !email || !phone) {
        alert("Please fill in all personal details.");
        return;
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert("Please enter a valid email address.");
        return;
    }

    // Gather date details
    const fromDate = document.getElementById("from_date").value;
    const toDate = document.getElementById("to_date").value;

    // Validate date fields
    if (!fromDate || !toDate) {
        alert("Please select both From Date and To Date.");
        return;
    }

    if (new Date(fromDate) > new Date(toDate)) {
        alert("From Date cannot be later than To Date.");
        return;
    }

    // Gather room booking data
    const rooms = document.querySelectorAll(".room");
    const roomData = [];

    rooms.forEach((room, index) => {
        const roomDetails=document.querySelector('.room-details');
        const roomId = room.id.replace("room-", ""); // Extract room ID from the container's ID
        const roomName =roomDetails.querySelector('.card-title').textContent;

        const adultCount = parseInt(document.getElementById(`adult-count-${roomId}`).value, 10) || 0;
        const childCount = parseInt(document.getElementById(`child-count-${roomId}`).value, 10) || 0;

        roomData.push({
            room: parseInt(roomId, 10), // Room ID
            name: roomName,            // Room name
            adults: adultCount,        // Number of adults
            children: childCount,      // Number of children
        });
    });
    

    // Ensure at least one room is booked
    if (roomData.length === 0) {
        alert("Please book at least one room.");
        return;
    }

    // Combine data into a single payload
    const payload = {
        personal_details: {
            title,
            first_name: firstName,
            email,
            phone,
            country,
        },
        booking_dates: {
            from_date: fromDate,
            to_date: toDate,
        },
        rooms: roomData,
    };

    // Get CSRF token
    const csrfToken = document.getElementById("csrf_token").value;

    // Send the data to the server without waiting for a response
    fetch("/submit_booking", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(payload),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.redirect_url) {
                window.location.href = data.redirect_url; // Perform the redirect
            } else if (data.error) {
                alert(`Error: ${data.error}`);
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });
    

}
  