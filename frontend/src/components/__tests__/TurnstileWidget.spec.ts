import { mount } from "@vue/test-utils"
import { afterEach, describe, expect, it, vi } from "vitest"

import TurnstileWidget from "@/components/TurnstileWidget.vue"

describe("TurnstileWidget", () => {
  afterEach(() => {
    delete window.turnstile
    document.querySelectorAll("script[data-turnstile]").forEach((n) => n.remove())
  })

  it("monta el widget y emite el token", async () => {
    const render = vi.fn((_el, options) => {
      options.callback("token-demo")
      return "widget-1"
    })
    window.turnstile = {
      render,
      reset: vi.fn(),
      remove: vi.fn(),
    }

    const wrapper = mount(TurnstileWidget, {
      props: { siteKey: "site-key-test" },
    })
    await vi.waitFor(() => expect(render).toHaveBeenCalled())
    expect(wrapper.emitted("token")?.[0]).toEqual(["token-demo"])
    expect(wrapper.get("[data-testid=turnstile]").exists()).toBe(true)
  })

  it("limpia el token al expirar", async () => {
    let expired: (() => void) | undefined
    window.turnstile = {
      render: vi.fn((_el, options) => {
        expired = options["expired-callback"]
        return "widget-2"
      }),
      reset: vi.fn(),
      remove: vi.fn(),
    }

    const wrapper = mount(TurnstileWidget, {
      props: { siteKey: "site-key-test" },
    })
    await vi.waitFor(() => expect(expired).toBeTypeOf("function"))
    expired?.()
    expect(wrapper.emitted("token")?.at(-1)).toEqual([""])
    expect(wrapper.emitted("expired")).toBeTruthy()
  })
})
