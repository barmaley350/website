export function useStatData() {
    const runtimeConfig = useRuntimeConfig()
    const apiUrl = import.meta.server
    ? runtimeConfig.apiInternal      // на сервере — полный внутренний URL
    : runtimeConfig.public.apiBase   // на клиенте — относительный путь

    const { data: statData, pending, error } = useFetch(`${apiUrl}stats/`, {
        // server: true, // SSR
        // client: true, // гидратация/клиент
        key: 'stat-data',
    })
    return { statData, pending, error  }
}