
import math

class Base64NumericEncoder:

    def __init__(self, numeric_type = None, float_precision = None, signed = None, encoding_depth = None, character_set = None):
        self.numeric_type = numeric_type or float
        self.encoding_depth = encoding_depth or 4
        self.float_precision = float_precision or 4
        self.signed = signed or False

        # Default to base64, but accept an input character set
        character_set =  character_set or [str(x) for x in range(10)] + [chr(x) for x in range(65, 91, 1)] + [chr(x) for x in range(97, 123, 1)] + ['-', '_']

        self.set_encoding_character_set(character_set)

        if numeric_type == int:
            self.float_precision = 0

        number_of_states = self.encoding_size ** self.encoding_depth

        if self.signed:
            self.max_state = int(number_of_states / 2)
            self.min_state = -1 * self.max_state
        else:
            self.max_state = (number_of_states)
            self.min_state = 0 

        if self.numeric_type == float:
            self.max_value = self.max_state / (10 ** self.float_precision)
            self.min_value = self.min_state / (10 ** self.float_precision)
        else:
            self.max_value = self.max_state
            self.min_value = self.min_state

    @staticmethod
    def get_base_90():
        character_set = [str(x) for x in range(10)] + [chr(x) for x in range(65, 91, 1)] + [chr(x) for x in range(97, 123, 1)] + ['-', '_', '!', '#', '$', '%', '&', '(', ')', '*', '+', ',', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '`', '}', '{', '|', '~'] 
        return character_set

    @staticmethod
    def get_base_64():
        character_set = [str(x) for x in range(10)] + [chr(x) for x in range(65, 91, 1)] + [chr(x) for x in range(97, 123, 1)] + ['-', '_']
        return character_set
    
    @staticmethod
    def get_base_16():
        character_set = [str(x) for x in range(10)] + [chr(x) for x in range(65, 71, 1)]
        return character_set
        
    def set_encoding_character_set(self, character_set):
        self.encoding_table = {}
        self.decoding_table = {}
        self.encoding_size = len(character_set)
        for i, c in enumerate(character_set):
            self.encoding_table[i] = c
            self.decoding_table[c] = i

    def validate_encoding(self, numeric: float):
        if numeric > self.max_value:
            raise ValueError(f'Numeric value is too large for this encoding. Received {numeric}, range is {self.min_value} to {self.max_value} for encoding depth {self.encoding_depth}, precision {self.float_precision}, and signed {self.signed}') 
        if numeric < self.min_value:
            raise ValueError(f'Numeric value is too small for this encoding. Received {numeric}, range is {self.min_value} to {self.max_value} for encoding depth {self.encoding_depth}, precision {self.float_precision}, and signed {self.signed}') 
    
    def validate_decoding(self, string: str):
        if len(string) != self.encoding_depth:
            raise ValueError(f'String received doesn\'t match the encoding depth of {self.encoding_depth}.') 


    def encode(self, numeric: float):
        self.validate_encoding(numeric)
        encoding = ['0'] * self.encoding_depth

        if self.numeric_type == float:
            numeric *= (10 ** self.float_precision)
            numeric = round(numeric)

        if self.signed:
            numeric += self.max_state

        for i in range(self.encoding_depth):
            place_value = (self.encoding_size ** (self.encoding_depth - i - 1))
            if numeric >= place_value:
                encode_index = int(numeric / place_value)
                encoding[i] = self.encoding_table[encode_index]
                numeric = numeric % place_value

        return ''.join(encoding)

    def decode(self, string: str):
        self.validate_decoding(string)
        val = 0

        # Calculate encoded value
        for i, ch in enumerate(string):
            val += self.decoding_table[ch] * (self.encoding_size ** (self.encoding_depth - i - 1))

        # Adjust for signage
        if self.signed:
            val -= self.max_state

        # Scale for decimal
        if self.numeric_type == float:
            val /= (10 ** self.float_precision)     
        return val

if __name__ == '__main__':
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = int, float_precision = 1)
    
    # test code
    c = encoder.min_state
    while c < encoder.max_state:
        print(c, encoder.encode(c), encoder.decode(encoder.encode(c)))
        if encoder.numeric_type == float:
            c += 10 ** (-1 * encoder.float_precision)
            c = round(c, encoder.float_precision)
        else:
            c += 1
        break


