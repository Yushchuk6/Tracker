
class Plot {
    constructor(id, data, layout, config) {
        this.id = id;
        this.data = data;
        this.layout = layout;
        this.config = config;

        Plotly.newPlot(id, plot_data, plot_layout, plot_config);
    }

    update_trace(update) {
        const trace = this.data.find(e => e.name === update.name);

        this._add_to_dict(trace, update)

        Plotly.redraw(this.id);
        console.log(`[update] trace \'${update.name}\' updated`);
    }

    update_layout(update) {
        Plotly.relayout(this.id, update)
        console.log(`[update] layout updated`);
        console.log(Plotly);
    }

    _add_to_dict(origin, update) {
        for (const [key, value] of Object.entries(update)) {
            origin[key] = value
        }
    }
}