from tree_sitter_language_pack import get_language, get_parser
language = get_language('python')
parser = get_parser('python')
print(f"Python language parser loaded: {language is not None}")
