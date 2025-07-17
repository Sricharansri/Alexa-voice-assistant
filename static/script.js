function startListening() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    document.getElementById("responseText").innerText = "Speech recognition not supported.";
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.start();

  recognition.onresult = function (event) {
    const command = event.results[0][0].transcript;
    console.log("You said:", command);

    fetch('/command', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ command: command })
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById("responseText").innerText = data.response;
    })
    .catch(error => {
      console.error("Fetch error:", error);
      document.getElementById("responseText").innerText = "Server error. Try again.";
    });
  };

  recognition.onerror = function (event) {
    console.error("Speech recognition error:", event.error);
    document.getElementById("responseText").innerText = "Speech recognition error: " + event.error;
  };

  recognition.onend = function () {
    console.log("Speech recognition ended");
  };
}
