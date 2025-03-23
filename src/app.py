import streamlit as st
import base64
from core.data_handler import data_handler
from core.visualization_handler import viz_handler

# Thêm CSS trực tiếp cho ảnh nền
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* Make content containers slightly transparent to show background */
        .css-18e3th9, .css-1d391kg, .stTabs [data-baseweb="tab-panel"] {{
            background-color: rgba(255, 255, 255, 0.85) !important;
            border-radius: 8px;
            padding: 10px;
        }}
        
        /* Style for widgets */
        .stSelectbox, .stMultiSelect {{
            background-color: rgba(255, 255, 255, 0.92) !important;
        }}
        
        /* Style for charts and visualization containers */
        [data-testid="stBlock"] {{
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }}
        
        /* Chỉ áp dụng text-shadow cho văn bản trong main-title */
        .main-title h1, .main-title h2, .main-title p {{
            color: white !important;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6);
        }}
        
        /* Loại bỏ text-shadow cho các văn bản khác */
        body, h1, h2, h3, p, label {{
            text-shadow: none;
        }}
        
        /* Style for main header section */
        .main-title {{
            text-align: center;
            padding: 40px 20px;
            margin-bottom: 30px;
            background-color: rgba(0, 0, 0, 0.4);
            border-radius: 12px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        }}
        
        .main-title h1 {{
            color: white !important;
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            font-size: 3.5rem;
            margin-bottom: 10px;
            letter-spacing: 1px;
            text-transform: uppercase;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }}
        
        .main-title h2 {{
            color: white !important;
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 10px;
            letter-spacing: 1px;
            text-transform: uppercase;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }}
        
        .main-title p {{
            color: white !important;
            font-family: 'Poppins', sans-serif;
            font-size: 1.2rem;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.6;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }}
        
        /* Hide the default Streamlit title */
        .css-1q8dd3e {{
            display: none;
        }}
        
        /* Add a gradient overlay to the header */
        .main-title::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(43, 108, 176, 0.5) 0%, rgba(37, 64, 143, 0.3) 100%);
            border-radius: 12px;
            z-index: -1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def get_chart_recommendations(selected_indicators):
    """Lấy các đề xuất biểu đồ phù hợp dựa trên số lượng chỉ số được chọn"""
    num_indicators = len(selected_indicators)
    
    recommendations = {
        'Biểu đồ xu hướng': {
            'icon': '📈',
            'description': 'Hiển thị biến động các chỉ số theo thời gian',
            'conditions': 'Phù hợp với 1-5 chỉ số',
            'status': 'recommended' if 1 <= num_indicators <= 5 else 'possible' if num_indicators > 5 else 'not_recommended'
        },
        'Biểu đồ vùng': {
            'icon': '🏞️',
            'description': 'Hiển thị xu hướng với diện tích tô màu',
            'conditions': 'Phù hợp với 2-5 chỉ số',
            'status': 'recommended' if 2 <= num_indicators <= 5 else 'possible' if num_indicators > 5 else 'not_recommended'
        },
        'Biểu đồ cột': {
            'icon': '📊',
            'description': 'So sánh giá trị các chỉ số theo thời gian',
            'conditions': 'Phù hợp với 1-6 chỉ số',
            'status': 'recommended' if 1 <= num_indicators <= 6 else 'possible' if num_indicators > 6 else 'not_recommended'
        },
        'Biểu đồ phân tán': {
            'icon': '🔍',
            'description': 'Phân tích tương quan giữa hai chỉ số',
            'conditions': 'Chính xác 2 chỉ số',
            'status': 'recommended' if num_indicators == 2 else 'not_recommended'
        },
        'Ma trận tương quan': {
            'icon': '🧩',
            'description': 'Hiển thị mối tương quan giữa nhiều chỉ số',
            'conditions': 'Từ 2 chỉ số trở lên',
            'status': 'recommended' if num_indicators >= 4 else 'possible' if num_indicators >= 2 else 'not_recommended'
        },
        'Biểu đồ bong bóng': {
            'icon': '🫧',
            'description': 'Phân tích mối quan hệ giữa 3 chỉ số',
            'conditions': 'Chính xác 3 chỉ số',
            'status': 'recommended' if num_indicators == 3 else 'not_recommended'
        },
        'Biểu đồ mùa vụ': {
            'icon': '📅',
            'description': 'Phân tích biến động theo mùa của một chỉ số',
            'conditions': 'Chính xác 1 chỉ số',
            'status': 'recommended' if num_indicators == 1 else 'not_recommended'
        },
        'Biểu đồ xu hướng chi tiết': {
            'icon': '📉',
            'description': 'Phân tích xu hướng dài hạn của một chỉ số',
            'conditions': 'Chính xác 1 chỉ số',
            'status': 'recommended' if num_indicators == 1 else 'not_recommended'
        },
        'Biểu đồ hộp': {
            'icon': '📦',
            'description': 'Hiển thị phân phối và giá trị bất thường',
            'conditions': 'Từ 1 chỉ số trở lên',
            'status': 'recommended' if 1 <= num_indicators <= 6 else 'possible' if num_indicators > 6 else 'not_recommended'
        },
        'Biểu đồ radar': {
            'icon': '🕸️',
            'description': 'So sánh giá trị chuẩn hóa nhiều chỉ số',
            'conditions': 'Từ 3 chỉ số trở lên',
            'status': 'recommended' if num_indicators >= 3 and num_indicators <= 8 else 'possible' if num_indicators > 8 else 'not_recommended'
        },
        'Bản đồ nhiệt thời gian': {
            'icon': '🗓️',
            'description': 'Phân tích biến động theo tháng và năm',
            'conditions': 'Chính xác 1 chỉ số',
            'status': 'recommended' if num_indicators == 1 else 'not_recommended'
        },
        'Biểu đồ dòng chảy': {
            'icon': '🌊',
            'description': 'Hiển thị sự thay đổi theo thời gian',
            'conditions': 'Từ 1-5 chỉ số',
            'status': 'recommended' if 1 <= num_indicators <= 5 else 'possible' if num_indicators > 5 else 'not_recommended'
        },
        'Biểu đồ bánh': {
            'icon': '🥧',
            'description': 'So sánh tỷ trọng tại một thời điểm',
            'conditions': 'Từ 2 chỉ số trở lên',
            'status': 'recommended' if num_indicators >= 2 and num_indicators <= 7 else 'possible' if num_indicators > 7 else 'not_recommended'
        },
        'Biểu đồ histogram': {
            'icon': '📊',
            'description': 'Phân tích phân phối tần suất giá trị',
            'conditions': 'Chính xác 1 chỉ số',
            'status': 'recommended' if num_indicators == 1 else 'not_recommended'
        }
    }
    
    # Sắp xếp theo mức độ phù hợp: recommended -> possible -> not_recommended
    sorted_charts = {}
    # Thêm các biểu đồ được đề xuất trước
    for chart, info in recommendations.items():
        if info['status'] == 'recommended':
            sorted_charts[chart] = info
            
    # Sau đó là biểu đồ có thể dùng được
    for chart, info in recommendations.items():
        if info['status'] == 'possible':
            sorted_charts[chart] = info
            
    # Cuối cùng là biểu đồ không phù hợp
    for chart, info in recommendations.items():
        if info['status'] == 'not_recommended':
            sorted_charts[chart] = info
    
    return sorted_charts

