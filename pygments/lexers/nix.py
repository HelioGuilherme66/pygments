"""
    pygments.lexers.nix
    ~~~~~~~~~~~~~~~~~~~

    Lexers for the NixOS Nix language.

    :copyright: Copyright 2006-2022 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer, include
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Literal

__all__ = ['NixLexer']


class NixLexer(RegexLexer):
    """
    For the `Nix language <http://nixos.org/nix/>`_.

    .. versionadded:: 2.0
    """

    name = 'Nix'
    aliases = ['nixos', 'nix']
    filenames = ['*.nix']
    mimetypes = ['text/x-nix']

    flags = re.MULTILINE | re.UNICODE

    keywords = ['rec', 'with', 'let', 'in', 'inherit', 'assert', 'if',
                'else', 'then', '...']
    builtins = ['import', 'abort', 'baseNameOf', 'dirOf', 'isNull', 'builtins',
                'map', 'removeAttrs', 'throw', 'toString', 'derivation']
    operators = ['++', '+', '?', '.', '!', '//', '==',
                 '!=', '&&', '||', '->', '=']

    punctuations = ["(", ")", "[", "]", ";", "{", "}", ":", ",", "@"]

    tokens = {
        'root': [
            # comments starting with #
            (r'#.*$', Comment.Single),

            # multiline comments
            (r'/\*', Comment.Multiline, 'comment'),

            # whitespace
            (r'\s+', Text),

            # keywords
            ('(%s)' % '|'.join(re.escape(entry) + '\\b' for entry in keywords), Keyword),

            # highlight the builtins
            ('(%s)' % '|'.join(re.escape(entry) + '\\b' for entry in builtins),
             Name.Builtin),

            (r'\b(true|false|null)\b', Name.Constant),

            # operators
            ('(%s)' % '|'.join(re.escape(entry) for entry in operators),
             Operator),

            # word operators
            (r'\b(or|and)\b', Operator.Word),

            # punctuations
            ('(%s)' % '|'.join(re.escape(entry) for entry in punctuations), Punctuation),

            # integers
            (r'[0-9]+', Number.Integer),

            # strings
            (r'"', String.Double, 'doublequote'),
            (r"''", String.Single, 'singlequote'),

            # paths
            (r'[\w.+-]*(\/[\w.+-]+)+', Literal),
            (r'\<[\w.+-]+(\/[\w.+-]+)*\>', Literal),

            # urls
            (r'[a-zA-Z][a-zA-Z0-9\+\-\.]*\:[\w%/?:@&=+$,\\.!~*\'-]+', Literal),

            # names of variables
            (r'[\w-]+\s*=', String.Symbol),
            (r'[a-zA-Z_][\w\'-]*', Text),

        ],
        'comment': [
            (r'[^/*]+', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline),
        ],
        'singlequote': [
            (r"'''", String.Escape),
            (r"''\$\{", String.Escape),
            (r"''\n", String.Escape),
            (r"''\r", String.Escape),
            (r"''\t", String.Escape),
            (r"''", String.Single, '#pop'),
            (r'\$\{', String.Interpol, 'antiquote'),
            (r"[^']", String.Single),
        ],
        'doublequote': [
            (r'\\', String.Escape),
            (r'\\"', String.Escape),
            (r'\\$\{', String.Escape),
            (r'"', String.Double, '#pop'),
            (r'\$\{', String.Interpol, 'antiquote'),
            (r'[^"]', String.Double),
        ],
        'antiquote': [
            (r"\}", String.Interpol, '#pop'),
            # TODO: we should probably escape also here ''${ \${
            (r"\$\{", String.Interpol, '#push'),
            include('root'),
        ],
    }

    def analyse_text(text):
        rv = 0.0
        # TODO: let/in
        if re.search(r'import.+?<[^>]+>', text):
            rv += 0.4
        if re.search(r'mkDerivation\s+(\(|\{|rec)', text):
            rv += 0.4
        if re.search(r'=\s+mkIf\s+', text):
            rv += 0.4
        if re.search(r'\{[a-zA-Z,\s]+\}:', text):
            rv += 0.1
        return rv
