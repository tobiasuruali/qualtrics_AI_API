from pydantic import BaseModel
from enum import Enum


class ChatInput(BaseModel):
    user_input: str
    session_id: str


class ResponseSubject(str, Enum):
    CC = "Climate change and environmental issues"
    PC = "Political and democratic instability"
    IB = "Immigration and border security"
    IR = "International relations and national security"


class PolicyViews(str, Enum):
    # Environmental Policies
    UA = "Urgent Action: Prioritize immediate and extensive environmental policies, even if it impacts jobs and the economy."
    BA = "Balanced Approach: Support environmental policies but balance them with economic and job considerations."
    EF = "Economic Focus: Prioritize economic growth and job preservation over immediate enactment of extensive environmental policies."
    CL = "Climate Skepticism: Question the urgency or extent of climate change and oppose significant policies that could impact the economy."

    # Concerns about Donald Trump's Influence
    SC = "Significant Concern: A potential political return of Donald Trump is a serious concern for American democracy."
    CC = "Cautiously Concerned: Have reservations about Donald Trump's influence, but trust in the democratic process to manage these concerns."
    NNT = "Neutral or No Threat: Do not see Donald Trump's potential return as a significant threat to American democracy."
    SDT = "Supportive: A potential return of Donald Trump is positive and beneficial for American democracy."

    # Immigration Policies
    OP = "Open Policy: Support highly open immigration policies with minimal restrictions on entry into the United States."
    CP = "Controlled Policy: Favor immigration but with reasonable controls and vetting to manage it effectively."
    RP = "Restrictive Policy: Believe current immigration levels are too high and advocate for stricter policies to reduce immigration."
    ZT = "Zero Tolerance: Support reinstating the immigration policies from the Trump administration, including travel bans, deportations, and stricter border controls."

    # National Security Postures
    AP = "Aggressive Posture: Advocate for a strong and aggressive stance against perceived national security threats from Russia and China."
    DE = "Diplomatic Engagement: Support a firm but diplomatic approach, prioritizing dialogue and negotiations with Russia and China."
    EOC = "Emphasis on Cooperation: Favor focusing more on cooperation and collaboration rather than confrontation with Russia and China."
    LTV = "Limited Threat View: Do not view Russia and China as significant threats and oppose aggressive policies towards them."