def get_indicator_explanation_safe(indicator):
    """Lấy thông tin giải thích an toàn về chỉ số, tránh KeyError"""
    explanation = viz_handler.get_indicator_explanation(indicator)
    if not isinstance(explanation, dict):
        return {
            'title': indicator,
            'description': 'Không có thông tin chi tiết',
            'impact': 'Chưa có đánh giá tác động',
            'interpretation': 'Chưa có hướng dẫn giải thích',
            'threshold': {}
        }
    
    # Đảm bảo tất cả các khóa cần thiết đều tồn tại
    if 'title' not in explanation:
        explanation['title'] = indicator
    if 'description' not in explanation:
        explanation['description'] = 'Chỉ số kinh tế quan trọng cần theo dõi'
    if 'impact' not in explanation:
        explanation['impact'] = 'Có ảnh hưởng đến chính sách và hoạt động kinh tế'
    if 'interpretation' not in explanation:
        explanation['interpretation'] = 'Cần phân tích trong bối cảnh tổng thể'
    if 'threshold' not in explanation:
        explanation['threshold'] = {}
        
    return explanation

def create_chart(selected_chart, selected_indicators):
    """Tạo biểu đồ dựa trên loại biểu đồ và các chỉ số được chọn"""
    # Ánh xạ tên biểu đồ với hàm tạo biểu đồ tương ứng
    chart_functions = {
        'Biểu đồ xu hướng': lambda x: viz_handler.create_line_chart(x) if x else None,
        'Biểu đồ cột': lambda x: viz_handler.create_bar_chart(x) if x else None,
        'Biểu đồ phân tán': lambda x: viz_handler.create_scatter_plot(x) if len(x) == 2 else None,
        'Ma trận tương quan': lambda x: viz_handler.create_correlation_heatmap(x) if len(x) >= 2 else None,
        'Biểu đồ mùa vụ': lambda x: viz_handler.create_seasonal_chart(x[0]) if x else None,
        'Biểu đồ xu hướng chi tiết': lambda x: viz_handler.create_trend_chart(x[0]) if x else None,
        'Biểu đồ hộp': lambda x: viz_handler.create_box_plot(x) if x else None,
        'Biểu đồ histogram': lambda x: viz_handler.create_histogram(x[0]) if x else None,
        'Biểu đồ vùng': lambda x: viz_handler.create_area_chart(x) if len(x) >= 2 else None,
        'Biểu đồ radar': lambda x: viz_handler.create_radar_chart(x) if len(x) >= 3 else None,
        'Biểu đồ bong bóng': lambda x: viz_handler.create_bubble_chart(x) if len(x) == 3 else None,
        'Bản đồ nhiệt thời gian': lambda x: viz_handler.create_calendar_heatmap(x[0]) if x else None,
        'Biểu đồ dòng chảy': lambda x: viz_handler.create_sankey_chart(x) if x else None,
        'Biểu đồ bánh': lambda x: viz_handler.create_pie_chart(x) if len(x) >= 2 else None
    }
    
    if selected_chart in chart_functions:
        return chart_functions[selected_chart](selected_indicators)
    return None

