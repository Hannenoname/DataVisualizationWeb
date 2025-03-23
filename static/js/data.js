/**
 * Data handling functions for the Economic Dashboard
 */

// Indicator metadata with display names and explanations
const indicatorMetadata = {
    'Brent': {
        displayName: 'Giá dầu Brent',
        explanation: 'Giá dầu Brent là giá giao dịch của dầu thô Brent, một chỉ số quan trọng của thị trường dầu mỏ quốc tế. Khi giá dầu tăng, chi phí vận chuyển và sản xuất hàng hóa thường tăng theo, ảnh hưởng đến giá cả.',
        unit: 'USD/thùng',
        category: 'Hàng hóa quốc tế'
    },
    'China_CPI': {
        displayName: 'Chỉ số giá tiêu dùng Trung Quốc',
        explanation: 'Chỉ số giá tiêu dùng (CPI) của Trung Quốc phản ánh mức độ thay đổi giá của giỏ hàng hóa và dịch vụ tiêu dùng tại Trung Quốc. Vì Trung Quốc là đối tác thương mại lớn của Việt Nam, CPI Trung Quốc có thể ảnh hưởng đến giá hàng nhập khẩu từ Trung Quốc.',
        unit: '%',
        category: 'Kinh tế quốc tế'
    },
    'Core_Inlation': {
        displayName: 'Lạm phát cơ bản',
        explanation: 'Lạm phát cơ bản (không bao gồm thực phẩm và năng lượng) phản ánh xu hướng lạm phát dài hạn và ít biến động hơn lạm phát tổng thể. Đây là chỉ số quan trọng để đánh giá áp lực giá cả cơ bản của nền kinh tế.',
        unit: '%',
        category: 'Lạm phát'
    },
    'Export': {
        displayName: 'Xuất khẩu',
        explanation: 'Xuất khẩu là tổng giá trị hàng hóa và dịch vụ bán ra nước ngoài. Xuất khẩu tăng thường là dấu hiệu tích cực cho nền kinh tế và có thể giúp tăng giá trị đồng nội tệ.',
        unit: 'Tỷ USD',
        category: 'Thương mại'
    },
    'Food_Inflation': {
        displayName: 'Lạm phát thực phẩm',
        explanation: 'Lạm phát thực phẩm đo lường sự thay đổi giá của các mặt hàng thực phẩm. Đây là một chỉ số quan trọng ở Việt Nam vì thực phẩm chiếm tỷ trọng lớn trong chi tiêu của người dân.',
        unit: '%',
        category: 'Lạm phát'
    },
    'Gold': {
        displayName: 'Giá vàng',
        explanation: 'Giá vàng thường được coi là kênh đầu tư an toàn trong thời kỳ bất ổn kinh tế. Giá vàng tăng có thể phản ánh lo ngại về lạm phát hoặc bất ổn kinh tế.',
        unit: 'USD/ounce',
        category: 'Hàng hóa quốc tế'
    },
    'Import': {
        displayName: 'Nhập khẩu',
        explanation: 'Nhập khẩu là tổng giá trị hàng hóa và dịch vụ mua từ nước ngoài. Nhập khẩu tăng có thể cho thấy nhu cầu trong nước mạnh nhưng cũng có thể gây áp lực lên tỷ giá và cán cân thương mại.',
        unit: 'Tỷ USD',
        category: 'Thương mại'
    },
    'Industrial_products': {
        displayName: 'Sản phẩm công nghiệp',
        explanation: 'Chỉ số sản phẩm công nghiệp phản ánh hoạt động sản xuất trong các ngành công nghiệp. Đây là một chỉ báo quan trọng về sức khỏe của nền kinh tế.',
        unit: 'Chỉ số',
        category: 'Sản xuất'
    },
    'Agriculture, Forestry and Fishing': {
        displayName: 'Nông, lâm nghiệp và thủy sản',
        explanation: 'Chỉ số nông, lâm nghiệp và thủy sản phản ánh sản lượng của các ngành này. Đây là những ngành quan trọng trong nền kinh tế Việt Nam, đặc biệt ở các vùng nông thôn.',
        unit: 'Chỉ số',
        category: 'Sản xuất'
    },
    'MonthlyCPI': {
        displayName: 'CPI hàng tháng',
        explanation: 'Chỉ số giá tiêu dùng hàng tháng đo lường mức thay đổi giá của giỏ hàng hóa và dịch vụ tiêu dùng hàng tháng. Đây là chỉ số chính để đo lường lạm phát.',
        unit: '%',
        category: 'Lạm phát'
    },
    'Unemployment Rate': {
        displayName: 'Tỷ lệ thất nghiệp',
        explanation: 'Tỷ lệ thất nghiệp là phần trăm lực lượng lao động không có việc làm. Tỷ lệ thấp thường là tín hiệu tốt cho nền kinh tế nhưng có thể gây áp lực tăng lương, dẫn đến lạm phát cao hơn.',
        unit: '%',
        category: 'Lao động'
    },
    'USD_VND': {
        displayName: 'Tỷ giá USD/VND',
        explanation: 'Tỷ giá USD/VND là giá của một đô la Mỹ tính bằng đồng Việt Nam. Tỷ giá tăng (VND mất giá) có thể làm tăng giá hàng nhập khẩu, góp phần vào lạm phát.',
        unit: 'VND',
        category: 'Tỷ giá'
    },
    'VN_coffee,tea,mate,spices': {
        displayName: 'Cà phê, trà và gia vị Việt Nam',
        explanation: 'Chỉ số giá cà phê, trà và gia vị Việt Nam phản ánh giá cả của các mặt hàng xuất khẩu quan trọng này của Việt Nam.',
        unit: 'Chỉ số',
        category: 'Hàng hóa trong nước'
    },
    'VN_fiscal_deficit': {
        displayName: 'Thâm hụt tài chính Việt Nam',
        explanation: 'Thâm hụt tài chính là sự chênh lệch giữa chi tiêu của chính phủ và thu ngân sách. Thâm hụt lớn có thể dẫn đến tăng nợ công và có khả năng gây lạm phát trong dài hạn.',
        unit: 'Tỷ VND',
        category: 'Tài chính công'
    },
    'VN_Gasoline_Prices': {
        displayName: 'Giá xăng Việt Nam',
        explanation: 'Giá xăng Việt Nam ảnh hưởng trực tiếp đến chi phí vận chuyển và gián tiếp đến giá của hầu hết hàng hóa và dịch vụ.',
        unit: 'VND/lít',
        category: 'Hàng hóa trong nước'
    },
    'VN_Interest_Rate': {
        displayName: 'Lãi suất Việt Nam',
        explanation: 'Lãi suất Việt Nam ảnh hưởng đến chi phí vay vốn và quyết định tiết kiệm/đầu tư. Lãi suất cao thường được sử dụng để kiểm soát lạm phát, nhưng có thể làm chậm tăng trưởng kinh tế.',
        unit: '%',
        category: 'Tài chính'
    },
    'VN_money_supply': {
        displayName: 'Cung tiền Việt Nam',
        explanation: 'Cung tiền là tổng lượng tiền lưu thông trong nền kinh tế. Cung tiền tăng nhanh có thể dẫn đến lạm phát nếu không đi kèm với tăng trưởng kinh tế tương ứng.',
        unit: 'Tỷ VND',
        category: 'Tài chính'
    },
    'VN_rice_price': {
        displayName: 'Giá gạo Việt Nam',
        explanation: 'Giá gạo Việt Nam là một chỉ số quan trọng vì gạo là thực phẩm chính của người Việt Nam và là mặt hàng xuất khẩu quan trọng.',
        unit: 'VND/kg',
        category: 'Hàng hóa trong nước'
    },
    'VN_Trade_Balance': {
        displayName: 'Cán cân thương mại Việt Nam',
        explanation: 'Cán cân thương mại là sự chênh lệch giữa giá trị xuất khẩu và nhập khẩu. Cán cân thương mại thặng dư (xuất khẩu lớn hơn nhập khẩu) thường có lợi cho tỷ giá và tăng trưởng kinh tế.',
        unit: 'Tỷ USD',
        category: 'Thương mại'
    },
    'PC1': {
        displayName: 'Thành phần chính 1',
        explanation: 'Thành phần chính 1 là một chỉ số tổng hợp được tạo ra từ phân tích thành phần chính, tóm tắt xu hướng chung của nhiều biến kinh tế.',
        unit: 'Chỉ số',
        category: 'Tổng hợp'
    }
};

