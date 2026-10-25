import { mount } from "@vue/test-utils"
import { describe, expect, it } from "vitest"

import Button from "@/components/Button.vue"

describe("Button", () => {
  it("muestra loader y se bloquea mientras espera al servidor", () => {
    const wrapper = mount(Button, {
      props: { loading: true },
      slots: { default: "Guardar" },
    })
    const boton = wrapper.get("button")
    expect(boton.attributes("disabled")).toBeDefined()
    expect(boton.attributes("aria-busy")).toBe("true")
    expect(wrapper.get("[data-testid=loader]").exists()).toBe(true)
    expect(wrapper.text()).toContain("Guardar")
  })

  it("queda libre cuando no hay petición en curso", () => {
    const wrapper = mount(Button, { slots: { default: "Guardar" } })
    expect(wrapper.find("[data-testid=loader]").exists()).toBe(false)
    expect(wrapper.get("button").attributes("disabled")).toBeUndefined()
    expect(wrapper.get("button").attributes("aria-busy")).toBeUndefined()
  })

  it("separa botones apilados de ancho completo", () => {
    const wrapper = mount({
      components: { Button },
      template: "<div><Button>Uno</Button><Button>Dos</Button></div>",
    })
    const botones = wrapper.findAll("button")
    expect(botones[0].classes()).toContain("app-btn-stack")
    expect(botones[1].classes()).toContain("app-btn-stack")
  })

  it("no apila con margen los botones mini de una misma fila", () => {
    const wrapper = mount(Button, {
      props: { size: "mini" },
      slots: { default: "Abrir" },
    })
    expect(wrapper.get("button").classes()).not.toContain("app-btn-stack")
  })
})
