#!/bin/bash

# Цвета для выделения активного пункта
RED='\033[0;41m'      # Красный фон
GREEN='\033[0;32m'    # Зелёный текст
NC='\033[0m'          # Сброс цвета

FASTAPI_DIR="./services/fastapi"
ROOT_DIR=$(pwd)

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
#
seed_data() {
    clear
    cd $ROOT_DIR
    cd $FASTAPI_DIR 
    read -p "Введите параметры ( --drop -u 10 -p 100 -o 10000 -c 200) / --help для справки: " params
    uv run python3 -m app.scripts.seed_data $params
}

uv_add() {
    clear
    cd $ROOT_DIR
    cd $FASTAPI_DIR 
    read -p "Название модуля: " module_name
    uv run uv add $module_name
}

uv_remove() {
    clear
    cd $ROOT_DIR
    cd $FASTAPI_DIR 
    read -p "Название модуля: " module_name
    uv run uv remove $module_name
}

apply_mirgations() {
    clear
    cd $ROOT_DIR
    cd $FASTAPI_DIR 
    uv run alembic upgrade head
}

make_mirgations() {
    clear
    read -p "Описание миграции (флаг -m): " description
    cd $ROOT_DIR
    cd $FASTAPI_DIR 
    uv run alembic revision --autogenerate -m "${description}"
}
gen_compose_viz() {
    clear
    cd $ROOT_DIR
    uv run cpv -m png -o ./files/docker -l -s docker-compose.yaml
}
# Функции для запуска ruff
run_ruff_check() {
    clear
    cd $ROOT_DIR
    uv run ruff check $FASTAPI_DIR
}

run_ruff_check_statistics() {
    clear
    cd $ROOT_DIR
    uv run ruff check --statistics $FASTAPI_DIR
}

run_ruff_check_fix() {
    clear
    cd $ROOT_DIR
    uv run ruff check --fix $FASTAPI_DIR
}

git_push() {
    clear
    cd $ROOT_DIR
    git push github main
    git push gitlab main
}
# Пункты меню
options=(
    "(1) ruff check --statistics"
    "(2) ruff check"
    "(3) ruff check --fix"
    "(4) git push github / gitlab"
    "(5) Gen docker-compose.yaml compose-viz"
    "(6) Make migrations (alembic revision --autogenerate -m)"
    "(7) Apply migrations (alembic upgrade head)"
    "(8) uv add"
    "(9) uv remove"
    "(10) Сгенерировать данные"
    # "(q) Выход"
)

# Изначально выбран первый пункт (индекс 0)
selected=0
# Количество пунктов
count=${#options[@]}

# Функция отрисовки меню
draw_menu() {
    clear
    echo "Используйте стрелки ↑/↓ и Enter. q - для выхода."
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
        5) make_mirgations;;
        6) apply_mirgations;;
        7) uv_add;;
        8) uv_remove;;
        9) seed_data;;
        # 7) echo "Выход"; exit 0;;
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