// Chart type metadata
const chartTypes = [
    {
        id: 'line',
        name: 'Biểu đồ đường',
        color: 'green',
        icon: '📈',
        suitability: 'recommended',
        reason: 'Dễ thấy xu hướng giá cả qua thời gian.',
        minIndicators: 1,
        maxIndicators: 1,
        description: 'Biểu đồ đường thể hiện sự thay đổi của một chỉ số theo thời gian. Thích hợp để xem xu hướng tăng, giảm của chỉ số.'
    },
    {
        id: 'multi-line',
        name: 'Biểu đồ đường nhiều chỉ số',
        color: 'yellow',
        icon: '📉',
        suitability: 'possible',
        reason: 'So sánh được nhiều chỉ số, nhưng rối nếu quá nhiều đường.',
        minIndicators: 2,
        maxIndicators: 5,
        description: 'Biểu đồ đường nhiều chỉ số cho phép so sánh xu hướng của nhiều chỉ số kinh tế cùng lúc. Giới hạn ở 2-5 chỉ số để tránh gây rối.'
    },
    {
        id: 'area',
        name: 'Biểu đồ vùng chồng',
        color: 'yellow',
        icon: '📊',
        suitability: 'possible',
        reason: 'Thấy được đóng góp của từng thành phần theo thời gian.',
        minIndicators: 2,
        maxIndicators: 4,
        description: 'Biểu đồ vùng chồng thể hiện đóng góp tương đối của các chỉ số theo thời gian. Hữu ích để thấy phần đóng góp của mỗi thành phần.'
    },
    {
        id: 'bar',
        name: 'Biểu đồ cột',
        color: 'yellow',
        icon: '📊',
        suitability: 'possible',
        reason: 'Dễ so sánh giá trị giữa các tháng trong năm.',
        minIndicators: 1,
        maxIndicators: 1,
        description: 'Biểu đồ cột phù hợp để so sánh giá trị của một chỉ số theo thời gian, đặc biệt hữu ích khi muốn thấy rõ sự chênh lệch.'
    },
    {
        id: 'scatter',
        name: 'Biểu đồ phân tán',
        color: 'green',
        icon: '🔍',
        suitability: 'recommended',
        reason: 'Dễ thấy mối quan hệ giữa hai chỉ số, như giá dầu và lạm phát.',
        minIndicators: 2,
        maxIndicators: 2,
        description: 'Biểu đồ phân tán giúp thấy mối tương quan giữa hai chỉ số. Mỗi điểm đại diện cho một thời điểm (tháng/năm).'
    },
    {
        id: 'heatmap',
        name: 'Ma trận tương quan',
        color: 'red',
        icon: '🧩',
        suitability: 'not-recommended',
        reason: 'Phức tạp và khó hiểu cho người không quen với thống kê.',
        minIndicators: 3,
        maxIndicators: 8,
        description: 'Ma trận tương quan thể hiện mức độ tương quan giữa nhiều chỉ số kinh tế. Màu đỏ: tương quan thuận mạnh, màu xanh: tương quan nghịch.'
    },
    {
        id: 'seasonal',
        name: 'Biểu đồ mùa vụ',
        color: 'green',
        icon: '🗓️',
        suitability: 'recommended',
        reason: 'Dễ thấy mẫu mùa vụ theo tháng, như giá thực phẩm tăng vào Tết.',
        minIndicators: 1,
        maxIndicators: 1,
        description: 'Biểu đồ mùa vụ phân tích tính mùa vụ của một chỉ số. Hiển thị 12 biểu đồ nhỏ, mỗi biểu đồ cho một tháng.'
    },
    {
        id: 'calendar',
        name: 'Bản đồ nhiệt theo thời gian',
        color: 'yellow',
        icon: '📅',
        suitability: 'possible',
        reason: 'Thấy được biến động theo tháng và năm nhưng cần không gian lớn.',
        minIndicators: 1,
        maxIndicators: 1,
        description: 'Bản đồ nhiệt theo thời gian hiển thị sự thay đổi của một chỉ số theo từng tháng qua các năm dưới dạng bản đồ nhiệt màu.'
    }
];

