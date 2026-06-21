import Theme from "vitepress/theme";
import "./styles/vars.css";
import "./styles/common.css";
import Playground from "./components/Playground.vue";

export default {
    ...Theme,
    enhanceApp({ app }) {
        app.component("Playground", Playground);
    }
};
