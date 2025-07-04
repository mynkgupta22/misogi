import re
from collections import Counter
from typing import List, Dict, Any

def get_sentiment(text: str) -> str:
    """
    A simple sentiment analysis implementation using keyword matching.
    Returns 'positive', 'negative', or 'neutral'.
    """
    positive_words = {
        'good', 'great', 'excellent', 'beneficial', 'helpful', 'positive',
        'improve', 'better', 'best', 'success', 'successful', 'benefit',
        'essential', 'important', 'crucial', 'significant', 'efficient'
    }
    
    negative_words = {
        'bad', 'poor', 'terrible', 'harmful', 'negative', 'worst',
        'difficult', 'hard', 'problem', 'threat', 'dangerous', 'risk',
        'challenge', 'concern', 'critical', 'urgent', 'struggle'
    }
    
    words = text.lower().split()
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
    
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    return 'neutral'

def extract_keywords(text: str, limit: int = 5) -> List[str]:
    """
    Extract keywords using a simple frequency-based approach.
    Excludes common stop words.
    """
    stop_words = {
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
        'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
        'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they',
        'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one',
        'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out',
        'if', 'about', 'who', 'get', 'which', 'go', 'me', 'is', 'are',
        'was', 'were', 'has', 'can', 'more', 'now'
    }
    
    # Clean text and split into words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Remove stop words and count frequencies
    words = [word for word in words if word not in stop_words and len(word) > 2]
    word_freq = Counter(words)
    
    # Return top keywords
    return [word for word, _ in word_freq.most_common(limit)]

def calculate_readability(text: str) -> Dict[str, Any]:
    """
    Calculate basic readability metrics including word count,
    sentence count, and average words per sentence.
    """
    # Split into sentences (simple implementation)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Count words
    words = re.findall(r'\b\w+\b', text)
    
    # Calculate metrics
    sentence_count = len(sentences)
    word_count = len(words)
    avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
    
    return {
        'sentence_count': sentence_count,
        'word_count': word_count,
        'avg_words_per_sentence': round(avg_words_per_sentence, 2)
    }

def analyze_text(text: str) -> Dict[str, Any]:
    """
    Perform complete text analysis including sentiment,
    keywords, and readability metrics.
    """
    sentiment = get_sentiment(text)
    keywords = extract_keywords(text)
    readability = calculate_readability(text)
    
    return {
        'sentiment': sentiment,
        'keywords': keywords,
        'readability': readability
    } 