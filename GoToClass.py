import sublime
import sublime_plugin


class GoToClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for sel in self.view.sel():
            if sel.empty():
                sel = self.view.word(sel)
            word_sel = self.view.substr(sel)
            word_sel = word_sel.replace('_', ' ')
            self.view.window().run_command("show_overlay", {"overlay": "goto", "text": word_sel})
