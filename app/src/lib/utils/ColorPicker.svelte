<!-- 
    
    https://github.com/cooolbros/svelte-colourpicker/blob/main/src/lib/ColourPicker.svelte

    MIT License

    Copyright (c) 2022 Peter Wobcke

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

-->


<svelte:options immutable />

<script context="module" lang="ts">
    
    export let width: string = "0.8rem";
    export let height: string = "0.8rem";
    
    const hueColours = ["#ff0000", "#ffff00", "#00ff00", "#00ffff", "#0000ff", "#ff00ff", "#ff0000"]

    const size = 230

    type RGB = { r: number; g: number; b: number }
    type RGBA = RGB & A

    type HSV = { h: number; s: number; v: number }
    type HSVA = HSV & A

    type A = { a: number }

    const numberRegExp = "(\\d*\\.?\\d{1,3})"
    const delimiterRegExp = "[, ]+"

    const rgbRegExp = new RegExp(`rgb\\(\\s*${numberRegExp}${delimiterRegExp}${numberRegExp}${delimiterRegExp}${numberRegExp}\\s*\\)`, "i")
    const rgbaRegExp = new RegExp(`rgba\\(\\s*${numberRegExp}${delimiterRegExp}${numberRegExp}${delimiterRegExp}${numberRegExp}${delimiterRegExp}${numberRegExp}\\s*\\)`, "i")

    const hexRegExp = (n: number) => `([\\dA-F]{${n}})`

    const hex3RegExp = new RegExp(`^#?${hexRegExp(1).repeat(3)}$`, "i")
    const hex6RegExp = new RegExp(`^#?${hexRegExp(2).repeat(3)}$`, "i")
    const hex8RegExp = new RegExp(`^#?${hexRegExp(2).repeat(4)}$`, "i")

    function colour(input: string | RGB | RGBA | HSV | HSVA) {
        let r: number, g: number, b: number, h: number, s: number, v: number, a: number, rgba: string, hex: `#${string}`

        if (typeof input == "string") {
            let result: RegExpMatchArray | null

            if ((result = rgbRegExp.exec(input))) {
                r = parseFloat(result[1])
                g = parseFloat(result[2])
                b = parseFloat(result[3])
                a = 1
            } else if ((result = rgbaRegExp.exec(input))) {
                r = parseFloat(result[1])
                g = parseFloat(result[2])
                b = parseFloat(result[3])
                a = parseFloat(result[4])
            } else if ((result = hex3RegExp.exec(input))) {
                r = parseInt(result[1].repeat(2), 16)
                g = parseInt(result[2].repeat(2), 16)
                b = parseInt(result[3].repeat(2), 16)
                a = 1
                hex = `#${input}`
            } else if ((result = hex6RegExp.exec(input))) {
                r = parseInt(result[1], 16)
                g = parseInt(result[2], 16)
                b = parseInt(result[3], 16)
                a = 1
                hex = `#${input}`
            } else if ((result = hex8RegExp.exec(input))) {
                r = parseInt(result[1], 16)
                g = parseInt(result[2], 16)
                b = parseInt(result[3], 16)
                a = parseInt(result[4], 16)
                hex = `#${input}`
            } else {
                throw new Error(`Invalid input: "${input}"`)
            }

            const hsv = RGBToHSV(r, g, b)

            h = hsv.h
            s = hsv.s
            v = hsv.v
        } else if ("r" in input) {
            r = input.r
            g = input.g
            b = input.b

            const hsv = RGBToHSV(r, g, b)

            h = hsv.h
            s = hsv.s
            v = hsv.v

            a = "a" in input ? input.a : 1
        } else {
            h = input.h
            s = input.s
            v = input.v

            const rgb = HSVToRGB(h, s, v)

            r = rgb.r
            g = rgb.g
            b = rgb.b

            a = "a" in input ? input.a : 1
        }

        rgba = `rgba(${r}, ${g}, ${b}, ${a})`
        hex ??= `#${r.toString(16).padStart(2, "0")}${g.toString(16).padStart(2, "0")}${b.toString(16).padStart(2, "0")}${a != 1 ? Math.round(a * 255).toString(16) : ""}`

        return {
            r,
            g,
            b,
            h,
            s,
            v,
            a,
            rgba,
            hex
        }
    }

    /**
     * https://www.rapidtables.com/convert/color/rgb-to-hsv.html
     * https://www.geeksforgeeks.org/program-change-rgb-color-model-hsv-color-model/
     */
    function RGBToHSV(r: number, g: number, b: number): HSV {
        let h: number, s: number, v: number

        const r1 = r / 255
        const g1 = g / 255
        const b1 = b / 255

        const max = Math.max(r1, g1, b1)
        const min = Math.min(r1, g1, b1)

        const difference = max - min

        if (difference == 0) {
            h = 0
        } else {
            switch (max) {
                case r1:
                    h = (60 * ((g1 - b1) / difference) + 360) % 360
                    break
                case g1:
                    h = (60 * ((b1 - r1) / difference) + 120) % 360
                    break
                case b1:
                    h = (60 * ((r1 - g1) / difference) + 240) % 360
                    break
                default:
                    throw new Error("h did not match r1 | g1 | b1")
            }
        }

        s = max == 0 ? 0 : difference / max
        v = max

        return { h, s, v }
    }

    /**
     * https://www.rapidtables.com/convert/color/hsv-to-rgb.html
     */
    function HSVToRGB(h: number, s: number, v: number): RGB {
        let r: number, g: number, b: number

        const chroma = s * v
        const x = chroma * (1 - Math.abs(((h / 60) % 2) - 1))
        const m = v - chroma

        let r1: number, g1: number, b1: number

        if (h < 60) {
            r1 = chroma
            g1 = x
            b1 = 0
        } else if (60 <= h && h < 120) {
            r1 = x
            g1 = chroma
            b1 = 0
        } else if (h < 180) {
            r1 = 0
            g1 = chroma
            b1 = x
        } else if (h < 240) {
            r1 = 0
            g1 = x
            b1 = chroma
        } else if (h < 300) {
            r1 = x
            g1 = 0
            b1 = chroma
        } /* if (h < 360) */ else {
            r1 = chroma
            g1 = 0
            b1 = x
        }

        r = Math.round((r1 + m) * 255)
        g = Math.round((g1 + m) * 255)
        b = Math.round((b1 + m) * 255)

        return { r, g, b }
    }

    function clamp(value: number, min: number, max: number): number {
        if (value < min) {
            return min
        }
        if (value > max) {
            return max
        }
        return value
    }
