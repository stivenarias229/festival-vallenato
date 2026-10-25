import { mount } from "@vue/test-utils"
import { describe, expect, it } from "vitest"

import StepIndicator from "@/components/StepIndicator.vue"

describe("StepIndicator", () => {
  it("marca los pasos hasta el actual", () => {
    const wrapper = mount(StepIndicator, { props: { current: 2 } })
    const items = wrapper.findAll("li")
    expect(items).toHaveLength(4)
    expect(items[2].classes()).toContain("text-gold")
    expect(items[3].classes()).toContain("text-[#6f6580]")
  })
})
