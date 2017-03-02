import timeit


class EventHandler():

    def __init__(self):
        self.actions = {}

    def tick(self):

        for action in self.actions.values():

            if timeit.default_timer() - action["start_time"] < action["delay"]:
                continue

            if action["args"] and action["kwargs"]:
                action["function"](*action["args"], **action["kwargs"])
            elif action["args"]:
                action["function"](*action["args"])
            else:
                action["function"]()

    def start(self, name, function, *args, **kwargs):
        # in seconds
        delay = kwargs.pop('delay', 0.3)
        self.actions[name] = {}
        self.actions[name]["function"] = function
        self.actions[name]["args"] = args
        self.actions[name]["kwargs"] = kwargs
        self.actions[name]["delay"] = delay
        self.actions[name]["start_time"] = timeit.default_timer()

    def end(self, name):
        del self.actions[name]

    def handle_event(self, button, event, name, function, start, *args, **kwargs):
        if start:
            self.start(name, function, button, *args, **kwargs)
        else:
            self.end(name)

    def connect_with_press_up(self, widget, function, *args):

        widget.connect("clicked", function, *args)
        widget.connect("button-press-event", self.handle_event, str(function), function, True, *args)
        widget.connect("button-release-event", self.handle_event, str(function), function, False, *args)
