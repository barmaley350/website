export function useStatData() {
    const runtimeConfig = useRuntimeConfig()
    let url = "baseURL" in runtimeConfig ? runtimeConfig.baseURL + 'stats' : window.location.origin + '/backend/api/v1/stats'
    const { data: statData, pending, error } = useFetch(url, {
        server: true, // SSR
        // client: true, // гидратация/клиент
    })
    return { statData, pending, error  }
}