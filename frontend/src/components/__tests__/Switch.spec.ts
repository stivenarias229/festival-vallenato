import { mount } from "@vue/test-utils"
import { describe, expect, it } from "vitest"

import Switch from "@/components/Switch.vue"

describe("Switch", () => {
  it("expone el estado con role switch", async () => {
    const wrapper = mount(Switch, { props: { modelValue: false, label: "Activo" } })
    const input = wrapper.get("input")
    expect(input.attributes("role")).toBe("switch")
    expect(input.attributes("aria-checked")).toBe("false")
    await input.setValue(true)
    expect(wrapper.emitted("update:modelValue")?.[0]).toEqual([true])
  })

  it("bloquea y muestra loader mientras guarda", () => {
    const wrapper = mount(Switch, { props: { modelValue: true, loading: true } })
    expect(wrapper.get("input").attributes("disabled")).toBeDefined()
    expect(wrapper.get("input").attributes("aria-busy")).toBe("true")
    expect(wrapper.get("[data-testid=loader]").exists()).toBe(true)
  })
})
