"""
Advanced word filtering system with smart detection of obfuscated profanity
Handles various obfuscation methods including spacing, symbols, and character substitution
"""

import re
import logging
from typing import Tuple, Dict, List, Set
from config import BAD_WORD_REPLACEMENTS, OBFUSCATION_CHARS, SEPARATORS, MIN_WORD_LENGTH

logger = logging.getLogger(__name__)

class WordFilter:
    def __init__(self):
        """Initialize the word filter with compiled regex patterns"""
        self.bad_words = BAD_WORD_REPLACEMENTS
        self.obfuscation_chars = OBFUSCATION_CHARS
        self.separators = SEPARATORS
        self.min_word_length = MIN_WORD_LENGTH
        
        # Compile regex patterns for efficient matching
        self.patterns = self._compile_patterns()
        
        logger.info(f"WordFilter initialized with {len(self.bad_words)} bad words and {len(self.patterns)} patterns")
    
    def _escape_regex_chars(self, text: str) -> str:
        """Escape special regex characters in text"""
        return re.escape(text)
    
    def _create_obfuscation_pattern(self, word: str) -> str:
        """Create a regex pattern that matches obfuscated versions of a word"""
        pattern_parts = []
        
        for char in word.lower():
            if char in self.obfuscation_chars:
                # Create character class with all possible substitutions
                substitutions = [re.escape(char)] + [re.escape(sub) for sub in self.obfuscation_chars[char]]
                pattern_parts.append(f"[{''.join(substitutions)}]")
            else:
                pattern_parts.append(re.escape(char))
        
        # Join with optional separators between characters
        separator_pattern = f"[{''.join(re.escape(sep) for sep in self.separators)}]*"
        full_pattern = separator_pattern.join(pattern_parts)
        
        # Add word boundaries and make it case-insensitive
        return f"\\b{full_pattern}\\b"
    
    def _create_spacing_pattern(self, word: str) -> str:
        """Create pattern for spaced out words (e.g. 'f u c k')"""
        chars = list(word.lower())
        # Allow 1-3 spaces or other separators between each character
        separator_pattern = f"[{''.join(re.escape(sep) for sep in self.separators + [' '])}]{{1,3}}"
        return f"\\b{separator_pattern.join(re.escape(char) for char in chars)}\\b"
    
    def _create_mixed_case_pattern(self, word: str) -> str:
        """Create pattern for mixed case variations (e.g. 'FuCk', 'FUCK')"""
        pattern_chars = []
        for char in word:
            if char.isalpha():
                pattern_chars.append(f"[{char.upper()}{char.lower()}]")
            else:
                pattern_chars.append(re.escape(char))
        return f"\\b{''.join(pattern_chars)}\\b"
    
    def _create_repeated_char_pattern(self, word: str) -> str:
        """Create pattern for repeated characters (e.g. 'fuuuuck', 'shiiit')"""
        pattern_chars = []
        for char in word.lower():
            if char in 'aeiou':  # Vowels often repeated
                pattern_chars.append(f"{re.escape(char)}+")
            else:
                pattern_chars.append(re.escape(char))
        return f"\\b{''.join(pattern_chars)}\\b"
    
    def _compile_patterns(self) -> Dict[str, List[re.Pattern]]:
        """Compile all regex patterns for efficient matching"""
        patterns = {}
        
        for bad_word, replacement in self.bad_words.items():
            if len(bad_word) < self.min_word_length:
                continue
                
            word_patterns = []
            
            # 1. Exact match (case-insensitive)
            exact_pattern = f"\\b{re.escape(bad_word)}\\b"
            word_patterns.append(re.compile(exact_pattern, re.IGNORECASE))
            
            # 2. Obfuscation pattern (character substitution)
            obfuscation_pattern = self._create_obfuscation_pattern(bad_word)
            word_patterns.append(re.compile(obfuscation_pattern, re.IGNORECASE))
            
            # 3. Spacing pattern
            spacing_pattern = self._create_spacing_pattern(bad_word)
            word_patterns.append(re.compile(spacing_pattern, re.IGNORECASE))
            
            # 4. Mixed case pattern (redundant with IGNORECASE, but kept for clarity)
            mixed_case_pattern = self._create_mixed_case_pattern(bad_word)
            word_patterns.append(re.compile(mixed_case_pattern))
            
            # 5. Repeated character pattern
            repeated_char_pattern = self._create_repeated_char_pattern(bad_word)
            word_patterns.append(re.compile(repeated_char_pattern, re.IGNORECASE))
            
            # 6. Common leetspeak variations
            leetspeak_word = bad_word
            leetspeak_replacements = {
                'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7', 'l': '1'
            }
            for original, leet in leetspeak_replacements.items():
                leetspeak_word = leetspeak_word.replace(original, leet)
            
            if leetspeak_word != bad_word:
                leetspeak_pattern = f"\\b{re.escape(leetspeak_word)}\\b"
                word_patterns.append(re.compile(leetspeak_pattern, re.IGNORECASE))
            
            patterns[bad_word] = word_patterns
        
        return patterns
    
    def _find_bad_words_in_text(self, text: str) -> List[Tuple[str, str, int, int]]:
        """
        Find all bad words in text and return their positions and replacements
        Returns list of (original_word, replacement, start_pos, end_pos)
        """
        found_words = []
        
        for bad_word, replacement in self.bad_words.items():
            if bad_word not in self.patterns:
                continue
                
            for pattern in self.patterns[bad_word]:
                matches = pattern.finditer(text)
                for match in matches:
                    found_words.append((
                        match.group(),  # The actual matched text
                        replacement,    # The replacement word
                        match.start(),  # Start position
                        match.end()     # End position
                    ))
        
        # Sort by position to handle overlapping matches
        found_words.sort(key=lambda x: x[2])
        
        # Remove overlapping matches (keep the first one found)
        filtered_words = []
        last_end = -1
        
        for word_info in found_words:
            if word_info[2] >= last_end:  # No overlap
                filtered_words.append(word_info)
                last_end = word_info[3]
        
        return filtered_words
    
    def filter_message(self, message: str) -> Tuple[str, bool]:
        """
        Filter a message and replace bad words with funny alternatives
        Returns (filtered_message, contains_bad_words)
        """
        if not message or len(message) > 2000:  # Discord message limit
            return message, False
        
        # Find all bad words in the message
        bad_words_found = self._find_bad_words_in_text(message)
        
        if not bad_words_found:
            return message, False
        
        # Replace bad words from right to left to maintain positions
        filtered_message = message
        for original, replacement, start_pos, end_pos in reversed(bad_words_found):
            filtered_message = (
                filtered_message[:start_pos] + 
                replacement + 
                filtered_message[end_pos:]
            )
        
        logger.debug(f"Filtered message: {len(bad_words_found)} bad words replaced")
        return filtered_message, True
    
    def test_word_detection(self, test_word: str) -> Dict[str, bool]:
        """
        Test word detection against all patterns (for debugging)
        Returns dict of pattern_type -> matched
        """
        results = {}
        
        for bad_word, patterns in self.patterns.items():
            if bad_word.lower() in test_word.lower():
                for i, pattern in enumerate(patterns):
                    pattern_types = [
                        'exact', 'obfuscation', 'spacing', 'mixed_case', 
                        'repeated_char', 'leetspeak'
                    ]
                    pattern_type = pattern_types[min(i, len(pattern_types) - 1)]
                    
                    match = pattern.search(test_word)
                    results[f"{bad_word}_{pattern_type}"] = bool(match)
        
        return results
    
    def get_statistics(self) -> Dict[str, int]:
        """Get statistics about the word filter"""
        total_patterns = sum(len(patterns) for patterns in self.patterns.values())
        
        return {
            'total_bad_words': len(self.bad_words),
            'total_patterns': total_patterns,
            'average_patterns_per_word': total_patterns // len(self.bad_words) if self.bad_words else 0,
            'obfuscation_chars': len(self.obfuscation_chars),
            'separators': len(self.separators)
        }
