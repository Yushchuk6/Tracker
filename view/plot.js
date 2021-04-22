


// function test() {
//     const res = {}
//     res['name'] = 'path';
//     res['lat'] = [1, 2, 3, 4];
//     res['lon'] = [10, 4, 8, 2];

//     update_trace('plot', res);
// }



class Plot {
    constructor(id, data, layout, config){
        this.id = id;
        this.data = data;
        this.layout = layout;
        this.config = config;

        Plotly.newPlot(id, plot_data, plot_layout, plot_config);
    }

    update_trace(update) {
        const trace = this.data.find(e => e.name === update.name);
    
        for (const [key, value] of Object.entries(update)) {
            trace[key] = value
        }
    
        Plotly.redraw(this.id);
        console.log(`[update] trace \'${update.name}\' updated`);
    }
}