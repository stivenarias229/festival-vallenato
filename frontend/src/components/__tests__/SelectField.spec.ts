import { mount, type VueWrapper } from "@vue/test-utils"
import { afterEach, describe, expect, it } from "vitest"

import SelectField from "@/components/SelectField.vue"

const opciones = [
  { value: "acc", label: "Acordeón" },
  { value: "music", label: "Canción vallenata inédita" },
  { value: "star", label: "Artista emergente" },
]

describe("SelectField", () => {
  let wrapper: VueWrapper | undefined

  afterEach(() => {
    wrapper?.unmount()
    document.body.innerHTML = ""
  })

  const montar = (props: Record<string, unknown> = {}) => {
    wrapper = mount(SelectField, {
      props: { options: opciones, modelValue: "star", ...props },
      attachTo: document.body,
    })
    return wrapper
  }

  it("muestra la opción actual en el disparador", () => {
    montar()
    expect(wrapper?.get("button").text()).toContain("Artista emergente")
    expect(document.querySelector("[role=listbox]")).toBeNull()
  })

  it("abre opciones con contraste y permite elegir", async () => {
    montar()
    await wrapper?.get("button").trigger("click")
    const lista = document.querySelector("[role=listbox]")
    expect(lista).toBeTruthy()
    expect(lista?.textContent).toContain("Acordeón")
    expect(lista?.textContent).toContain("Canción vallenata inédita")
    expect(lista?.className).toContain("bg-s2")
    const elegido = document.querySelector('[role=option][aria-selected="true"]')
    expect(elegido?.textContent).toContain("Artista emergente")
    const acordeon = [...document.querySelectorAll("[role=option]")].find((nodo) =>
      nodo.textContent?.includes("Acordeón"),
    ) as HTMLButtonElement
    acordeon.click()
    await wrapper?.vm.$nextTick()
    expect(wrapper?.emitted("update:modelValue")?.[0]).toEqual(["acc"])
    expect(document.querySelector("[role=listbox]")).toBeNull()
  })

  it("no abre el listado si está deshabilitado", async () => {
    montar({ disabled: true })
    await wrapper?.get("button").trigger("click")
    expect(document.querySelector("[role=listbox]")).toBeNull()
  })
})
