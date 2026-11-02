import { mount } from "@vue/test-utils"
import PrimeVue from "primevue/config"
import { afterEach, beforeAll, describe, expect, it, vi } from "vitest"

import Actividad from "@/pages/Panel/Actividad.vue"
import { opcionesPrimeVue } from "@/primevue"
import { ESPERA_BUSQUEDA_MS } from "@/composables/useTablaServidor"

const routerGet = vi.hoisted(() => vi.fn())

vi.mock("@inertiajs/vue3", () => ({
  Head: { name: "Head", template: "<div />" },
  router: { get: routerGet },
  usePage: () => ({
    url: "/panel/actividad?page=1",
    props: {
      auth: { user: { id: 99, nombre: "Admin", email: "admin@festival.example", rol: "administrador" } },
      urls: {
        panel: "/panel",
        panel_actividad: "/panel/actividad",
        panel_actividad_exportar: "/panel/actividad/exportar",
      },
      flash: {},
    },
  }),
}))

describe("Actividad del panel", () => {
  beforeAll(() => {
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: (query: string) => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: () => {},
        removeListener: () => {},
        addEventListener: () => {},
        removeEventListener: () => {},
        dispatchEvent: () => false,
      }),
    })
  })

  afterEach(() => {
    vi.useRealTimers()
    routerGet.mockReset()
  })

  it("pone los filtros de acción y entidad arriba, del mismo tamaño que la búsqueda", async () => {
    const wrapper = mount(Actividad, {
      props: {
        actividad: [],
        paginacion: { number: 1, per_page: 10, count: 0 },
        consulta: { q: "", sort: "", order: "desc", filtros: { accion: "", entidad_afectada: "" } },
      },
      global: {
        plugins: [[PrimeVue, opcionesPrimeVue]],
        stubs: { PageHeader: true, MochilaBand: true },
      },
    })

    const buscar = wrapper.get('input[aria-label="Buscar"]')
    const accion = wrapper.get('input[aria-label="Filtrar por acción"]')
    const entidad = wrapper.get('input[aria-label="Filtrar por entidad"]')
    expect(buscar.classes()).toEqual(accion.classes())
    expect(accion.classes()).toEqual(entidad.classes())
    expect(buscar.classes()).toContain("barra-filtro")
    expect(wrapper.get(".barra-listado").element.children).toHaveLength(3)
    expect(wrapper.find(".p-datatable-thead input").exists()).toBe(false)

    vi.useFakeTimers()
    await accion.setValue("crear")
    expect(routerGet).not.toHaveBeenCalled()
    await vi.advanceTimersByTimeAsync(ESPERA_BUSQUEDA_MS)
    expect(routerGet).toHaveBeenCalledWith(
      "/panel/actividad",
      expect.objectContaining({ page: 1, accion: "crear" }),
      expect.objectContaining({ only: ["actividad", "paginacion", "consulta"] }),
    )
  })
})
