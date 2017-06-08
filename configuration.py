from configparser import ConfigParser


# TODO remove most of code, its useless
class Configuration:

    def __getattr__(self, option_name):
        if option_name in self.register:
            return eval(self.register[option_name])
        else:
            print ("There is no option >> " + option_name + " <<")
            return False

    def set(self, option_name, value):
        self.register[option_name] = repr(value)
        self.config.set("options", option_name, repr(value))

    def __init__(self, path_to_file=None):
        self.register = {}
        if path_to_file:
            self.load_from_file(path_to_file)

    def load_from_file(self, file_name):

        config = ConfigParser()
        config.read(file_name)

        # TODO: remember section and when update or set - also use it

        for section in config.sections():
            self.register.update(dict(config.items(section)))

        self.config = config
        self.path = file_name

    def save_to_file(self, file_name=None):

        if not file_name:
            file_name = self.path

        with open(file_name, "w") as f:
            self.config.write(f)
