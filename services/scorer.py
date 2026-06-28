import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def score_sentiment(headline, company):
    prompt = f"""You are a financial sentiment analyser.

Analyse this news headline about {company} and classify its sentiment.

Headline: "{headline}"

Respond in this exact format and nothing else:
SENTIMENT: [POSITIVE/NEGATIVE/NEUTRAL]
CONFIDENCE: [0.0 to 1.0]
REASON: [one short sentence]"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    text = response.choices[0].message.content.strip()

    sentiment = "NEUTRAL"
    confidence = 0.5
    reason = ""

    for line in text.split("\n"):
        if line.startswith("SENTIMENT:"):
            sentiment = line.split(":")[1].strip()
        elif line.startswith("CONFIDENCE:"):
            try:
                confidence = float(line.split(":")[1].strip())
            except:
                confidence = 0.5
        elif line.startswith("REASON:"):
            reason = line.split(":", 1)[1].strip()

    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "reason": reason
    }

if __name__ == "__main__":
    test_headlines = [
        "Zomato reports record quarterly revenue, beats analyst expectations",
        "Zomato faces backlash over delivery partner working conditions",
        "Zomato launches new subscription plan for frequent users"
    ]

    for headline in test_headlines:
        result = score_sentiment(headline, "Zomato")
        print(f"\nHeadline: {headline}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Reason: {result['reason']}")