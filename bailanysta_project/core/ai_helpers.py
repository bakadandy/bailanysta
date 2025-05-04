import random
from django.conf import settings
import spacy
import re
import os
from nltk.corpus import stopwords
import nltk

# Try to download NLTK data if needed
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Try to load spacy model - fallback to a simpler approach if not available
try:
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except (ImportError, OSError):
    SPACY_AVAILABLE = False
    print("Spacy model not available. Using simpler text processing.")

# Set to False to force mock implementations
USE_MOCK = True

def extract_keywords(text, max_keywords=5):
    """Extract keywords from text using spaCy or a simple approach"""
    if not SPACY_AVAILABLE:
        # Simple approach: just get non-stopwords
        try:
            stop_words = set(stopwords.words('english'))
            words = re.findall(r'\b\w+\b', text.lower())
            keywords = [word for word in words if word not in stop_words and len(word) > 3]
            # Return the most frequent ones
            from collections import Counter
            return [word for word, _ in Counter(keywords).most_common(max_keywords)]
        except:
            # If that fails too, just return random words from the text
            words = re.findall(r'\b\w+\b', text)
            return list(set([word for word in words if len(word) > 3]))[:max_keywords]
    
    # Use spaCy for better keyword extraction
    doc = nlp(text)
    keywords = []
    for token in doc:
        if (not token.is_stop and 
            not token.is_punct and 
            token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and
            len(token.text) > 3):
            keywords.append(token.text.lower())
    
    # Get most common keywords
    from collections import Counter
    return [word for word, _ in Counter(keywords).most_common(max_keywords)]

# Content generation templates
POST_TEMPLATES = [
    "{topic} has been on my mind lately. What are your thoughts on this? {hashtags}",
    "Just had an interesting discussion about {topic}! It's fascinating how it impacts our daily lives. {hashtags}",
    "Anyone else excited about the future of {topic}? The possibilities seem endless! {hashtags}",
    "Today I learned something new about {topic}. It's amazing how much there is to discover. {hashtags}",
    "Question for everyone: What's your experience with {topic}? I'd love to hear your perspective! {hashtags}",
    "Working on a new project related to {topic}. Can't wait to share more details soon! {hashtags}",
    "The more I learn about {topic}, the more questions I have. Anyone else feel the same? {hashtags}",
    "Thinking about how {topic} is changing our world. What do you think the future holds? {hashtags}",
    "There's something special about {topic} that keeps drawing me back. Anyone else fascinated by this? {hashtags}",
    "Just read an interesting article about {topic}. It's opened my eyes to new perspectives! {hashtags}"
]

TOPIC_CATEGORIES = {
    "tech": ["AI", "blockchain", "programming", "cybersecurity", "virtual reality", "machine learning", "web development", "coding", "data science", "automation"],
    "lifestyle": ["fitness", "wellness", "mindfulness", "nutrition", "self-care", "productivity", "remote work", "travel", "personal growth", "meditation"],
    "business": ["entrepreneurship", "startup", "marketing", "e-commerce", "leadership", "innovation", "business strategy", "remote teams", "digital marketing", "freelancing"],
    "creative": ["photography", "writing", "design", "art", "music", "filmmaking", "storytelling", "content creation", "creativity", "inspiration"],
    "social": ["community", "networking", "social media", "online events", "virtual meetups", "collaboration", "remote communication", "digital relationships", "online communities", "virtual networking"]
}

HASHTAG_CATEGORIES = {
    "tech": ["#tech", "#innovation", "#digital", "#future", "#coding", "#developer", "#programming", "#AI", "#technology", "#startup"],
    "lifestyle": ["#lifestyle", "#wellness", "#mindfulness", "#health", "#selfcare", "#balance", "#growth", "#journey", "#motivation", "#habits"],
    "business": ["#business", "#entrepreneur", "#success", "#strategy", "#growth", "#leadership", "#startup", "#innovation", "#marketing", "#networking"],
    "creative": ["#creative", "#inspiration", "#design", "#art", "#creativity", "#create", "#artist", "#maker", "#passion", "#vision"],
    "social": ["#community", "#connect", "#together", "#social", "#network", "#sharing", "#conversation", "#engage", "#discussion", "#collaboration"]
}

def mock_generate_post(prompt, max_length=280):
    """Generate a fake post based on the prompt"""
    # Extract category from prompt if possible
    category = "tech"  # default
    for cat, keywords in TOPIC_CATEGORIES.items():
        if any(keyword.lower() in prompt.lower() for keyword in keywords):
            category = cat
            break
    
    # Generate relevant hashtags
    hashtags = " ".join(random.sample(HASHTAG_CATEGORIES[category], 3))
    
    # Choose a template and fill it
    template = random.choice(POST_TEMPLATES)
    post = template.format(topic=prompt, hashtags=hashtags)
    
    # Ensure it's not too long
    if len(post) > max_length:
        post = post[:max_length-3] + "..."
        
    return post

def mock_suggest_hashtags(content, max_hashtags=5):
    """Generate fake hashtags based on content"""
    # Try to extract keywords from the content
    try:
        keywords = extract_keywords(content, max_hashtags)
        return ["#" + keyword for keyword in keywords]
    except:
        # Fallback to predefined categories
        for cat, keywords in TOPIC_CATEGORIES.items():
            if any(keyword.lower() in content.lower() for keyword in keywords):
                return random.sample(HASHTAG_CATEGORIES[cat], min(max_hashtags, len(HASHTAG_CATEGORIES[cat])))
        
        # If nothing matches, return general hashtags
        return random.sample(["#trending", "#thoughts", "#share", "#connect", "#discuss", "#interesting", "#community"], max_hashtags)

def generate_post_content(prompt, max_length=280):
    """Generate a social media post about the given prompt"""
    return mock_generate_post(prompt, max_length)

def suggest_hashtags(content, max_hashtags=5):
    """Suggest hashtags for the given content"""
    return mock_suggest_hashtags(content, max_hashtags)