// Change these to your liking
const q0 = 'What is your favorite movie?';
const embeddedDataTarget = 'user'; // This is the name of the embedded data field where the conversation will be stored.
const embeddedDataTarget2 =
    'bot';  // This is the name of the embedded data field where the boolean
                // flag for inappropriate questions will be stored

// Only change this if you know what you're doing
const chatbotUrl = 'https://blues-wishes-now-vocal.trycloudflare.com/chat'; // This is the URL of the chatbot.

// Get the responses to questions 6 and 10
var sessionId = "${e://Field/SessionID}"
var responseSchool = "${q://QID6/ChoiceGroup/SelectedChoices}";
var responseLeaning = "${q://QID10/ChoiceNumericEntryValue/1}";
var responseSubject = "${q://QID25/ChoiceGroup/SelectedChoicesTextEntry}"
var responseChatPath = "reasoned"

// Create the URL with parameters
var urlWithParameters = chatbotUrl +
    '?session_id=' + encodeURIComponent(sessionId) +
    '&responseSchool=' + encodeURIComponent(responseSchool) +
    '&responseLeaning=' + encodeURIComponent(responseLeaning) +
    '&responseSubject=' + encodeURIComponent(responseSubject) +
	'&responseChatpath=' + encodeURIComponent(responseChatPath);
//create variable to send in the get request for the iframe

Qualtrics.SurveyEngine.addOnload(function()
{
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
	
	//Add Chatbot Type as embeded field
	Qualtrics.SurveyEngine.setEmbeddedData("chatbot_type", responseChatPath)
	
    // Hide the Next button.
    this.hideNextButton();

});

Qualtrics.SurveyEngine.addOnReady(function()
{
	/*Place your JavaScript here to run when the page is fully displayed*/
});

Qualtrics.SurveyEngine.addOnUnload(function()
{
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
    // If the message is "conversationready", send the initial question to the prototype chatbot.
    if (msg.data == "conversation_end"){
    	unhideNextButton();
    } else if (msg.data.hasOwnProperty("user")) {
		console.log("enters here")
		user = JSON.stringify(msg.data.user); // questions
		bot = JSON.stringify(msg.data.bot); // responses
	
		// Get user and bot messages
        let userResponses = msg.data.user; // Array of user messages
        let botResponses = msg.data.bot; // Array of bot messages

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
	
	/* Option 2 
	if (msg.data == "conversation_end"){
       clickNextButton();
    } */
    // console.log(msg.data);
    // If the message contains dialogue, store it in the embedded data and click the Next button.
	

	// clickNextButton();
}


function applyBetterDefaultStyles(el) {
    // Set the iframe's display to block.
    el.style.display = 'block';

    // Set the iframe's margins to 0.
    el.style.margin = '0';

    // Set the iframe's height to 60% of the viewport height.
    el.style.height = '100vh';

    // Set the iframe's width to 100% of the viewport width.
    el.style.width = '100%';

    // Set the iframe's border to none.
    el.style.border = 'none';
}