def get_chart_explanation(selected_chart):
    """Lấy giải thích về cách đọc biểu đồ"""
    explanation = viz_handler.get_chart_explanation(selected_chart)
    
    if not isinstance(explanation, dict):
        return {
            'title': selected_chart,
            'description': 'Công cụ trực quan hóa dữ liệu.',
            'usage': 'Giúp phân tích và hiểu rõ hơn về dữ liệu.',
            'reading_guide': ['Xem xét xu hướng và mối quan hệ trong dữ liệu']
        }
    
    return explanation

# Hàm gợi ý biểu đồ tự động dựa trên chỉ số đã chọn
def suggest_charts(selected_indicators):
    if not selected_indicators:
        return []
    
    suggestions = []
    num_indicators = len(selected_indicators)
    
    # Xác định có phải tất cả đều là chỉ số giá cả/lạm phát không
    price_related = all(ind in ["Core_Inlation", "Food_Inflation", "MonthlyCPI", "China_CPI"] for ind in selected_indicators)
    
    # Xác định có phải tất cả là chỉ số thương mại không
    trade_related = all(ind in ["Export", "Import", "VN_Trade_Balance", "USD_VND"] for ind in selected_indicators)
    
    # Kiểm tra xem có chỉ số hàng hóa không
    commodity_related = any(ind in ["Brent", "Gold", "VN_Gasoline_Prices", "VN_rice_price", "VN_coffee,tea,mate,spices"] for ind in selected_indicators)
    
    # Gợi ý dựa trên số lượng chỉ số
    if num_indicators == 1:
        suggestions.extend(["Biểu đồ đường", "Biểu đồ cột", "Biểu đồ histogram"])
        if price_related or trade_related or commodity_related:
            suggestions.append("Biểu đồ xu hướng chi tiết")
    elif num_indicators == 2:
        suggestions.extend(["Biểu đồ đường", "Biểu đồ cột", "Biểu đồ scatter"])
        if (price_related and trade_related) or (price_related and commodity_related) or (trade_related and commodity_related):
            suggestions.append("Biểu đồ phân tích hồi quy")
    elif 3 <= num_indicators <= 5:
        suggestions.extend(["Biểu đồ đường", "Biểu đồ cột", "Biểu đồ radar", "Biểu đồ bong bóng"])
        if any(ind in ["Export", "Import"] for ind in selected_indicators) and "VN_Trade_Balance" in selected_indicators:
            suggestions.append("Biểu đồ cột ghép")
    else:  # > 5 indicators
        suggestions.extend(["Biểu đồ heatmap", "Biểu đồ radar", "Biểu đồ song song"])
    
    # Nếu toàn bộ là lạm phát/giá cả
    if price_related and num_indicators > 1:
        suggestions.extend(["Biểu đồ diện tích", "Biểu đồ cột ghép"])
    
    # Nếu có cả Export và Import
    if "Export" in selected_indicators and "Import" in selected_indicators:
        suggestions.extend(["Biểu đồ cột ghép", "Biểu đồ sánh đôi"])
    
    return list(set(suggestions))  # Loại bỏ trùng lặp

