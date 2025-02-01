document.getElementById('joinQueueForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;

    // Send the POST request to the server
    fetch('/join_queue', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);

            // Open a new tab to show the user's queue status
            window.open(data.queue_url, '_blank');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
