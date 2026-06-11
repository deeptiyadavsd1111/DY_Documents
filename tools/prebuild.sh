#!/usr/bin/env bash
set -euo pipefail
infolog="lint.info.log"
errorlog="lint.error.log"

# ESLint docusaurus source files

if npx eslint src; then
    echo "INFO: eslint passed docusaurus source files"
else
    echo "ERROR: eslint failed, please address the errors above"
    exit 1
fi

# Markdown lint

if npx markdownlint --ignore _site/ --ignore node_modules/ --ignore docusaurus/node_modules/ --ignore docs/contributions/thanks.md "docs/**/*.md" --disable MD013 MD033 MD045 MD029 MD024 MD025; then
    echo "INFO: markdownlint check passed"
else
    echo "ERROR: markdownlint failed"
    exit 1
fi

# searches the file tree recursively
# NOTE: cspell emits errors onto stdout, and informational text about what it's doing onto stderr...
if npx cspell docs/**/**/**/**/*.md --config tools/cspell.json 1>"$errorlog" 2>"$infolog"; then
    echo "INFO: cspell check passed"
    # Eg.: CSpell: Files checked: 43, Issues found: 1 in 1 files
    tail -n1 "$infolog"
else
    echo "ERROR: cspell failed, check $infolog for verbose detail. $errorlog was:"
    cat "$errorlog" >&2
    exit 1
fi

if npx remark . --use remark-validate-links --frail "docs/**/*.md" --ignore ".github/**" --ignore "src/**"; then
    echo "INFO: Link check passed"
else
    echo "ERROR: Link check failed"
    exit 1
fi