</script>

<script lang="ts">
    import { createEventDispatcher, tick } from "svelte"
    import { fade, fly } from "svelte/transition"

    export let value: string = "rgba(255, 0, 0, 1)"

    const dispatch = createEventDispatcher<{ change: { rgb: RGB; hsv: HSV; hex: `#${string}` } & A }>()

    let c = colour(value)

    $: c && onColourChanged()

    function onColourChanged() {
        value = c.rgba
        dispatch("change", { rgb: { r: c.r, b: c.b, g: c.g }, hsv: { h: c.h, s: c.s, v: c.v }, hex: c.hex, a: c.a })
    }

    $: value && onValueChanged()

    function onValueChanged() {
        if (value != c.rgba) {
            c = colour(value)
        }
    }

    let open = false
    let dragging = false

    async function openPicker() {
        open = true
        await tick()
        drawColourCanvas()
        drawHueSlider()
        drawOpacitySlider()
    }

    async function tryClosePicker() {
        await tick()
        if (!dragging) {
            open = false
        }
    }

    let colourCanvas: HTMLCanvasElement
    let hueSlider: HTMLCanvasElement
    let opacitySlider: HTMLCanvasElement

    // #region Draw Canvas

    function drawColourCanvas() {
        const context = colourCanvas.getContext("2d")!

        context.clearRect(0, 0, colourCanvas.width, colourCanvas.height)

        const horizontalGradient = context.createLinearGradient(0, 0, colourCanvas.width, 0)
        horizontalGradient.addColorStop(0, "#ffffff")
        horizontalGradient.addColorStop(1, colour({ h: c.h, s: 1, v: 1 }).rgba)
        context.fillStyle = horizontalGradient
        context.fillRect(0, 0, colourCanvas.width, colourCanvas.height)

        const verticalGradient = context.createLinearGradient(0, 0, 0, colourCanvas.height)
        verticalGradient.addColorStop(0, "transparent")
        verticalGradient.addColorStop(1, "#000000")
        context.fillStyle = verticalGradient
        context.fillRect(0, 0, colourCanvas.width, colourCanvas.height)
    }

    function drawHueSlider() {
        const context = hueSlider.getContext("2d")!
        context.clearRect(0, 0, hueSlider.width, hueSlider.height)
        const gradient = context.createLinearGradient(0, 0, 0, hueSlider.height)
        for (let i = 0, offset = 0, step = 1 / (hueColours.length - 1); i < hueColours.length; i++, offset += step) {
            gradient.addColorStop(offset, hueColours[i])
        }
        context.fillStyle = gradient
        context.fillRect(0, 0, hueSlider.width, hueSlider.height)
    }

    function drawOpacitySlider() {
        const context = opacitySlider.getContext("2d")!
        context.clearRect(0, 0, opacitySlider.width, opacitySlider.height)

        const gradient = context.createLinearGradient(0, 0, 0, opacitySlider.height)
        gradient.addColorStop(0, "transparent")
        gradient.addColorStop(1, colour({ h: c.h, s: c.s, v: c.v, a: 1 }).rgba)
        context.fillStyle = gradient
        context.fillRect(0, 0, opacitySlider.width, opacitySlider.height)
    }

    // #endregion

    // #region Events

    const initListener = (fn: (e: MouseEvent) => void): ((e: MouseEvent) => void) => {
        const fn_preventDefault = (e: MouseEvent) => {
            e.preventDefault()
            fn(e)
        }
        return function (e: MouseEvent) {
            if (e.button != 0) {
                return
            }
            dragging = true
            fn(e)
            addEventListener("mousemove", fn_preventDefault)
            addEventListener("mouseup", () => {
                removeEventListener("mousemove", fn_preventDefault)
                dragging = false
            })
        }
    }

    function colourCanvasMove(e: MouseEvent): void {
        const rect = colourCanvas.getBoundingClientRect()
        c = colour({ h: c.h, s: clamp(e.pageX - rect.left, 0, size) / size, v: (size - clamp(e.pageY - rect.top, 0, size)) / size, a: c.a })
        drawOpacitySlider()
    }

    function hueSliderMove(e: MouseEvent): void {
        c = colour({ h: (clamp(e.pageY - hueSlider.getBoundingClientRect().top, 0, size) / size) * 360, s: c.s, v: c.v, a: c.a })
        drawColourCanvas()
        drawOpacitySlider()
    }

    function opacitySliderMove(e: MouseEvent): void {
        c = colour({ h: c.h, s: c.s, v: c.v, a: parseFloat((clamp(e.pageY - opacitySlider.getBoundingClientRect().top, 0, size) / size).toFixed(2)) })
    }

    function hexInputChange(e: Event & { currentTarget: EventTarget & HTMLInputElement }) {
        let value = e.currentTarget.value
        if (value.startsWith("#")) {
            value = value.substring(1)
        }
        if ([3, 6, 8].includes(value.length)) {
            c = colour(value)
        }
    }

    function redInputChange(e: Event & { currentTarget: EventTarget & HTMLInputElement }) {
        const value = parseFloat(e.currentTarget.value)
        if (value >= 0 && value <= 255) {
            c = colour({ r: value, g: c.g, b: c.b, a: c.a })
            drawColourCanvas()
            drawOpacitySlider()
        }
    }

    function greenInputChange(e: Event & { currentTarget: EventTarget & HTMLInputElement }) {
        const value = parseFloat(e.currentTarget.value)
        if (value >= 0 && value <= 255) {
            c = colour({ r: c.r, g: value, b: c.b, a: c.a })
            drawColourCanvas()
            drawOpacitySlider()
        }
    }

    function blueInputChange(e: Event & { currentTarget: EventTarget & HTMLInputElement }) {
        const value = parseFloat(e.currentTarget.value)
        if (value >= 0 && value <= 255) {
            c = colour({ r: c.r, g: c.g, b: value, a: c.a })
            drawColourCanvas()
            drawOpacitySlider()
        }
    }

    function alphaInputChange(e: Event & { currentTarget: EventTarget & HTMLInputElement }) {
        const value = parseFloat(e.currentTarget.value)
        if (value >= 0 && value <= 1) {
            c = colour({ h: c.h, s: c.s, v: c.v, a: value })
        }
    }

    // #endregion
