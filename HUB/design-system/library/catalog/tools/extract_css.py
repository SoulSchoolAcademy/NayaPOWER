"""Extract per-piece real CSS from library source files, scoped under .nb-scope."""
import re, json, os

# Portable: the library root is two dirs above this script (library/catalog/tools -> library).
LIB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

def find_source(fname):
    for root, dirs, files in os.walk(LIB):
        dirs.sort()  # deterministic: a cold clone finds the same file
        if fname in files:
            return os.path.join(root, fname)
    return None

def get_css(path):
    s = open(path, encoding='utf-8', errors='ignore').read()
    blocks = re.findall(r'<style[^>]*>(.*?)</style>', s, re.S)
    return '\n'.join(blocks)

def strip_comments(css):
    return re.sub(r'/\*.*?\*/', '', css, flags=re.S)

def split_rules(css):
    """Split top-level rules; returns list of (prelude, body)."""
    rules, i, n = [], 0, len(css)
    while i < n:
        # skip whitespace
        while i < n and css[i].isspace():
            i += 1
        if i >= n:
            break
        if css[i] == '@':
            # at-rule: find { ... } or ;
            j = css.find('{', i)
            k = css.find(';', i)
            if j == -1 or (k != -1 and k < j):
                i = k + 1 if k != -1 else n
                continue
            depth, p = 0, j
            while p < n:
                if css[p] == '{':
                    depth += 1
                elif css[p] == '}':
                    depth -= 1
                    if depth == 0:
                        break
                p += 1
            rules.append((css[i:j].strip(), css[j:p + 1]))
            i = p + 1
        else:
            j = css.find('{', i)
            if j == -1:
                break
            depth, p = 0, j
            while p < n:
                if css[p] == '{':
                    depth += 1
                elif css[p] == '}':
                    depth -= 1
                    if depth == 0:
                        break
                p += 1
            rules.append((css[i:j].strip(), css[j:p + 1]))
            i = p + 1
    return rules

def scope_selector(sel, scope='.nb-scope'):
    """Prefix a selector with the scope, handling :root/html/body."""
    sel = sel.strip()
    if not sel:
        return sel
    # :root, html, body become the scope itself
    if re.fullmatch(r':root|html|body', sel):
        return scope
    # already scoped
    if sel.startswith(scope):
        return sel
    return scope + ' ' + sel

def extract_for(classes, css):
    """Return scoped CSS text for rules referencing any of classes."""
    css = strip_comments(css)
    rules = split_rules(css)
    wanted = set(classes)
    kept, keyframes_needed, imports = [], set(), []
    root_rules = []

    def selector_hits(prelude):
        # split selector list
        for sel in prelude.split(','):
            sel = sel.strip()
            # find class names in selector
            found = set(re.findall(r'\.([a-zA-Z0-9_-]+)', sel))
            if found & wanted:
                return True
        return False

    for prelude, body in rules:
        if prelude.startswith('@import'):
            imports.append(prelude + ';')
            continue
        if prelude.startswith('@font-face'):
            kept.append(prelude + ' ' + body)
            continue
        if prelude.startswith('@keyframes'):
            # keep if referenced later; store for now
            name = prelude.split()[1] if len(prelude.split()) > 1 else ''
            kept.append(('KEYFRAMES', name, prelude + ' ' + body))
            continue
        if prelude.startswith('@media'):
            inner = split_rules(body[1:-1])
            inner_kept = []
            for ip, ib in inner:
                if ip.startswith('@keyframes'):
                    name = ip.split()[1] if len(ip.split()) > 1 else ''
                    kept.append(('KEYFRAMES', name, ip + ' ' + ib))
                    continue
                if selector_hits(ip):
                    sels = ', '.join(scope_selector(s) for s in ip.split(','))
                    inner_kept.append(sels + ' ' + ib)
                    for m in re.finditer(r'animation(?:-name)?\s*:\s*([^;]+)', ib):
                        for nm in m.group(1).split(','):
                            keyframes_needed.add(nm.strip().split()[0])
            if inner_kept:
                kept.append(prelude + ' {' + '\n'.join(inner_kept) + '}')
            continue
        if re.fullmatch(r':root', prelude.strip()):
            root_rules.append(prelude + ' ' + body)
            continue
        if selector_hits(prelude):
            sels = ', '.join(scope_selector(s) for s in prelude.split(','))
            kept.append(sels + ' ' + body)
            for m in re.finditer(r'animation(?:-name)?\s*:\s*([^;]+)', body):
                for nm in m.group(1).split(','):
                    keyframes_needed.add(nm.strip().split()[0])

    out = []
    out.extend(imports)
    # :root vars -> scoped
    for r in root_rules:
        out.append(re.sub(r'^:root', '.nb-scope', r, count=1))
    for k in kept:
        if isinstance(k, tuple):
            _, name, text = k
            if name in keyframes_needed:
                out.append(text)
        else:
            out.append(k)
    return '\n'.join(out)

if __name__ == '__main__':
    import sys
    # quick self-test on one button entry, repo-relative
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    cat = json.load(open(os.path.join(tools_dir, '..', 'block-catalog.json')))
    e = next(x for x in cat if x['model'] == 'NAYA-BTN-001')
    src = find_source(e['sources'][0]['source_file'])
    css = get_css(src)
    scoped = extract_for(e['css_classes'], css)
    print('source:', src)
    print('scoped css bytes:', len(scoped))
    print(scoped[:600])
