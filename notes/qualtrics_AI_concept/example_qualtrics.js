// Change these to your liking
const q0 = 'What is your favorite movie?';
const embeddedDataTarget = 'dialogue'; // This is the name of the embedded data field where the conversation will be stored.
const embeddedDataTarget2 =
    'flagged';  // This is the name of the embedded data field where the booelan
                // flag for inappropriate questions will be stored

// Only change this if you know what you're doing
const chatbotUrl = 'https://chatty-surveys-palm.uc.r.appspot.com'; // This is the URL of the chatbot.

/**
 * Create the iframe that contains the prototype and listen for message events from it.
 */

Qualtrics.SurveyEngine.addOnload(function () {
    // Set the initial embedded data.
    Qualtrics.SurveyEngine.setEmbeddedData(embeddedDataTarget, JSON.stringify([]));

    // Create the iframe element.
    var el = document.createElement('iframe');

    // Apply some default styles to the iframe.
    applyBetterDefaultStyles(el);

    // Set the iframe's source to the chatbot URL.
    el.src = chatbotUrl;

    // Set the iframe's ID to "ifr".
    el.id = "ifr";

    // Append the iframe element to the question element.
    $(this.questionId).appendChild(el);

    // Add a listener for message events from the prototype chatbot.
    window.addEventListener('message', receiveMessage);

    // Hide the Next button.
    this.hideNextButton();
});

Qualtrics.SurveyEngine.addOnUnload(function () {
    // Remove the listener for message events from the prototype chatbot.
    window.removeEventListener('message', receiveMessage);
});

Qualtrics.SurveyEngine.addOnReady(function () {
});

function unhideNextButton() {
    // Unhide the Next button.
    document.getElementById('NextButton').style.display = 'default';
}

function clickNextButton() {
    // Click the Next button.
    document.getElementById('NextButton').click();
}

function receiveMessage(msg) {
    // If the message is "conversationready", send the initial question to the prototype chatbot.
    if (msg.data == "conversationready"){
        el = document.getElementById("ifr")
        el.contentWindow.postMessage(q0, "*");
    }
    console.log(msg.data);
    // If the message contains dialogue, store it in the embedded data and click the Next button.
    if (msg.data.hasOwnProperty('dialogue')) {
        dialogue = JSON.stringify(msg.data.dialogue);
        flagged = JSON.stringify(msg.data.flagged);
        Qualtrics.SurveyEngine.setEmbeddedData(embeddedDataTarget, dialogue);

        Qualtrics.SurveyEngine.setEmbeddedData(embeddedDataTarget2, flagged);

        clickNextButton();
    }
}

function applyBetterDefaultStyles(el) {
    // Set the iframe's display to block.
    el.style.display = 'block';

    // Set the iframe's margins to 0.
    el.style.margin = '0';

    // Set the iframe's height to 60% of the viewport height.
    el.style.height = '60vh';

    // Set the iframe's width to 100% of the viewport width.
    el.style.width = '100%';

    // Set the iframe's border to none.
    el.style.border = 'none';
}
