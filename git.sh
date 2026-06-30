#!/usr/bin/env bash

# read -r -d '' PROMPT <<'EOF'
# Создай commit message по Conventional Commits на основе git diff.
# Используй тип feat/fix/refactor/docs/style/test/chore.
# Формат: "<тип>: <одно предложение до 50 символов без markdown и пояснений>".
# EOF
read -r -d '' PROMPT <<'EOF'
Создай commit message по Conventional Commits на основе git diff.
Используй тип feat/fix/refactor/docs/style/test/chore.
Формат заголовка: "<тип>: <одно предложение до 50 символов без markdown и пояснений>". Заголовок напиши на английском языке.
После заголовка оставь пустую строку и добавь тело коммита: кратко опиши на русском языке какие именно изменения были сделаны (не более 3–4 строк каждая с новой строки), зачем это нужно и на что может повлиять. Не используй markdown.
EOF

diff_output=$(git diff --cached)

if [[ -z "$diff_output" ]]; then
    echo "Нет изменений в индексе"
else
    {
        printf '%s\n\n' "$PROMPT"
        printf '%s\n' "$diff_output"
    } | xclip -selection clipboard

    echo "Diff и промпт скопированы в буфер обмена"
fi