// Relationship between indicators for explanations
const relationshipExplanations = {
    'Brent_Core_Inlation': 'Giá dầu Brent thường có mối quan hệ thuận với lạm phát cơ bản. Khi giá dầu tăng, chi phí vận chuyển và sản xuất tăng, dẫn đến giá thành sản phẩm cao hơn, góp phần vào lạm phát cơ bản.',
    'Brent_VN_Gasoline_Prices': 'Giá dầu Brent có ảnh hưởng trực tiếp đến giá xăng tại Việt Nam. Khi giá dầu thế giới tăng, giá xăng trong nước thường tăng theo, mặc dù có thể bị điều tiết bởi Quỹ Bình ổn giá xăng dầu.',
    'Core_Inlation_VN_Interest_Rate': 'Ngân hàng Nhà nước thường điều chỉnh lãi suất để kiểm soát lạm phát. Khi lạm phát cơ bản tăng cao, lãi suất thường được tăng để giảm cung tiền và kiềm chế lạm phát.',
    'Food_Inflation_MonthlyCPI': 'Lạm phát thực phẩm đóng góp đáng kể vào CPI hàng tháng vì thực phẩm chiếm tỷ trọng lớn trong giỏ hàng hóa tiêu dùng của người Việt Nam. Biến động giá thực phẩm thường ảnh hưởng rõ rệt đến CPI tổng thể.',
    'USD_VND_Import': 'Tỷ giá USD/VND ảnh hưởng trực tiếp đến giá hàng nhập khẩu. Khi đồng Việt Nam mất giá (tỷ giá tăng), hàng nhập khẩu trở nên đắt đỏ hơn, có thể làm giảm lượng nhập khẩu hoặc tăng giá hàng nhập khẩu.',
    'Export_VN_Trade_Balance': 'Xuất khẩu là một thành phần của cán cân thương mại. Khi xuất khẩu tăng mà nhập khẩu không đổi hoặc tăng ít hơn, cán cân thương mại sẽ cải thiện (thặng dư tăng hoặc thâm hụt giảm).',
    'VN_Interest_Rate_VN_money_supply': 'Lãi suất và cung tiền có mối quan hệ nghịch. Khi Ngân hàng Nhà nước tăng lãi suất, chi phí vay vốn tăng, làm giảm lượng tiền trong lưu thông, giảm cung tiền.'
};

