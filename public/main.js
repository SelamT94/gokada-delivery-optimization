// public/main.js
document.addEventListener('DOMContentLoaded', function() {
    const map = L.map('map').setView([6.5244, 3.3792], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(map);

    // Load taxi trip data
    d3.csv('../data/preprocessed_data.csv').then(function(data) {

        // Draw polyline and markers on the map
        data.forEach(d => {
            const startLatLng = [d['Origin Lat'], d['Origin Lon']];
            const endLatLng = [d['Destination Lat'], d['Destination Lon']];
            const tripDistance = d['Trip Distance (km)'].toFixed(2);
            const tripDuration = d['trip_duration'].toFixed(2);
            const tripDate = d['Trip Date '];

            // Add a polyline for each trip
            const polyline = L.polyline([startLatLng, endLatLng], { color: 'blue' }).addTo(map);

            // Add marker with popup for trip details
            const popupContent = `
                <b>Trip Details</b><br>
                Distance: ${tripDistance} km<br>
                Duration: ${tripDuration} min<br>
                Start Time: ${d['trip_start_time']}<br>
                End Time: ${d['trip_end_time']}
            `;
            const marker = L.marker(startLatLng).addTo(map);
            marker.bindPopup(popupContent);
        });

        // Create a bar chart for trip durations
        const durations = data.map(d => parseFloat(d['trip_duration']));
        const binWidth = 5; // Set bin width for histogram
        const bins = d3.bin()(durations);

        const xScale = d3.scaleLinear()
            .domain([0, d3.max(bins, d => d.x1)])
            .range([0, 400]);

        const yScale = d3.scaleLinear()
            .domain([0, d3.max(bins, d => d.length)])
            .range([300, 0]);

        const xAxis = d3.axisBottom(xScale);
        const yAxis = d3.axisLeft(yScale);

        const svgBar = d3.select('#bar-chart')
            .append('svg')
            .attr('width', 400)
            .attr('height', 300);

        svgBar.selectAll('rect')
            .data(bins)
            .enter()
            .append('rect')
            .attr('x', d => xScale(d.x0))
            .attr('y', d => yScale(d.length))
            .attr('width', d => xScale(d.x1) - xScale(d.x0) - 1)
            .attr('height', d => 300 - yScale(d.length))
            .attr('fill', 'steelblue');

        svgBar.append('g')
            .attr('transform', `translate(0, ${300})`)
            .call(xAxis);

        svgBar.append('g')
            .call(yAxis);

        // Create a line chart for trip distance over time
        const distancesOverTime = d3.nest()
            .key(d => d['Trip Date '])
            .rollup(v => d3.sum(v, d => parseFloat(d['Trip Distance (km)'])))
            .entries(data);

        const parseDate = d3.timeParse('%Y-%m-%d %H:00:00');

        const xScaleLine = d3.scaleTime()
            .domain(d3.extent(distancesOverTime, d => parseDate(d.key)))
            .range([0, 800]);

        const yScaleLine = d3.scaleLinear()
            .domain([0, d3.max(distancesOverTime, d => d.value)])
            .range([300, 0]);

        const xAxisLine = d3.axisBottom(xScaleLine);
        const yAxisLine = d3.axisLeft(yScaleLine);

        const svgLine = d3.select('#line-chart')
            .append('svg')
            .attr('width', 800)
            .attr('height', 300);

        svgLine.append('path')
            .datum(distancesOverTime)
            .attr('fill', 'none')
            .attr('stroke', 'steelblue')
            .attr('stroke-width', 2)
            .attr('d', d3.line()
                .x(d => xScaleLine(parseDate(d.key)))
                .y(d => yScaleLine(d.value))
            );

        svgLine.append('g')
            .attr('transform', `translate(0, ${300})`)
            .call(xAxisLine);

        svgLine.append('g')
            .call(yAxisLine);
    });
});
