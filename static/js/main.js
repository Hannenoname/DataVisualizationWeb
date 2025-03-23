// Global variables
let selectedIndicators = new Set();
let selectedChartType = null;
let data = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    // Load data
    loadData();
    
    // Setup event listeners
    setupEventListeners();
});

// Load data from CSV
async function loadData() {
    try {
        const response = await fetch('data/economic_data.csv');
        const csvText = await response.text();
        data = d3.csvParse(csvText);
        console.log('Data loaded successfully:', data);
    } catch (error) {
        console.error('Error loading data:', error);
        showError('Không thể tải dữ liệu. Vui lòng thử lại sau.');
    }
}

// Setup event listeners
function setupEventListeners() {
    // Indicator selection
    document.querySelectorAll('input[name="indicators"]').forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            if (e.target.checked) {
                selectedIndicators.add(e.target.value);
                e.target.closest('.indicator-label').classList.add('selected');
            } else {
                selectedIndicators.delete(e.target.value);
                e.target.closest('.indicator-label').classList.remove('selected');
            }
            updateVisualization();
        });
    });

    // Chart type selection
    document.querySelectorAll('.chart-option').forEach(option => {
        option.addEventListener('click', () => {
            document.querySelectorAll('.chart-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            option.classList.add('selected');
            selectedChartType = option.querySelector('.chart-name').textContent;
            updateVisualization();
        });
    });
}

// Update visualization
function updateVisualization() {
    const visualization = d3.select('#visualization');
    visualization.selectAll('*').remove();

    if (selectedIndicators.size === 0) {
        showPlaceholder();
        return;
    }

    if (!selectedChartType) {
        showPlaceholder('Vui lòng chọn loại biểu đồ');
        return;
    }

    switch (selectedChartType) {
        case 'Biểu Đồ Đường':
            createLineChart();
            break;
        case 'Biểu Đồ Vùng':
            createAreaChart();
            break;
        case 'Biểu Đồ Phân Tán':
            createScatterPlot();
            break;
        default:
            showPlaceholder('Loại biểu đồ không được hỗ trợ');
    }
}

// Create line chart
function createLineChart() {
    const margin = { top: 20, right: 30, bottom: 30, left: 40 };
    const width = 800 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    const svg = d3.select('#visualization')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Create scales
    const x = d3.scaleTime()
        .domain(d3.extent(data, d => new Date(d.Date)))
        .range([0, width]);

    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => Math.max(...selectedIndicators.map(ind => +d[ind])))])
        .range([height, 0]);

    // Add axes
    svg.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x));

    svg.append('g')
        .call(d3.axisLeft(y));

    // Add lines
    const line = d3.line()
        .x(d => x(new Date(d.Date)))
        .y(d => y(+d[selectedIndicators.values().next().value]));

    svg.append('path')
        .datum(data)
        .attr('fill', 'none')
        .attr('stroke', '#3498db')
        .attr('stroke-width', 2)
        .attr('d', line);
}

// Create area chart
function createAreaChart() {
    // Implementation similar to line chart but with area
}

// Create scatter plot
function createScatterPlot() {
    // Implementation for scatter plot
}

// Show placeholder
function showPlaceholder(message = 'Chọn các chỉ số và loại biểu đồ để bắt đầu phân tích') {
    const visualization = d3.select('#visualization');
    visualization.selectAll('*').remove();

    visualization.append('div')
        .attr('class', 'placeholder')
        .html(`
            <i class="fas fa-chart-line"></i>
            <p>${message}</p>
        `);
}

// Show error message
function showError(message) {
    const visualization = d3.select('#visualization');
    visualization.selectAll('*').remove();

    visualization.append('div')
        .attr('class', 'error')
        .html(`
            <i class="fas fa-exclamation-circle"></i>
            <p>${message}</p>
        `);
} 