</script>

<svelte:window on:mouseup={open && !dragging ? tryClosePicker : null} />

<div class="container flex items-center align-center">
    <div class="colour-input-container transparent">
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <div class="colour-input" style="width: {width}; height: {height}" style:--value={value} on:click|stopPropagation={openPicker} on:keypress|stopPropagation={openPicker} />
    </div>
    {#if open}
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <div
            class="colour-picker-container"
            in:fly={{ y: 10, duration: 150 }}
            out:fade={{ duration: 50 }}
            on:click|stopPropagation
            on:keypress|stopPropagation
            on:mouseup={(e) => !dragging && e.stopPropagation()}
        >
            <div class="colour-picker-arrow">
                <div class="colour-picker">
                    <div class="main">
                        <div class="canvas-container">
                            <canvas bind:this={colourCanvas} width={size} height={size} on:mousedown={initListener(colourCanvasMove)} />
                            <div
                                class="pointer pointer-both"
                                style:--pointer-bg={colour({ h: c.h, s: c.s, v: c.v, a: 1 }).rgba}
                                style:--x={`${c.s * size}px`}
                                style:--y={`${size - c.v * size}px`}
                            />
                        </div>
                        <div class="canvas-container">
                            <canvas bind:this={hueSlider} width={18} height={size} on:mousedown={initListener(hueSliderMove)} />
                            <div class="pointer pointer-vertical" style:--pointer-bg={colour({ h: c.h, s: 1, v: 1 }).rgba} style:--y={`${(c.h / 360) * size}px`} />
                        </div>
                        <div class="canvas-container transparent">
                            <canvas bind:this={opacitySlider} width={18} height={size} on:mousedown={initListener(opacitySliderMove)} />
                            <div class="pointer pointer-vertical" style:--pointer-bg={c.rgba} style:--y={`${c.a * size}px`} />
                        </div>
                    </div>
                    <div class="inputs-container">
                        <input type="text" maxlength={7} id="hex" value={c.hex} on:input={hexInputChange} />
                        <input type="number" autocomplete="off" min={0} max={255} id="r" value={c.r} on:input={redInputChange} />
                        <input type="number" autocomplete="off" min={0} max={255} id="g" value={c.g} on:input={greenInputChange} />
                        <input type="number" autocomplete="off" min={0} max={255} id="b" value={c.b} on:input={blueInputChange} />
                        <input type="number" autocomplete="off" min={0} max={255} id="a" value={c.a} on:input={alphaInputChange} />
                        <label for="hex">HEX</label>
                        <label for="r">R</label>
                        <label for="g">G</label>
                        <label for="b">B</label>
                        <label for="a">A</label>
                    </div>
                </div>
            </div>
        </div>
    {/if}
</div>

<style>
    :global([data-theme="dark"]) .container {
        --colour-picker-fg: #fff;
        --colour-picker-bg: #181818;
    }

    * {
        margin: 0;
        padding: 0;
        line-height: 1;
        box-sizing: border-box;
    }

    .container {
        position: relative;
        width: 2rem;
        height: 2rem;
        --colour-picker-fg: #000;
        --colour-picker-bg: #fff;
    }

    .colour-input-container {
        border-radius: 50%;
    }

    .colour-input {
        background-color: var(--value);
        border-radius: 50%;
        cursor: pointer;
        transition: 0ms;
    }

    .colour-picker-container {
        margin-top: 0.5rem;
        position: absolute;
        z-index: 1;
        transform-origin: top left;
        filter: drop-shadow(2px 2px 5px rgba(0, 0, 0, 0.2));
    }

    .colour-picker-arrow {
        padding-top: 0.5rem;
        background-image: linear-gradient(180deg, var(--colour-picker-bg) 0 0.5rem, transparent 0.5rem 100%);
        clip-path: polygon(0 0.5rem, 0.5rem 0.5rem, 1rem 0, 1.5rem 0.5rem, 100% 0.5rem, 100% 100%, 0 100%);
    }

    .colour-picker {
        padding: 0.5rem;
        background: var(--colour-picker-bg);
        border-radius: 3px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .main {
        display: flex;
        justify-content: space-between;
        gap: 10px;
    }

    .canvas-container {
        position: relative;
    }

    canvas {
        display: block;
        border-radius: 3px;
    }

    .pointer {
        position: absolute;
        width: 12px;
        height: 12px;
        background: var(--pointer-bg);
        border: 2px solid #ffffff;
        border-radius: 50%;
        box-shadow: 0 0 1px rgba(0, 0, 0, 0.2);
        transition: 0ms !important;
        pointer-events: none;
    }

    .pointer-both {
        left: var(--x);
        top: var(--y);
        transform: translate(-6px, -6px);
    }

    .pointer-vertical {
        left: 3px;
        top: var(--y);
        transform: translateY(-6px);
    }

    .inputs-container {
        display: grid;
        grid-template-columns: 1fr repeat(4, auto);
        gap: 0.5rem;
    }

    input {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
        font-size: 0.9rem;
        color: var(--colour-picker-fg);
        padding: 4px;
        background: none;
        border: 1px solid rgba(0, 0, 0, 0.2);
        border-radius: 3px;
    }

    input[type="text"] {
        width: 5rem;
    }

    input:focus {
        outline: 1px solid rgb(0, 150, 255);
    }

    input[type="number"] {
        width: 2.75rem;
        appearance: textfield;
        -moz-appearance: textfield; /* Firefox */
    }

    input[type="number"]::-webkit-outer-spin-button,
    input[type="number"]::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }

    label {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
        font-size: 0.8rem;
        color: rgb(89, 89, 89);
        line-height: 1;
    }

    .transparent {
        --bg: rgba(0, 0, 0, 0.1);
        background-image: linear-gradient(45deg, var(--bg) 25%, transparent 25%, transparent 75%, var(--bg) 75%, var(--bg)),
            linear-gradient(45deg, var(--bg) 25%, transparent 25%, transparent 75%, var(--bg) 75%, var(--bg));
        background-position: 0px 0px, 4px 4px;
        background-size: 8px 8px;
    }

    :global([data-theme="dark"]) .transparent {
        --bg: rgba(50, 50, 50, 0.1);
    }
</style>