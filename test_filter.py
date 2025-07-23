#!/usr/bin/env python3
"""
Test script to demonstrate the word filtering functionality
Shows how the bot detects and replaces various forms of bad words
"""

from word_filter import WordFilter

def test_filter_examples():
    """Test the word filter with various examples"""
    word_filter = WordFilter()
    
    # Test cases showing various obfuscation methods
    test_messages = [
        "This is a normal message",  # No bad words
        "What the fuck is going on?",  # Direct bad word
        "What the f*ck is happening?",  # Asterisk obfuscation
        "That's f.u.c.k.i.n.g awesome!",  # Dot separation
        "This sh1t is crazy",  # Number substitution
        "Don't be such a b-i-t-c-h",  # Dash separation
        "That's some bull sh!t right there",  # Multiple obfuscations
        "F U C K this situation",  # Spaced out
        "Holy sh*t that's amazing",  # Mixed obfuscation
        "What a d@mn good day",  # Symbol substitution
        "This is some cr@p",  # @ symbol
        "Stop being so b1tchy",  # Leetspeak
        "That's fuuuuucking incredible",  # Repeated characters
        "FUCK YEAH!",  # All caps
        "FuCk ThIs CrAp",  # Mixed case
        "This is a55 backwards",  # Leetspeak for ass
        "What the h3ll is that?",  # Number for letter
    ]
    
    print("🤖 Discord Profanity Filter Bot - Word Filter Test")
    print("=" * 60)
    
    for i, message in enumerate(test_messages, 1):
        filtered_message, has_bad_words = word_filter.filter_message(message)
        
        print(f"\n{i}. Test Message:")
        print(f"   Original: {message}")
        print(f"   Filtered: {filtered_message}")
        print(f"   Has Bad Words: {'✅ Yes' if has_bad_words else '❌ No'}")
        
        if has_bad_words:
            print(f"   Status: 🧼 CLEANED")
        else:
            print(f"   Status: ✨ CLEAN")
    
    # Show statistics
    stats = word_filter.get_statistics()
    print(f"\n📊 Filter Statistics:")
    print(f"   Total Bad Words: {stats['total_bad_words']}")
    print(f"   Total Patterns: {stats['total_patterns']}")
    print(f"   Average Patterns per Word: {stats['average_patterns_per_word']}")
    print(f"   Obfuscation Characters: {stats['obfuscation_chars']}")
    print(f"   Separators: {stats['separators']}")

if __name__ == "__main__":
    test_filter_examples()