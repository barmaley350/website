export const usePaginationState = () => {
  const page = useState<number>('paginationPage', () => {
    // При инициализации читаем из sessionStorage
    const saved = sessionStorage.getItem('paginationPage')
    return saved ? Number(saved) : 1
  })

  // Сохраняем в sessionStorage при изменении
  watch(page, (newPage) => {
    sessionStorage.setItem('paginationPage', String(newPage))
  })

  return { page }
}