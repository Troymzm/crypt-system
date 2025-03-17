import re
import string

# 英文字母频率分布 (基于标准英文文本)
ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09,
    'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23,
    'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}

# 常见英文单词字典
ENGLISH_WORDS = {
    2: ["am", "an", "as", "at", "by", "do", "go", "he", "if", "in", "is", "it", "me", "my", 
        "no", "of", "on", "or", "so", "to", "up", "us", "we"],
    3: ["ago", "all", "and", "any", "but", "can", "day", "end", "had", "her", "his", "how", 
        "let", "may", "not", "now", "one", "our", "out", "own", "she", "the","was", "you"],
    4: ["also", "away", "best", "dear", "down", "even", "ever", "have", "just", "many", 
        "most", "much", "need", "next", "none", "once", "only", "over", "past", "same", 
        "such", "this", "than", "then", "that", "upon", "what", "very", "wish", "your"],
    5: ["about", "above", "after", "again", "ahead", "along", "could", "least", "later", 
        "often", "other", "shall", "since", "there", "where", "which", "under", "until", "would"],
    6: ["across", "before", "behind", "belong", "beside", "double", "during", "enough", 
        "except", "hardly", "merely", "rather", "really", "seldom", "though", "unless"],
    7: ["because"]
}

class SubstitutionCipher:
    def __init__(self):
        self.ciphertext = ""
        self.key_mapping = {}  # 映射关系: 密文字母 -> 明文字母
        self.reverse_mapping = {}  # 反向映射: 明文字母 -> 密文字母
        self.frequency = {}
        self.words = []
        
    def encrypt(self, plaintext, key):
        """使用给定密钥加密明文"""
        if len(key) != 26 or not all(c in string.ascii_lowercase for c in key):
            print("错误：密钥必须是26个小写字母的排列")
            return None
        
        mapping = dict(zip(string.ascii_lowercase, key))
        result = ""
        for char in plaintext:
            if char.lower() in mapping:
                result += mapping[char.lower()]
            else:
                result += char
        return result
    
    def decrypt(self, ciphertext, key):
        """使用给定密钥解密密文"""
        if len(key) != 26 or not all(c in string.ascii_lowercase for c in key):
            print("错误：密钥必须是26个小写字母的排列")
            return None
        
        reverse_mapping = {v: k for k, v in zip(string.ascii_lowercase, key)}
        result = ""
        for char in ciphertext:
            if char in reverse_mapping:
                result += reverse_mapping[char].upper()
            else:
                result += char
        return result
    
    def load_ciphertext(self, text):
        """加载密文并进行初始处理"""
        self.ciphertext = text.lower()
        self.key_mapping = {}
        self.reverse_mapping = {}
        self.analyze_frequency()
        self.extract_words()
        
    def analyze_frequency(self):
        """分析密文中字母频率"""
        text = re.sub(r'[^a-z]', '', self.ciphertext)
        if not text:
            self.frequency = {}
            return
            
        total = len(text)
        self.frequency = {char: text.count(char) / total * 100 for char in set(text)}
        
    def extract_words(self):
        """从密文中提取单词"""
        self.words = re.findall(r'[a-z]+', self.ciphertext)
    
    def suggest_mapping(self):
        """基于频率分析提供映射建议"""
        suggestions = []
        sorted_freq = sorted(self.frequency.items(), key=lambda x: x[1], reverse=True)
        sorted_eng = sorted(ENGLISH_FREQ.items(), key=lambda x: x[1], reverse=True)
        
        for i, (cipher_char, _) in enumerate(sorted_freq[:10]):
            if cipher_char not in self.key_mapping:
                eng_char = sorted_eng[i][0].lower()
                suggestions.append(f"建议：'{cipher_char}' 可能对应 '{eng_char.upper()}'，频率: {self.frequency[cipher_char]:.2f}%")
        
        return suggestions
    
    def suggest_patterns(self):
        """基于单词分析提供映射建议"""
        suggestions = []
        decrypted_words = []
        
        # 分析单个字母的单词
        single_letters = [word for word in self.words if len(word) == 1]
        if single_letters:
            for letter in set(single_letters):
                if not (letter in self.key_mapping):
                    suggestions.append(f"单字母单词 '{letter}' 可能是 'A' 或 'I'")
                
        # 分析常见单词模式
        for word in set(self.words):
            length = len(word)
            
            # 检查单词是否已完全破译
            fully_decrypted = True
            decrypted_word = ""
            for char in word:
                if char in self.key_mapping:
                    decrypted_word += self.key_mapping[char]
                else:
                    fully_decrypted = False
                    break
            
            # 如果单词已完全破译，添加到已破译单词列表
            if fully_decrypted:
                decrypted_words.append(f"'{word}' -> '{decrypted_word}'")
                continue
                
            if length in ENGLISH_WORDS and length <= 7:
                pattern = self.get_word_pattern(word)
                matches = []
                
                # 考虑已经破译的字母
                known_mapping = {}
                for i, char in enumerate(word):
                    if char in self.key_mapping:
                        known_mapping[i] = self.key_mapping[char]
                
                for eng_word in ENGLISH_WORDS[length]:
                    # 检查已知字母是否匹配
                    skip = False
                    for i, expected_char in known_mapping.items():
                        if i < len(eng_word) and expected_char != eng_word[i].upper():
                            skip = True
                            break
                    
                    if skip:
                        continue
                        
                    if self.get_word_pattern(eng_word.lower()) == pattern:
                        # 检查当前映射是否与已知映射冲突
                        consistent = True
                        temp_mapping = {}
                        
                        for c_char, e_char in zip(word, eng_word.lower()):
                            if c_char in self.key_mapping and self.key_mapping[c_char] != e_char.upper():
                                consistent = False
                                break
                            if e_char.upper() in self.reverse_mapping and self.reverse_mapping[e_char.upper()] != c_char:
                                consistent = False
                                break
                            temp_mapping[c_char] = e_char.upper()
                        
                        if consistent:
                            matches.append(f"{eng_word.upper()}")
                
                if matches and len(matches) <= 5:
                    suggestions.append(f"单词 '{word}' 可能是: {', '.join(matches)}")
                
        return suggestions
    
    def get_word_pattern(self, word):
        """获取单词的模式"""
        word = word.lower()
        pattern = []
        seen = {}
        
        for char in word:
            if char not in seen:
                seen[char] = len(seen)
            pattern.append(str(seen[char]))
        
        return '.'.join(pattern)
    
    def update_mapping(self, cipher_char, plain_char):
        """更新映射关系"""
        if not cipher_char.islower() or not plain_char.isupper():
            print("错误：密文必须是小写字母，明文必须是大写字母")
            return False
            
        # 检查冲突
        if cipher_char in self.key_mapping and self.key_mapping[cipher_char] != plain_char:
            print(f"警告：覆盖已有映射 {cipher_char} -> {self.key_mapping[cipher_char]}")
        
        if plain_char in self.reverse_mapping and self.reverse_mapping[plain_char] != cipher_char:
            print(f"警告：明文 {plain_char} 已经映射到 {self.reverse_mapping[plain_char]}")
            old_cipher = self.reverse_mapping[plain_char]
            del self.key_mapping[old_cipher]
        
        # 更新映射
        self.key_mapping[cipher_char] = plain_char
        self.reverse_mapping[plain_char] = cipher_char
        return True
    
    def clear_mapping(self, cipher_char=None):
        """清除映射关系"""
        if cipher_char:
            if cipher_char in self.key_mapping:
                plain_char = self.key_mapping[cipher_char]
                del self.key_mapping[cipher_char]
                del self.reverse_mapping[plain_char]
        else:
            self.key_mapping = {}
            self.reverse_mapping = {}
    
    def get_current_plaintext(self):
        """根据当前映射获取明文"""
        result = []
        for char in self.ciphertext:
            if char in self.key_mapping:
                result.append(self.key_mapping[char])
            elif char.isalpha():
                result.append('_')  
            else:
                result.append(char)
        return ''.join(result)
    
    def get_current_key(self):
        """获取当前密钥"""
        key = ['_'] * 26
        for cipher_char, plain_char in self.key_mapping.items():
            if 'a' <= cipher_char <= 'z':
                key[ord(cipher_char) - ord('a')] = plain_char
        return ''.join(key)
    
    def display_current_state(self):
        """显示当前破译状态"""
        if not self.ciphertext:
            return "尚未加载密文"
        
        result = []
        for char in self.ciphertext:
            if char in self.key_mapping:
                result.append(self.key_mapping[char])
            else:
                result.append(char)
        
        return ''.join(result)
        
    def get_decrypted_words(self):
        """获取已完全破译的单词列表"""
        decrypted = []
        
        for word in set(self.words):
            # 检查单词是否已完全破译
            fully_decrypted = True
            decrypted_word = ""
            for char in word:
                if char in self.key_mapping:
                    decrypted_word += self.key_mapping[char]
                else:
                    fully_decrypted = False
                    break
            
            if fully_decrypted:
                decrypted.append((word, decrypted_word))
                
        return decrypted