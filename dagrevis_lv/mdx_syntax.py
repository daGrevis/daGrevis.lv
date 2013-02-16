from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension


def makeExtension(configs=None):
    return SyntaxExtension(configs=configs)


class SyntaxPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        for line in lines:
            new_lines.append(line)
        return new_lines


class SyntaxExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add("syntax", SyntaxPreprocessor(md), "_begin")
