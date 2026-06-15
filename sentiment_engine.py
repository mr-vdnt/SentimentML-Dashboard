import re
import datetime
import random
import uuid

positive_words = [
    'love', 'great', 'awesome', 'excellent', 'amazing', 'good', 'fast', 'responsive', 'best',
    'fantastic', 'helpful', 'immediately', 'solved', 'beautiful', 'perfect', 'happy', 'superb'
]

negative_words = [
    'bad', 'worst', 'terrible', 'crash', 'crashed', 'hate', 'slow', 'awful', 'bug', 'broken',
    'confusing', 'unsubscribing', 'fail', 'angry', 'issue', 'delayed', 'garbage'
]

def analyze_sentiment(text: str) -> str:
    lower_text = text.lower()
    score = 0
    words = re.split(r'\W+', lower_text)
    
    for w in words:
        if w in positive_words:
            score += 1.5
        if w in negative_words:
            score -= 1.5
            
    if score >= 1:
        return 'Positive'
    if score <= -1:
        return 'Negative'
    return 'Neutral'

def generate_mock_data():
    raw_comments = [
        {"text": "I absolutely love the new features! So fast and responsive. 🚀", "platform": "Twitter"},
        {"text": "The app crashed three times today. Worst update ever. 😡", "platform": "App Store"},
        {"text": "It's okay, nothing special but gets the job done.", "platform": "YouTube"},
        {"text": "Customer support was incredibly helpful and solved my issue immediately!", "platform": "Twitter"},
        {"text": "Terrible experience. The UI is confusing and slow.", "platform": "App Store"},
        {"text": "Just installed it. Let's see how it goes.", "platform": "YouTube"},
        {"text": "Highly recommended to everyone, fantastic product.", "platform": "Twitter"},
        {"text": "I hate the new subscription model. Unsubscribing.", "platform": "App Store"}
    ]
    
    comments = []
    for i, comment in enumerate(raw_comments):
        random_millis = random.randint(0, 10000000)
        date_obj = datetime.datetime.now() - datetime.timedelta(milliseconds=random_millis)
        comments.append({
            "id": f"cmd-{i}",
            "text": comment["text"],
            "platform": comment["platform"],
            "date": date_obj.isoformat(),
            "sentiment": analyze_sentiment(comment["text"])
        })
    return comments
