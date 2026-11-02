import { flushPromises, mount } from "@vue/test-utils"
import PrimeVue from "primevue/config"
import { afterEach, beforeAll, describe, expect, it, vi } from "vitest"

import Usuarios from "@/pages/Panel/Usuarios.vue"
import { opcionesPrimeVue } from "@/primevue"
import { ESPERA_BUSQUEDA_MS } from "@/composables/useTablaServidor"

const routerGet = vi.hoisted(() => vi.fn())

vi.mock("@inertiajs/vue3", () => ({
  Head: { name: "Head", template: "<div />" },
  router: { get: routerGet, post: vi.fn() },
  usePage: () => ({
    url: "/panel/usuarios?page=1",
    props: {
      auth: { user: { id: 99, nombre: "Admin", email: "admin@festival.example", rol: "administrador" } },
      urls: {
        panel: "/panel",
        panel_usuarios: "/panel/usuarios",
        panel_usuarios_exportar: "/panel/usuarios/exportar",
      },
      flash: {},
    },
  }),
}))

const consultaVacia = {
  q: "",
  sort: "",
  order: "desc" as const,
  filtros: { rol: "", estado: "" },
}

const montar = (
  extra: { usuarios?: unknown[]; count?: number; consulta?: typeof consultaVacia; selectReal?: boolean } = {},
) =>
  mount(Usuarios, {
    props: {
      usuarios: extra.usuarios ?? [],
      paginacion: { number: 1, per_page: 10, count: extra.count ?? 0 },
      consulta: extra.consulta ?? consultaVacia,
    },
    attachTo: extra.selectReal ? document.body : undefined,
    global: {
      plugins: [[PrimeVue, opcionesPrimeVue]],
      stubs: {
        PageHeader: true,
        MochilaBand: true,
        ...(extra.selectReal ? {} : { SelectField: true }),
        Switch: true,
      },
    },
  })

describe("Usuarios del panel", () => {
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

  it("muestra el vacío y los enlaces de exportación", () => {
    const wrapper = montar({
      consulta: { q: "ana", sort: "nombre", order: "asc", filtros: { rol: "votante", estado: "" } },
    })
    expect(wrapper.text()).toContain("No hay resultados")
    expect(wrapper.get('a[href*="formato=csv"]').attributes("href")).toBe(
      "/panel/usuarios/exportar?formato=csv&q=ana&sort=nombre&order=asc&rol=votante",
    )
    expect(wrapper.get('a[href*="formato=xlsx"]').attributes("href")).toContain("formato=xlsx")
    expect(wrapper.get('a[href*="formato=csv"]').attributes("href")).not.toContain("page=")
    expect(wrapper.get(".barra-listado").element.children).toHaveLength(3)
    expect(wrapper.get('input[aria-label="Buscar"]').classes()).toContain("barra-filtro")
  })

  it("busca con espera y pagina en el servidor", async () => {
    const wrapper = montar({
      usuarios: [
        {
          id: 1,
          nombre: "Camila",
          email: "camila@correo.com",
          rol: "votante",
          estado: "activo",
          fecha_registro: "2026-01-01T00:00:00",
          tiene_votos: false,
        },
      ],
      count: 25,
    })
    vi.useFakeTimers()
    await wrapper.get('input[aria-label="Buscar"]').setValue("ana")
    await vi.advanceTimersByTimeAsync(ESPERA_BUSQUEDA_MS)
    expect(routerGet).toHaveBeenCalledWith(
      "/panel/usuarios",
      expect.objectContaining({ page: 1, q: "ana" }),
      expect.objectContaining({ only: ["usuarios", "paginacion", "consulta"] }),
    )

    vi.useRealTimers()
    routerGet.mockClear()
    await wrapper.get(".p-paginator-next").trigger("click")
    await flushPromises()
    expect(routerGet).toHaveBeenCalledWith(
      "/panel/usuarios",
      expect.objectContaining({ page: 2, per_page: 10 }),
      expect.any(Object),
    )
  })

  it("abre el filtro de rol con el listado oscuro", async () => {
    const wrapper = montar({
      selectReal: true,
      usuarios: [
        {
          id: 1,
          nombre: "Camila",
          email: "camila@correo.com",
          rol: "votante",
          estado: "activo",
          fecha_registro: "2026-01-01T00:00:00",
          tiene_votos: false,
        },
      ],
    })
    expect(wrapper.find("select").exists()).toBe(false)
    const filtroRol = wrapper.get('button[aria-label="Filtrar por rol"]')
    expect(filtroRol.classes()).not.toContain("py-2")
    expect(filtroRol.classes()).toContain("field")
    await filtroRol.trigger("click")
    const lista = document.querySelector("[role=listbox]")
    expect(lista?.className).toContain("bg-s2")
    expect(lista?.textContent).toContain("Administrador")
    wrapper.unmount()
  })
})