// Seasonal explanation for indicators
const seasonalExplanations = {
    'Food_Inflation': 'Lạm phát thực phẩm ở Việt Nam thường có tính mùa vụ rõ rệt. Giá thực phẩm thường tăng vào những tháng cuối năm do nhu cầu tiêu dùng tăng vào dịp Tết Nguyên đán. Ngoài ra, mùa mưa bão (khoảng tháng 7-10) có thể ảnh hưởng đến nguồn cung thực phẩm, đẩy giá lên cao.',
    'MonthlyCPI': 'CPI hàng tháng thường tăng vào tháng 12 và tháng 1 do nhu cầu tiêu dùng tăng trong dịp Tết Nguyên đán. Đầu năm học mới (tháng 8-9) cũng thường thấy CPI tăng do chi phí giáo dục tăng.',
    'VN_rice_price': 'Giá gạo thường biến động theo mùa vụ thu hoạch. Việt Nam có hai vụ lúa chính: vụ Đông Xuân (thu hoạch khoảng tháng 5-6) và vụ Hè Thu (thu hoạch khoảng tháng 9-10). Giá gạo thường giảm sau khi thu hoạch và tăng trước vụ mới.',
    'Export': 'Hoạt động xuất khẩu thường tăng mạnh vào cuối năm để đáp ứng nhu cầu mùa lễ hội ở các thị trường phương Tây. Ngược lại, xuất khẩu thường giảm vào tháng 1-2 do ảnh hưởng của Tết Nguyên đán.',
    'VN_Gasoline_Prices': 'Giá xăng dầu thường tăng vào mùa du lịch (hè) do nhu cầu đi lại tăng, và có thể biến động mạnh theo giá dầu thế giới.'
};

// Data loading and processing
let economicData = [];
let selectedIndicators = [];
let selectedChartType = '';

// Load data from JSON file
async function loadData() {
    try {
        const response = await fetch('/static/data/economic_data.json');
        const data = await response.json();
        
        // Format the data for use in visualizations
        economicData = data.map(d => {
            // Parse date strings to Date objects
            const date = new Date(d.Date);
            return {
                ...d,
                formattedDate: `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}`
            };
        });
        
        // Sort data by date
        economicData.sort((a, b) => new Date(a.Date) - new Date(b.Date));
        
        return economicData;
    } catch (error) {
        console.error('Error loading data:', error);
        return [];
    }
}

// Get the list of available indicators (excluding Year, Month, Date, YearMonth)
function getAvailableIndicators() {
    if (economicData.length === 0) return [];
    
    return Object.keys(economicData[0]).filter(key => 
        !['Year', 'Month', 'Date', 'YearMonth', 'formattedDate'].includes(key)
    );
}

