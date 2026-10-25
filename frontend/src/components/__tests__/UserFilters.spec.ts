import { mount } from "@vue/test-utils"
import { describe, expect, it } from "vitest"

import UserFilters from "@/components/UserFilters.vue"

describe("UserFilters", () => {
  it("emite filtro y búsqueda", async () => {
    const wrapper = mount(UserFilters, { props: { q: "", filtro: "todos" } })
    await wrapper.get("input").setValue("camila")
    expect(wrapper.emitted("buscar")?.[0]).toEqual(["camila"])
    const chips = wrapper.findAll("button")
    await chips[1].trigger("click")
    expect(wrapper.emitted("filtrar")?.[0]).toEqual(["votante"])
  })
})
