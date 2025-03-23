import sys
import os
import traceback
from core.data_handler import data_handler
from core.visualization_handler import viz_handler

def test_all_features():
    """Kiểm tra tất cả tính năng của ứng dụng Economic Data Analyzer"""
    print("Bắt đầu kiểm tra tính năng...")
    
    # Lấy danh sách tất cả chỉ số
    indicators = data_handler.get_available_indicators()
    print(f"Có {len(indicators)} chỉ số: {', '.join(indicators)}")
    
    # Kiểm tra data handler
    print("\n=== Kiểm tra Data Handler ===")
    test_data_handler(indicators)
    
    # Kiểm tra các biểu đồ
    print("\n=== Kiểm tra Visualization Handler ===")
    test_visualizations(indicators)
    
    print("\nKiểm tra hoàn tất!")

def test_data_handler(indicators):
    """Kiểm tra các chức năng của Data Handler"""
    try:
        # Test filter_data với tất cả chỉ số
        all_data = data_handler.filter_data(indicators=indicators)
        print(f"✅ filter_data (tất cả chỉ số): Thành công (shape: {all_data.shape})")
        
        # Test filter_data với một chỉ số
        test_indicator = indicators[0]
        filtered_data = data_handler.filter_data(indicators=[test_indicator])
        print(f"✅ filter_data (1 chỉ số): Thành công (shape: {filtered_data.shape})")
        
        # Test filter_data với nhiều chỉ số
        multi_indicators = indicators[:3]
        filtered_data = data_handler.filter_data(indicators=multi_indicators)
        print(f"✅ filter_data (nhiều chỉ số): Thành công (shape: {filtered_data.shape})")
        
        # Test create_correlation_data
        corr_matrix = data_handler.create_correlation_data(indicators[:5])
        print(f"✅ create_correlation_data: Thành công (shape: {corr_matrix.shape})")
        
    except Exception as e:
        print(f"❌ Data Handler lỗi: {e}")
        traceback.print_exc()

def test_visualizations(indicators):
    """Kiểm tra tất cả các loại biểu đồ"""
    visualization_tests = [
        ("create_line_chart", test_line_chart),
        ("create_scatter_plot", test_scatter_plot),
        ("create_calendar_heatmap", test_calendar_heatmap),
        ("create_seasonal_chart", test_seasonal_chart),
        ("create_correlation_heatmap", test_correlation_heatmap),
        ("create_trend_chart", test_trend_chart),
        ("create_bar_chart", test_bar_chart),
        ("create_pie_chart", test_pie_chart),
        ("create_sankey_chart", test_sankey_chart)
    ]
    
    for name, test_func in visualization_tests:
        try:
            test_func(indicators)
            print(f"✅ {name}: Thành công")
        except Exception as e:
            print(f"❌ {name} lỗi: {e}")
            traceback.print_exc()

def test_line_chart(indicators):
    """Kiểm tra biểu đồ đường"""
    # Test với 1 chỉ số
    fig = viz_handler.create_line_chart([indicators[0]])
    if fig is None:
        raise ValueError("Biểu đồ trả về None")
    
    # Test với nhiều chỉ số
    fig = viz_handler.create_line_chart(indicators[:3])
    if fig is None:
        raise ValueError("Biểu đồ trả về None")
    
    # Test với danh sách rỗng
    fig = viz_handler.create_line_chart([])
    if fig is not None:
        raise ValueError("Biểu đồ không trả về None với danh sách rỗng")

def test_scatter_plot(indicators):
    """Kiểm tra biểu đồ phân tán"""
    # Test với đúng 2 chỉ số
    fig = viz_handler.create_scatter_plot(indicators[:2])
    if fig is None:
        raise ValueError("Biểu đồ trả về None")
    
    # Test với 1 chỉ số
    fig = viz_handler.create_scatter_plot([indicators[0]])
    if fig is not None:
        raise ValueError("Biểu đồ không trả về None với 1 chỉ số")
    
    # Test với 3 chỉ số
    fig = viz_handler.create_scatter_plot(indicators[:3])
    if fig is not None:
        raise ValueError("Biểu đồ không trả về None với 3 chỉ số")

