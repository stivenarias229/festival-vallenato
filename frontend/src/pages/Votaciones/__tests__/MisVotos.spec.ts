import { mount } from "@vue/test-utils"
import { describe, expect, it, vi } from "vitest"

import MisVotos from "@/pages/Votaciones/MisVotos.vue"

const pageProps = {
  urls: { categorias: "/categorias", mis_votos: "/mis-votos" },
}

vi.mock("@inertiajs/vue3", () => ({
  Head: { name: "Head", template: "<div />" },
  Link: { name: "Link", template: "<a><slot /></a>", props: ["href"] },
  usePage: () => ({ props: pageProps }),
}))

const montar = (votos: unknown[] = []) =>
  mount(MisVotos, {
    props: { votos },
    global: {
      stubs: {
        Button: { name: "Button", template: "<a><slot /></a>", props: ["href"] },
        EmptyState: {
          name: "EmptyState",
          template: "<div><p>{{ titulo }}</p><slot /></div>",
          props: ["titulo", "descripcion"],
        },
        MochilaBand: true,
        PageHeader: true,
      },
    },
  })

describe("MisVotos", () => {
  it("muestra estado vacío sin votos", () => {
    const wrapper = montar([])
    expect(wrapper.text()).toContain("Aún no has votado")
  })

  it("lista categoría, votación y opción elegida", () => {
    const wrapper = montar([
      {
        id: 1,
        fecha_hora: "2026-11-06T20:00:00Z",
        categoria: { id: 1, nombre: "Acordeón" },
        votacion: { id: 10, titulo: "Canción favorita" },
        opcion: { id: 100, nombre: "Opción A" },
      },
    ])
    expect(wrapper.text()).toContain("Acordeón")
    expect(wrapper.text()).toContain("Canción favorita")
    expect(wrapper.text()).toContain("Opción A")
    expect(wrapper.text()).toContain("Votar en otra categoría")
  })
})
