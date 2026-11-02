import { computed, onUnmounted, reactive, ref, watch } from "vue"
import { router } from "@inertiajs/vue3"

export const ESPERA_BUSQUEDA_MS = 400

export interface ConsultaTabla {
  q: string
  sort: string
  order: "asc" | "desc"
  filtros: Record<string, string>
}

export interface PaginacionTabla {
  number: number
  per_page: number
  count: number
}

export interface EventoPagina {
  page: number
  rows: number
}

export interface EventoOrden {
  sortField?: string | ((item: unknown) => string) | null
  sortOrder?: 1 | 0 | -1 | null
}

export interface EventoFiltro {
  filters?: Record<string, unknown>
}

export interface FiltroColumna {
  value: string | null
  matchMode: "contains"
}

interface EstadoVisita {
  page: number
  per_page: number
  q: string
  sort: string
  order: "asc" | "desc"
  filtros: Record<string, string>
}

function leerValor(crudo: unknown): string {
  if (typeof crudo === "string") return crudo.trim()
  if (!crudo || typeof crudo !== "object") return ""
  if ("constraints" in crudo && Array.isArray(crudo.constraints)) return leerValor(crudo.constraints[0])
  if (!("value" in crudo)) return ""
  const valor = crudo.value
  if (valor == null) return ""
  return String(valor).trim()
}

function paramsDe(estado: EstadoVisita): Record<string, string | number> {
  const params: Record<string, string | number> = {
    page: estado.page,
    per_page: estado.per_page,
  }
  if (estado.q) params.q = estado.q
  if (estado.sort) {
    params.sort = estado.sort
    params.order = estado.order
  }
  for (const [clave, valor] of Object.entries(estado.filtros)) {
    if (valor) params[clave] = valor
  }
  return params
}

export function useTablaServidor(opciones: {
  url: () => string
  only: readonly string[]
  consulta: () => ConsultaTabla
  paginacion: () => PaginacionTabla
  filtros: readonly string[]
  filtrosTexto: readonly string[]
}) {
  const cargando = ref(false)
  const q = ref(opciones.consulta().q)
  const valoresFiltro = reactive<Record<string, string>>(
    Object.fromEntries(opciones.filtros.map((clave) => [clave, opciones.consulta().filtros[clave] ?? ""])),
  )
  let temporizador: ReturnType<typeof setTimeout> | undefined
  let visitas = 0

  watch(
    () => opciones.consulta().q,
    (valor) => {
      if (!temporizador) q.value = valor
    },
  )

  watch(
    () => opciones.consulta().filtros,
    (filtros) => {
      if (temporizador) return
      for (const clave of opciones.filtros) {
        valoresFiltro[clave] = filtros[clave] ?? ""
      }
    },
  )

  onUnmounted(() => {
    if (temporizador) clearTimeout(temporizador)
  })

  const first = computed(() => Math.max(0, (opciones.paginacion().number - 1) * opciones.paginacion().per_page))
  const sortField = computed(() => opciones.consulta().sort || undefined)
  const sortOrder = computed((): 1 | -1 | undefined => {
    if (!opciones.consulta().sort) return undefined
    return opciones.consulta().order === "asc" ? 1 : -1
  })
  const filters = computed(() => {
    const meta: Record<string, FiltroColumna> = {}
    for (const clave of opciones.filtros) {
      const valor = opciones.consulta().filtros[clave] ?? ""
      meta[clave] = { value: valor || null, matchMode: "contains" }
    }
    return meta
  })

  function estadoActual(cambios: Partial<EstadoVisita> = {}): EstadoVisita {
    const actual = opciones.consulta()
    return {
      page: cambios.page ?? opciones.paginacion().number,
      per_page: cambios.per_page ?? opciones.paginacion().per_page,
      q: (cambios.q ?? q.value).trim(),
      sort: cambios.sort ?? actual.sort,
      order: cambios.order ?? actual.order,
      filtros: { ...actual.filtros, ...cambios.filtros },
    }
  }

  function visitar(estado: EstadoVisita, esperar: boolean) {
    const params = paramsDe(estado)
    const disparar = () => {
      temporizador = undefined
      const actual = ++visitas
      cargando.value = true
      router.get(opciones.url(), params, {
        preserveState: true,
        preserveScroll: true,
        replace: true,
        only: [...opciones.only],
        onFinish: () => {
          if (actual === visitas) cargando.value = false
        },
      })
    }
    if (temporizador) clearTimeout(temporizador)
    if (!esperar) {
      disparar()
      return
    }
    temporizador = setTimeout(disparar, ESPERA_BUSQUEDA_MS)
  }

  function buscar(valor: string) {
    q.value = valor
    visitar(estadoActual({ page: 1, q: valor }), true)
  }

  function onPage(evento: EventoPagina) {
    visitar(estadoActual({ page: evento.page + 1, per_page: evento.rows }), false)
  }

  function onSort(evento: EventoOrden) {
    const campo = typeof evento.sortField === "string" ? evento.sortField : ""
    const activo = campo !== "" && evento.sortOrder !== 0 && evento.sortOrder != null
    visitar(
      estadoActual({
        page: 1,
        sort: activo ? campo : "",
        order: evento.sortOrder === 1 ? "asc" : "desc",
      }),
      false,
    )
  }

  function onFilter(evento: EventoFiltro) {
    const filtros: Record<string, string> = {}
    let espera = false
    const previos = opciones.consulta().filtros
    for (const clave of opciones.filtros) {
      const valor = leerValor(evento.filters?.[clave])
      filtros[clave] = valor
      if (opciones.filtrosTexto.includes(clave) && valor !== (previos[clave] ?? "")) {
        espera = true
      }
    }
    visitar(estadoActual({ page: 1, filtros }), espera)
  }

  function hrefExportar(base: string, formato: "csv" | "xlsx") {
    const actual = opciones.consulta()
    const params = new URLSearchParams()
    params.set("formato", formato)
    if (actual.q) params.set("q", actual.q)
    if (actual.sort) {
      params.set("sort", actual.sort)
      params.set("order", actual.order)
    }
    for (const [clave, valor] of Object.entries(actual.filtros)) {
      if (valor) params.set(clave, valor)
    }
    return `${base}?${params.toString()}`
  }

  function asignarFiltro(modelo: { value: string | null }, evento: Event, callback: () => void) {
    const texto = (evento.target as HTMLInputElement).value.trim()
    modelo.value = texto || null
    callback()
  }

  function filtrar(clave: string, valor: string | number | null) {
    const crudo = valor == null ? "" : String(valor)
    const texto = crudo.trim()
    const esperar = opciones.filtrosTexto.includes(clave)
    valoresFiltro[clave] = esperar ? crudo : texto
    visitar(estadoActual({ page: 1, filtros: { [clave]: texto } }), esperar)
  }

  return {
    cargando,
    q,
    first,
    sortField,
    sortOrder,
    filters,
    buscar,
    onPage,
    onSort,
    onFilter,
    hrefExportar,
    asignarFiltro,
    filtrar,
    valoresFiltro,
  }
}