def test_calendar_heatmap(indicators):
    """Kiểm tra biểu đồ heatmap theo lịch"""
    # Test với 1 chỉ số
    fig = viz_handler.create_calendar_heatmap(indicators[0])
    if fig is None:
        raise ValueError("Biểu đồ trả về None")
    
    # Test với chỉ số rỗng
    fig = viz_handler.create_calendar_heatmap("")
    if fig is not None:
        raise ValueError("Biểu đồ không trả về None với chỉ số rỗng")

def test_seasonal_chart(indicators):
    """Kiểm tra biểu đồ mùa vụ"""
    # Test với 1 chỉ số
    fig = viz_handler.create_seasonal_chart(indicators[0])
    if fig is None:
        raise ValueError("Biểu đồ trả về None")
    
    # Test với chỉ số rỗng
    fig = viz_handler.create_seasonal_chart("")
    if fig is not None:
        raise ValueError("Biểu đồ không trả về None với chỉ số rỗng")

def test_correlation_heatmap(indicators):
    """Kiểm tra biểu đồ nhiệt tương quan"""
    # Test với nhiều chỉ số
    fig = viz_handler.create_correlation_heatmap(indicators[:5])
    if fig is None:
        raise ValueError("Biểu đồ trả về None")
    
    # Test với 1 chỉ số
    fig = viz_handler.create_correlation_heatmap([indicators[0]])
    if fig is not None:
        raise ValueError("Biểu đồ không trả về None với 1 chỉ số")
    
    # Test với danh sách rỗng
    fig = viz_handler.create_correlation_heatmap([])
    if fig is not None:
        raise ValueError("Biểu đồ không trả về None với danh sách rỗng")

def test_trend_chart(indicators):
    """Kiểm tra biểu đồ xu hướng"""
    # Test với 1 chỉ số
    fig = viz_handler.create_trend_chart(indicators[0])
    if fig is None:
        raise ValueError("Biểu đồ trả về None")
    
    # Test với chỉ số rỗng
    fig = viz_handler.create_trend_chart("")
    if fig is not None:
        raise ValueError("Biểu đồ không trả về None với chỉ số rỗng")

def test_bar_chart(indicators):
    """Kiểm tra biểu đồ cột"""
    # Test với nhiều chỉ số
    fig = viz_handler.create_bar_chart(indicators[:3])
    if fig is None:
        raise ValueError("Biểu đồ trả về None")
    
    # Test với 1 chỉ số
    fig = viz_handler.create_bar_chart([indicators[0]])
    if fig is None:
        raise ValueError("Biểu đồ trả về None")
    
    # Test với danh sách rỗng
    fig = viz_handler.create_bar_chart([])
    if fig is not None:
        raise ValueError("Biểu đồ không trả về None với danh sách rỗng")

def test_pie_chart(indicators):
    """Kiểm tra biểu đồ tròn"""
    # Test với nhiều chỉ số
    fig = viz_handler.create_pie_chart(indicators[:3])
    if fig is None:
        raise ValueError("Biểu đồ trả về None")
    
    # Test với 1 chỉ số
    fig = viz_handler.create_pie_chart([indicators[0]])
    if fig is not None:
        raise ValueError("Biểu đồ không trả về None với 1 chỉ số")

def test_sankey_chart(indicators):
    """Kiểm tra biểu đồ Sankey"""
    # Test với nhiều chỉ số
    fig = viz_handler.create_sankey_chart(indicators[:3])
    if fig is None:
        raise ValueError("Biểu đồ trả về None")
    
    # Test với 1 chỉ số
    fig = viz_handler.create_sankey_chart([indicators[0]])
    if fig is None:
        raise ValueError("Biểu đồ trả về None với 1 chỉ số")
    
    # Test với danh sách rỗng
    fig = viz_handler.create_sankey_chart([])
    if fig is not None:
        raise ValueError("Biểu đồ không trả về None với danh sách rỗng")

if __name__ == "__main__":
    test_all_features() 