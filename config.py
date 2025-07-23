"""
Configuration file for the Discord Profanity Filter Bot
Contains bad word mappings and bot settings
"""

# Mapping of bad words to their funny replacements
BAD_WORD_REPLACEMENTS = {
    # F-word variations
    'fuck': 'fluff',
    'fucking': 'fluffing',
    'fucked': 'fluffed',
    'fucker': 'fluffer',
    'fck': 'fluff',
    'fuk': 'fluff',
    'fock': 'fluff',
    'fvck': 'fluff',
    
    # S-word variations
    'shit': 'poopoo',
    'shitting': 'poopooing',
    'shitted': 'poopooed',
    'shitty': 'poopy',
    'sht': 'poopoo',
    'shyt': 'poopoo',
    
    # B-word variations
    'bitch': 'beach',
    'bitching': 'beaching',
    'bitchy': 'beachy',
    'btch': 'beach',
    'b1tch': 'beach',
    
    # A-word variations
    'ass': 'booty',
    'arse': 'booty',
    'asshole': 'bootyhole',
    'a55': 'booty',
    'azz': 'booty',
    
    # D-word variations
    'damn': 'darn',
    'damned': 'darned',
    'damning': 'darning',
    'dammit': 'darnit',
    'damnit': 'darnit',
    
    # H-word variations
    'hell': 'heck',
    'hellish': 'heckish',
    'h3ll': 'heck',
    
    # C-word variations (strong profanity)
    'cunt': 'cutie',
    'c*nt': 'cutie',
    'cnt': 'cutie',
    
    # P-word variations
    'piss': 'pee',
    'pissed': 'peed',
    'pissing': 'peeing',
    'p1ss': 'pee',
    
    # D-word variations (slur context)
    'dick': 'banana',
    'dickhead': 'bananahead',
    'd1ck': 'banana',
    'dik': 'banana',
    
    # Additional common profanity
    'bastard': 'buddy',
    'bloody': 'silly',
    'crap': 'crud',
    'prick': 'pickle',
    'slut': 'sweetie',
    'whore': 'person',
    'retard': 'silly',
    'retarded': 'silly',
    'gay': 'happy',  # Only when used as slur context
    'fag': 'stick',
    'faggot': 'bundle',
    'nigger': 'buddy',
    'nigga': 'buddy',
    'n1gger': 'buddy',
    'n1gga': 'buddy',
    
    # Internet slang profanity
    'wtf': 'what the fluff',
    'stfu': 'shush',
    'gtfo': 'go away',
    'omfg': 'oh my gosh',
    'lmfao': 'lol',
    'rofl': 'haha',
    
    # Indian Hindi profanity and slang
    # Family-related curses (most common in Hindi)
    'madarchod': 'buddy',
    'mc': 'buddy',
    'behanchod': 'friend',
    'bc': 'friend',
    'maa ka bhosada': 'mother dear',
    'mkb': 'mother dear',
    
    # Anatomical/sexual terms
    'randi': 'friend',
    'lauda': 'banana',
    'lund': 'banana',
    'chut': 'flower',
    'gaandu': 'buddy',
    'gandu': 'buddy',
    
    # General Hindi insults
    'bhosadike': 'friend',
    'bhosdi': 'friend',
    'bhadwe': 'buddy',
    'bhadwa': 'buddy',
    'haramkhor': 'silly person',
    'harami': 'silly person',
    'hijada': 'person',
    'hijra': 'person',
    'saala': 'friend',
    'sala': 'friend',
    'saali': 'friend',
    'sali': 'friend',
    
    # Mild Hindi curse equivalents
    'ullu ka pattha': 'silly goose',
    'kutta': 'doggy',
    'kutti': 'puppy',
    'gadha': 'donkey',
    'pagal': 'silly',
    'paagal': 'silly',
    
    # Religious/caste slurs (replaced with neutral terms)
    'bhagwan': 'friend',  # When used as curse
    'allah': 'friend',    # When used as curse
    
    # Common Hinglish combinations
    'madarchod sala': 'silly buddy',
    'behanchod gandu': 'silly friend',
    'randi rona': 'silly crying',
    'chutiya': 'silly person',
    'chutia': 'silly person',
    
    # South Indian additions
    'poda': 'go away',
    'maire': 'friend',
    'kameeni': 'silly person',
    'kamina': 'silly person',
    'badmaash': 'troublemaker',
    'badmash': 'troublemaker',
    
    # Punjabi additions
    'bhen di': 'sister dear',
    'phuddi': 'flower',
    'choot': 'flower',
    'pencho': 'friend',
    'penchod': 'friend',
    
    # Bengali additions
    'magir chele': 'silly person',
    'tor maa': 'your mother',
    'chudbo': 'silly',
    
    # Tamil additions  
    'ommala': 'friend',
    'punda': 'friend',
    'koothi': 'friend',
    
    # Telugu additions
    'dengey': 'silly',
    'lanjakoduku': 'silly person',
    'rascal': 'troublemaker',
    
    # ========== EXPANDED COMPREHENSIVE BAD WORDS (400+ Additional) ==========
    # Based on comprehensive online profanity databases and modern slang
    
    # Sexual/Explicit terms that were missing
    'acrotomophilia': 'inappropriate behavior', 'algophilia': 'weird behavior', 'anilingus': 'intimate activity',
    'autoerotic': 'private time', 'auto erotic': 'private time', 'babeland': 'special place', 'ball gag': 'mouth accessory', 
    'ball kicking': 'sports move', 'ball licking': 'cleaning activity', 'ball sucking': 'vacuum activity',
    'bangbros': 'music group', 'bang bros': 'music group', 'bangbus': 'transportation', 'bang bus': 'transportation', 
    'bareback': 'no saddle riding', 'barely legal': 'just allowed', 'bastinado': 'foot massage', 'bdsm': 'lifestyle choice',
    'bean flicker': 'vegetable preparer', 'beaver cleaver': 'wood chopper', 'beaver lips': 'animal mouth',
    'bellend': 'friendly person', 'birdlock': 'cage device', 'blow your load': 'empty your truck',
    'blowjob': 'wind job', 'blow job': 'wind job', 'blow-job': 'wind job', 'blumpkin': 'pumpkin variety', 
    'bone smuggler': 'dog toy carrier', 'booty call': 'treasure hunt', 'brown shower': 'mud rain', 'brown showers': 'mud rain',
    'bukkake': 'art technique', 'bullet vibe': 'fast feeling', 'bum chum': 'bottom friend', 'bum-chum': 'bottom friend',
    'bum driller': 'construction worker', 'butt pilot': 'airplane captain', 'butt pirate': 'treasure hunter',
    'butt-pirate': 'treasure hunter', 'butt rider': 'horse person', 'butt robber': 'sneaky person', 
    'butthole engineer': 'construction expert', 'camel toe': 'desert footprint', 'carpet muncher': 'vacuum cleaner',
    'carpetmuncher': 'vacuum cleaner', 'chocolate rosebud': 'sweet flower', 'chocolate rosebuds': 'sweet flowers',
    'circlejerk': 'group meeting', 'circle-jerk': 'group meeting', 'cleveland steamer': 'train service', 
    'clover clamps': 'garden tools', 'cleveland accordion': 'musical instrument', 'cleveland hot waffle': 'breakfast food',
    
    # Comprehensive ass/arse variations that were missing
    '4r5e': 'horse', '5h1t': 'poopoo', '5hit': 'poopoo', 'a55': 'donkey', 'a55hole': 'silly person',
    'a_s_s': 'donkey', 'ar5e': 'booty', 'ash0le': 'silly person', 'ash0les': 'silly people',
    'ass-fucker': 'donkey rider', 'ass-hat': 'silly hat', 'ass-pirate': 'treasure hunter',
    'assbag': 'silly bag', 'assbagger': 'bag person', 'assbandit': 'sneaky person', 'assbang': 'loud noise',
    'assbanged': 'made noise', 'assbanger': 'noise maker', 'assbangs': 'loud sounds', 'assbite': 'small nibble',
    'assblaster': 'loud speaker', 'assclown': 'funny person', 'asscock': 'rooster', 'asscowboy': 'ranch hand',
    'asscracker': 'code breaker', 'assface': 'funny face', 'assfuck': 'donkey friend', 'assfucker': 'donkey rider',
    'assfukka': 'donkey buddy', 'assgoblin': 'silly creature', 'assh0le': 'silly person', 'assh0lez': 'silly people',
    'asshat': 'silly hat', 'asshead': 'silly head', 'assho1e': 'silly person', 'assholz': 'silly people',
    'asshopper': 'jumping person', 'asshore': 'beach person', 'assjacker': 'car person', 'assjockey': 'rider',
    'asskiss': 'friendly greeting', 'asskisser': 'friendly person', 'assklown': 'funny person', 'asslick': 'cleaning',
    'asslicker': 'cleaner', 'asslover': 'donkey fan', 'assman': 'donkey person', 'assmaster': 'expert person',
    'assmonkey': 'silly animal', 'assmunch': 'snack time', 'assmuncher': 'snacker', 'assnigger': 'buddy',
    'asspacker': 'moving person', 'asspirate': 'treasure hunter', 'asspuppies': 'cute animals',
    'assrammer': 'construction worker', 'assranger': 'park worker', 'assshit': 'silly poopoo',
    'assshole': 'silly person', 'asssucker': 'vacuum', 'asswad': 'silly person', 'asswhole': 'complete silly',
    'asswhore': 'silly person', 'asswipe': 'cleaning cloth', 'asswipes': 'cleaning supplies',
    
    # Comprehensive bitch variations that were missing
    'b!+ch': 'beach', 'b!tchin': 'beaching', 'b*tch': 'beach', 'bi+ch': 'beach', 'bi7ch': 'beach',
    'biatch': 'beach', 'bitchass': 'beach donkey', 'bitched': 'beached', 'bitcher': 'beacher',
    'bitchers': 'beachers', 'bitchez': 'beaches', 'bitchslap': 'beach slap', 'bitchtit': 'beach bird',
    'biteme': 'bite food', 'beeyotch': 'beach', 'beotch': 'beach', 'beatch': 'beach',
    
    # Comprehensive cock/rooster variations
    'c u n t': 'silly person', 'c-0-c-k': 'rooster', 'c-o-c-k': 'rooster', 'c-u-n-t': 'silly person',
    'c.0.c.k': 'rooster', 'c.o.c.k.': 'rooster', 'c.u.n.t': 'silly person', 'c0ck': 'rooster',
    'c0cks': 'roosters', 'c0cksucker': 'rooster friend', 'c0k': 'rooster', 'cawk': 'rooster', 'cawks': 'roosters',
    'cockbite': 'rooster bite', 'cockblock': 'rooster block', 'cockblocker': 'rooster blocker',
    'cockburger': 'rooster burger', 'cockcowboy': 'rooster rider', 'cockface': 'rooster face',
    'cockfight': 'rooster fight', 'cockfucker': 'rooster friend', 'cockhead': 'rooster head',
    'cockholster': 'rooster holder', 'cockjockey': 'rooster rider', 'cockknob': 'rooster knob',
    'cockknocker': 'door knocker', 'cockknoker': 'door knocker', 'cocklicker': 'rooster cleaner',
    'cocklover': 'rooster fan', 'cockmaster': 'rooster expert', 'cockmongler': 'rooster person',
    'cockmongruel': 'rooster food', 'cockmonkey': 'rooster animal', 'cockmunch': 'rooster snack',
    'cockmuncher': 'rooster snacker', 'cocknob': 'rooster knob', 'cocknose': 'rooster nose',
    'cocknugget': 'rooster nugget', 'cockqueen': 'rooster royalty', 'cockrider': 'rooster rider',
    'cockshit': 'rooster poopoo', 'cocksman': 'rooster person', 'cocksmith': 'rooster maker',
    'cocksmoker': 'rooster smoker', 'cocksucer': 'rooster friend', 'cocksuck': 'rooster activity',
    'cocksucked': 'rooster sucked', 'cocksucker': 'rooster friend', 'cocksucking': 'rooster activity',
    'cocksucks': 'rooster activities', 'cocksuka': 'rooster friend', 'cocksukka': 'rooster friend',
    'cocktease': 'rooster tease', 'cokmuncher': 'rooster snacker', 'coksucka': 'rooster friend',
    
    # Comprehensive cunt variations
    'cunteyed': 'silly eyed', 'cuntface': 'silly face', 'cuntfuck': 'silly friend', 'cuntfucker': 'silly buddy', 
    'cunthole': 'silly hole', 'cunthunter': 'silly hunter', 'cuntlick': 'silly lick', 'cuntlicker': 'silly licker', 
    'cuntlicking': 'silly licking', 'cuntrag': 'silly rag', 'cunts': 'silly people', 'cuntslut': 'silly person', 
    'cuntsucker': 'silly sucker', 'cuntz': 'silly people', 'cunn': 'silly person', 'cunnie': 'silly person',
    'cunnilingus': 'intimate activity', 'cunntt': 'silly person', 'cunny': 'silly person',
    
    # Additional body part references
    'boob': 'chest', 'boobs': 'chest', 'b00b': 'chest', 'b00bs': 'chest', 'b00bies': 'birds', 'b00biez': 'birds', 
    'b00bz': 'birds', 'tits': 'birds', 'titties': 'small birds', 'nipple': 'small point', 'nipples': 'small points',
    'penis': 'banana', 'vagina': 'flower', 'clitoris': 'body part', 'clitorus': 'body part', 'clit': 'body part',
    'cl1t': 'body part', 'clits': 'body parts', 'clitty': 'small body part',
    
    # Sexual activity references
    'masturbate': 'self care', 'masturbation': 'self care', 'masturbating': 'self caring', 'jerk off': 'relax',
    'jerking off': 'relaxing', 'jack off': 'relax', 'jacking off': 'relaxing', 'wank': 'relax', 'wanking': 'relaxing',
    'wanker': 'relaxer', 'orgasm': 'climax', 'orgasms': 'climaxes', 'climax': 'peak', 'ejaculate': 'release',
    'ejaculation': 'release', 'ejaculating': 'releasing', 'cum': 'arrive', 'cumming': 'arriving', 'cuming': 'arriving',
    'cumshot': 'arrival shot', 'cumshots': 'arrival shots', 'facial': 'face treatment', 'creampie': 'dessert',
    
    # Modern internet slang and toxicity
    'simp': 'simple person', 'simping': 'being simple', 'thot': 'thoughtful person', 'sus': 'suspicious', 
    'sussy': 'suspicious', 'triggered': 'activated', 'karen': 'manager seeker', 'chad': 'confident person', 
    'incel': 'lonely person', 'femcel': 'lonely person', 'coomer': 'addicted person', 'gooner': 'obsessed person', 
    'scrote': 'male person', 'pickme': 'attention seeker', 'milf': 'attractive mom', 'dilf': 'attractive dad', 
    'normie': 'normal person', 'newfag': 'new person', 'oldfag': 'experienced person', 'wagecuck': 'worker', 
    'neet': 'not employed', 'roastie': 'experienced person', 'femoid': 'female person', 'moid': 'male person',
    'based': 'authentic', 'redpilled': 'aware', 'bluepilled': 'naive', 'blackpilled': 'pessimistic',
    'whitepilled': 'optimistic', 'cope': 'manage', 'seethe': 'frustrated', 'dilate': 'expand',
    
    # Gaming toxicity terms
    'noob': 'new player', 'newbie': 'new player', 'scrub': 'beginner', 'tryhard': 'dedicated player',
    'sweaty': 'competitive', 'camper': 'strategic player', 'hacker': 'skilled player', 'cheater': 'rule breaker',
    'toxic': 'negative', 'griefing': 'bothering', 'trolling': 'joking around', 'flaming': 'criticizing',
    'rekt': 'defeated', 'pwned': 'owned', 'owned': 'defeated', 'destroyed': 'beaten', 'clapped': 'defeated',
    'trash': 'poor quality', 'garbage': 'poor quality', 'ez': 'easy', 'gg ez': 'good game easy',
    
    # Racial slurs and variations (replaced with friendly terms)
    'beaner': 'coffee lover', 'beaners': 'coffee lovers', 'chink': 'person', 'chinks': 'people', 'chinky': 'person',
    'gook': 'person', 'gooks': 'people', 'spic': 'person', 'spics': 'people', 'wetback': 'person', 'wetbacks': 'people',
    'kike': 'person', 'kikes': 'people', 'honky': 'person', 'honkies': 'people', 'cracker': 'snack', 'crackers': 'snacks',
    'redneck': 'country person', 'hillbilly': 'mountain person', 'white trash': 'person', 'ghetto': 'neighborhood',
    'hood rat': 'neighborhood person', 'thug': 'tough person', 'gangster': 'group member', 'pimp': 'manager',
    
    # LGBTQ+ slurs (replaced with neutral/positive terms)
    'dyke': 'strong person', 'bulldyke': 'tough person', 'bulldike': 'tough person', 'lesbo': 'person', 'lezzie': 'person',
    'homo': 'person', 'homos': 'people', 'queer': 'unique person', 'tranny': 'person', 'shemale': 'person',
    'ladyboy': 'person', 'trap': 'surprise', 'sissy': 'sensitive person', 'pansy': 'flower',
    
    # Religious slurs
    'kike': 'person', 'kyke': 'person', 'christ killer': 'person', 'raghead': 'person', 'towelhead': 'person',
    'camel jockey': 'desert rider', 'sand nigger': 'desert person', 'haji': 'pilgrim', 'muzzie': 'person',
    
    # Body shaming terms
    'fatass': 'large person', 'fatty': 'large person', 'lardass': 'large person', 'whale': 'sea mammal',
    'pig': 'farm animal', 'cow': 'farm animal', 'hippo': 'river horse', 'buffalo': 'prairie animal',
    'twig': 'thin branch', 'stick': 'thin wood', 'skeleton': 'bones', 'anorexic': 'thin person',
    'midget': 'short person', 'dwarf': 'small person', 'giant': 'tall person', 'freak': 'unique person',
    
    # Disability slurs
    'retard': 'silly person', 'retarded': 'silly', 'tard': 'silly person', 'mental': 'thoughtful',
    'psycho': 'excited person', 'crazy': 'creative', 'insane': 'enthusiastic', 'nuts': 'snacks',
    'bonkers': 'energetic', 'loony': 'silly person', 'wacko': 'funny person', 'spaz': 'energetic person',
    
    # Drug references
    'pot': 'cooking vessel', 'weed': 'garden plant', 'dope': 'silly person', 'crack': 'opening', 'coke': 'soda',
    'meth': 'chemistry', 'heroin': 'medicine', 'cocaine': 'white powder', 'ecstasy': 'happiness', 'lsd': 'letters',
    'molly': 'person name', 'acid': 'chemistry', 'shrooms': 'mushrooms', 'hash': 'food dish',
}

