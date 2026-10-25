import { mount } from "@vue/test-utils"
import { describe, expect, it } from "vitest"

import Icon from "@/components/Icon.vue"

describe("Icon", () => {
  it("renderiza el trazo del icono pedido", () => {
    const wrapper = mount(Icon, { props: { name: "home", size: 24 } })
    const svg = wrapper.get("svg")
    expect(svg.attributes("viewBox")).toBe("0 0 24 24")
    expect(svg.attributes("stroke-width")).toBe("1.7")
    expect(svg.html()).toContain("M3 11l9-8 9 8")
  })

  it("acepta alias del prototipo", () => {
    const wrapper = mount(Icon, { props: { name: "acc" } })
    expect(wrapper.html()).toContain("M6 7l2 10")
  })
})
