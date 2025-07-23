#!/usr/bin/env python3
"""
Test script to demonstrate Indian Hindi profanity filtering functionality
Shows how the bot detects and replaces various forms of Indian bad words
"""

from word_filter import WordFilter

def test_indian_filter_examples():
    """Test the word filter with various Indian profanity examples"""
    word_filter = WordFilter()
    
    # Test cases showing various Indian profanity and obfuscation methods
    test_messages = [
        "Namaste, how are you doing today?",  # Clean message
        "Tu madarchod hai yaar",  # Direct Hindi profanity
        "Don't be such a r@ndi",  # Symbol obfuscation
        "What a ch*tiya person",  # Asterisk obfuscation
        "Behen.chod.sala.kutta",  # Dot separation
        "M C BC hai tu",  # Abbreviations
        "That guy is such a g@@ndu",  # Multiple symbols
        "Har4mi insaan hai",  # Number substitution
        "Ch-u-t-i-y-a behavior",  # Dash separation
        "MADARCHOD SALA KAMEENA",  # All caps Hindi
        "bh@dwe k@ put@r",  # Multiple @ symbols
        "Such a b@dm@@sh person",  # Mixed obfuscation
        "Tu kitna pagal hai yaar",  # Mild Hindi curse
        "Ullu ka pattha samajhta hai",  # Hindi idiom curse
        "Kutta kamina hai wo",  # Multiple Hindi words
        "Stop this r@ndi ron@",  # Hinglish combination
        "What a pench0d guy",  # Punjabi with number
        "Tu punda hai re",  # Tamil profanity
        "Dengey ra babu",  # Telugu profanity
        "Magir chele kothakar",  # Bengali profanity
        "Bhen di takki",  # Punjabi family curse
        "Lauda lasan karta hai",  # Anatomical reference
        "Choot marne wala",  # Vulgar Hindi
        "Gaandu giri mat kar",  # Hindi slang
        "Bhosadi ke bacche",  # Strong Hindi profanity
    ]
    
    print("🇮🇳 Indian Profanity Filter Test - Hindi/Regional Languages")
    print("=" * 70)
    
    for i, message in enumerate(test_messages, 1):
        filtered_message, has_bad_words = word_filter.filter_message(message)
        
        print(f"\n{i}. Test Message:")
        print(f"   Original: {message}")
        print(f"   Filtered: {filtered_message}")
        print(f"   Has Indian Profanity: {'✅ Yes' if has_bad_words else '❌ No'}")
        
        if has_bad_words:
            print(f"   Status: 🧼 CLEANED")
        else:
            print(f"   Status: ✨ CLEAN")
    
    # Show updated statistics with Indian words
    stats = word_filter.get_statistics()
    print(f"\n📊 Updated Filter Statistics (with Indian Languages):")
    print(f"   Total Bad Words: {stats['total_bad_words']}")
    print(f"   Total Patterns: {stats['total_patterns']}")
    print(f"   Average Patterns per Word: {stats['average_patterns_per_word']}")
    print(f"   Obfuscation Characters: {stats['obfuscation_chars']}")
    print(f"   Separators: {stats['separators']}")
    
    print(f"\n🌏 Supported Languages:")
    print(f"   • Hindi (हिन्दी) - Most common profanity")
    print(f"   • Punjabi (ਪੰਜਾਬੀ) - Regional variations")
    print(f"   • Bengali (বাংলা) - Eastern India")
    print(f"   • Tamil (தமிழ்) - South India")
    print(f"   • Telugu (తెలుగు) - Andhra Pradesh/Telangana")
    print(f"   • Hinglish - Hindi-English combinations")

if __name__ == "__main__":
    test_indian_filter_examples()