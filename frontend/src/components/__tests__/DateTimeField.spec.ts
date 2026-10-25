import { mount, type VueWrapper } from "@vue/test-utils"
import { afterEach, describe, expect, it, vi } from "vitest"

import DateTimeField from "@/components/DateTimeField.vue"

describe("DateTimeField", () => {
  let wrapper: VueWrapper | undefined

  afterEach(() => {
    wrapper?.unmount()
    vi.unstubAllGlobals()
  })

  it("muestra un texto legible en lugar del formato nativo", () => {
    wrapper = mount(DateTimeField, {
      props: { modelValue: "2026-10-25T14:30", placeholder: "Fecha de inicio" },
    })
    expect(wrapper.text()).toMatch(/25/)
    expect(wrapper.text()).toMatch(/2026/)
    expect(wrapper.text()).not.toContain("dd/mm/aaaa")
  })

  it("abre el selector al pulsar cualquier parte del campo", async () => {
    const showPicker = vi.fn()
    wrapper = mount(DateTimeField, { props: { modelValue: "", placeholder: "Fecha de inicio" } })
    const input = wrapper.get("input").element as HTMLInputElement
    input.showPicker = showPicker
    await wrapper.get("[data-testid=datetime-field]").trigger("click")
    expect(showPicker).toHaveBeenCalledTimes(1)
  })

  it("no abre el selector si está deshabilitado", async () => {
    const showPicker = vi.fn()
    wrapper = mount(DateTimeField, { props: { modelValue: "", disabled: true } })
    const input = wrapper.get("input").element as HTMLInputElement
    input.showPicker = showPicker
    await wrapper.get("[data-testid=datetime-field]").trigger("click")
    expect(showPicker).not.toHaveBeenCalled()
  })
})
