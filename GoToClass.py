import sublime
import sublime_plugin


class GoToClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = self.view.settings()
        separator = settings.get("go_to_class_separator")

        for sel in self.view.sel():
            if sel.empty():
                sel = self.view.word(sel)
            word_sel = self.view.substr(sel)
            word_sel = word_sel.replace(separator, ' ')
            self.view.window().run_command("show_overlay", {"overlay": "goto", "text": word_sel})


class GoToFunctionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = self.view.settings()
        separator = settings.get("go_to_class_separator")

        for sel in self.view.sel():
            if sel.empty():
                sel = self.view.word(sel)
            word_sel = '@' + self.view.substr(sel)
            # word_sel = word_sel.replace(separator, ' ')
            self.view.window().run_command("show_overlay", {"overlay": "goto", "text": word_sel})


class GoToDataCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = self.view.settings()
        separator = settings.get("go_to_class_separator")

        for sel in self.view.sel():
            if sel.empty():
                sel = self.view.word(sel)
            word_sel = '#' + self.view.substr(sel)
            # word_sel = word_sel.replace(separator, ' ')
            self.view.window().run_command("show_overlay", {"overlay": "goto", "text": word_sel})