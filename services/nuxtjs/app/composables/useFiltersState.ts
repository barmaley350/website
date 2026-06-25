export const useFiltersState = () => {
  const filters = useState<Record<string, any>>('filters', () => {
    const saved = sessionStorage.getItem('filters')
    return saved ? JSON.parse(saved) : {}
  })

  // Сохраняем при изменении любого свойства (глубокий watch)
  watch(filters, (newFilters) => {
    sessionStorage.setItem('filters', JSON.stringify(newFilters))
  }, { deep: true })

  // Дополнительно: метод для обновления одного поля
  const setFilter = <T>(key: string, value: T) => {
    filters.value = { ...filters.value, [key]: value }
  }

  // Метод для сброса всех фильтров
  const resetFilters = () => {
    filters.value = {}
  }

  return { filters, setFilter, resetFilters }
}