import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

class CustomCBOChecker(BaseChecker):
    __implements__ = IAstroidChecker
    name = "custom-cbo-checker"
    priority = -1
    msgs = {
        "R5001": (
            "Coupling Between Object Classes (CBO) (%s) is too high. Max is 16.",
            "custom-cbo",
            "The number of imported classes and modules is too high",
        ),
    }

    def visit_module(self, node):
        imports = sum([1 for _ in node.get_children() if isinstance(_, astroid.Import)])
        for class_def in [n for n in node.get_children() if isinstance(n, astroid.ClassDef)]:
            imports += sum([1 for _ in class_def.get_children() if isinstance(_, astroid.Import)])

        if imports >= 16:
            self.add_message("custom-cbo", node=node, args=(imports,))

def register(linter):
    linter.register_checker(CustomCBOChecker(linter))
    