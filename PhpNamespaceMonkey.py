import json, os, re, sublime, sublime_plugin, time

class PhpNamespaceMonkey():
    namespaces = {}

    def addBoilerplate(self, view):
        settings = sublime.load_settings('PhpNamespaceMonkey.sublime-settings')

        if not view.file_name() or not self.isPhpClassFile(view.file_name()) or view.size(): return

        if time.time() - os.path.getctime(view.file_name()) > 1: return

        namespace = self.resolveNamespace(view.file_name())
        className = self.resolveClassName(view.file_name())
        type = self.resolveType(className)

        if not namespace: return

        namespaceStyle = settings.get('namespace_style')

        if namespaceStyle == 'same-line':
            view.run_command('append', { 'characters': '<?php namespace {};\n'.format(namespace) })
        elif namespaceStyle == 'next-line':
            view.run_command('append', { 'characters': '<?php\nnamespace {};\n'.format(namespace) })
        elif namespaceStyle == 'psr-2':
            view.run_command('append', { 'characters': '<?php\n\nnamespace {};\n'.format(namespace) })

        if settings.get('include_class_definition'):
            view.run_command('append', { 'characters': '\n{} {}\n{{\n}}\n'.format(type, className) })

    def loadNamespaces(self, view, force = False):
        if not view.window(): return

        for path in view.window().folders():
            if path in self.namespaces and not force: continue

            self.namespaces[path] = namespaces = []

            composerJsonPath = path + '/composer.json'

            if not os.path.isfile(composerJsonPath): continue

            composerJson = json.loads(open(composerJsonPath, 'r').read())

            if not composerJson['autoload']: continue

            for key in [ 'psr-0', 'psr-4' ]:
                if not key in composerJson['autoload']: continue

                for namespace, paths in composerJson['autoload'][key].items():
                    if not namespace: continue

                    if not isinstance(paths, list): paths = [ paths ]

                    for path in paths:
                        if not path.endswith('/'): path += '/'

                        namespaces.append({ 'path': path, 'namespace': namespace })

    def isPhpClassFile(self, path):
        fileName = path.split('/')[-1]

        return len(fileName) > 0 and fileName[0] == fileName[0].upper() and fileName.endswith('.php')

    def resolveNamespace(self, path):
        for folder, folderNamespaces in self.namespaces.items():
            if path.startswith(folder):
                path = path.replace(folder, '').lstrip('/')
                namespaces = folderNamespaces
                break

        if not namespaces: return

        namespace = [namespace for namespace in namespaces if path.startswith(namespace['path'])][0]

        if not namespace: return

        subnamespace = '\\'.join(path.replace(namespace['path'], '').replace('.php', '').split('/')[:-1])

        return re.sub(r"\\$", '', namespace['namespace'] + subnamespace)

    def resolveClassName(self, path):
        return path.replace('.php', '').split('/')[-1]

    def resolveType(self, className):
        matches = re.search('(Interface|Trait|Abstract)$', className)

        type = matches.group(1).lower() if matches else 'class'

        if type == 'abstract': type += ' class'

        return type

class PhpNamespaceMonkeyListener(sublime_plugin.EventListener):
    def on_activated_async(self, view):
        global monkey

        monkey.loadNamespaces(view)
        monkey.addBoilerplate(view)

class PhpNamespaceMonkeyReloadNamespacesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global monkey

        monkey.loadNamespaces(self.view, True)

    def description(self):
        return "PHP Namespace Monkey: Reload namespaces"

monkey = PhpNamespaceMonkey()
