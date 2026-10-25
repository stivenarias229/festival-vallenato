import { mount } from "@vue/test-utils"
import { describe, expect, it } from "vitest"

import StatusPill from "@/components/StatusPill.vue"

describe("StatusPill", () => {
  it("muestra abierta en jade", () => {
    const wrapper = mount(StatusPill, { props: { estado: "abierta" } })
    expect(wrapper.text()).toContain("abierta")
    expect(wrapper.classes()).toContain("text-jade")
  })

  it("muestra próxima en dorado", () => {
    const wrapper = mount(StatusPill, { props: { estado: "proxima" } })
    expect(wrapper.text()).toContain("próxima")
    expect(wrapper.classes()).toContain("text-gold")
  })

  it("muestra cerrada en gris", () => {
    const wrapper = mount(StatusPill, { props: { estado: "cerrada" } })
    expect(wrapper.text()).toContain("cerrada")
    expect(wrapper.classes()).toContain("text-mut")
  })
})
