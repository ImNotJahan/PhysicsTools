def get(context, pos):
    return context.getChild(pos)

def get_str(context, pos=None) -> str:
    if pos is None:
        return context.getText()
    return context.getChild(pos).getText()

def get_eval(interpreter, context, pos=None):
    if pos is None:
        return interpreter.visit(context)
    return interpreter.visit(context.getChild(pos))

def count(context):
    return context.getChildCount()