import difflib

def show_body_diff(body1, body2):
    diff = difflib.unified_diff(
        body1.splitlines(),
        body2.splitlines(),
        fromfile='Normal',
        tofile='Poisoned',
        lineterm=''
    )
    return list(diff)
