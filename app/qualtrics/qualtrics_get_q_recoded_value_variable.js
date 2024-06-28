
// Getting the Recoded Value from a Question Reply
Qualtrics.SurveyEngine.addOnload(function()
{
	/*Place your JavaScript here to run when the page loads*/

});

Qualtrics.SurveyEngine.addOnReady(function()
{
	/*Place your JavaScript here to run when the page is fully displayed*/

});

Qualtrics.SurveyEngine.addOnUnload(function()
{
	/*Place your JavaScript here to run when the page is unloaded*/

});
Qualtrics.SurveyEngine.addOnPageSubmit(function() {
    var qobj = this;
    var vnames = [];
    jQuery.each(qobj.getSelectedChoices(), function(i, val) {
        vnames.push(qobj.getChoiceVariableName(val));
    });
    Qualtrics.SurveyEngine.setEmbeddedData("varResponseSubjectPosition", vnames.join(", "));
});