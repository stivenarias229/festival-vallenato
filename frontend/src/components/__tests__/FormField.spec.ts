import { mount } from "@vue/test-utils"
import { describe, expect, it } from "vitest"

import FormField from "@/components/FormField.vue"

describe("FormField", () => {
  it("muestra el error de validación", () => {
    const wrapper = mount(FormField, {
      props: { label: "Correo", error: "Este correo ya está registrado.", forId: "email" },
      slots: { default: '<input id="email" />' },
    })
    expect(wrapper.get("[role=alert]").text()).toContain("Este correo ya está registrado.")
    expect(wrapper.get("label").attributes("for")).toBe("email")
  })

  it("deja la etiqueta visible cuando el campo ya tiene valor", () => {
    const wrapper = mount(FormField, {
      props: { label: "Categoría", compact: true, forId: "categoria" },
      slots: { default: '<input id="categoria" value="Artista emergente" />' },
    })
    expect(wrapper.get("label").text()).toBe("Categoría")
    expect(wrapper.get("label").attributes("for")).toBe("categoria")
  })
})
