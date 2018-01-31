import sublime
import sublime_plugin


"""Generate fully qualified class name

1. If string does not start with a backslash, search 'Result' in 'use'
2. If not found, join the string with a 'namespace'
"""
def getFullyQualifiedClassName(view, string, selection = False):
    # If string starts with a backslash - do nothing
    if string[0] == '\\':
        return string

    found = False
    alias = string.split('\\')[0];

    # check if we inside 'namespace' or 'use' lines
    if selection != False:
        if view.match_selector(selection.begin(), 'meta.namespace.php'):
            return '\\' + string

        if view.match_selector(selection.begin(), 'meta.use.php'):
            found = True # hack to skip 'meta.namespace.php' logic below

            # if we select string in 'as' statement, then the whole string
            # is not a classname but an alias and we should remove it,
            # as it does not contain any real information.
            # Example: 'use Magento\Framework\App\Action\Action as Hello;'
            # If string is 'Hello' - get rid of it. All info that we need
            # is in alias variable now.
            if string.find('\\') == -1:
                string = ''

    if len(string) > 0:
        string = '\\' + string

    # Search alias in 'uses'
    for region in view.find_by_selector('meta.use.php'):
        use = view.substr(region);
        if not use.endswith(alias):
            continue
        found = True
        class_name = use.split()[1]
        string = string[(len(alias) + 1):]
        string = class_name + string
        break

    # Join '\string' with a 'namespace'
    if found == False:
        for region in view.find_by_selector('meta.namespace.php'):
            namespace = view.substr(region);
            string = namespace.split()[1] + string

    return '\\' + string.strip('\\')


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


class GoToFullyQualifiedClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = self.view.settings()
        separator = settings.get("go_to_class_separator")
        expand_separators = " []|!{}()<>-+$:;.,'*\n\""

        for sel in self.view.sel():
            sel = self.view.word(sel)

            # Expand selection to include all phrase with backslashes
            sel = self.view.expand_by_class(
                sel,
                sublime.CLASS_WORD_START | sublime.CLASS_WORD_END,
                expand_separators
            );

            string = self.view.substr(sel).strip(expand_separators)
            string = getFullyQualifiedClassName(self.view, string, sel)

            string = string.replace(separator, ' ')
            self.view.window().run_command("show_overlay", {"overlay": "goto", "text": string})


class GoToParentClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.find_by_selector('entity.other.inherited-class.php')

        if len(regions) == 0:
            return;

        parent_class = []
        for region in regions:
            string = self.view.substr(region)
            string = getFullyQualifiedClassName(self.view, string)
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
