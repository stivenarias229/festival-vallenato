import { ref } from "vue"
import { router } from "@inertiajs/vue3"

type Datos = Record<string, string | number | boolean | File | null | undefined>

export function useServerAction() {
  const processing = ref(false)
  const key = ref<string | null>(null)

  const terminar = () => {
    processing.value = false
    key.value = null
  }

  const iniciar = (clave?: string) => {
    processing.value = true
    key.value = clave ?? null
  }

  const isBusy = (clave?: string) => processing.value && (clave === undefined || key.value === clave)

  const post = (url: string, data: Datos, clave?: string) => {
    iniciar(clave)
    router.post(url, data, { onFinish: terminar })
  }

  const get = (url: string, params: Datos = {}, clave?: string) => {
    iniciar(clave)
    router.get(url, params, { onFinish: terminar })
  }

  return { processing, key, isBusy, post, get }
}
