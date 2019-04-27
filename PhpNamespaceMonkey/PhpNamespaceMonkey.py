import json, os, re, sublime, sublime_plugin, time

class PhpNamespaceMonkey(sublime_plugin.EventListener):
    namespaces = {}

    def on_activated_async(self, view):
        self.loadNamespaces(view)
        self.addBoilerplate(view)

    def addBoilerplate(self, view):
        settings = sublime.load_settings('PhpNamespaceMonkey.sublime-settings')

        if not view.file_name() or not self.isPhpClassFile(view.file_name()) or view.size(): return

        if time.time() - os.path.getctime(view.file_name()) > 1: return

        namespace = self.resolveNamespace(view.file_name())
        className = self.resolveClassName(view.file_name())

        if not namespace: return

        namespaceStyle = settings.get('namespace_style')

        if namespaceStyle == 'same-line':
            view.run_command('append', { 'characters': '<?php namespace {};\n'.format(namespace) })
        elif namespaceStyle == 'next-line':
            view.run_command('append', { 'characters': '<?php\nnamespace {};\n'.format(namespace) })
        elif namespaceStyle == 'psr-2':
            view.run_command('append', { 'characters': '<?php\n\nnamespace {};\n'.format(namespace) })

        if settings.get('include_class_definition'):
            view.run_command('append', { 'characters': '\nclass {}\n{{\n}}\n'.format(className) })

    def loadNamespaces(self, view):
        if not view.window(): return

        for path in view.window().folders():
            if path in self.namespaces: continue

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
