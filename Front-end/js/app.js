function getSummary() {
    let url = document.getElementById('urlInput').value;
    
    fetch('/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            document.getElementById('feedbackArea').innerText = data.error;
        } else {
            document.getElementById('feedbackArea').innerText = data.summary;
        }
    })
    .catch(error => {
        document.getElementById('feedbackArea').innerText = "An error occurred: " + error.message;
    });
}
