import jsonpickle

from plotcard_option import PlotCardOption


class PlotCard:

    def __init__(self, id_num, title, subtitle, text, options, options_actions):
        self.version = "0.1"
        self.id = int(id_num.get())
        self.title = title.get()
        self.subtitle = subtitle.get()
        self.text = text.get("1.0", "end")[:-1]
        self.plotcardoptions = []
        for i in range(0, len(options)):
            self.plotcardoptions.append(PlotCardOption(options[i], options_actions[i]))

    def json(self):
        return jsonpickle.encode(self, indent=4, separators=(',', ': '))