// Calculate statistics for a specific indicator
function calculateStats(indicator) {
    if (economicData.length === 0) return null;
    
    const values = economicData.map(d => d[indicator]).filter(v => v !== undefined && v !== null);
    
    if (values.length === 0) return null;
    
    return {
        min: Math.min(...values),
        max: Math.max(...values),
        avg: values.reduce((sum, val) => sum + val, 0) / values.length,
        latest: values[values.length - 1],
        change: values[values.length - 1] - values[values.length - 2]
    };
}

// Calculate correlation between two indicators
function calculateCorrelation(indicator1, indicator2) {
    if (economicData.length === 0) return 0;
    
    const pairs = economicData.map(d => [d[indicator1], d[indicator2]])
        .filter(pair => pair[0] !== undefined && pair[0] !== null && 
                         pair[1] !== undefined && pair[1] !== null);
    
    if (pairs.length < 2) return 0;
    
    // Calculate mean for each indicator
    const mean1 = pairs.reduce((sum, pair) => sum + pair[0], 0) / pairs.length;
    const mean2 = pairs.reduce((sum, pair) => sum + pair[1], 0) / pairs.length;
    
    // Calculate correlation coefficient
    let num = 0;
    let den1 = 0;
    let den2 = 0;
    
    for (const [val1, val2] of pairs) {
        const diff1 = val1 - mean1;
        const diff2 = val2 - mean2;
        
        num += diff1 * diff2;
        den1 += diff1 * diff1;
        den2 += diff2 * diff2;
    }
    
    if (den1 === 0 || den2 === 0) return 0;
    
    return num / Math.sqrt(den1 * den2);
}

// Get data for a specific month across all years
function getMonthlyData(indicator, month) {
    return economicData.filter(d => d.Month === month)
        .map(d => ({
            year: d.Year,
            value: d[indicator]
        }))
        .sort((a, b) => a.year - b.year);
}

// Get relationship explanation for two indicators
function getRelationshipExplanation(indicator1, indicator2) {
    const key1 = `${indicator1}_${indicator2}`;
    const key2 = `${indicator2}_${indicator1}`;
    
    return relationshipExplanations[key1] || 
           relationshipExplanations[key2] || 
           `Mối quan hệ giữa ${indicatorMetadata[indicator1]?.displayName || indicator1} và ${indicatorMetadata[indicator2]?.displayName || indicator2} phụ thuộc vào nhiều yếu tố kinh tế phức tạp và có thể thay đổi theo thời gian.`;
}

// Get seasonal explanation for an indicator
function getSeasonalExplanation(indicator) {
    return seasonalExplanations[indicator] || 
           'Các chỉ số kinh tế thường có tính mùa vụ do các yếu tố như chu kỳ sản xuất, tiêu dùng theo mùa, và các sự kiện đặc biệt trong năm như Tết Nguyên đán.';
}

// Recommend chart types based on selected indicators
function recommendChartTypes(indicators) {
    const count = indicators.length;
    
    return chartTypes.map(chart => {
        let suitability = 'not-recommended';
        
        if (count >= chart.minIndicators && count <= chart.maxIndicators) {
            if (['line', 'seasonal', 'calendar'].includes(chart.id) && count === 1) {
                suitability = 'recommended';
            } else if (chart.id === 'scatter' && count === 2) {
                suitability = 'recommended';
            } else if (['multi-line', 'area', 'bar', 'heatmap'].includes(chart.id)) {
                suitability = 'possible';
            }
        }
        
        return {
            ...chart,
            suitability
        };
    });
}

// Get historical events to annotate charts
function getHistoricalEvents() {
    return [
        { year: 2008, month: 9, event: 'Khủng hoảng tài chính toàn cầu' },
        { year: 2011, month: 3, event: 'Động đất và sóng thần Nhật Bản' },
        { year: 2015, month: 8, event: 'Trung Quốc phá giá đồng nhân dân tệ' },
        { year: 2020, month: 3, event: 'Đại dịch COVID-19 bùng phát' },
        { year: 2022, month: 2, event: 'Xung đột Nga-Ukraine' }
    ];
}

// Export data module
window.dataModule = {
    loadData,
    getAvailableIndicators,
    calculateStats,
    calculateCorrelation,
    getMonthlyData,
    getRelationshipExplanation,
    getSeasonalExplanation,
    recommendChartTypes,
    getHistoricalEvents,
    indicatorMetadata,
    chartTypes
};