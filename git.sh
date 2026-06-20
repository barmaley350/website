#!/usr/bin/env bash

read -r -d '' PROMPT <<'EOF'
Создай commit message по Conventional Commits на основе git diff.
Используй тип feat/fix/refactor/docs/style/test/chore.
Формат: "<тип>: <одно предложение до 50 символов без markdown и пояснений>".
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
