import { mount } from "@vue/test-utils"
import { describe, expect, it } from "vitest"

import EmptyState from "@/components/EmptyState.vue"

describe("EmptyState", () => {
  it("renderiza título y descripción", () => {
    const wrapper = mount(EmptyState, {
      props: { titulo: "Sin datos", descripcion: "Vuelve más tarde" },
    })
    expect(wrapper.text()).toContain("Sin datos")
    expect(wrapper.text()).toContain("Vuelve más tarde")
  })
})
