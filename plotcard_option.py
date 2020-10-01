import re

class PlotCardOption:
    def __init__(self, text, action_string):
        self.text = text.get()
        self.action_string = action_string.get()
        self.goto_format = r"GOTO\(\s*[0-9A-Za-z]+\s*\)"  # matches "GOTO(    hasdkujf97asfd86789     )" etc
        self.goto_format_int_start_index = 5
        self.goto_format_int_end_index = -1

    def get_possible_destination_ids(self):
        # If is simply and int saying where to go, return that (in a list, so same as otherwise)
        if self.represents_int(self.action_string):
            return [int(self.action_string)]

        # Otherwise, find all the "GOTO(x)"s in the string and pull out the int's from them
        possible_ids = []
        all_goto_strings = re.findall(self.goto_format, self.action_string)
        if len(all_goto_strings) == 0:
            return []
        for goto_string in all_goto_strings:
            possible_id = goto_string[self.goto_format_int_start_index:self.goto_format_int_end_index]

            if self.represents_int(possible_id):
                possible_ids.append(int(possible_id))
        return possible_ids

    @staticmethod
    def represents_int(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

