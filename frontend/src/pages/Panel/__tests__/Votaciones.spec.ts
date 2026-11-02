import { flushPromises, mount } from "@vue/test-utils"
import PrimeVue from "primevue/config"
import { beforeAll, describe, expect, it, vi } from "vitest"

import Votaciones from "@/pages/Panel/Votaciones.vue"
import { opcionesPrimeVue } from "@/primevue"

const routerGet = vi.hoisted(() => vi.fn())

vi.mock("@inertiajs/vue3", () => ({
  Head: { name: "Head", template: "<div />" },
  Link: { name: "Link", props: ["href"], template: '<a :href="href"><slot /></a>' },
  router: { get: routerGet, post: vi.fn() },
  useForm: (datos: Record<string, unknown>) => ({ ...datos, processing: false, post: vi.fn() }),
  usePage: () => ({
    url: "/panel/votaciones?page=1",
    props: {
      auth: { user: { id: 99, nombre: "Admin", email: "admin@festival.example", rol: "administrador" } },
      urls: {
        panel: "/panel",
        panel_votaciones: "/panel/votaciones",
        panel_votaciones_exportar: "/panel/votaciones/exportar",
      },
      flash: {},
    },
  }),
}))

const votacion = {
  id: 1,
  titulo: "Mejor canción",
  categoria_id: 2,
  categoria_nombre: "Canción vallenata inédita",
  fecha_inicio: "2026-10-01T00:00:00",
  fecha_fin: "2026-11-03T00:00:00",
  estado: "abierta",
  estado_efectivo: "abierta",
  reglas: "",
  visibilidad_resultados: "internos",
  limite_votos_por_usuario: 1,
  resumen_fecha: "Hasta el 3 de noviembre",
  opciones_count: 3,
}

describe("Votaciones del panel", () => {
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

  it("filtra por estado con el selector del panel y no ofrece filtro de categoría", async () => {
    const wrapper = mount(Votaciones, {
      props: {
        categorias: [{ id: 2, nombre: "Canción vallenata inédita" }],
        votaciones: [votacion],
        paginacion: { number: 1, per_page: 10, count: 1 },
        consulta: { q: "", sort: "", order: "desc", filtros: { estado: "" } },
      },
      attachTo: document.body,
      global: {
        plugins: [[PrimeVue, opcionesPrimeVue]],
        stubs: { PageHeader: true, MochilaBand: true },
      },
    })

    expect(wrapper.find('[aria-label="Filtrar por categoría"]').exists()).toBe(false)
    expect(wrapper.find("select").exists()).toBe(false)
    expect(wrapper.get(".barra-listado").element.children).toHaveLength(2)
    const filtroEstado = wrapper.get('button[aria-label="Filtrar por estado"]')
    expect(filtroEstado.classes()).not.toContain("py-2")
    expect(filtroEstado.classes()).toContain("field")

    await filtroEstado.trigger("click")
    const lista = document.querySelector("[role=listbox]")
    expect(lista?.className).toContain("bg-s2")
    expect(lista?.textContent).toContain("Abierta")

    const abierta = [...document.querySelectorAll("[role=option]")].find((nodo) =>
      nodo.textContent?.includes("Abierta"),
    ) as HTMLButtonElement
    abierta.click()
    await flushPromises()

    expect(routerGet).toHaveBeenCalledWith(
      "/panel/votaciones",
      expect.objectContaining({ page: 1, estado: "abierta" }),
      expect.objectContaining({ only: ["votaciones", "paginacion", "consulta"] }),
    )
    wrapper.unmount()
  })
})
