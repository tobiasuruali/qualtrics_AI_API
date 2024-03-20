
# Experiment

## Design
- General Questions about Person, Political Leaning and Topics of interest

- Randomly Assigning participants to some media literacy


1. Treatment: Chatbot vs Non-Chatbot 
2. Treatment: Manipulative vs Non-Manipulative News

Regression on Results on Experimental Group vs Control Group

Dependent Variable =
Dependent Variable = How reasoned is the response of the participant to the question asked by the chatbot
Dpeending on wordcount of the response deper 

Control Group: Just conventional ad hominem attack i.e Attack on Biden from Trump

News: Manipulative 


Todos:
Send scrapers to Lucien with working
Thesis Manipulative News before end of december

Validating the news with Survey Answers (inside youtube comments)

Floating API stuff:
https://docs.s3it.uzh.ch/cloud/networking_options/#public-access-floating-ip

Experiment 
Non Manipulative News
Chatbot
Manipulative

Steps:
1. Technical implementation of chatbot (possibiliets of implementation and context taken)
2. Decide Treatments
3. Collect Data and Analysis


Rozenbeek does experiment with each manipulative trait. meaning 5 experiments. 

## Questions:

Should I adjust the API to only use one technique?$

## Feedback on Ad Classification (19.01.2023)
Validation of Output my own classification is okay for Masters
Validation of Output on Qualtrics as coder (External Validation)


Validation Confusion Matrix:
Duplicate Row(if it's multiple categories for one ad) and add the category to the row: 

```json
{
  "Emotionally Manipulative Language": [0, "The text does not evoke strong emotions directed at persuading the audience to a particular viewpoint or action."],
  "Incoherence": [1, "The text mentions buying cars on Mars, which is unrelated and nonsensical in the context of calling someone an idiot and bafoon, thus making the statement incoherent."],
  "False Dichotomies": [0, "The text does not present a situation where only two alternatives are being portrayed as the only possibilities."],
  "Scapegoating": [0, "The text does not blame a specific individual or group for larger societal problems."],
  "Ad Hominem Attacks": [1, "The text directly attacks a person’s character by calling them 'an idiot and a bafoon,' rather than addressing any specific arguments or stances they may have."]
}
```	
Take a sample of 50 ads and classify them yourself.  
- Coded classification by me  
- Classification by GPT  
Compare the two on 2 axis to prove that output is good/validated 
F1 above 0.7

If more time: Task outsiders to classify the ads and compare with GPT and my classification.

### Visualization of Classified Ads
Visualization of Manipulative technique and how well each of them have impressions (by category democratic and republican)
Visualize the usage of the techniques over time (by category democratic and republican)



## Feedback on Chatbot (19.01.2023) 

At the end explain their views (dependent variables)


Iframe should be complete Sentences

5 Responses Maximum 
Tell GPT: You have 5 interactions to convince the respondent 

Male or Female Cuter Avatar 
Cute Robot Avatar


Contrast to Political Video / Reasoned / Manipulative Chatbot
Findings: Can Manipulative chatbot be more persuasive than a politican? 

Send Andrea the prompts: Manipulative Bot AND Reasoned Chatbot 
Once finalized: We go through the survey

Fix Design Errors (Small textfield, avatar, conversation not cutting off)
Reasoned PATH

Small Pilot: Interact with Chatbot (Feedback, Errors, etc)



**To Do's:**

**MVP (Minimum Viable Product)**
- Chatbot with limit of 5 responses
- Chatbot can save all responses or "full conversation" to Qualtrics Embeded Data (Preferably in a JSON format)
- Implement a Reasoned Chatbot Variant that does not respond with manipulative techniques (Already prepared, will send to new route)
- Chatbot takes the responses of previous question into consideration when executing the prompt (f-string with previous response). Already implemented in GetRequest
- Hosted somewhere (AWS, Uni Zurich Cloud, etc)

**Nice to have**
- Prettier more modern Layout (Distinct Visuals for Chatbot and User and different colors)
- Cuter Avatar/Icons for the User and Chatbot Response (For better user engagement)
- Check if API is save from major security vulnerabilities 

**Bugs**
- Chatbot only saves/returns last response and question in iframe (Doesn't remember the whole conversation)
- Check why chatHistory clears and not scrolling
- Do not understand the logic of why chatbot remembers the whole conversation in localhost but not in Qualtrics
- iframe crops the chatbot interactions (once the chatbot remembers)
- Chatbot does not cut off after 5 responses
