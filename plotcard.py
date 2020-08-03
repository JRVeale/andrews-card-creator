import jsonpickle


class PlotCard:

    def __init__(self, title, subtitle, text, options):
        self.title = title.get()
        self.subtitle = subtitle.get()
        self.text = text.get("1.0", "end")[:-1]
        self.options = []
        for o in options[1:]:
            self.options.append(o.get())

    def json(self):
        return jsonpickle.encode(self, indent=4, separators=(',', ': '))

    #def json(self):
    #    string = "{\n\t\"title\": \"" + self.title + "\",\n"
    #    string += "\t\"subtitle\": \"" + self.subtitle + "\",\n"
    #    string += "\t\"text\": \"" + self.text + "\",\n"
    #    string += "\t\"options\": [\n"
    #    for option in self.options:
    #        string += "\t\t\"" + option + "\",\n"
    #    string += "\t]\n}"
    #    print(string)
    #    return string
