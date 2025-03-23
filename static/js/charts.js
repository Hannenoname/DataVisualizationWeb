/**
 * Chart visualization functions for the Economic Dashboard
 */

// Chart creation module
const chartsModule = (function() {
    // Settings for all charts
    const margin = { top: 50, right: 50, bottom: 70, left: 70 };
    const colors = d3.schemeCategory10;
    const transitionDuration = 700;
    
    // Clear the visualization container
    function clearVisualization() {
        d3.select('#visualization').select('.chart-container').remove();
    }
    
    // Format date for display
    function formatDate(date) {
        const d = new Date(date);
        return `${d.getFullYear()}-${(d.getMonth() + 1).toString().padStart(2, '0')}`;
    }
    
    // Add tooltip to the chart
    function addTooltip() {
        return d3.select('#tooltip')
            .style('display', 'none')
            .classed('tooltip', true);
    }
    
    // Show tooltip
    function showTooltip(tooltip, html, event) {
        tooltip
            .style('display', 'block')
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 28) + 'px')
            .html(html);
    }
    
    // Hide tooltip
    function hideTooltip(tooltip) {
        tooltip.style('display', 'none');
    }
    
    // Add historical events annotations to the chart
    function addHistoricalEvents(svg, xScale, events, chartHeight) {
        const eventMarkers = svg.append('g')
            .attr('class', 'events');
            
        eventMarkers.selectAll('.event-line')
            .data(events)
            .enter()
            .append('line')
            .attr('class', 'event-line')
            .attr('x1', d => xScale(new Date(d.year, d.month - 1)))
            .attr('x2', d => xScale(new Date(d.year, d.month - 1)))
            .attr('y1', margin.top)
            .attr('y2', chartHeight - margin.bottom)
            .attr('stroke', '#ff9800')
            .attr('stroke-width', 1)
            .attr('stroke-dasharray', '3,3');
            
        eventMarkers.selectAll('.event-label')
            .data(events)
            .enter()
            .append('text')
            .attr('class', 'event-label')
            .attr('x', d => xScale(new Date(d.year, d.month - 1)))
            .attr('y', margin.top - 10)
            .attr('text-anchor', 'middle')
            .attr('font-size', '10px')
            .attr('fill', '#ff9800')
            .text(d => d.event);
    }
    
    // Create a line chart for a single indicator
    function createLineChart(data, indicator) {
        clearVisualization();
        
        const tooltip = addTooltip();
        const container = d3.select('#visualization')
            .append('div')
            .attr('class', 'chart-container');
            
        const width = container.node().getBoundingClientRect().width;
        const height = 500;
        const chartWidth = width;
        const chartHeight = height;
        
        // Create SVG
        const svg = container.append('svg')
            .attr('width', chartWidth)
            .attr('height', chartHeight);
            
        // Parse dates and create scales
        const parseDate = d3.timeParse('%Y-%m-%d');
        
        // Create scales
        const xScale = d3.scaleTime()
            .domain(d3.extent(data, d => new Date(d.Date)))
            .range([margin.left, chartWidth - margin.right]);
            
        const yScale = d3.scaleLinear()
            .domain([
                d3.min(data, d => d[indicator]) * 0.9,
                d3.max(data, d => d[indicator]) * 1.1
            ])
            .range([chartHeight - margin.bottom, margin.top]);
            
        // Create line generator
        const line = d3.line()
            .x(d => xScale(new Date(d.Date)))
            .y(d => yScale(d[indicator]))
            .curve(d3.curveMonotoneX);
            
        // Add X and Y axes
        const xAxis = d3.axisBottom(xScale)
            .ticks(10)
            .tickFormat(d3.timeFormat('%Y-%m'));
            
        svg.append('g')
            .attr('class', 'x-axis')
            .attr('transform', `translate(0, ${chartHeight - margin.bottom})`)
            .call(xAxis)
            .selectAll('text')
            .style('text-anchor', 'end')
            .attr('dx', '-.8em')
            .attr('dy', '.15em')
            .attr('transform', 'rotate(-45)');
            
        const yAxis = d3.axisLeft(yScale);
        
        svg.append('g')
            .attr('class', 'y-axis')
            .attr('transform', `translate(${margin.left}, 0)`)
            .call(yAxis);
            
        // Add axis labels
        svg.append('text')
            .attr('class', 'x-axis-label')
            .attr('x', chartWidth / 2)
            .attr('y', chartHeight - 10)
            .attr('text-anchor', 'middle')
            .text('Thời gian');
            
        svg.append('text')
            .attr('class', 'y-axis-label')
            .attr('transform', 'rotate(-90)')
            .attr('x', -(chartHeight / 2))
            .attr('y', 20)
            .attr('text-anchor', 'middle')
            .text(window.dataModule.indicatorMetadata[indicator]?.displayName || indicator);
            
        // Add the line path
        const path = svg.append('path')
            .datum(data)
            .attr('fill', 'none')
            .attr('stroke', colors[0])
            .attr('stroke-width', 2)
            .attr('d', line);
            
        // Animate the line
        const pathLength = path.node().getTotalLength();
        
        path
            .attr('stroke-dasharray', pathLength + ' ' + pathLength)
            .attr('stroke-dashoffset', pathLength)
            .transition()
            .duration(transitionDuration)
            .ease(d3.easeLinear)
            .attr('stroke-dashoffset', 0);
            
        // Add data points
        svg.selectAll('.data-point')
            .data(data)
            .enter()
            .append('circle')
            .attr('class', 'data-point')
            .attr('cx', d => xScale(new Date(d.Date)))
            .attr('cy', d => yScale(d[indicator]))
            .attr('r', 0)
            .attr('fill', colors[0])
            .transition()
            .delay((d, i) => i * (transitionDuration / data.length))
            .duration(300)
            .attr('r', 4);
            
        // Add hover interactions to data points
        svg.selectAll('.data-point')
            .on('mouseover', function(event, d) {
                const indName = window.dataModule.indicatorMetadata[indicator]?.displayName || indicator;
                const unit = window.dataModule.indicatorMetadata[indicator]?.unit || '';
                
                const html = `
                    <div class="tooltip-title">${indName}</div>
                    <div>Thời gian: ${formatDate(d.Date)}</div>
                    <div>Giá trị: ${d[indicator].toFixed(2)} ${unit}</div>
                `;
                
                showTooltip(tooltip, html, event);
                
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr('r', 6);
            })
            .on('mouseout', function() {
                hideTooltip(tooltip);
                
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr('r', 4);
            });
            
        // Add historical events
        addHistoricalEvents(svg, xScale, window.dataModule.getHistoricalEvents(), chartHeight);
        
        // Add chart title
        svg.append('text')
            .attr('class', 'chart-title')
            .attr('x', chartWidth / 2)
            .attr('y', margin.top / 2)
            .attr('text-anchor', 'middle')
            .attr('font-size', '16px')
            .attr('font-weight', 'bold')
            .text(`Xu hướng ${window.dataModule.indicatorMetadata[indicator]?.displayName || indicator} theo thời gian`);
            
        // Update explanation
        updateExplanation('line', [indicator]);
    }
    
    // Create a multi-line chart for multiple indicators
    function createMultiLineChart(data, indicators) {
        clearVisualization();
        
        const tooltip = addTooltip();
        const container = d3.select('#visualization')
            .append('div')
            .attr('class', 'chart-container');
            
        const width = container.node().getBoundingClientRect().width;
        const height = 500;
        const chartWidth = width;
        const chartHeight = height;
        
        // Create SVG
        const svg = container.append('svg')
            .attr('width', chartWidth)
            .attr('height', chartHeight);
            
        // Create scales
        const xScale = d3.scaleTime()
            .domain(d3.extent(data, d => new Date(d.Date)))
            .range([margin.left, chartWidth - margin.right]);
            
        // Find min and max across all indicators
        let allValues = [];
        indicators.forEach(indicator => {
            allValues = allValues.concat(data.map(d => d[indicator]));
        });
        
        const yScale = d3.scaleLinear()
            .domain([
                d3.min(allValues) * 0.9,
                d3.max(allValues) * 1.1
            ])
            .range([chartHeight - margin.bottom, margin.top]);
            
        // Create line generator
        const line = indicator => d3.line()
            .x(d => xScale(new Date(d.Date)))
            .y(d => yScale(d[indicator]))
            .curve(d3.curveMonotoneX);
            
        // Add X and Y axes
        const xAxis = d3.axisBottom(xScale)
            .ticks(10)
            .tickFormat(d3.timeFormat('%Y-%m'));
            
        svg.append('g')
            .attr('class', 'x-axis')
            .attr('transform', `translate(0, ${chartHeight - margin.bottom})`)
            .call(xAxis)
            .selectAll('text')
            .style('text-anchor', 'end')
            .attr('dx', '-.8em')
            .attr('dy', '.15em')
            .attr('transform', 'rotate(-45)');
            
        const yAxis = d3.axisLeft(yScale);
        
        svg.append('g')
            .attr('class', 'y-axis')
            .attr('transform', `translate(${margin.left}, 0)`)
            .call(yAxis);
            
        // Add axis labels
        svg.append('text')
            .attr('class', 'x-axis-label')
            .attr('x', chartWidth / 2)
            .attr('y', chartHeight - 10)
            .attr('text-anchor', 'middle')
            .text('Thời gian');
            
        svg.append('text')
            .attr('class', 'y-axis-label')
            .attr('transform', 'rotate(-90)')
            .attr('x', -(chartHeight / 2))
            .attr('y', 20)
            .attr('text-anchor', 'middle')
            .text('Giá trị chỉ số');
            
        // Add lines for each indicator
        indicators.forEach((indicator, i) => {
            const path = svg.append('path')
                .datum(data)
                .attr('fill', 'none')
                .attr('stroke', colors[i % colors.length])
                .attr('stroke-width', 2)
                .attr('d', line(indicator));
                
            // Animate the line
            const pathLength = path.node().getTotalLength();
            
            path
                .attr('stroke-dasharray', pathLength + ' ' + pathLength)
                .attr('stroke-dashoffset', pathLength)
                .transition()
                .duration(transitionDuration)
                .ease(d3.easeLinear)
                .attr('stroke-dashoffset', 0);
                
            // Add data points
            svg.selectAll(`.data-point-${i}`)
                .data(data)
                .enter()
                .append('circle')
                .attr('class', `data-point data-point-${i}`)
                .attr('cx', d => xScale(new Date(d.Date)))
                .attr('cy', d => yScale(d[indicator]))
                .attr('r', 0)
                .attr('fill', colors[i % colors.length])
                .transition()
                .delay((d, i) => i * (transitionDuration / data.length))
                .duration(300)
                .attr('r', 3);
        });
        
        // Add hover interactions
        svg.selectAll('.data-point')
            .on('mouseover', function(event, d) {
                const pointClass = this.getAttribute('class').split(' ')[1];
                const index = parseInt(pointClass.split('-')[2]);
                const indicator = indicators[index];
                const indName = window.dataModule.indicatorMetadata[indicator]?.displayName || indicator;
                const unit = window.dataModule.indicatorMetadata[indicator]?.unit || '';
                
                const html = `
                    <div class="tooltip-title">${indName}</div>
                    <div>Thời gian: ${formatDate(d.Date)}</div>
                    <div>Giá trị: ${d[indicator].toFixed(2)} ${unit}</div>
                `;
                
                showTooltip(tooltip, html, event);
                
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr('r', 5);
            })
            .on('mouseout', function() {
                hideTooltip(tooltip);
                
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr('r', 3);
            });
            
        // Add legend
        const legend = svg.append('g')
            .attr('class', 'legend')
            .attr('transform', `translate(${chartWidth - margin.right - 120}, ${margin.top})`);
            
        indicators.forEach((indicator, i) => {
            const legendRow = legend.append('g')
                .attr('transform', `translate(0, ${i * 20})`);
                
            legendRow.append('rect')
                .attr('width', 10)
                .attr('height', 10)
                .attr('fill', colors[i % colors.length]);
                
            legendRow.append('text')
                .attr('x', 15)
                .attr('y', 10)
                .attr('text-anchor', 'start')
                .attr('font-size', '12px')
                .text(window.dataModule.indicatorMetadata[indicator]?.displayName || indicator);
        });
        
        // Add historical events
        addHistoricalEvents(svg, xScale, window.dataModule.getHistoricalEvents(), chartHeight);
        
        // Add chart title
        svg.append('text')
            .attr('class', 'chart-title')
            .attr('x', chartWidth / 2)
            .attr('y', margin.top / 2)
            .attr('text-anchor', 'middle')
            .attr('font-size', '16px')
            .attr('font-weight', 'bold')
            .text('So sánh xu hướng các chỉ số kinh tế theo thời gian');
            
        // Update explanation
        updateExplanation('multi-line', indicators);
    }
    
    // Create a stacked area chart
    function createStackedAreaChart(data, indicators) {
        clearVisualization();
        
        const tooltip = addTooltip();
        const container = d3.select('#visualization')
            .append('div')
            .attr('class', 'chart-container');
            
        const width = container.node().getBoundingClientRect().width;
        const height = 500;
        const chartWidth = width;
        const chartHeight = height;
        
        // Create SVG
        const svg = container.append('svg')
            .attr('width', chartWidth)
            .attr('height', chartHeight);
            
        // Create scales
        const xScale = d3.scaleTime()
            .domain(d3.extent(data, d => new Date(d.Date)))
            .range([margin.left, chartWidth - margin.right]);
            
        // Stack the data
        const stack = d3.stack()
            .keys(indicators)
            .order(d3.stackOrderNone)
            .offset(d3.stackOffsetNone);
            
        const stackedData = stack(data);
        
        const yScale = d3.scaleLinear()
            .domain([0, d3.max(stackedData[stackedData.length - 1], d => d[1])])
            .range([chartHeight - margin.bottom, margin.top]);
            
        // Create area generator
        const area = d3.area()
            .x(d => xScale(new Date(d.data.Date)))
            .y0(d => yScale(d[0]))
            .y1(d => yScale(d[1]))
            .curve(d3.curveMonotoneX);
            
        // Add X and Y axes
        const xAxis = d3.axisBottom(xScale)
            .ticks(10)
            .tickFormat(d3.timeFormat('%Y-%m'));
            
        svg.append('g')
            .attr('class', 'x-axis')
            .attr('transform', `translate(0, ${chartHeight - margin.bottom})`)
            .call(xAxis)
            .selectAll('text')
            .style('text-anchor', 'end')
            .attr('dx', '-.8em')
            .attr('dy', '.15em')
            .attr('transform', 'rotate(-45)');
            
        const yAxis = d3.axisLeft(yScale);
        
        svg.append('g')
            .attr('class', 'y-axis')
            .attr('transform', `translate(${margin.left}, 0)`)
            .call(yAxis);
            
        // Add axis labels
        svg.append('text')
            .attr('class', 'x-axis-label')
            .attr('x', chartWidth / 2)
            .attr('y', chartHeight - 10)
            .attr('text-anchor', 'middle')
            .text('Thời gian');
            
        svg.append('text')
            .attr('class', 'y-axis-label')
            .attr('transform', 'rotate(-90)')
            .attr('x', -(chartHeight / 2))
            .attr('y', 20)
            .attr('text-anchor', 'middle')
            .text('Đóng góp của các chỉ số');
            
        // Add areas for each indicator
        const layers = svg.selectAll('.layer')
            .data(stackedData)
            .enter()
            .append('g')
            .attr('class', 'layer');
            
        layers.append('path')
            .attr('class', 'area')
            .style('fill', (d, i) => colors[i % colors.length])
            .attr('d', area)
            .attr('opacity', 0)
            .transition()
            .duration(transitionDuration)
            .attr('opacity', 0.7);
            
        // Add hover interactions
        layers
            .on('mouseover', function(event, d) {
                const indicator = d.key;
                const indName = window.dataModule.indicatorMetadata[indicator]?.displayName || indicator;
                
                const html = `
                    <div class="tooltip-title">${indName}</div>
                    <div>Đóng góp vào tổng thể</div>
                `;
                
                showTooltip(tooltip, html, event);
                
                d3.select(this).select('path')
                    .transition()
                    .duration(200)
                    .attr('opacity', 0.9);
            })
            .on('mouseout', function() {
                hideTooltip(tooltip);
                
                d3.select(this).select('path')
                    .transition()
                    .duration(200)
                    .attr('opacity', 0.7);
            });
            
        // Add legend
        const legend = svg.append('g')
            .attr('class', 'legend')
            .attr('transform', `translate(${chartWidth - margin.right - 120}, ${margin.top})`);
            
        indicators.forEach((indicator, i) => {
            const legendRow = legend.append('g')
                .attr('transform', `translate(0, ${i * 20})`);
                
            legendRow.append('rect')
                .attr('width', 10)
                .attr('height', 10)
                .attr('fill', colors[i % colors.length]);
                
            legendRow.append('text')
                .attr('x', 15)
                .attr('y', 10)
                .attr('text-anchor', 'start')
                .attr('font-size', '12px')
                .text(window.dataModule.indicatorMetadata[indicator]?.displayName || indicator);
        });
        
        // Add historical events
        addHistoricalEvents(svg, xScale, window.dataModule.getHistoricalEvents(), chartHeight);
        
        // Add chart title
        svg.append('text')
            .attr('class', 'chart-title')
            .attr('x', chartWidth / 2)
            .attr('y', margin.top / 2)
            .attr('text-anchor', 'middle')
            .attr('font-size', '16px')
            .attr('font-weight', 'bold')
            .text('Đóng góp của các thành phần vào chỉ số tổng hợp');
            
        // Update explanation
        updateExplanation('area', indicators);
    }
    
    // Create a scatter plot for two indicators
    function createScatterPlot(data, indicators) {
        if (indicators.length !== 2) {
            return;
        }
        
        clearVisualization();
        
        const tooltip = addTooltip();
        const container = d3.select('#visualization')
            .append('div')
            .attr('class', 'chart-container');
            
        const width = container.node().getBoundingClientRect().width;
        const height = 500;
        const chartWidth = width;
        const chartHeight = height;
        
        // Create SVG
        const svg = container.append('svg')
            .attr('width', chartWidth)
            .attr('height', chartHeight);
            
        // Extract indicators
        const xIndicator = indicators[0];
        const yIndicator = indicators[1];
        
        // Create scales
        const xScale = d3.scaleLinear()
            .domain([
                d3.min(data, d => d[xIndicator]) * 0.9,
                d3.max(data, d => d[xIndicator]) * 1.1
            ])
            .range([margin.left, chartWidth - margin.right]);
            
        const yScale = d3.scaleLinear()
            .domain([
                d3.min(data, d => d[yIndicator]) * 0.9,
                d3.max(data, d => d[yIndicator]) * 1.1
            ])
            .range([chartHeight - margin.bottom, margin.top]);
            
        // Create color scale for years
        const years = Array.from(new Set(data.map(d => d.Year))).sort();
        const colorScale = d3.scaleSequential()
            .domain([d3.min(years), d3.max(years)])
            .interpolator(d3.interpolateViridis);
            
        // Add X and Y axes
        const xAxis = d3.axisBottom(xScale);
        svg.append('g')
            .attr('class', 'x-axis')
            .attr('transform', `translate(0, ${chartHeight - margin.bottom})`)
            .call(xAxis);
            
        const yAxis = d3.axisLeft(yScale);
        svg.append('g')
            .attr('class', 'y-axis')
            .attr('transform', `translate(${margin.left}, 0)`)
            .call(yAxis);
            
        // Add axis labels
        svg.append('text')
            .attr('class', 'x-axis-label')
            .attr('x', chartWidth / 2)
            .attr('y', chartHeight - 10)
            .attr('text-anchor', 'middle')
            .text(window.dataModule.indicatorMetadata[xIndicator]?.displayName || xIndicator);
            
        svg.append('text')
            .attr('class', 'y-axis-label')
            .attr('transform', 'rotate(-90)')
            .attr('x', -(chartHeight / 2))
            .attr('y', 20)
            .attr('text-anchor', 'middle')
            .text(window.dataModule.indicatorMetadata[yIndicator]?.displayName || yIndicator);
            
        // Add scatter plot points
        svg.selectAll('.data-point')
            .data(data)
            .enter()
            .append('circle')
            .attr('class', 'data-point')
            .attr('cx', d => xScale(d[xIndicator]))
            .attr('cy', d => yScale(d[yIndicator]))
            .attr('r', 0)
            .attr('fill', d => colorScale(d.Year))
            .transition()
            .delay((d, i) => i * (transitionDuration / data.length))
            .duration(300)
            .attr('r', 5);
            
        // Add hover interactions
        svg.selectAll('.data-point')
            .on('mouseover', function(event, d) {
                const xIndName = window.dataModule.indicatorMetadata[xIndicator]?.displayName || xIndicator;
                const yIndName = window.dataModule.indicatorMetadata[yIndicator]?.displayName || yIndicator;
                const xUnit = window.dataModule.indicatorMetadata[xIndicator]?.unit || '';
                const yUnit = window.dataModule.indicatorMetadata[yIndicator]?.unit || '';
                
                const html = `
                    <div class="tooltip-title">${d.Year}-${d.Month}</div>
                    <div>${xIndName}: ${d[xIndicator].toFixed(2)} ${xUnit}</div>
                    <div>${yIndName}: ${d[yIndicator].toFixed(2)} ${yUnit}</div>
                `;
                
                showTooltip(tooltip, html, event);
                
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr('r', 8);
            })
            .on('mouseout', function() {
                hideTooltip(tooltip);
                
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr('r', 5);
            });
            
        // Add regression line
        const regression = calculateRegressionLine(data, xIndicator, yIndicator);
        
        if (regression) {
            const line = d3.line()
                .x(d => xScale(d.x))
                .y(d => yScale(d.y));
                
            svg.append('path')
                .datum(regression.points)
                .attr('class', 'regression-line')
                .attr('fill', 'none')
                .attr('stroke', '#ff5722')
                .attr('stroke-width', 2)
                .attr('stroke-dasharray', '5,5')
                .attr('d', line)
                .attr('opacity', 0)
                .transition()
                .delay(transitionDuration)
                .duration(500)
                .attr('opacity', 1);
        }
        
        // Add year color legend
        const legendWidth = 200;
        const legendHeight = 20;
        
        const legendX = chartWidth - margin.right - legendWidth;
        const legendY = margin.top;
        
        const legendScale = d3.scaleLinear()
            .domain([d3.min(years), d3.max(years)])
            .range([0, legendWidth]);
            
        const defs = svg.append('defs');
        
        const gradient = defs.append('linearGradient')
            .attr('id', 'year-gradient')
            .attr('x1', '0%')
            .attr('y1', '0%')
            .attr('x2', '100%')
            .attr('y2', '0%');
            
        years.forEach(year => {
            const offset = (year - d3.min(years)) / (d3.max(years) - d3.min(years));
            
            gradient.append('stop')
                .attr('offset', `${offset * 100}%`)
                .attr('stop-color', colorScale(year));
        });
        
        svg.append('rect')
            .attr('x', legendX)
            .attr('y', legendY)
            .attr('width', legendWidth)
            .attr('height', legendHeight)
            .style('fill', 'url(#year-gradient)');
            
        svg.append('text')
            .attr('x', legendX)
            .attr('y', legendY - 5)
            .attr('text-anchor', 'start')
            .attr('font-size', '12px')
            .text(d3.min(years));
            
        svg.append('text')
            .attr('x', legendX + legendWidth)
            .attr('y', legendY - 5)
            .attr('text-anchor', 'end')
            .attr('font-size', '12px')
            .text(d3.max(years));
            
        svg.append('text')
            .attr('x', legendX + legendWidth / 2)
            .attr('y', legendY - 5)
            .attr('text-anchor', 'middle')
            .attr('font-size', '12px')
            .text('Năm');
            
        // Add chart title
        svg.append('text')
            .attr('class', 'chart-title')
            .attr('x', chartWidth / 2)
            .attr('y', margin.top / 2)
            .attr('text-anchor', 'middle')
            .attr('font-size', '16px')
            .attr('font-weight', 'bold')
            .text(`Mối quan hệ giữa ${window.dataModule.indicatorMetadata[xIndicator]?.displayName || xIndicator} và ${window.dataModule.indicatorMetadata[yIndicator]?.displayName || yIndicator}`);
            
        // Update explanation
        updateExplanation('scatter', indicators);
    }
    
    // Create a correlation heatmap
    function createHeatmap(data, indicators) {
        clearVisualization();
        
        const tooltip = addTooltip();
        const container = d3.select('#visualization')
            .append('div')
            .attr('class', 'chart-container');
            
        const width = container.node().getBoundingClientRect().width;
        const height = 600;
        const chartWidth = width;
        const chartHeight = height;
        
        // Create SVG
        const svg = container.append('svg')
            .attr('width', chartWidth)
            .attr('height', chartHeight);
            
        // Calculate correlation matrix
        const matrix = [];
        const displayNames = [];
        
        indicators.forEach(ind1 => {
            const row = [];
            indicators.forEach(ind2 => {
                row.push(window.dataModule.calculateCorrelation(ind1, ind2));
            });
            matrix.push(row);
            displayNames.push(window.dataModule.indicatorMetadata[ind1]?.displayName || ind1);
        });
        
        const cellSize = Math.min(
            (chartWidth - margin.left - margin.right) / indicators.length,
            (chartHeight - margin.top - margin.bottom) / indicators.length
        );
        
        // Create color scale
        const colorScale = d3.scaleSequential()
            .domain([-1, 1])
            .interpolator(d3.interpolateRdBu);
            
        // Create scales
        const xScale = d3.scaleBand()
            .domain(displayNames)
            .range([margin.left, margin.left + cellSize * indicators.length]);
            
        const yScale = d3.scaleBand()
            .domain(displayNames)
            .range([margin.top, margin.top + cellSize * indicators.length]);
            
        // Add cells
        const rows = svg.selectAll('.row')
            .data(matrix)
            .enter()
            .append('g')
            .attr('class', 'row')
            .attr('transform', (d, i) => `translate(0, ${yScale(displayNames[i])})`);
            
        const cells = rows.selectAll('.cell')
            .data((d, i) => d.map((value, j) => ({ value, i, j })))
            .enter()
            .append('rect')
            .attr('class', 'cell')
            .attr('x', (d, i) => xScale(displayNames[i]))
            .attr('width', cellSize)
            .attr('height', cellSize)
            .attr('fill', d => colorScale(d.value))
            .attr('opacity', 0)
            .transition()
            .duration(transitionDuration)
            .delay((d, i) => i * 50)
            .attr('opacity', 1);
            
        // Add cell values
        svg.selectAll('.cell-value')
            .data(matrix.flatMap((row, i) => row.map((value, j) => ({ value, i, j }))))
            .enter()
            .append('text')
            .attr('class', 'cell-value')
            .attr('x', d => xScale(displayNames[d.j]) + cellSize / 2)
            .attr('y', d => yScale(displayNames[d.i]) + cellSize / 2)
            .attr('text-anchor', 'middle')
            .attr('alignment-baseline', 'middle')
            .attr('font-size', '10px')
            .attr('fill', d => Math.abs(d.value) > 0.5 ? 'white' : 'black')
            .text(d => d.value.toFixed(2))
            .attr('opacity', 0)
            .transition()
            .duration(transitionDuration)
            .delay((d, i) => i * 50 + 300)
            .attr('opacity', 1);
            
        // Add X and Y axes
        const xAxis = d3.axisBottom(xScale);
        svg.append('g')
            .attr('class', 'x-axis')
            .attr('transform', `translate(0, ${margin.top + cellSize * indicators.length})`)
            .call(xAxis)
            .selectAll('text')
            .style('text-anchor', 'end')
            .attr('dx', '-.8em')
            .attr('dy', '.15em')
            .attr('transform', 'rotate(-45)');
            
        const yAxis = d3.axisLeft(yScale);
        svg.append('g')
            .attr('class', 'y-axis')
            .attr('transform', `translate(${margin.left}, 0)`)
            .call(yAxis);
            
        // Add hover interactions
        rows.selectAll('.cell')
            .on('mouseover', function(event, d) {
                const ind1 = indicators[d.i];
                const ind2 = indicators[d.j];
                const indName1 = window.dataModule.indicatorMetadata[ind1]?.displayName || ind1;
                const indName2 = window.dataModule.indicatorMetadata[ind2]?.displayName || ind2;
                
                const html = `
                    <div class="tooltip-title">Tương quan: ${d.value.toFixed(2)}</div>
                    <div>Giữa ${indName1} và ${indName2}</div>
                    <div>${getCorrelationDescription(d.value)}</div>
                `;
                
                showTooltip(tooltip, html, event);
                
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr('stroke', 'black')
                    .attr('stroke-width', 2);
            })
            .on('mouseout', function() {
                hideTooltip(tooltip);
                
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr('stroke', 'none');
            });
            
        // Add color legend
        const legendWidth = 200;
        const legendHeight = 20;
        
        const legendX = chartWidth / 2 - legendWidth / 2;
        const legendY = chartHeight - margin.bottom / 2;
        
        const legendScale = d3.scaleLinear()
            .domain([-1, 1])
            .range([0, legendWidth]);
            
        const defs = svg.append('defs');
        
        const gradient = defs.append('linearGradient')
            .attr('id', 'correlation-gradient')
            .attr('x1', '0%')
            .attr('y1', '0%')
            .attr('x2', '100%')
            .attr('y2', '0%');
            
        gradient.append('stop')
            .attr('offset', '0%')
            .attr('stop-color', colorScale(-1));
            
        gradient.append('stop')
            .attr('offset', '50%')
            .attr('stop-color', colorScale(0));
            
        gradient.append('stop')
            .attr('offset', '100%')
            .attr('stop-color', colorScale(1));
            
        svg.append('rect')
            .attr('x', legendX)
            .attr('y', legendY)
            .attr('width', legendWidth)
            .attr('height', legendHeight)
            .style('fill', 'url(#correlation-gradient)');
            
        svg.append('text')
            .attr('x', legendX)
            .attr('y', legendY - 5)
            .attr('text-anchor', 'start')
            .attr('font-size', '12px')
            .text('-1 (Tương quan nghịch)');
            
        svg.append('text')
            .attr('x', legendX + legendWidth)
            .attr('y', legendY - 5)
            .attr('text-anchor', 'end')
            .attr('font-size', '12px')
            .text('1 (Tương quan thuận)');
            
        svg.append('text')
            .attr('x', legendX + legendWidth / 2)
            .attr('y', legendY - 5)
            .attr('text-anchor', 'middle')
            .attr('font-size', '12px')
            .text('0 (Không tương quan)');
            
        // Add chart title
        svg.append('text')
            .attr('class', 'chart-title')
            .attr('x', chartWidth / 2)
            .attr('y', margin.top / 2)
            .attr('text-anchor', 'middle')
            .attr('font-size', '16px')
            .attr('font-weight', 'bold')
            .text('Ma trận tương quan giữa các chỉ số kinh tế');
            
        // Update explanation
        updateExplanation('heatmap', indicators);
    }
    
    // Create a seasonal plot
    function createSeasonalPlot(data, indicator) {
        clearVisualization();
        
        const tooltip = addTooltip();
        const container = d3.select('#visualization')
            .append('div')
            .attr('class', 'chart-container');
            
        const width = container.node().getBoundingClientRect().width;
        const height = 700;
        const chartWidth = width;
        const chartHeight = height;
        
        // Create SVG
        const svg = container.append('svg')
            .attr('width', chartWidth)
            .attr('height', chartHeight);
            
        // Calculate grid dimensions
        const rows = 3;
        const cols = 4;
        
        const gridMargin = { top: 80, right: 20, bottom: 50, left: 60 };
        const cellWidth = (chartWidth - gridMargin.left - gridMargin.right) / cols;
        const cellHeight = (chartHeight - gridMargin.top - gridMargin.bottom) / rows;
        
        // Get years range
        const years = Array.from(new Set(data.map(d => d.Year))).sort();
        
        // Create scales for year and value
        const xScale = d3.scaleLinear()
            .domain([d3.min(years), d3.max(years)])
            .range([0, cellWidth - 40]);
            
        // Find min and max values for the indicator
        const allValues = data.map(d => d[indicator]);
        const yScale = d3.scaleLinear()
            .domain([d3.min(allValues) * 0.9, d3.max(allValues) * 1.1])
            .range([cellHeight - 40, 0]);
            
        // Create line generator
        const line = d3.line()
            .x(d => xScale(d.Year))
            .y(d => yScale(d[indicator]))
            .curve(d3.curveMonotoneX);
            
        // Add cells for each month
        for (let month = 1; month <= 12; month++) {
            const row = Math.floor((month - 1) / cols);
            const col = (month - 1) % cols;
            
            const cellX = gridMargin.left + col * cellWidth;
            const cellY = gridMargin.top + row * cellHeight;
            
            // Create cell group
            const cell = svg.append('g')
                .attr('class', 'month-cell')
                .attr('transform', `translate(${cellX}, ${cellY})`);
                
            // Add cell background
            cell.append('rect')
                .attr('width', cellWidth - 10)
                .attr('height', cellHeight - 10)
                .attr('fill', '#f9f9f9')
                .attr('stroke', '#ddd')
                .attr('rx', 5);
                
            // Add month title
            const months = ['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6', 
                            'Tháng 7', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12'];
                            
            cell.append('text')
                .attr('x', (cellWidth - 10) / 2)
                .attr('y', 15)
                .attr('text-anchor', 'middle')
                .attr('font-size', '12px')
                .attr('font-weight', 'bold')
                .text(months[month - 1]);
                
            // Filter data for this month
            const monthData = data.filter(d => d.Month === month);
            
            // Skip if no data
            if (monthData.length === 0) continue;
            
            // Calculate mean value for this month
            const monthMean = d3.mean(monthData, d => d[indicator]);
            
            // Add axes
            const xAxis = d3.axisBottom(xScale)
                .ticks(3)
                .tickFormat(d3.format('d'));
                
            cell.append('g')
                .attr('class', 'x-axis')
                .attr('transform', `translate(20, ${cellHeight - 30})`)
                .call(xAxis)
                .selectAll('text')
                .attr('font-size', '10px');
                
            const yAxis = d3.axisLeft(yScale)
                .ticks(3);
                
            cell.append('g')
                .attr('class', 'y-axis')
                .attr('transform', `translate(20, 20)`)
                .call(yAxis)
                .selectAll('text')
                .attr('font-size', '10px');
                
            // Add the line
            const path = cell.append('path')
                .datum(monthData)
                .attr('fill', 'none')
                .attr('stroke', 'steelblue')
                .attr('stroke-width', 2)
                .attr('transform', `translate(20, 20)`)
                .attr('d', line);
                
            // Animate the line
            const pathLength = path.node().getTotalLength();
            
            path
                .attr('stroke-dasharray', pathLength + ' ' + pathLength)
                .attr('stroke-dashoffset', pathLength)
                .transition()
                .duration(transitionDuration)
                .ease(d3.easeLinear)
                .attr('stroke-dashoffset', 0);
                
            // Add mean line
            cell.append('line')
                .attr('x1', 20)
                .attr('x2', cellWidth - 30)
                .attr('y1', yScale(monthMean) + 20)
                .attr('y2', yScale(monthMean) + 20)
                .attr('stroke', 'red')
                .attr('stroke-width', 1)
                .attr('stroke-dasharray', '3,3')
                .attr('opacity', 0)
                .transition()
                .delay(transitionDuration)
                .duration(300)
                .attr('opacity', 1);
                
            // Add mean label
            cell.append('text')
                .attr('x', cellWidth - 35)
                .attr('y', yScale(monthMean) + 20)
                .attr('text-anchor', 'end')
                .attr('font-size', '10px')
                .attr('fill', 'red')
                .text(`TB: ${monthMean.toFixed(2)}`)
                .attr('opacity', 0)
                .transition()
                .delay(transitionDuration + 300)
                .duration(300)
                .attr('opacity', 1);
                
            // Add data points
            cell.selectAll('.data-point')
                .data(monthData)
                .enter()
                .append('circle')
                .attr('class', 'data-point')
                .attr('cx', d => xScale(d.Year) + 20)
                .attr('cy', d => yScale(d[indicator]) + 20)
                .attr('r', 0)
                .attr('fill', 'steelblue')
                .transition()
                .delay((d, i) => i * (transitionDuration / monthData.length))
                .duration(300)
                .attr('r', 3);
                
            // Add hover interactions to data points
            cell.selectAll('.data-point')
                .on('mouseover', function(event, d) {
                    const indName = window.dataModule.indicatorMetadata[indicator]?.displayName || indicator;
                    const unit = window.dataModule.indicatorMetadata[indicator]?.unit || '';
                    
                    const html = `
                        <div class="tooltip-title">${months[month - 1]} ${d.Year}</div>
                        <div>${indName}: ${d[indicator].toFixed(2)} ${unit}</div>
                        <div>Chênh lệch với TB: ${(d[indicator] - monthMean).toFixed(2)}</div>
                    `;
                    
                    showTooltip(tooltip, html, event);
                    
                    d3.select(this)
                        .transition()
                        .duration(200)
                        .attr('r', 5);
                })
                .on('mouseout', function() {
                    hideTooltip(tooltip);
                    
                    d3.select(this)
                        .transition()
                        .duration(200)
                        .attr('r', 3);
                });
        }
        
        // Add chart title
        svg.append('text')
            .attr('class', 'chart-title')
            .attr('x', chartWidth / 2)
            .attr('y', gridMargin.top / 2)
            .attr('text-anchor', 'middle')
            .attr('font-size', '16px')
            .attr('font-weight', 'bold')
            .text(`Xu hướng mùa vụ theo tháng - ${window.dataModule.indicatorMetadata[indicator]?.displayName || indicator}`);
            
        // Update explanation
        updateExplanation('seasonal', [indicator]);
    }
    
    // Calculate regression line for scatter plot
    function calculateRegressionLine(data, xIndicator, yIndicator) {
        const validData = data.filter(d => 
            d[xIndicator] !== undefined && d[xIndicator] !== null && 
            d[yIndicator] !== undefined && d[yIndicator] !== null
        );
        
        if (validData.length < 2) return null;
        
        // Extract x and y values
        const xValues = validData.map(d => d[xIndicator]);
        const yValues = validData.map(d => d[yIndicator]);
        
        // Calculate means
        const xMean = d3.mean(xValues);
        const yMean = d3.mean(yValues);
        
        // Calculate slope and intercept
        let numerator = 0;
        let denominator = 0;
        
        for (let i = 0; i < validData.length; i++) {
            numerator += (xValues[i] - xMean) * (yValues[i] - yMean);
            denominator += (xValues[i] - xMean) * (xValues[i] - xMean);
        }
        
        if (denominator === 0) return null;
        
        const slope = numerator / denominator;
        const intercept = yMean - slope * xMean;
        
        // Generate points for the line
        const xMin = d3.min(xValues);
        const xMax = d3.max(xValues);
        
        const points = [
            { x: xMin, y: xMin * slope + intercept },
            { x: xMax, y: xMax * slope + intercept }
        ];
        
        return {
            slope,
            intercept,
            points
        };
    }
    
    // Get description for correlation values
    function getCorrelationDescription(value) {
        const absValue = Math.abs(value);
        
        if (absValue >= 0.8) {
            return value > 0 ? 'Tương quan thuận rất mạnh' : 'Tương quan nghịch rất mạnh';
        } else if (absValue >= 0.6) {
            return value > 0 ? 'Tương quan thuận mạnh' : 'Tương quan nghịch mạnh';
        } else if (absValue >= 0.4) {
            return value > 0 ? 'Tương quan thuận trung bình' : 'Tương quan nghịch trung bình';
        } else if (absValue >= 0.2) {
            return value > 0 ? 'Tương quan thuận yếu' : 'Tương quan nghịch yếu';
        } else {
            return 'Gần như không có tương quan';
        }
    }
    
    // Update explanation panel
    function updateExplanation(chartType, indicators) {
        const explanationContent = d3.select('#explanation-content');
        
        // Clear previous content
        explanationContent.html('');
        
        // Add chart type explanation
        const chartInfo = window.dataModule.chartTypes.find(c => c.id === chartType);
        
        if (chartInfo) {
            explanationContent.append('h3')
                .text(`Về biểu đồ ${chartInfo.name}`);
                
            explanationContent.append('p')
                .text(chartInfo.description);
        }
        
        // Add indicator explanations
        if (indicators.length === 1) {
            // For single indicator charts
            const indicator = indicators[0];
            const metadata = window.dataModule.indicatorMetadata[indicator];
            
            if (metadata) {
                explanationContent.append('h3')
                    .text(`Về chỉ số ${metadata.displayName}`);
                    
                explanationContent.append('p')
                    .text(metadata.explanation);
                    
                // Add seasonal explanation for seasonal charts
                if (chartType === 'seasonal') {
                    explanationContent.append('h3')
                        .text('Mẫu mùa vụ');
                        
                    explanationContent.append('p')
                        .text(window.dataModule.getSeasonalExplanation(indicator));
                }
            }
        } else if (indicators.length === 2 && chartType === 'scatter') {
            // For scatter plots, explain relationship between two indicators
            const ind1 = indicators[0];
            const ind2 = indicators[1];
            
            const meta1 = window.dataModule.indicatorMetadata[ind1];
            const meta2 = window.dataModule.indicatorMetadata[ind2];
            
            if (meta1 && meta2) {
                explanationContent.append('h3')
                    .text(`Mối quan hệ giữa ${meta1.displayName} và ${meta2.displayName}`);
                    
                explanationContent.append('p')
                    .text(window.dataModule.getRelationshipExplanation(ind1, ind2));
                    
                // Add correlation value
                const corr = window.dataModule.calculateCorrelation(ind1, ind2);
                
                explanationContent.append('p')
                    .html(`<strong>Hệ số tương quan:</strong> ${corr.toFixed(2)} (${getCorrelationDescription(corr)})`);
            }
        } else {
            // For multi-indicator charts
            explanationContent.append('h3')
                .text('Về các chỉ số đã chọn');
                
            const corrTable = explanationContent.append('table')
                .attr('class', 'correlation-table')
                .style('width', '100%')
                .style('border-collapse', 'collapse')
                .style('margin-top', '10px');
                
            // Add header
            const header = corrTable.append('tr');
            header.append('th').text('Chỉ số');
            header.append('th').text('Tương quan cao nhất với');
            
            // Add rows
            indicators.forEach(ind1 => {
                const row = corrTable.append('tr');
                const meta1 = window.dataModule.indicatorMetadata[ind1];
                
                row.append('td').text(meta1?.displayName || ind1);
                
                // Find strongest correlation
                let maxCorr = 0;
                let maxInd = '';
                
                indicators.forEach(ind2 => {
                    if (ind1 !== ind2) {
                        const corr = Math.abs(window.dataModule.calculateCorrelation(ind1, ind2));
                        if (corr > maxCorr) {
                            maxCorr = corr;
                            maxInd = ind2;
                        }
                    }
                });
                
                if (maxInd) {
                    const meta2 = window.dataModule.indicatorMetadata[maxInd];
                    row.append('td').text(`${meta2?.displayName || maxInd} (${maxCorr.toFixed(2)})`);
                } else {
                    row.append('td').text('Không có dữ liệu');
                }
            });
        }
    }
    
    // Public methods
    return {
        createLineChart,
        createMultiLineChart,
        createStackedAreaChart,
        createScatterPlot,
        createHeatmap,
        createSeasonalPlot
    };
})();

// Export charts module
window.chartsModule = chartsModule;