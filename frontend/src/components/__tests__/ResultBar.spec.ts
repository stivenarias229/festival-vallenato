import { mount } from "@vue/test-utils"
import { describe, expect, it } from "vitest"

import ResultBar from "@/components/ResultBar.vue"

describe("ResultBar", () => {
  it("muestra porcentaje y nombre", () => {
    const wrapper = mount(ResultBar, {
      props: { nombre: "Opción A", porcentaje: 46, votos: 12 },
    })
    expect(wrapper.text()).toContain("Opción A")
    expect(wrapper.text()).toContain("46%")
    expect(wrapper.get("i").attributes("style")).toContain("46%")
  })
})
