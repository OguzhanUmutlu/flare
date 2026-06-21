---
layout: home

title: Flare
titleTemplate: Programmatic Minecraft Datapacks in Python

hero:
  name: Flare 🔥
  text: Programmatic Datapacks in Python
  tagline: "Write Minecraft logic using full Python power: scores, NBT, execute chains, recursion, and more. Compile to optimized datapacks instantly."
  image:
    src: ./assets/icon_transparent.png
    alt: Flare
    classes: floating-logo
  actions:
    - theme: brand
      text: Get Started
      link: /guide/
    - theme: alt
      text: Playground
      link: /playground
    - theme: alt
      text: View on GitHub
      link: https://github.com/OguzhanUmutlu/flare

features:
  - icon: 🐍
    title: Python-Native
    details: Flare is just Python. Use any library, any logic - your full dev environment works out of the box.
  - icon: ⚡
    title: Instant Compilation
    details: Generate optimized `.mcfunction` datapacks in milliseconds. Watch mode rebuilds on every save.
  - icon: 🎯
    title: Scoreboard & NBT
    details: First-class score and NBT types with automatic path-chaining, type inference, and operator overloading.
  - icon: 🔁
    title: True Recursion
    details: Flare's static Call Graph Analyzer detects recursion and automatically switches to an NBT stack - no setup required.
  - icon: 🧮
    title: Advanced Math
    details: IEEE 754 float32/float64, big integers, and a full trig/log math library compiled to native scoreboard operations.
  - icon: 🕹️
    title: Live Playground
    details: Try Flare right in your browser - no install needed. Powered by Pyodide.
---

<style>
.floating-logo {
  animation: float 4s ease-in-out infinite;
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-15px);
  }
  100% {
    transform: translateY(0px);
  }
}

.VPHero .image-src {
  filter:
    drop-shadow(0 0 18px rgba(0, 0, 0, 0.85))
    drop-shadow(0 0 40px rgba(255, 200, 80, 0.5))
    brightness(1.15)
    contrast(1.05);
}
</style>
