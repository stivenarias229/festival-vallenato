import { mount } from "@vue/test-utils"
import { describe, expect, it } from "vitest"

import OptionCard from "@/components/OptionCard.vue"

describe("OptionCard", () => {
  it("marca la opción seleccionada", () => {
    const wrapper = mount(OptionCard, {
      props: { nombre: "Opción A", descripcion: "Artista A", selected: true },
    })
    expect(wrapper.classes().join(" ")).toContain("border-gold")
  })

  it("emite click al elegir", async () => {
    const wrapper = mount(OptionCard, {
      props: { nombre: "Opción B", descripcion: "Artista B" },
    })
    await wrapper.trigger("click")
    expect(wrapper.emitted("click")).toBeTruthy()
  })
})