# Characters commonly used for obfuscation (including Indian romanization)
OBFUSCATION_CHARS = {
    'a': ['@', '4', 'á', 'à', 'â', 'ā', 'ă', 'aa'],
    'e': ['3', 'é', 'è', 'ê', 'ē', 'ě', 'ee'],
    'i': ['1', '!', 'í', 'ì', 'î', 'ī', 'ii', 'ee'],
    'o': ['0', 'ó', 'ò', 'ô', 'ō', 'ő', 'oo', 'au'],
    'u': ['ú', 'ù', 'û', 'ū', 'ů', 'oo', 'ou'],
    's': ['5', '$', 'š', 'ss', 'z'],
    't': ['7', '+', 'th', 'tt'],
    'l': ['1', '|', 'll'],
    'g': ['9', '6', 'gh', 'gg'],
    'c': ['(', '<', 'ch', 'k', 'ck'],
    'k': ['|<', 'c', 'ck', 'kh'],
    'n': ['|\|', 'nn', 'nh'],
    'b': ['8', '|3', 'bh', 'bb'],
    'd': ['|)', 'dh', 'dd'],
    'f': ['|=', 'ph', 'ff'],
    'h': ['|-|', '#', 'kh', 'gh', 'th', 'bh', 'dh', 'ph'],
    'm': ['|\\/|', 'mm'],
    'p': ['|>', 'ph', 'pp'],
    'r': ['|2', 'rr'],
    'v': ['\\/', '|/', 'w'],
    'w': ['\\/\\/', 'vv', 'v'],
    'x': ['><', 'ks'],
    'y': ['\\|/', 'yy'],
    'z': ['2', 's', 'zz'],
    # Indian language specific romanization patterns
    'aa': ['a', '@', '4'],
    'ee': ['i', '1', 'e'],
    'oo': ['u', 'o', '0'],
    'ch': ['c', '<', 'chh'],
    'kh': ['k', 'x'],
    'gh': ['g', '9'],
    'th': ['t', '7'],
    'bh': ['b', '8'],
    'dh': ['d', '|)'],
    'ph': ['f', 'p'],
    'au': ['o', '0', 'ow'],
}

# Common separators used in obfuscation
SEPARATORS = ['.', '-', '_', '*', ' ', '|', '/', '\\', '+', '=', '~', '^']

# Bot configuration
WEBHOOK_CACHE_SIZE = 50  # Maximum number of webhooks to cache
LOG_LEVEL = 'INFO'  # Logging level

# Regex flags for case-insensitive matching
REGEX_FLAGS = 'IGNORECASE'

# Minimum word length to consider for filtering (avoids false positives)
MIN_WORD_LENGTH = 3

# Maximum message length for processing (Discord limit is 2000)
MAX_MESSAGE_LENGTH = 2000

# Rate limiting settings
MAX_MESSAGES_PER_MINUTE = 60
WEBHOOK_RATE_LIMIT_DELAY = 1  # seconds between webhook requests

# Channel types to monitor (excludes DMs)
MONITORED_CHANNEL_TYPES = [
    'text',
    'news',  # announcement channels
    'public_thread',
    'private_thread',
    'news_thread'
]
