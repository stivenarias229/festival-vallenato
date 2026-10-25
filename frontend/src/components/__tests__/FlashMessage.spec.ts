import { mount, type VueWrapper } from "@vue/test-utils"
import { afterEach, describe, expect, it, vi } from "vitest"

import FlashMessage from "@/components/FlashMessage.vue"

vi.mock("@inertiajs/vue3", () => ({
  usePage: () => ({ props: { flash: {} } }),
}))

describe("FlashMessage", () => {
  let wrapper: VueWrapper | undefined

  afterEach(() => {
    wrapper?.unmount()
    document.body.innerHTML = ""
    vi.useRealTimers()
  })

  const montar = (flash: { success?: string; error?: string; info?: string }) => {
    wrapper = mount(FlashMessage, {
      props: { flash },
      attachTo: document.body,
    })
    return wrapper
  }

  it("muestra un toast de éxito visible y no ocupa el flujo de la página", () => {
    montar({ success: "Estado de la categoría actualizado." })
    const toast = document.querySelector("[data-testid=toast-stack] article")
    expect(toast?.getAttribute("role")).toBe("status")
    expect(toast?.textContent).toContain("Listo")
    expect(toast?.textContent).toContain("Estado de la categoría actualizado.")
    expect(document.querySelector("[data-testid=toast-stack]")?.className).toContain("fixed")
  })

  it("usa alerta para errores", () => {
    montar({ error: "Revisa los datos de la categoría." })
    const toast = document.querySelector("[data-testid=toast-stack] article")
    expect(toast?.getAttribute("role")).toBe("alert")
    expect(toast?.textContent).toContain("Error")
    expect(toast?.textContent).toContain("Revisa los datos de la categoría.")
  })

  it("se cierra al pulsar el botón", async () => {
    montar({ info: "Debes verificar tu correo antes de votar." })
    const cerrar = document.querySelector('[aria-label="Cerrar aviso"]') as HTMLButtonElement
    expect(cerrar).toBeTruthy()
    cerrar.click()
    await wrapper?.vm.$nextTick()
    expect(document.querySelector("[data-testid=toast-stack]")).toBeNull()
  })

  it("desaparece solo después de unos segundos", async () => {
    vi.useFakeTimers()
    montar({ success: "Edición guardada." })
    expect(document.body.textContent).toContain("Edición guardada.")
    await vi.advanceTimersByTimeAsync(5600)
    expect(document.querySelector("[data-testid=toast-stack]")).toBeNull()
  })
})
