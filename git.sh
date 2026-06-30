#!/usr/bin/env bash

MESSAGE=""

if [[ -n "$1" && -n "$2" ]]; then
    case "$1" in
    related)
        MESSAGE="Relate to #$2"
        ;;
    close)
        MESSAGE="Close #$2"
        ;;
    fix)
        MESSAGE="Fix #$2"
        ;;
    *)
        echo "Неизвестная команда: $1. Привязка к задачам не будет выполнена"
        exit 1
        ;;
    esac
else
  echo "Аргументы не указаны. Привязка к задачам не будет выполнена"
fi


# read -r -d '' PROMPT <<'EOF'
# Создай commit message по Conventional Commits на основе git diff.
# Используй тип feat/fix/refactor/docs/style/test/chore.
# Формат: "<тип>: <одно предложение до 50 символов без markdown и пояснений>".
# EOF
read -r -d '' PROMPT <<EOF
Создай commit message по Conventional Commits на основе git diff.
Используй тип feat/fix/refactor/docs/style/test/chore.
Формат заголовка: "<тип>: <одно предложение до 50 символов без markdown и пояснений>". Заголовок напиши на английском языке.
После заголовка оставь пустую строку и добавь тело коммита: кратко опиши на русском языке какие именно изменения были сделаны (не более 3–4 строк каждая с новой строки), зачем это нужно и на что может повлиять. Не используй markdown.
Добавь в конце две пустых строки и напиши "${MESSAGE}".
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
