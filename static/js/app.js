/**
 * Main application logic for the Economic Dashboard
 */

// Main application module
(function() {
    // State variables
    let economicData = [];
    let selectedIndicators = [];
    let selectedChartType = null;
    
    // DOM elements
    const dataSelectionEl = document.getElementById('data-selection');
    const chartSelectionEl = document.getElementById('chart-selection');
    const selectedDataInfoEl = document.getElementById('selected-data-info');
    const explanationContentEl = document.getElementById('explanation-content');
    const chartTitleEl = document.getElementById('chart-title');
    
    // Initialize the application
    async function init() {
        try {
            // Load economic data
            economicData = await window.dataModule.loadData();
            
            if (economicData.length === 0) {
                alert('Không thể tải dữ liệu kinh tế. Vui lòng thử lại sau.');
                return;
            }
            
            // Populate indicator selection
            populateIndicatorSelection();
            
            // Populate chart type selection
            populateChartTypeSelection();
            
            // Add event listeners
            addEventListeners();
            
            // Initialize with some default selections
            selectDefaultOptions();
            
        } catch (error) {
            console.error('Error initializing application:', error);
            alert('Đã xảy ra lỗi khi khởi tạo ứng dụng. Vui lòng thử lại sau.');
        }
    }
    
    // Populate indicator selection panel
    function populateIndicatorSelection() {
        const indicators = window.dataModule.getAvailableIndicators();
        
        // Group indicators by category
        const categories = {};
        
        indicators.forEach(indicator => {
            const metadata = window.dataModule.indicatorMetadata[indicator] || {
                displayName: indicator,
                category: 'Khác'
            };
            
            if (!categories[metadata.category]) {
                categories[metadata.category] = [];
            }
            
            categories[metadata.category].push({
                id: indicator,
                displayName: metadata.displayName,
                explanation: metadata.explanation
            });
        });
        
        // Clear previous content
        dataSelectionEl.innerHTML = '<h2>Chọn chỉ số kinh tế</h2>';
        
        // Create HTML for each category
        Object.entries(categories).forEach(([category, items]) => {
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'indicator-category';
            
            const categoryTitle = document.createElement('h3');
            categoryTitle.textContent = category;
            categoryDiv.appendChild(categoryTitle);
            
            items.forEach(item => {
                const label = document.createElement('label');
                label.className = 'indicator-label';
                
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.value = item.id;
                checkbox.dataset.name = item.displayName;
                checkbox.dataset.explanation = item.explanation;
                
                const span = document.createElement('span');
                span.textContent = item.displayName;
                
                label.appendChild(checkbox);
                label.appendChild(span);
                categoryDiv.appendChild(label);
            });
            
            dataSelectionEl.appendChild(categoryDiv);
        });
    }
    
    // Populate chart type selection panel
    function populateChartTypeSelection() {
        // Clear previous content
        chartSelectionEl.innerHTML = '<h2>Chọn loại biểu đồ</h2>';
        
        const chartTypes = window.dataModule.chartTypes;
        
        // Create HTML for each chart type
        chartTypes.forEach(chart => {
            const chartOption = document.createElement('div');
            chartOption.className = `chart-option ${chart.suitability}`;
            chartOption.dataset.chartId = chart.id;
            
            const chartIcon = document.createElement('div');
            chartIcon.className = 'chart-icon';
            chartIcon.textContent = chart.icon;
            
            const chartInfo = document.createElement('div');
            chartInfo.className = 'chart-info';
            
            const chartName = document.createElement('span');
            chartName.className = 'chart-name';
            chartName.textContent = chart.name;
            
            const chartReason = document.createElement('span');
            chartReason.className = 'chart-reason';
            chartReason.textContent = chart.reason;
            
            chartInfo.appendChild(chartName);
            chartInfo.appendChild(chartReason);
            
            chartOption.appendChild(chartIcon);
            chartOption.appendChild(chartInfo);
            
            chartSelectionEl.appendChild(chartOption);
        });
    }
    
    // Add event listeners
    function addEventListeners() {
        // Indicator checkboxes
        dataSelectionEl.addEventListener('change', handleIndicatorChange);
        
        // Chart type options
        chartSelectionEl.addEventListener('click', handleChartTypeClick);
    }
    
    // Handle indicator change
    function handleIndicatorChange(event) {
        if (event.target.type === 'checkbox') {
            updateSelectedIndicators();
            updateChartRecommendations();
            renderVisualization();
        }
    }
    
    // Handle chart type click
    function handleChartTypeClick(event) {
        const chartOption = event.target.closest('.chart-option');
        
        if (chartOption) {
            const chartId = chartOption.dataset.chartId;
            
            // Check if we can use this chart with current indicators
            const chartInfo = window.dataModule.chartTypes.find(c => c.id === chartId);
            
            if (chartInfo) {
                if (selectedIndicators.length < chartInfo.minIndicators) {
                    alert(`Biểu đồ này cần ít nhất ${chartInfo.minIndicators} chỉ số. Vui lòng chọn thêm chỉ số.`);
                    return;
                }
                
                if (selectedIndicators.length > chartInfo.maxIndicators) {
                    alert(`Biểu đồ này chỉ hỗ trợ tối đa ${chartInfo.maxIndicators} chỉ số. Vui lòng bỏ chọn một số chỉ số.`);
                    return;
                }
                
                // Update selected chart type
                selectedChartType = chartId;
                
                // Update UI
                document.querySelectorAll('.chart-option').forEach(option => {
                    option.classList.remove('selected');
                });
                
                chartOption.classList.add('selected');
                
                // Render visualization
                renderVisualization();
            }
        }
    }
    
    // Update selected indicators array
    function updateSelectedIndicators() {
        selectedIndicators = [];
        
        dataSelectionEl.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            if (checkbox.checked) {
                selectedIndicators.push(checkbox.value);
            }
        });
        
        // Update selected data info
        updateSelectedDataInfo();
    }
    
    // Update recommendations for chart types based on selected indicators
    function updateChartRecommendations() {
        const recommendations = window.dataModule.recommendChartTypes(selectedIndicators);
        
        // Update UI
        document.querySelectorAll('.chart-option').forEach(option => {
            const chartId = option.dataset.chartId;
            const chartInfo = recommendations.find(c => c.id === chartId);
            
            if (chartInfo) {
                option.className = `chart-option ${chartInfo.suitability}`;
            }
        });
    }
    
    // Update selected data info
    function updateSelectedDataInfo() {
        if (selectedIndicators.length === 0) {
            selectedDataInfoEl.innerHTML = '<p>Chưa chọn chỉ số nào.</p>';
            return;
        }
        
        let html = '<h3>Các chỉ số đã chọn</h3><ul>';
        
        selectedIndicators.forEach(indicator => {
            const metadata = window.dataModule.indicatorMetadata[indicator] || { displayName: indicator, unit: '' };
            const stats = window.dataModule.calculateStats(indicator);
            
            if (stats) {
                html += `
                    <li>
                        <strong>${metadata.displayName}</strong>
                        <ul>
                            <li>Giá trị mới nhất: ${stats.latest.toFixed(2)} ${metadata.unit}</li>
                            <li>Giá trị trung bình: ${stats.avg.toFixed(2)} ${metadata.unit}</li>
                            <li>Thay đổi gần đây: ${stats.change > 0 ? '+' : ''}${stats.change.toFixed(2)} ${metadata.unit}</li>
                        </ul>
                    </li>
                `;
            }
        });
        
        html += '</ul>';
        selectedDataInfoEl.innerHTML = html;
    }
    
    // Render visualization based on selected chart type and indicators
    function renderVisualization() {
        if (selectedIndicators.length === 0 || !selectedChartType) {
            return;
        }
        
        // Render the appropriate chart
        switch (selectedChartType) {
            case 'line':
                if (selectedIndicators.length === 1) {
                    window.chartsModule.createLineChart(economicData, selectedIndicators[0]);
                }
                break;
                
            case 'multi-line':
                if (selectedIndicators.length >= 2) {
                    window.chartsModule.createMultiLineChart(economicData, selectedIndicators);
                }
                break;
                
            case 'area':
                if (selectedIndicators.length >= 2) {
                    window.chartsModule.createStackedAreaChart(economicData, selectedIndicators);
                }
                break;
                
            case 'scatter':
                if (selectedIndicators.length === 2) {
                    window.chartsModule.createScatterPlot(economicData, selectedIndicators);
                }
                break;
                
            case 'heatmap':
                if (selectedIndicators.length >= 3) {
                    window.chartsModule.createHeatmap(economicData, selectedIndicators);
                }
                break;
                
            case 'seasonal':
                if (selectedIndicators.length === 1) {
                    window.chartsModule.createSeasonalPlot(economicData, selectedIndicators[0]);
                }
                break;
                
            default:
                console.warn('Unsupported chart type:', selectedChartType);
        }
    }
    
    // Select default options
    function selectDefaultOptions() {
        // Select default indicators
        const defaultIndicators = ['Food_Inflation', 'Core_Inlation', 'MonthlyCPI'];
        
        defaultIndicators.forEach(indicator => {
            const checkbox = dataSelectionEl.querySelector(`input[value="${indicator}"]`);
            if (checkbox) {
                checkbox.checked = true;
            }
        });
        
        // Update selected indicators
        updateSelectedIndicators();
        
        // Update chart recommendations
        updateChartRecommendations();
        
        // Select default chart type
        const defaultChartType = 'multi-line';
        const chartOption = document.querySelector(`.chart-option[data-chart-id="${defaultChartType}"]`);
        
        if (chartOption) {
            chartOption.classList.add('selected');
            selectedChartType = defaultChartType;
        }
        
        // Render visualization
        renderVisualization();
    }
    
    // Initialize on page load
    document.addEventListener('DOMContentLoaded', init);
})();