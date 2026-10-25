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
})
