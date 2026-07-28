class Parsing:
    def __init__(self):
        self._to_remove = str.maketrans('', '', '(),')

    @staticmethod
    def clean_string(input):
        return input.translate(Parsing._to_remove)

    @staticmethod
    def _try_parse_optional(parser, optional_input): 
        if optional_input is None:
            return None
        try:
            return parser(optional_input)
        except ValueError:
            return None

    @staticmethod
    def try_parse_float(optional_input):
        return Parsing._try_parse_optional(float, optional_input)

    @staticmethod
    def try_parse_int(optional_input):
        return Parsing._try_parse_optional(int, optional_input)
