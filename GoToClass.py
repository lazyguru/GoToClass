import sublime
import sublime_plugin
import re


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


class GoToParentClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        content = self.view.substr(sublime.Region(0, self.view.size()))
        # TODO match class declaration lines: class\s+(.*)\s+{. Then remove comments and find the parent class names
        pattern = re.compile('^(final\s+|abstract\s+)*class\s+\S+\s+extends\s+(\S+)', re.MULTILINE|re.IGNORECASE)
        matches = pattern.findall(content)

        if len(matches) == 0:
            return;

        # transform matches into list of unique parent class names
        parent_class = []
        [parent_class.append(match[1]) for match in matches if match[1] not in parent_class]

        if len(parent_class) > 1:
            def on_parent_class_select(index):
                if index == -1:
                    return
                # bugfix: show_overlay after show_quick_panel is not working without set_timeout?
                # self.show_overlay(parent_class[index])
                sublime.set_timeout(lambda: self.show_overlay(parent_class[index]), 10)

            # Show quick panel with parent class names if more than one is found
            self.view.window().show_quick_panel(parent_class, on_parent_class_select)
        else:
            self.show_overlay(parent_class[0])

    def show_overlay(self, text):
        self.view.window().focus_view(self.view)
        settings = self.view.settings()
        separator = settings.get("go_to_class_separator")
        text = text.replace(separator, ' ')
        self.view.window().run_command("show_overlay", {"overlay": "goto", "text": text})


class GoToFunctionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = self.view.settings()
        separator = settings.get("go_to_class_separator")

        for sel in self.view.sel():
            if sel.empty():
                sel = self.view.word(sel)
            word_sel = '@' + self.view.substr(sel)
            self.view.window().run_command("show_overlay", {"overlay": "goto", "text": word_sel})


class GoToDataCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = self.view.settings()
        separator = settings.get("go_to_class_separator")

        for sel in self.view.sel():
            if sel.empty():
                sel = self.view.word(sel)
            word_sel = '#' + self.view.substr(sel)
            self.view.window().run_command("show_overlay", {"overlay": "goto", "text": word_sel})
