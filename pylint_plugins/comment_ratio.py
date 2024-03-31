import astroid

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker

class CommentRatioChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'comment-ratio'
    msgs = {
        'I9999': (
            'Comment to code ratio: LOCM/SLOC * 100%% = %s%%',
            'comment-ratio-info',
            'Displays the comment to code ratio.',
        ),
        'R9999': (
            'Comment to code ratio too low (%s): LOCM/SLOC * 100%% < 15%%',
            'low-comment-ratio',
            'The ratio of lines of comments to lines of code is below 15%%.',
        ),
    }

    def __init__(self, linter=None):
        super().__init__(linter)

    def open(self):
        self.total_lines_of_code = 0
        self.total_lines_of_comments = 0

    def count_lines_and_comments(self, node):
        lines_of_code = 0
        lines_of_comments = 0

        for child_node in node.get_children():
            if isinstance(child_node, astroid.Comment):
                lines_of_comments += 1
            else:
                lines_of_code += 1

        return lines_of_code, lines_of_comments

    def process_module(self, node):
        loc, locm = self.count_lines_and_comments(node)
        self.total_lines_of_code += loc
        self.total_lines_of_comments += locm

        locm_percentage = (self.total_lines_of_comments / self.total_lines_of_code) * 100
        if locm_percentage < 15:
            self.add_message('low-comment-ratio', line=1, args=(locm_percentage,))
        else:
            self.add_message('comment-ratio-info', line=1, args=(locm_percentage,))

def register(linter):
    linter.register_checker(CommentRatioChecker(linter))