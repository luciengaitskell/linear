(function() {
    "use strict";

    var π = Math.PI
    var τ = 2 * Math.PI

    var types = {
        /*
            NOTE: `n` alternates sin1x, cos1x, sin2x, cos2x, ...
                however n goes 1,2,3,4,...
         */

        square: function(n) {
            if (n % 2 === 0) return 0;  // skip cos
            n = Math.ceil(n/2);

            return (((n + 1) % 2) ? 0 : 1) / n;
        },
        triangle: function(n) {
            if (n % 2 === 0) return 0;  // skip cos
            n = Math.ceil(n/2);

            if (!(n % 2)) return 0;
            return ((n % 4 === 1) ? 1 : -1) / (n * n);
        },
        sawtooth: function(n) {
            if (n % 2 === 0) return 0;  // skip cos
            n = Math.ceil(n/2);
            return (((n + 1) % 2) ? 1 : -1) / n;
        },
        pulse: function(n) {
            if (n % 2 === 0) return 0;  // skip cos
            return 0.1;
        },
        exercise22: function(n) {
            if (!(n % 2 ===0)) return 0;    // skip sin
            n = Math.ceil(n/2)

            return ((n % 2) ? -1 : 1) * (1/((n)**2));
        }
    };

    function FT(A, N, φ) {
        φ = φ || 0;
        return function(x) {
            var n = -1, y = 0;
            while (++n < N) {
                // NOTE: This n is NOT the same n given to the render functions
                //  defined above. The start at n=1 which corresponds to A[n=0]

                if (!(n%2)) {   // IF n EVEN
                    y += A[n] * Math.sin(τ * (Math.floor(n/2) + 1) * x + φ);
                } else {
                    y += A[n] * Math.cos(τ * (Math.floor(n/2) + 1) * x + φ);
                }

            }
            return y;
        }
    }

    function once(fn) {
        var exec = false;
        return function() {
            if (exec) return;
            exec = true,
            fn && fn();
        };
    }

    var
        margin = {top: 40, right: 100, bottom: 40, left: 150},
        W = 960,
        H = 500,
        w = W - margin.left - margin.right,
        h = H - margin.top - margin.bottom,

        radius = 140,
        theta  = 0,
        xmax   = 1.5,
        rate   = 1 / 60,

        tDomain = d3.range(0, 1.1, 1 / 1000),   // trace domain
        gDomain = d3.range(0, xmax, xmax / 1000), // graph domain

        C = types.square, // coeffiecients
        Lo = 6,           // set size
        L = 12,            // size
        F = 0.3,          // frequence

        yCirc = d3.scale.linear().domain([-1, 1]).range([h/2 + radius, h/2 - radius]),
        xCirc = d3.scale.linear().domain([-1, 1]).range([0, 2 * radius]),
        rAxis = d3.scale.linear().domain([0, 1]).range([0, radius]),
        xAxis = d3.scale.linear().range([radius, W - margin.left]),

        Fxy, fx, fy,

        draw, timer, data = [];

    var graph = d3.svg.line()
        .x(function(d) { return xAxis(d); })
        .y(function(d) { return yCirc(fy(theta - d)); });

    var proj = d3.svg.line()
        .x(function(d) { return xCirc(d.x); })
        .y(function(d) { return yCirc(d.y); });

    var trace = d3.svg.line()
        .x(function(d) { return xCirc(fx(d)); })
        .y(function(d) { return yCirc(fy(d)); });

    function gTransform(d) {
        return "translate(" + xCirc(d.x) + "," + yCirc(d.y) + ")";
    }

    function hTransform(d) {
        return "translate(" + xAxis(d.f) + "," + yCirc(0) + ")";
    }

    var svg = d3.select("main")
        .append("svg")
        .attr("width", W)
        .attr("height", H)

    svg.append("line")
        .attr("class", "axis")
        .attr("y1", margin.top + yCirc(0)).attr("x1", 0)
        .attr("y2", margin.top + yCirc(0)).attr("x2", W);

    svg.append("line")
        .attr("class", "axis")
        .attr("x1", margin.left + xCirc(0)).attr("y1", 0)
        .attr("x2", margin.left + xCirc(0)).attr("y2", H);

    var vis = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var gPath = vis.append("path").attr("class", "graph");
    var tPath = vis.append("path").attr("class", "trace");
    var pPath = vis.append("path").attr("class", "proj");

    function cache() {
        var A;
        if (typeof C === "function") {
            A = d3.range(1, L + 1).map(C);
        } else {
            A = C.slice(0, L);
        }

        fx = FT(A, L - 1, π/2);
        fy = FT(A, L - 1, 0),

            Fxy = A.map(function(a, i) {
                return { X: FT(A, i, π/2), Y: FT(A, i, 0), r: Math.abs(a) };
            });
    }

    function calc() {
        if (!Fxy) cache();
        Fxy.forEach(function(f, i) {
            var d = data[i] || (data[i] = {x:0,y:0,r:0});
            d.x = f.X(theta);
            d.y = f.Y(theta);
            d.r = f.r;
            d.f = i + 1;
        });
        data.length = Fxy.length;
        return data;
    }

    function coeff() {
        var co = vis.selectAll(".coeff").data(calc());

        // exit
        co.exit().remove();

        // enter
        var en = co.enter().append("g").attr("class", "coeff");

        en.append("circle").attr("class", "circle");
        en.append("circle").attr("class", "dot").attr("r", 3);

        // update
        co.classed("last",  function(d, i) { return i === L - 1; });
        co.classed("first", function(d, i) { return i === 0; });

        co.select(".circle").attr("r", function(d) { return rAxis(d.r); })

        return co;
    }

    function drawGraph() {
        xAxis.domain([0, xmax]);
        coeff().attr("transform", gTransform);
        var last = data[data.length - 1];
        pPath.attr("d", proj([last, {x:0,y:last.y}]));
        gPath.attr("d", graph(gDomain));
        tPath.attr("d", trace(tDomain));
    }

    function drawHisto() {
        xAxis.domain([1, L]);
        coeff().attr("transform", hTransform);
    }

    function toggle(callback) {
        var tran;
        tran = (draw === drawGraph) ? hTransform : gTransform;
        draw = (draw === drawGraph) ? drawHisto : drawGraph;
        coeff().transition()
            .duration(1000)
            .attr("transform", tran)
            .each("end", once(callback));
    }


    function toggleGraph() {
        xAxis.domain([0, xmax]);
        toggle(function() {
            pPath.classed("hide", false);
            gPath.classed("hide", false);
            tPath.classed("hide", false);
            play();
        });
    }

    function toggleHisto() {
        xAxis.domain([1, L]);
        pPath.classed("hide", true);
        gPath.classed("hide", true);
        tPath.classed("hide", true);
        pause(); toggle(drawHisto);
    }

    function play() {
        if (timer) return;
        (function loop() {
            drawGraph();
            theta += F * rate;
            timer = setTimeout(loop, rate * 1000);
        })();
    }

    function pause() {
        if (!timer) return;
        clearTimeout(timer);
        timer = null;
    }

    function redraw() {
        cache(); draw();
    }

    d3.select("svg").on("click", function() { (draw === drawHisto) ? toggleGraph() : toggleHisto(); });
    d3.select("#freq").on("change", function() { F = +this.value; redraw(); });
    d3.select("#size").on("change", function() {
        Lo = +this.value;
        L = Lo*2;
        redraw();
    });
    d3.select("#type").on("change", function() { C = types[this.value]; redraw(); });

    draw = drawGraph;
    play();

})();