import { defineComponent, ref } from "vue"
import { mount } from "@vue/test-utils"
import { afterEach, describe, expect, it, vi } from "vitest"

import {
  ESPERA_BUSQUEDA_MS,
  useTablaServidor,
  type ConsultaTabla,
  type PaginacionTabla,
} from "@/composables/useTablaServidor"

const routerGet = vi.hoisted(() => vi.fn())

vi.mock("@inertiajs/vue3", () => ({
  router: { get: routerGet },
}))

const montar = (
  inicial: {
    consulta?: ConsultaTabla
    paginacion?: PaginacionTabla
    filtrosTexto?: readonly string[]
  } = {},
) => {
  const consulta = ref<ConsultaTabla>(
    inicial.consulta ?? {
      q: "",
      sort: "",
      order: "desc",
      filtros: { rol: "", estado: "" },
    },
  )
  const paginacion = ref<PaginacionTabla>(inicial.paginacion ?? { number: 1, per_page: 10, count: 0 })
  let api!: ReturnType<typeof useTablaServidor>
  const wrapper = mount(
    defineComponent({
      setup() {
        api = useTablaServidor({
          url: () => "/panel/usuarios",
          only: ["usuarios", "paginacion", "consulta"],
          consulta: () => consulta.value,
          paginacion: () => paginacion.value,
          filtros: ["rol", "estado"],
          filtrosTexto: inicial.filtrosTexto ?? [],
        })
        return () => null
      },
    }),
  )
  return { wrapper, api, consulta, paginacion }
}

describe("useTablaServidor", () => {
  afterEach(() => {
    vi.useRealTimers()
    routerGet.mockReset()
  })

  it("espera 400 ms para buscar y vuelve a la página 1", async () => {
    vi.useFakeTimers()
    const { api, paginacion } = montar()
    paginacion.value = { number: 3, per_page: 25, count: 40 }
    api.buscar("a")
    await vi.advanceTimersByTimeAsync(200)
    api.buscar("ana")
    await vi.advanceTimersByTimeAsync(ESPERA_BUSQUEDA_MS - 1)
    expect(routerGet).not.toHaveBeenCalled()
    await vi.advanceTimersByTimeAsync(1)
    expect(routerGet).toHaveBeenCalledTimes(1)
    expect(routerGet).toHaveBeenCalledWith(
      "/panel/usuarios",
      { page: 1, per_page: 25, q: "ana" },
      expect.objectContaining({
        preserveState: true,
        preserveScroll: true,
        replace: true,
        only: ["usuarios", "paginacion", "consulta"],
      }),
    )
    expect(api.cargando.value).toBe(true)
    routerGet.mock.calls[0][2].onFinish()
    expect(api.cargando.value).toBe(false)
  })

  it("traduce la página de PrimeVue a base 1 y conserva la consulta", () => {
    const { api } = montar({
      consulta: { q: "ana", sort: "email", order: "desc", filtros: { rol: "votante", estado: "" } },
      paginacion: { number: 1, per_page: 10, count: 30 },
    })
    api.onPage({ page: 1, rows: 25 })
    expect(routerGet).toHaveBeenCalledWith(
      "/panel/usuarios",
      { page: 2, per_page: 25, q: "ana", sort: "email", order: "desc", rol: "votante" },
      expect.any(Object),
    )
  })

  it("envía el orden y vuelve a la página 1", () => {
    const { api } = montar({ paginacion: { number: 4, per_page: 10, count: 40 } })
    api.onSort({ sortField: "nombre", sortOrder: 1 })
    expect(routerGet).toHaveBeenCalledWith(
      "/panel/usuarios",
      { page: 1, per_page: 10, sort: "nombre", order: "asc" },
      expect.any(Object),
    )
    routerGet.mockClear()
    api.onSort({ sortField: null, sortOrder: null })
    expect(routerGet.mock.calls[0][1]).toEqual({ page: 1, per_page: 10 })
  })

  it("aplica un filtro de lista al instante y uno de texto con espera", async () => {
    vi.useFakeTimers()
    const inmediato = montar({ paginacion: { number: 3, per_page: 10, count: 40 } })
    inmediato.api.onFilter({ filters: { rol: { value: "administrador" }, estado: { value: null } } })
    expect(routerGet).toHaveBeenCalledWith(
      "/panel/usuarios",
      { page: 1, per_page: 10, rol: "administrador" },
      expect.any(Object),
    )

    routerGet.mockClear()
    const texto = montar({ filtrosTexto: ["rol"] })
    texto.api.onFilter({ filters: { rol: { value: "crear" }, estado: { value: "" } } })
    expect(routerGet).not.toHaveBeenCalled()
    await vi.advanceTimersByTimeAsync(ESPERA_BUSQUEDA_MS)
    expect(routerGet).toHaveBeenCalledWith(
      "/panel/usuarios",
      { page: 1, per_page: 10, rol: "crear" },
      expect.any(Object),
    )
  })

  it("aplica un filtro de lista al instante y omite el vacío", () => {
    const { api } = montar({
      consulta: { q: "ana", sort: "", order: "desc", filtros: { rol: "", estado: "activo" } },
      paginacion: { number: 2, per_page: 10, count: 20 },
    })
    api.filtrar("rol", "administrador")
    expect(routerGet).toHaveBeenCalledWith(
      "/panel/usuarios",
      { page: 1, per_page: 10, q: "ana", rol: "administrador", estado: "activo" },
      expect.any(Object),
    )
    routerGet.mockClear()
    api.filtrar("estado", "  ")
    expect(routerGet.mock.calls[0][1]).toEqual({ page: 1, per_page: 10, q: "ana" })
  })

  it("espera 400 ms para un filtro de texto", async () => {
    vi.useFakeTimers()
    const { api } = montar({
      filtrosTexto: ["rol"],
      paginacion: { number: 3, per_page: 10, count: 40 },
    })
    api.filtrar("rol", "crear")
    expect(api.valoresFiltro.rol).toBe("crear")
    expect(routerGet).not.toHaveBeenCalled()
    await vi.advanceTimersByTimeAsync(ESPERA_BUSQUEDA_MS)
    expect(routerGet).toHaveBeenCalledWith(
      "/panel/usuarios",
      { page: 1, per_page: 10, rol: "crear" },
      expect.any(Object),
    )
  })

  it("arma el enlace de exportación sin la página", () => {
    const { api } = montar({
      consulta: { q: "ana", sort: "nombre", order: "asc", filtros: { rol: "votante", estado: "" } },
    })
    expect(api.hrefExportar("/panel/usuarios/exportar", "xlsx")).toBe(
      "/panel/usuarios/exportar?formato=xlsx&q=ana&sort=nombre&order=asc&rol=votante",
    )
  })
})
