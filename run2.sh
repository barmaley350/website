#!/bin/bash

# Цвета для выделения активного пункта
RED='\033[0;41m'  
GREEN='\033[0;32m'  
GRAY='\033[0;37m'
BLUE='\033[0;34m'
NC='\033[0m'       

FASTAPI_DIR="./services/fastapi"
ROOT_DIR=$(pwd)
DOCKER_BACKEND_CONTAINER="fastapi_prg-service.backend-1"

line() {
    cols=$(tput cols)
    for ((i=1; i<=cols; i++)); do echo -en "\u2500"; done
    echo -e ""
}
#
seed_data() {
    clear
    cd $ROOT_DIR
    cd $FASTAPI_DIR 
    read -p "Введите параметры ( --drop -u 10 -p 10000 -c 200) / --help для справки: " params
    docker exec -it $DOCKER_BACKEND_CONTAINER uv run python3 -m app.scripts.seed_data $params
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
    docker exec -it $DOCKER_BACKEND_CONTAINER uv run alembic upgrade head
}

make_mirgations() {
    clear
    read -p "Описание миграции (флаг -m): " description
    cd $ROOT_DIR
    cd $FASTAPI_DIR 
    docker exec -it $DOCKER_BACKEND_CONTAINER uv run alembic revision --autogenerate -m "${description}"
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
    "  ${GREEN}1${NC} - ${BLUE}ruff check --statistics${NC}"
    "  ${GREEN}2${NC} - ${BLUE}ruff check${NC}"
    "  ${GREEN}3${NC} - ${BLUE}ruff check --fix${NC}"
    "  ${GREEN}4${NC} - ${BLUE}git push github / gitlab${NC}"
    "  ${GREEN}5${NC} - ${BLUE}Gen docker-compose.yaml compose-viz${NC}
    \t Генерация docker-compose.yaml визуализации"
    "  ${GREEN}6${NC} - ${BLUE}Make migrations (alembic revision --autogenerate -m)${NC}
    \t Создание миграции. Выполняется в контейнере ${DOCKER_BACKEND_CONTAINER}"
    "  ${GREEN}7${NC} - ${BLUE}Apply migrations (alembic upgrade head)${NC}
    \t Применение миграции. Выполняется в контейнере ${DOCKER_BACKEND_CONTAINER}"
    "  ${GREEN}8${NC} - ${BLUE}uv add${NC}"
    "  ${GREEN}9${NC} - ${BLUE}uv remove${NC}"
    " ${GREEN}10${NC} - ${BLUE}Сгенерировать тестовые данные${NC}
    \t Выполняется в контейнере ${DOCKER_BACKEND_CONTAINER}"
)


# Функция обработки выбора
select_option() {
    case $selected in
        1) run_ruff_check_statistics;;
        2) run_ruff_check;;
        3) run_ruff_check_fix;;
        4) git_push;;
        5) gen_compose_viz;;
        6) make_mirgations;;
        7) apply_mirgations;;
        8) uv_add;;
        9) uv_remove;;
        10) seed_data;;
        # 7) echo "Выход"; exit 0;;
    esac
}

draw_menu() {
    clear
    line
    echo "Быстрые команды для работы с проектом"
    echo "Для запуска введите номер и нажмите Enter"
    line
    for i in "${!options[@]}"; do
        echo -e "${options[$i]}"
    done
    line
    read -p "Введите номер: " selected
    select_option
}

draw_menu


