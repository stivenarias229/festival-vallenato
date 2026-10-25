import { mount } from "@vue/test-utils"
import { describe, expect, it, vi } from "vitest"

import Inicio from "@/pages/Publico/Inicio.vue"

const pageProps = {
  auth: { user: null as { id: number; nombre: string; email: string; rol: string } | null },
  urls: { categorias: "/categorias", registro: "/registro" },
}

vi.mock("@inertiajs/vue3", () => ({
  Head: { name: "Head", template: "<div />" },
  Link: { name: "Link", template: "<a><slot /></a>", props: ["href"] },
  usePage: () => ({ props: pageProps }),
}))

const montar = () =>
  mount(Inicio, {
    global: {
      stubs: {
        AccordionHero: true,
        Icon: true,
        MochilaBand: true,
        PageHeader: true,
      },
    },
  })

describe("Inicio público", () => {
  it("ofrece crear cuenta cuando no hay sesión", () => {
    pageProps.auth.user = null
    const wrapper = montar()
    expect(wrapper.text()).toContain("Crear mi cuenta")
    expect(wrapper.text()).toContain("Explorar votaciones")
  })

  it("oculta crear cuenta cuando ya hay sesión", () => {
    pageProps.auth.user = {
      id: 1,
      nombre: "Votante Demo",
      email: "votante@correo.com",
      rol: "votante",
    }
    const wrapper = montar()
    expect(wrapper.text()).not.toContain("Crear mi cuenta")
    expect(wrapper.text()).toContain("Explorar votaciones")
  })
})
