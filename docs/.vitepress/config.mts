import { defineConfig } from "vitepress";

const ogDescription = "A modern, programmatic framework for building Minecraft datapacks natively in Python.";
const ogImage = "https://raw.githubusercontent.com/OguzhanUmutlu/flare/main/docs/public/assets/icon_transparent.png";
const ogTitle = "Flare";
const ogUrl = "https://flare.oguzhanumutlu.com";

const githubLink = "https://github.com/OguzhanUmutlu/flare";

export default defineConfig({
    title: "Flare",
    description: ogDescription,
    ignoreDeadLinks: true,
    cleanUrls: true,

    head: [
        ["link", { rel: "icon", type: "image/png", href: "./assets/icon.png" }],
        ["meta", { property: "og:type", content: "website" }],
        ["meta", { property: "og:title", content: ogTitle }],
        ["meta", { property: "og:image", content: ogImage }],
        ["meta", { property: "og:url", content: ogUrl }],
        ["meta", { property: "og:description", content: ogDescription }],
        ["meta", { name: "theme-color", content: "#ff6b35" }],
        ["link", { rel: "preconnect", href: "https://fonts.googleapis.com" }],
        ["link", { rel: "preconnect", href: "https://fonts.gstatic.com", crossorigin: "" }],
        ["link", { rel: "stylesheet", href: "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap" }]
    ],

    locales: {
        root: { label: "English" }
    },

    themeConfig: {
        logo: "./assets/icon_transparent.png",
        editLink: {
            pattern: "https://github.com/OguzhanUmutlu/flare/edit/main/docs/:path",
            text: "Suggest changes to this page"
        },
        socialLinks: [
            { icon: "github", link: githubLink }
        ],
        search: {
            provider: "local",
            options: {}
        },
        footer: {
            message: "Released under the MIT License.",
            copyright: "Copyright © 2026-present OguzhanUmutlu & Flare Contributors"
        },
        nav: [
            { text: "Guide", link: "/guide/", activeMatch: "/guide/" },
            { text: "Playground", link: "/playground", activeMatch: "/playground" },
            { text: "GitHub", link: githubLink }
        ],
        sidebar: {
            "/guide/": [
                {
                    text: "Introduction",
                    items: [
                        { text: "Getting Started", link: "/guide/" },
                        { text: "CLI Reference", link: "/guide/cli" }
                    ]
                },
                {
                    text: "Core Concepts",
                    items: [
                        { text: "Native Commands", link: "/guide/native-commands" },
                        { text: "Debugging", link: "/guide/debugging" },
                        { text: "Scores", link: "/guide/scores" },
                        { text: "NBT Variables", link: "/guide/nbt" },
                        { text: "Execute Modifiers", link: "/guide/execute" },
                        { text: "Control Flow", link: "/guide/control-flow" },
                        { text: "Exported Functions", link: "/guide/functions" }
                    ]
                },
                {
                    text: "Advanced",
                    items: [
                        { text: "Advanced Math", link: "/guide/math" },
                        { text: "Entity Selectors", link: "/guide/selectors" },
                        { text: "Beet Integration", link: "/guide/beet" },
                        { text: "Internals", link: "/guide/internals" }
                    ]
                }
            ]
        }
    }
});
