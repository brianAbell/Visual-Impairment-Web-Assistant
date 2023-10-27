/**
 * Fetch a summary of the given webpage URL from the backend.
 */
function getSummary() {
    let url = document.getElementById('urlInput').value;

    // Send a POST request to the Flask server with the URL
    fetch('/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }),
    })
    .then(response => {
        // Check if the response from the server is okay
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        // Parse the JSON response
        return response.json();
    })
    .then(data => {
        // Check if there's an error in the response
        if (data.error) {
            document.getElementById('feedbackArea').innerText = data.error;
        } else {
            // Display the summarized content in the textarea
            document.getElementById('feedbackArea').innerText = data.summary;
        }
    })
    .catch(error => {
        // Handle any errors that occurred during the fetch
        document.getElementById('feedbackArea').innerText = "An error occurred: " + error.message;
    });
}
