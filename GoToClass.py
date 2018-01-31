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


class GoToParentClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.find_by_selector('entity.other.inherited-class.php')

        if len(regions) == 0:
            return;

        parent_class = []
        for region in regions:
            string = self.view.substr(region)
            if string not in parent_class:
                parent_class.append(string)

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
