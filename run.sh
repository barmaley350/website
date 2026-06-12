#!/bin/bash

# Цвета для выделения активного пункта
RED='\033[0;41m'      # Красный фон
GREEN='\033[0;32m'    # Зелёный текст
NC='\033[0m'          # Сброс цвета

ROOT_DIR="./services/fastapi"
RUFF_RULES=""

# Проверка статуса выполнения команды
check_command_run_status() {
    command_run_status="$1"
    command_run="$2"

    output_text=$USER_INPUT
    if [[ -n "$command_run" ]]; then
        output_text+=" ($command_run)"
    fi


    if [ $command_run_status -ne 0 ]; then
        echo -en "\u2718 Ошибка выполнения комманды \u00AB$output_text\u00BB\n"
    fi
    echo -en "\u2714 Команда \u00AB$output_text\u00BB выполнилась успешно\n"

    # exit 0    
} 

gen_compose_viz() {
    clear
    uv run cpv -m png -o ./files/docker -s docker-compose.yaml
}
# Функции для запуска ruff
run_ruff_check() {
    clear
    uv run ruff check $ROOT_DIR
}

run_ruff_check_statistics() {
    clear
    uv run ruff check --statistics $ROOT_DIR
}

run_ruff_check_fix() {
    clear
    uv run ruff check --fix $ROOT_DIR
}

git_push() {
    clear
    git push github main
    git push gitlab main
}
# Пункты меню
options=(
    "(1) ruff check --statistics"
    "(2) ruff check"
    "(3) ruff check --fix"
    "(5) git push github / gitlab"
    "(6) Gen docker-compose.yaml compose-viz"
    "(q) Выход"
)

# Изначально выбран первый пункт (индекс 0)
selected=0
# Количество пунктов
count=${#options[@]}

# Функция отрисовки меню
draw_menu() {
    clear
    echo "Используйте стрелки ↑/↓ и Enter"
    echo
    for i in "${!options[@]}"; do
        if [[ $i -eq $selected ]]; then
            # Активный пункт: зелёный текст на красном фоне
            echo -e "${RED}${GREEN} ▶ ${options[$i]} ${NC}"
        else
            # Обычный пункт
            echo "   ${options[$i]}"
        fi
    done
}

# Функция обработки выбора
select_option() {
    case $selected in
        0) run_ruff_check_statistics;;
        1) run_ruff_check;;
        2) run_ruff_check_fix;;
        3) git_push;;
        4) gen_compose_viz;;
        5) echo "Выход"; exit 0;;
    esac
    echo "Нажмите любую клавишу для продолжения..."
    read -n 1
}

# Основной цикл
while true; do
    draw_menu
    # Читаем один символ без ожидания Enter
    read -s -n1 key

    # Проверяем, не является ли символ началом escape-последовательности (стрелки)
    if [[ $key == $'\e' ]]; then
        read -s -n2 -t 0.1 key2  # Читаем ещё два символа с таймаутом
        case $key2 in
            '[A')  # Стрелка вверх
                ((selected--))
                if [[ $selected -lt 0 ]]; then selected=$((count-1)); fi
                ;;
            '[B')  # Стрелка вниз
                ((selected++))
                if [[ $selected -ge $count ]]; then selected=0; fi
                ;;
            '[C')  # Стрелка вправо (можно использовать для быстрого выбора, например)
                select_option
                ;;
            '[D')  # Стрелка влево (не используется в простом меню)
                ;;
        esac
    elif [[ $key =~ ^[0-9]+$ ]]; then
        # Преобразуем символ в число и вычитаем 1 (так как индексы массива с 0)
        selected=$((key - 1))
        
        # Проверяем, что число не выходит за границы списка
        if [[ $selected -lt 0 || $selected -ge $count ]]; then
            echo "Неверный номер пункта" >&2
        else
            select_option  # Вызываем функцию выбора
        fi

    elif [[ $key == "" ]]; then
        # Enter (пустая строка, так как Enter передаётся как \n)
        select_option
    elif [[ $key == "q" || $key == "Q" ]]; then
        # echo "Выход по Q"
        exit 0
    fi
done