def main():
    """Hàm chính của ứng dụng Streamlit"""
    st.set_page_config(page_title="Economic Data Analyzer", page_icon="📊", layout="wide")
    
    # Thêm ảnh nền
    add_bg_from_local("Lovepik_com-401947920-blue-gradient-geometric-background.jpg")
    
    # Tiêu đề duy nhất ở giữa trang
    st.markdown("""
    <div class="main-title">
        <h1>Economic Data Analyzer</h1>
        <h2>📊 Phân Tích Dữ Liệu Kinh Tế</h2>
        <p>Phân tích dữ liệu kinh tế Việt Nam qua các chỉ số vĩ mô quan trọng.</p>
        <p>Khám phá xu hướng và mối quan hệ giữa các chỉ số kinh tế quan trọng của Việt Nam</p>
    </div>
    """, unsafe_allow_html=True)

    # Load custom CSS
    with open('.streamlit/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Add custom CSS for the visualization section
    st.markdown("""
    <style>
    /* Styles for the visualization section */
    .section-header {
        background-color: white;
        border-bottom: 2px solid #e2e8f0;
        padding: 15px;
        border-radius: 10px 10px 0 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .section-header h2 {
        color: #1e293b;
        font-size: 24px;
        font-weight: bold;
        margin: 0;
        padding: 0;
    }
    
    .chart-explanation {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-top: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .chart-explanation h3 {
        color: #1e293b;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    
    .chart-explanation h4 {
        color: #1e293b;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    
    .chart-explanation ul {
        padding-left: 20px;
    }
    
    .chart-explanation li {
        margin-bottom: 8px;
    }
    
    /* Force white background for Plotly chart container */
    [data-testid="stPlotlyChart"] {
        background-color: white !important;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    
    /* Cải thiện hiển thị biểu đồ cột */
    .js-plotly-plot .plotly .bars .point path {
        stroke-width: 1px !important;
        stroke: #000 !important;
    }
    
    /* Tăng kích thước chữ trong trục */
    .js-plotly-plot .plotly .xtick text,
    .js-plotly-plot .plotly .ytick text {
        font-size: 12px !important;
    }
    
    /* Nền trắng cho vùng biểu đồ */
    .js-plotly-plot .plotly .plot-container {
        background-color: white !important;
    }
    
    /* Làm đậm đường lưới để dễ đọc */
    .js-plotly-plot .plotly .gridlayer path {
        stroke-width: 0.5px !important;
        stroke: rgba(150, 150, 150, 0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Main container
    with st.container():
        # Selection panels
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("""
                <div class="panel">
                    <h2><i class="fas fa-chart-line"></i> Chọn Chỉ Số Kinh Tế</h2>
                    <p class="panel-description">Chọn một hoặc nhiều chỉ số để phân tích. Mỗi chỉ số sẽ được hiển thị với màu sắc riêng trên biểu đồ.</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Thêm CSS để làm gọn gàng hơn phần chọn chỉ số
            st.markdown("""
            <style>
            /* Thu gọn không gian trong hộp chọn chỉ số */
            .stCheckbox {
                margin-bottom: 0px !important;
                padding-bottom: 0px !important;
                min-height: 25px !important;
            }
            
            /* Giảm kích thước font và padding */
            .stCheckbox label {
                font-size: 0.9rem !important;
                padding: 3px 0 !important;
            }
            
            /* Làm nhỏ không gian cho expander */
            .streamlit-expanderHeader {
                font-size: 0.95rem !important;
                padding: 5px 10px !important;
            }
            
            .streamlit-expanderContent {
                padding: 0px 10px !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Group indicators by category
            indicator_groups = {
                "Lạm phát và Giá cả": ["Core_Inlation", "Food_Inflation", "MonthlyCPI", "China_CPI"],
                "Thương mại": ["Export", "Import", "VN_Trade_Balance", "USD_VND"],
                "Hàng hóa": ["Brent", "Gold", "VN_Gasoline_Prices", "VN_rice_price", "VN_coffee,tea,mate,spices"],
                "Kinh tế vĩ mô": ["Industrial_products", "Agriculture, Forestry and Fishing", "Unemployment Rate", 
                               "VN_fiscal_deficit", "VN_Interest_Rate", "VN_money_supply"]
            }
            
            selected_indicators = []
            
            # Thêm tracking số chỉ số được chọn
            selected_counts = {group: 0 for group in indicator_groups}
            
            for group_name, indicators in indicator_groups.items():
                # Sử dụng expander mặc định của Streamlit nhưng tùy chỉnh CSS đẹp hơn
                available_indicators = [ind for ind in indicators if ind in data_handler.available_indicators]
                
                with st.expander(f"📌 {group_name} ({sum(1 for ind in available_indicators if f'checkbox_{ind}' in st.session_state and st.session_state[f'checkbox_{ind}'])}/{len(available_indicators)})", expanded=True):
                    for indicator in available_indicators:
                        if st.checkbox(
                            viz_handler.indicator_names.get(indicator, indicator),
                            key=f"checkbox_{indicator}",
                            help=viz_handler.get_indicator_explanation(indicator)['description']
                        ):
                            selected_indicators.append(indicator)
                            selected_counts[group_name] += 1
            
            # CSS để làm nhóm chỉ số gọn hơn
            st.markdown("""
            <style>
                .st-expander {
                    border: 1px solid #e0e0e0 !important;
                    border-radius: 4px !important;
                    margin-bottom: 8px !important;
                    background-color: white !important;
                }
                .st-expander-header {
                    padding: 6px 10px !important;
                    background-color: #f9fafb !important;
                }
                .st-expander-content {
                    padding: 6px 10px !important;
                }
                div.row-widget.stCheckbox {
                    margin-bottom: 2px !important;
                    font-size: 0.9rem !important;
                }
                div.row-widget.stCheckbox label {
                    padding-top: 0 !important;
                    padding-bottom: 0 !important;
                }
                [data-testid="stExpander"] {
                    border: 1px solid #e0e0e0 !important;
                }
            </style>
            """, unsafe_allow_html=True)

        with col2:
            st.subheader("📊 Chọn biểu đồ phân tích")
            
            # General guidelines for chart selection
            st.markdown("""
            <div style="background-color: #f8f8f8; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                <h4 style="margin-top: 0;">🧭 Nguyên tắc chọn biểu đồ phù hợp:</h4>
                <ul style="margin-bottom: 0; padding-left: 20px;">
                    <li><b>Phân tích xu hướng</b>: Dùng biểu đồ đường/xu hướng cho dữ liệu theo thời gian</li>
                    <li><b>Phân tích so sánh</b>: Dùng biểu đồ cột/thanh để so sánh giá trị</li>
                    <li><b>Phân tích mối quan hệ</b>: Dùng scatter plot cho phân tích tương quan</li>
                    <li><b>Phân tích phân phối</b>: Dùng box plot/histogram cho phân bố dữ liệu</li>
                    <li><b>Phân tích đa chỉ số</b>: Dùng radar chart cho phân tích nhiều chỉ số</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Thêm gợi ý biểu đồ dựa trên chỉ số đã chọn
            if selected_indicators:
                suggested_charts = suggest_charts(selected_indicators)
                if suggested_charts:
                    st.markdown("""
                    <div style="background-color: #f8f9fa; border-radius: 5px; padding: 10px; margin-bottom: 15px; border-left: 4px solid #4CAF50;">
                        <h4 style="margin-top: 0; color: #2E7D32;">🧠 Gợi ý biểu đồ phù hợp</h4>
                        <p style="margin-bottom: 5px;">Dựa trên các chỉ số bạn đã chọn, chúng tôi gợi ý các loại biểu đồ sau:</p>
                        <ul style="margin-bottom: 0;">
                    """, unsafe_allow_html=True)
                    
                    for chart in suggested_charts:
                        st.markdown(f"<li><b>{chart}</b></li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div>", unsafe_allow_html=True)
            
            # Lấy danh sách biểu đồ được khuyến nghị dựa trên các chỉ số đã chọn
            recommendations = get_chart_recommendations(selected_indicators)
            selected_chart = None
            
            # Thêm chú thích về chỉ số kinh tế đã chọn
            if selected_indicators:
                indicator_names_vi = [viz_handler.indicator_names.get(ind, ind) for ind in selected_indicators]
                indicator_names_str = ", ".join(indicator_names_vi)
                
                # Xác định loại chỉ số đã chọn để cung cấp gợi ý phù hợp
                price_indicators = ['Core_Inlation', 'Food_Inflation', 'VN_Gasoline_Prices', 'Gold', 'MonthlyCPI', 'VN_rice_price', 'China_CPI']
                trade_indicators = ['Export', 'Import', 'VN_Trade_Balance', 'VN_coffee,tea,mate,spices']
                rate_indicators = ['USD_VND', 'VN_Interest_Rate', 'Unemployment Rate']
                production_indicators = ['Industrial_products', 'Agriculture, Forestry and Fishing', 'Brent']
                
                selected_price = [ind for ind in selected_indicators if ind in price_indicators]
                selected_trade = [ind for ind in selected_indicators if ind in trade_indicators]
                selected_rate = [ind for ind in selected_indicators if ind in rate_indicators]
                selected_production = [ind for ind in selected_indicators if ind in production_indicators]
                
                suggestions = []
                specific_charts = []
                
                # Gợi ý cho chỉ số giá cả
                if selected_price:
                    price_names = [viz_handler.indicator_names.get(ind, ind) for ind in selected_price]
                    price_str = ", ".join(price_names[:3])
                    if len(price_names) > 3:
                        price_str += f" và {len(price_names) - 3} chỉ số khác"
                    
                    suggestions.append(f"<span style='color:#0369a1'><b>{price_str}</b></span>: Sử dụng <b>biểu đồ xu hướng, biểu đồ vùng</b> để theo dõi xu hướng biến động giá theo thời gian.")
                    
                    if len(selected_price) == 1:
                        specific_charts.append(f"<b>Biểu đồ xu hướng chi tiết</b> hoặc <b>Biểu đồ mùa vụ</b> giúp phân tích chi tiết {price_names[0]} qua các giai đoạn")
                    elif len(selected_price) >= 2:
                        specific_charts.append(f"<b>Biểu đồ phân tán</b> giúp phân tích mối quan hệ giữa {price_names[0]} và {price_names[1]} (có ảnh hưởng qua lại?)")
                
                # Gợi ý cho chỉ số thương mại
                if selected_trade:
                    trade_names = [viz_handler.indicator_names.get(ind, ind) for ind in selected_trade]
                    trade_str = ", ".join(trade_names[:3])
                    if len(trade_names) > 3:
                        trade_str += f" và {len(trade_names) - 3} chỉ số khác"
                    
                    suggestions.append(f"<span style='color:#0369a1'><b>{trade_str}</b></span>: Sử dụng <b>biểu đồ cột, biểu đồ bong bóng</b> để so sánh giá trị và phân tích mối quan hệ.")
                    
                    if 'Export' in selected_trade and 'Import' in selected_trade and 'VN_Trade_Balance' in selected_trade:
                        specific_charts.append("<b>Biểu đồ vùng</b> với 3 chỉ số Xuất khẩu, Nhập khẩu và Cán cân thương mại sẽ thể hiện tốt mối quan hệ giữa chúng")
                    elif len(selected_trade) == 1:
                        specific_charts.append(f"<b>Biểu đồ cột</b> là lựa chọn tốt để so sánh giá trị {trade_names[0]} theo từng giai đoạn")
                
                # Gợi ý cho chỉ số tỷ lệ
                if selected_rate:
                    rate_names = [viz_handler.indicator_names.get(ind, ind) for ind in selected_rate]
                    rate_str = ", ".join(rate_names[:3])
                    if len(rate_names) > 3:
                        rate_str += f" và {len(rate_names) - 3} chỉ số khác"
                    
                    suggestions.append(f"<span style='color:#0369a1'><b>{rate_str}</b></span>: Sử dụng <b>biểu đồ xu hướng, biểu đồ phân tán</b> để xem diễn biến và mối tương quan.")
                    
                    if 'USD_VND' in selected_rate and 'VN_Interest_Rate' in selected_rate:
                        specific_charts.append("<b>Biểu đồ phân tán</b> giữa Tỷ giá USD/VND và Lãi suất sẽ cho thấy mối liên hệ giữa chính sách tiền tệ và tỷ giá")
                    elif 'Unemployment Rate' in selected_rate:
                        specific_charts.append("<b>Bản đồ nhiệt thời gian</b> cho Tỷ lệ thất nghiệp giúp phát hiện mẫu hình theo mùa và giai đoạn kinh tế")
                
                # Gợi ý cho chỉ số sản xuất
                if selected_production:
                    prod_names = [viz_handler.indicator_names.get(ind, ind) for ind in selected_production]
                    prod_str = ", ".join(prod_names[:3])
                    if len(prod_names) > 3:
                        prod_str += f" và {len(prod_names) - 3} chỉ số khác"
                    
                    suggestions.append(f"<span style='color:#0369a1'><b>{prod_str}</b></span>: Sử dụng <b>biểu đồ hộp, biểu đồ mùa vụ</b> để phân tích phân phối và yếu tố thời vụ.")
                    
                    if 'Brent' in selected_production and ('Industrial_products' in selected_production or 'Agriculture, Forestry and Fishing' in selected_production):
                        specific_charts.append("<b>Biểu đồ phân tán</b> giữa Giá dầu Brent và chỉ số sản xuất sẽ hiển thị ảnh hưởng của giá năng lượng tới sản xuất")
                
                # Gợi ý kết hợp giữa nhiều loại chỉ số
                if len(selected_indicators) >= 2:
                    if any(ind in price_indicators for ind in selected_indicators) and any(ind in trade_indicators for ind in selected_indicators):
                        specific_charts.append("<b>Ma trận tương quan</b> sẽ cho thấy mối liên hệ giữa các chỉ số giá cả và thương mại (như giá dầu ảnh hưởng tới xuất/nhập khẩu)")
                    
                    if len(selected_indicators) >= 3 and len(selected_indicators) <= 8:
                        specific_charts.append(f"<b>Biểu đồ radar</b> sẽ giúp so sánh toàn diện trạng thái của {len(selected_indicators)} chỉ số đã chọn")
                    
                    if len(selected_indicators) > 4:
                        specific_charts.append("<b>Ma trận tương quan</b> giúp nhanh chóng phát hiện các mối tương quan mạnh cần phân tích sâu hơn")
                
                # Cải thiện hiển thị bằng cách đơn giản hóa cấu trúc HTML
                st.markdown(f"""
                    <div style="background-color: #e0f2fe; padding: 15px; border-radius: 5px; margin-bottom: 15px; border: 1px solid #bae6fd;">
                        <p style="margin: 0; color: #0369a1; font-size: 0.95rem;">
                            <strong>Chỉ số đã chọn:</strong> {indicator_names_str}
                        </p>
                """, unsafe_allow_html=True)
                
                # Hiển thị từng gợi ý riêng biệt
                if suggestions:
                    st.markdown("""
                        <p style="margin: 10px 0 0 0; color: #0369a1; font-size: 0.9rem;">
                            <strong>Gợi ý biểu đồ phù hợp:</strong>
                        </p>
                    """, unsafe_allow_html=True)
                    
                    for suggestion in suggestions:
                        st.markdown(f"<p style='margin: 5px 0 0 15px; color: #0369a1; font-size: 0.85rem;'>• {suggestion}</p>", unsafe_allow_html=True)
                
                # Hiển thị các gợi ý cụ thể
                if specific_charts:
                    st.markdown("""
                        <p style="margin: 10px 0 0 0; color: #0369a1; font-size: 0.9rem;">
                            <strong>Gợi ý cụ thể:</strong>
                        </p>
                    """, unsafe_allow_html=True)
                    
                    for chart in specific_charts:
                        st.markdown(f"<p style='margin: 5px 0 0 15px; color: #0369a1; font-size: 0.85rem;'>• {chart}</p>", unsafe_allow_html=True)
                
                # Lưu ý cuối cùng
                st.markdown("""
                    <div style="font-size: 0.85rem; margin-top: 10px; padding-top: 8px; border-top: 1px dashed #bae6fd; color: #0284c7;">
                        <i>💡 Lưu ý: Kết hợp nhiều biểu đồ giúp phân tích toàn diện hơn.</i>
                    </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Group charts by analysis type
            chart_groups = {
                "Phân tích xu hướng": ["Biểu đồ xu hướng", "Biểu đồ xu hướng chi tiết", "Biểu đồ vùng"],
                "Phân tích so sánh": ["Biểu đồ cột", "Biểu đồ bánh"],
                "Phân tích mối quan hệ": ["Biểu đồ phân tán", "Ma trận tương quan", "Biểu đồ bong bóng"],
                "Phân tích phân phối": ["Biểu đồ hộp", "Biểu đồ histogram"],
                "Phân tích theo mùa": ["Biểu đồ mùa vụ", "Bản đồ nhiệt thời gian"],
                "Phân tích đa chiều": ["Biểu đồ radar", "Biểu đồ dòng chảy"]
            }
            
            # Display charts by group
            for group_name, chart_types in chart_groups.items():
                available_charts = [ct for ct in chart_types if ct in recommendations]
                if available_charts:
                    # Thêm mô tả cho từng nhóm
                    group_descriptions = {
                        "Phân tích xu hướng": "Phù hợp để theo dõi biến động dữ liệu theo thời gian",
                        "Phân tích so sánh": "Phù hợp để so sánh giá trị giữa các chỉ số hoặc các kỳ",
                        "Phân tích mối quan hệ": "Phù hợp để tìm mối tương quan giữa các chỉ số",
                        "Phân tích phân phối": "Phù hợp để nghiên cứu phân phối và biến động của dữ liệu",
                        "Phân tích theo mùa": "Phù hợp để phát hiện xu hướng theo mùa và chu kỳ",
                        "Phân tích đa chiều": "Phù hợp để so sánh nhiều chỉ số cùng lúc"
                    }
                    
                    description = group_descriptions.get(group_name, "")
                    
                    st.markdown(f"""
                        <div class="chart-group">
                            <h4>{group_name}</h4>
                            <p style="font-size: 0.85rem; color: #64748b; margin-top: 0; margin-bottom: 10px;">{description}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    for chart_type in available_charts:
                        chart = recommendations[chart_type]
                        status_colors = {
                            'recommended': '#dcfce7',
                            'possible': '#fef9c3',
                            'not_recommended': '#fee2e2'
                        }
                        status_icons = {
                            'recommended': '✅',
                            'possible': '⚠️',
                            'not_recommended': '❌'
                        }
                        bg_color = status_colors[chart['status']]
                        status_icon = status_icons[chart['status']]
                        
                        st.markdown(f"""
                            <div class="chart-option" style="background-color: {bg_color}; padding: 15px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #e2e8f0;">
                                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                                    <div style="font-size: 1.5rem; margin-right: 10px;">{chart['icon']}</div>
                                    <div style="flex-grow: 1;">
                                        <div style="font-weight: 600; color: #1e293b;">{chart_type}</div>
                                        <div style="font-size: 0.9rem; color: #64748b;">{chart['description']}</div>
                                    </div>
                                    <div style="font-size: 1.2rem;">{status_icon}</div>
                                </div>
                                <div style="font-size: 0.8rem; color: #64748b; margin-top: 5px;">
                                    {chart['conditions']}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if st.checkbox(f"Chọn biểu đồ này", key=f"chart_{chart_type}", value=False):
                            selected_chart = chart_type
                    
                    st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
            
            if not selected_chart:
                st.info("👆 Chọn một loại biểu đồ để hiển thị phân tích")
            
            # Add custom CSS for chart selection
            st.markdown("""
                <style>
                    .chart-group h4 {
                        color: #1e293b;
                        font-size: 1.1rem;
                        font-weight: 600;
                        margin: 15px 0 10px 0;
                    }
                    
                    /* Style for chart selection rows */
                    [data-testid="stHorizontalBlock"] {
                        background: white;
                        padding: 10px;
                        border-radius: 8px;
                        margin-bottom: 8px;
                        border: 1px solid #e2e8f0;
                        transition: all 0.2s ease;
                    }
                    
                    [data-testid="stHorizontalBlock"]:hover {
                        border-color: #3b82f6;
                        transform: translateX(5px);
                    }
                    
                    /* Style for checkboxes */
                    .stCheckbox {
                        padding: 5px 0;
                    }
                    
                    .stCheckbox label {
                        font-weight: 500;
                        color: #1e293b;
                    }
                    
                    /* Style for chart descriptions */
                    .chart-description ul {
                        list-style-type: none;
                    }
                    
                    .chart-description ul li:before {
                        content: "•";
                        color: #3b82f6;
                        font-weight: bold;
                        display: inline-block;
                        width: 1em;
                        margin-left: -1em;
                    }
                    
                    /* Highlight recommended charts */
                    [data-testid="stHorizontalBlock"].recommended {
                        background: #f0f9ff;
                        border-color: #3b82f6;
                    }
                </style>
            """, unsafe_allow_html=True)

        # Visualization section
        if selected_indicators:
            st.markdown('<div class="section-header"><h2>Biểu Đồ Phân Tích</h2></div>', unsafe_allow_html=True)
            
            if selected_chart:
                fig = create_chart(selected_chart, selected_indicators)
                if fig:
                    # Hiển thị biểu đồ
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Combined explanation section in one white container
                    explanation = get_chart_explanation(selected_chart)
                    
                    # Sử dụng st.container() để đảm bảo nội dung nằm trong container chính màu trắng của Streamlit
                    with st.container():
                        # Thêm một container có viền và nền màu trắng
                        st.markdown("""
                        <style>
                            .chart-guide-container {
                                background-color: white;
                                border-radius: 10px;
                                padding: 20px;
                                margin: 20px 0;
                                border: 1px solid #eaeaea;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                            }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        # Hướng dẫn đọc biểu đồ
                        st.markdown(f"""
                            <div class="chart-guide-container">
                                <h3 style="color: #1f77b4;">💡 Hướng dẫn đọc {explanation['title']}</h3>
                                <p>{explanation['description']}</p>
                                <p><strong>Mục đích sử dụng:</strong> {explanation['usage']}</p>
                                <h4>Cách đọc hiểu biểu đồ:</h4>
                                <ul>
                                    {"".join(f'<li>{point}</li>' for point in explanation['reading_guide'])}
                                </ul>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Giải thích chỉ số trong container riêng với background màu trắng
                    with st.container():
                        st.markdown("""
                        <div class="chart-guide-container">
                            <h3 style="color: #1f77b4;">💡 Giải thích chỉ số</h3>
                        """, unsafe_allow_html=True)
                        
                        for indicator in selected_indicators:
                            explanation = get_indicator_explanation_safe(indicator)
                            st.markdown(f"""
                                <div style='margin-bottom:20px; border-bottom: 1px solid #f0f0f0; padding-bottom: 15px;'>
                                    <h4>{explanation['title']}</h4>
                                    <p><strong>Mô tả:</strong> {explanation['description']}</p>
                                    <p><strong>Tác động:</strong> {explanation['impact']}</p>
                                    <p><strong>Cách đọc:</strong> {explanation['interpretation']}</p>
                                    <p><strong>Ngưỡng đánh giá:</strong></p>
                                    <ul>
                                        <li style="color: #ff7043;"><strong>Cao:</strong> {explanation['threshold']['high']}</li>
                                        <li style="color: #4caf50;"><strong>Trung bình:</strong> {explanation['threshold']['medium']}</li>
                                        <li style="color: #2196f3;"><strong>Thấp:</strong> {explanation['threshold']['low']}</li>
                                    </ul>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("👆 Vui lòng chọn ít nhất một chỉ số kinh tế để bắt đầu phân tích")

if __name__ == "__main__":
    main() 