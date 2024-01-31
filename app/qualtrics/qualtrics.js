// Change these to your liking
const embeddedDataTarget = 'user'; // Name of the embedded data field for the conversation
const embeddedDataTarget2 = 'bot';  // Name of the embedded data field for the boolean flag
const embeddedConversation = 'conversation';

// Only change this if you know what you're doing
const chatbotUrl = 'https://qualtrics-ai-api-c5bg57d2aa-uc.a.run.app/chat'; // Chatbot URL

// Get the responses to the questions
var sessionId = "${e://Field/SessionID}";
var responsePartyIDBase = "${q://QID6/ChoiceGroup/SelectedChoices}"; // Q6 response
var responsePartyIDExtra = "${q://QID28/ChoiceGroup/SelectedChoices}" +
                           "${q://QID29/ChoiceGroup/SelectedChoices}" +
                           "${q://QID30/ChoiceGroup/SelectedChoices}"; // One of Q28, Q29, Q30
var responsePolViews = "${q://QID25/ChoiceTextEntryValue}"; // PolViews
var responseSubject = "${q://QID31/ChoiceGroup/SelectedChoices}"; // Subject
var responseSubjectPosition = "${q://QID32/ChoiceGroup/SelectedChoices}" +
                              "${q://QID33/ChoiceGroup/SelectedChoices}" +
                              "${q://QID34/ChoiceGroup/SelectedChoices}" +
                              "${q://QID35/ChoiceGroup/SelectedChoices}"; // Subject Position
var responseChatPath = "reasoned"; // Hardcoded

// Log the variables for debugging
console.log("Session ID: ", sessionId);
console.log("Response Party ID Base: ", responsePartyIDBase);
console.log("Response Party ID Extra: ", responsePartyIDExtra);
console.log("Response Pol Views: ", responsePolViews);
console.log("Response Subject: ", responseSubject);
console.log("Response Subject Position: ", responseSubjectPosition);
console.log("Response Chat Path: ", responseChatPath);

// Concatenate the base and extra parts for responsePartyID
var responsePartyID = responsePartyIDBase + responsePartyIDExtra;

console.log("Response Party ID: ", responsePartyID);

// Create the URL with parameters
var urlWithParameters = chatbotUrl +
    '?session_id=' + encodeURIComponent(sessionId || '') +
    '&responsePartyID=' + encodeURIComponent((responsePartyIDBase || '') + (responsePartyIDExtra || '')) +
    '&responsePolViews=' + encodeURIComponent(responsePolViews || '') +
    '&responseSubject=' + encodeURIComponent(responseSubject || '') +
    '&responseSubjectPosition=' + encodeURIComponent(responseSubjectPosition || '') +
    '&responseChatpath=' + encodeURIComponent(responseChatPath || '');

console.log("URL with Parameters: ", urlWithParameters);


Qualtrics.SurveyEngine.addOnload(function() {
    // Set the initial embedded data.
    Qualtrics.SurveyEngine.setJSEmbeddedData(embeddedDataTarget, JSON.stringify([]));

    // Create the iframe element.
    var el = document.createElement('iframe');

    // Apply some default styles to the iframe.
    applyBetterDefaultStyles(el);

    // Set the iframe's source to the chatbot URL.
    el.src = urlWithParameters;

    // Set the iframe's ID to "ifr".
    el.id = "ifr";

    // Append the iframe element to the question element.
    $(this.questionId).appendChild(el);

    // Add a listener for message events from the prototype chatbot.
    window.addEventListener('message', receiveMessage);
    
    // Add Chatbot Type as embedded field
    Qualtrics.SurveyEngine.setEmbeddedData("chatbot_type", responseChatPath);

    // Hide the Next button.
    this.hideNextButton();
});

Qualtrics.SurveyEngine.addOnReady(function() {
    /* Place your JavaScript here to run when the page is fully displayed */
});

Qualtrics.SurveyEngine.addOnUnload(function() {
    // Remove the listener for message events from the prototype chatbot.
    window.removeEventListener('message', receiveMessage);
});

function unhideNextButton() {
    // Unhide the Next button.
    document.getElementById('NextButton').style.display = 'inline';
}

function clickNextButton() {
    // Click the Next button.
    document.getElementById('NextButton').click();
}

function receiveMessage(msg) {
    if (msg.data == "conversation_end") {
        // Option 1: Unhide the Next button
        unhideNextButton();

        // Option 2: Automatically click the Next button
        // clickNextButton();
    } else if (msg.data.hasOwnProperty("user")) {
        // Processing the message data
        processMessageData(msg.data);
    }
}

function processMessageData(data) {
    // Process and store message data
    let userResponses = data.user; // Array of user messages
    let botResponses = data.bot; // Array of bot messages

    // Save individual user and bot responses
    Qualtrics.SurveyEngine.setEmbeddedData(embeddedDataTarget, JSON.stringify(userResponses));
    Qualtrics.SurveyEngine.setEmbeddedData(embeddedDataTarget2, JSON.stringify(botResponses));

    // Combine and format the entire conversation
    let conversation = {
        user: userResponses,
        bot: botResponses
    };
    let conversationJSON = JSON.stringify(conversation);

    // Set the entire conversation in a separate embedded field
    Qualtrics.SurveyEngine.setEmbeddedData("conversation", conversationJSON);
}

function applyBetterDefaultStyles(el) {
    // Set the iframe's display to block.
    el.style.display = 'block';

    // Set the iframe's margins to 0.
    el.style.margin = '0';

    // Set the iframe's height to 60% of the viewport height.
    el.style.height = '80vh';

    // Set the iframe's width to 100% of the viewport width.
    el.style.width = '100%';

    // Set the iframe's border to none.
    el.style.border = 'none';
}
