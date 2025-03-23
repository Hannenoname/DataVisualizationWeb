import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from .data_handler import data_handler
import scipy.stats as stats
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

class VisualizationHandler:
    def __init__(self):
        """Initialize visualization handler"""
        self.data_handler = None
        from core.data_handler import data_handler
        self.data_handler = data_handler
        
        # Cập nhật bảng màu hiện đại và hài hòa
        self.color_scheme = {
            'Core_Inflation': '#3b82f6',  # Blue
            'Food_Inflation': '#f97316',  # Orange
            'USD_VND': '#16a34a',         # Green
            'Brent': '#ef4444',           # Red
            'Export': '#8b5cf6',          # Purple
            'Import': '#ec4899',          # Pink
            'VN_Trade_Balance': '#0ea5e9', # Light Blue
            'Gold': '#f59e0b',            # Amber
            'VN_Gasoline_Prices': '#dc2626', # Dark Red
            'VN_Interest_Rate': '#0891b2', # Cyan
            'Industrial_products': '#6366f1', # Indigo
            'MonthlyCPI': '#d946ef',      # Fuchsia
            'Unemployment Rate': '#84cc16', # Lime
            'VN_money_supply': '#0d9488',  # Teal
            'VN_rice_price': '#ca8a04',    # Yellow
            'VN_fiscal_deficit': '#9333ea', # Purple
            'China_CPI': '#7c3aed',        # Violet
            'Agriculture, Forestry and Fishing': '#65a30d', # Green
            'VN_coffee,tea,mate,spices': '#b45309', # Amber
        }
        
        # Danh sách màu dự phòng cho các chỉ số không được định nghĩa
        self.fallback_colors = [
            '#3b82f6', '#f97316', '#16a34a', '#ef4444', '#8b5cf6', 
            '#ec4899', '#0ea5e9', '#f59e0b', '#dc2626', '#0891b2',
            '#6366f1', '#d946ef', '#84cc16', '#0d9488', '#ca8a04'
        ]
        
        # Kiểu hiển thị hover
        self.hover_style = dict(
            bgcolor="rgba(255, 255, 255, 0.95)",
            font_size=12,
            font_family="Poppins, sans-serif",
            bordercolor="#e2e8f0"
        )
        
        # Định nghĩa tên tiếng Việt cho các chỉ số
        self.indicator_names = {
            'Core_Inlation': 'Lạm phát cơ bản',
            'Core_Inflation': 'Lạm phát cơ bản',
            'Food_Inflation': 'Lạm phát thực phẩm',
            'USD_VND': 'Tỷ giá USD/VND',
            'Brent': 'Giá dầu Brent',
            'Export': 'Kim ngạch xuất khẩu',
            'Import': 'Kim ngạch nhập khẩu',
            'VN_Trade_Balance': 'Cán cân thương mại',
            'Gold': 'Giá vàng',
            'VN_Gasoline_Prices': 'Giá xăng dầu',
            'VN_Interest_Rate': 'Lãi suất',
            'Industrial_products': 'Sản xuất công nghiệp',
            'MonthlyCPI': 'CPI hàng tháng',
            'Unemployment Rate': 'Tỷ lệ thất nghiệp',
            'VN_money_supply': 'Cung tiền M2',
            'VN_rice_price': 'Giá gạo',
            'China_CPI': 'CPI Trung Quốc',
            'VN_fiscal_deficit': 'Thâm hụt ngân sách',
            'Agriculture, Forestry and Fishing': 'Nông lâm ngư nghiệp',
            'VN_coffee,tea,mate,spices': 'Cà phê, chè, hương liệu'
        }
        
        # Định nghĩa các giải thích cho từng mức giá trị
        self.indicator_interpretations = {
            'Core_Inlation': {
                'low': 'Áp lực lạm phát thấp, có thể cần kích thích kinh tế',
                'medium': 'Lạm phát ở mức hợp lý, kinh tế ổn định',
                'high': 'Áp lực lạm phát cao, cần chính sách thắt chặt'
            },
            'Core_Inflation': {
                'low': 'Áp lực lạm phát thấp, có thể cần kích thích kinh tế',
                'medium': 'Lạm phát ở mức hợp lý, kinh tế ổn định',
                'high': 'Áp lực lạm phát cao, cần chính sách thắt chặt'
            },
            'Food_Inflation': {
                'low': 'Giá thực phẩm ổn định, có lợi cho người tiêu dùng',
                'medium': 'Giá thực phẩm tăng vừa phải',
                'high': 'Giá thực phẩm tăng cao, ảnh hưởng đến chi tiêu hộ gia đình'
            },
            'USD_VND': {
                'low': 'VND tăng giá, có lợi cho nhập khẩu và đi du lịch nước ngoài',
                'medium': 'Tỷ giá ổn định, thuận lợi cho kế hoạch kinh doanh',
                'high': 'VND mất giá, có lợi cho xuất khẩu nhưng bất lợi cho nhập khẩu'
            },
            'Brent': {
                'low': 'Giá dầu thấp, giảm chi phí sản xuất và vận tải',
                'medium': 'Giá dầu ở mức cân bằng',
                'high': 'Giá dầu cao, tăng chi phí sản xuất và vận tải'
            },
        }
        
        # Thêm các interpretation mặc định cho các chỉ số còn lại
        for indicator in self.indicator_names:
            if indicator not in self.indicator_interpretations:
                self.indicator_interpretations[indicator] = {
                    'low': 'Giá trị thấp hơn mức trung bình lịch sử',
                    'medium': 'Giá trị nằm trong khoảng trung bình lịch sử',
                    'high': 'Giá trị cao hơn mức trung bình lịch sử'
                }
        
        # Thêm các annotation lịch sử quan trọng
        self.historical_annotations = {
            '2007-01': {
                'event': 'Gia nhập WTO',
                'impact': 'Tăng trưởng xuất khẩu và đầu tư nước ngoài',
                'context': 'Việt Nam chính thức gia nhập Tổ chức Thương mại Thế giới'
            },
            '2008-06': {
                'event': 'Khủng hoảng tài chính toàn cầu',
                'impact': 'Tăng lạm phát, giảm tăng trưởng',
                'context': 'Khủng hoảng bùng nổ từ Mỹ và lan rộng toàn cầu'
            },
            '2011-02': {
                'event': 'Thắt chặt chính sách tiền tệ',
                'impact': 'Lãi suất tăng cao, tín dụng giảm',
                'context': 'Ngân hàng Nhà nước tăng lãi suất để kiểm soát lạm phát'
            },
            '2015-08': {
                'event': 'Phá giá đồng Nhân dân tệ',
                'impact': 'Tỷ giá USD/VND tăng mạnh',
                'context': 'Trung Quốc phá giá đồng tiền gây áp lực lên thị trường tiền tệ khu vực'
            },
            '2018-01': {
                'event': 'Chiến tranh thương mại Mỹ-Trung',
                'impact': 'Xuất khẩu tăng do dịch chuyển chuỗi cung ứng',
                'context': 'Mỹ áp thuế lên hàng hóa Trung Quốc, cơ hội cho hàng Việt'
            },
            '2020-01': {
                'event': 'Đại dịch COVID-19',
                'impact': 'Gián đoạn chuỗi cung ứng, tiêu dùng giảm mạnh',
                'context': 'Đại dịch bùng phát từ Trung Quốc và lan rộng toàn cầu'
            },
            '2022-02': {
                'event': 'Xung đột Nga-Ukraine',
                'impact': 'Giá năng lượng và lương thực tăng mạnh',
                'context': 'Xung đột tác động đến chuỗi cung ứng toàn cầu'
            },
            '2023-03': {
                'event': 'Khủng hoảng ngân hàng Mỹ',
                'impact': 'Biến động thị trường tài chính, FED tăng lãi suất',
                'context': 'Silicon Valley Bank và Signature Bank sụp đổ'
            }
        }

    def get_value_interpretation(self, indicator, value):
        """Get interpretation for a value based on its percentile"""
        if indicator not in self.indicator_interpretations:
            return "Không có thông tin diễn giải"
            
        interpretations = self.indicator_interpretations[indicator]
        if value <= 0.33:
            return interpretations["low"]
        elif value <= 0.66:
            return interpretations["medium"]
        else:
            return interpretations["high"]

    def get_hover_template(self, date_str, indicator, value):
        """Get hover template with detailed information"""
        explanation = self.get_indicator_explanation(indicator)
        
        # Xác định mức độ dựa trên ngưỡng
        thresholds = explanation.get('threshold', {})
        level = None
        if thresholds:
            if isinstance(value, (int, float)):
                if indicator in ['Core_Inflation', 'Food_Inflation']:
                    if value > 2: level = 'high'
                    elif value > 1: level = 'medium'
                    else: level = 'low'
                elif indicator == 'USD_VND':
                    if value > 2: level = 'high'
                    elif value > 0.5: level = 'medium'
                    else: level = 'low'
                elif indicator == 'Brent':
                    if value > 80: level = 'high'
                    elif value > 50: level = 'medium'
                    else: level = 'low'
                elif indicator in ['Export', 'Import']:
                    if value > 10: level = 'high'
                    elif value > 5: level = 'medium'
                    else: level = 'low'
                elif indicator == 'VN_Trade_Balance':
                    if value > 1: level = 'high'
                    elif value > -1: level = 'medium'
                    else: level = 'low'
        
        # Định dạng giá trị
        if isinstance(value, (int, float)):
            if indicator in ['Core_Inflation', 'Food_Inflation']:
                formatted_value = f"{value:.1f}%"
            elif indicator == 'USD_VND':
                formatted_value = f"{value:,.0f} VND"
            elif indicator == 'Brent':
                formatted_value = f"${value:.2f}/thùng"
            elif indicator in ['Export', 'Import', 'VN_Trade_Balance']:
                formatted_value = f"${value:.2f} tỷ"
            else:
                formatted_value = f"{value:,.2f}"
        else:
            formatted_value = str(value)

        # Tạo hover text
        hover_text = f"<b>{explanation['title']}</b><br>"
        hover_text += f"Thời điểm: {date_str}<br>"
        hover_text += f"Giá trị: {formatted_value}<br>"
        
        if level and thresholds.get(level):
            hover_text += f"<br>Đánh giá: {thresholds[level]}<br>"
        
        hover_text += f"<br><i>{explanation['interpretation']}</i>"
        
        # Thêm thông tin về tác động
        hover_text += f"<br><br>Tác động: {explanation['impact']}"
        
        return hover_text

    def create_common_layout(self, title, xaxis_title, yaxis_title):
        """Tạo template chung cho các biểu đồ để đảm bảo thiết kế nhất quán"""
        layout = dict(
            title=dict(
                text=title,
                font=dict(size=20, color='#1e293b', family='Montserrat, sans-serif'),
                x=0.5,
                xanchor='center'
            ),
            paper_bgcolor='white',
            plot_bgcolor='#f8fafc',
            xaxis=dict(
                title=xaxis_title,
                tickfont=dict(size=12, family='Poppins, sans-serif'),
                gridcolor='#e2e8f0',
                zeroline=True,
                zerolinecolor='#cbd5e1',
                zerolinewidth=1
            ),
            yaxis=dict(
                title=yaxis_title,
                tickfont=dict(size=12, family='Poppins, sans-serif'),
                gridcolor='#e2e8f0',
                zeroline=True,
                zerolinecolor='#cbd5e1',
                zerolinewidth=1
            ),
            hoverlabel=self.hover_style,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(family='Poppins, sans-serif', size=12),
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='#e2e8f0',
                borderwidth=1
            ),
            margin=dict(l=60, r=40, t=80, b=60),
            shapes=[],
            annotations=[]
        )
        return layout

    def apply_theme_to_figure(self, fig):
        """Áp dụng các tùy chỉnh hình ảnh và animation cho biểu đồ"""
        # Cập nhật màu sắc và font chữ
        fig.update_layout(
            font_family='Poppins, sans-serif',
            uniformtext_minsize=10,
            uniformtext_mode='hide',
            coloraxis_showscale=True,
            coloraxis_colorbar=dict(
                thicknessmode="pixels", thickness=15,
                outlinewidth=1,
                outlinecolor='#e2e8f0',
                lenmode="fraction", len=0.6,
                yanchor="middle",
                y=0.5,
                titlefont=dict(size=12, family='Poppins, sans-serif'),
                tickfont=dict(size=10, family='Poppins, sans-serif')
            )
        )
        
        # Thêm watermark cho biểu đồ
        fig.add_annotation(
            text="Economic Data Analyzer",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(
                family='Montserrat, sans-serif',
                size=36,
                color='rgba(200,200,200,0.1)'
            ),
            textangle=0,
            align="center",
        )
        
        # Thêm hiệu ứng chuyển động cho biểu đồ
        for i, trace in enumerate(fig.data):
            if hasattr(trace, 'marker'):
                if hasattr(trace.marker, 'color') and trace.marker.color is not None:
                    continue
                    
                if 'scatter' in trace.type.lower():
                    if isinstance(trace.marker, dict) or trace.marker is None:
                        fig.data[i].marker = dict(
                            opacity=0.8,
                            line=dict(width=1, color='white')
                        )
        
        return fig

    def create_line_chart(self, indicators):
        """Create line chart with enhanced hover information and annotations"""
        if not indicators:
            return None
        
        df = self.data_handler.filter_data(indicators=indicators)
        df['Time'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)
        
        # Tạo layout chung
        layout = self.create_common_layout(
            title="Biến động các chỉ số theo thời gian",
            xaxis_title="Thời gian",
            yaxis_title="Giá trị"
        )
        
        # Cập nhật trục X cho biểu đồ đường
        layout['xaxis']['tickangle'] = -45
        layout['xaxis']['tickformat'] = '%Y-%m'
        
        # Mở rộng diện tích biểu đồ để các nhãn không chồng lên nhau
        layout['height'] = 700  # Tăng chiều cao
        layout['margin'] = dict(t=80, l=60, r=40, b=120)  # Tăng lề dưới để có không gian cho nhãn
        
        fig = go.Figure(layout=layout)
        
        # Thêm đường cho từng chỉ số
        for idx, indicator in enumerate(indicators):
            hover_texts = [
                self.get_hover_template(time, indicator, value)
                for time, value in zip(df['Time'], df[indicator])
            ]
            
            # Tính toán % thay đổi
            pct_change = df[indicator].pct_change() * 100
            
            # Lấy màu từ bảng màu hoặc màu dự phòng nếu không có
            color = self.color_scheme.get(indicator, self.fallback_colors[idx % len(self.fallback_colors)])
            
            # Thêm đường chính
            fig.add_trace(go.Scatter(
                x=df['Time'],
                y=df[indicator],
                name=self.indicator_names.get(indicator, indicator),
                mode='lines+markers',
                line=dict(
                    width=3,
                    color=color,
                    shape='spline',  # Làm mịn đường
                    smoothing=1.3    # Độ mịn của đường
                ),
                marker=dict(
                    size=8,
                    color=color,
                    line=dict(width=2, color='white'),
                    symbol='circle'
                ),
                hovertemplate="%{customdata}<extra></extra>",
                customdata=hover_texts
            ))
            
            # Thêm điểm đánh dấu cho các thay đổi đáng kể
            significant_changes = df[abs(pct_change) > 5].index
            if len(significant_changes) > 0:
                # Tạo hover text cho từng điểm biến động mạnh
                significant_hover_texts = []
                for idx in significant_changes:
                    change_val = pct_change.loc[idx]
                    significant_hover_texts.append(
                        f"<b>{self.indicator_names.get(indicator, indicator)}</b><br>" +
                        f"Thời điểm: {df.loc[idx, 'Time']}<br>" +
                        f"Giá trị: {df.loc[idx, indicator]:.2f}<br>" +
                        f"Thay đổi: {change_val:.1f}%<br>" +
                        f"<b>Nhận định:</b> {'Tăng đột biến' if change_val > 0 else 'Giảm mạnh'}"
                    )
                
                fig.add_trace(go.Scatter(
                    x=df.loc[significant_changes, 'Time'],
                    y=df.loc[significant_changes, indicator],
                    mode='markers',
                    marker=dict(
                        symbol='star',
                        size=12,
                        color=color,
                        line=dict(width=2, color='white')
                    ),
                    name=f"{self.indicator_names.get(indicator, indicator)} - Biến động mạnh",
                    showlegend=False,
                    hovertemplate="%{customdata}<extra></extra>",
                    customdata=significant_hover_texts
                ))
        
        # Danh sách các sự kiện lịch sử quan trọng với các tháng cụ thể và giai đoạn
        historical_events = [
            {
                'event': 'Gia nhập WTO',
                'month': '2007-01',
                'period_start': '2007-01',
                'period_end': '2007-06',
                'impact': 'Nhẹ',
                'color': '#E0E0E0',  # xám nhạt
                'description': 'Tháng 1/2007: Gia nhập WTO'
            },
            {
                'event': 'Khủng hoảng giá thực phẩm',
                'month': '2007-12',
                'period_start': '2007-12',
                'period_end': '2008-06',
                'impact': 'Trung bình',
                'color': '#B0B0B0',  # xám trung
                'description': 'Tháng 12/2007: Khủng hoảng giá thực phẩm'
            },
            {
                'event': 'Khủng hoảng tài chính',
                'month': '2008-06',
                'period_start': '2008-06',
                'period_end': '2009-12',
                'impact': 'Lớn',
                'color': '#808080',  # xám đậm
                'description': 'Tháng 6/2008: Khủng hoảng tài chính'
            },
            {
                'event': 'Phục hồi sau khủng hoảng',
                'month': '2010-06',
                'period_start': '2010-01',
                'period_end': '2010-12',
                'impact': 'Nhẹ',
                'color': '#E0E0E0',  # xám nhạt
                'description': 'Tháng 6/2010: Phục hồi sau khủng hoảng'
            },
            {
                'event': 'Lạm phát cao',
                'month': '2011-06',
                'period_start': '2011-01',
                'period_end': '2011-12',
                'impact': 'Lớn',
                'color': '#808080',  # xám đậm
                'description': 'Tháng 6/2011: Lạm phát cao'
            },
            {
                'event': 'Giá gạo tăng',
                'month': '2018-08',
                'period_start': '2018-08',
                'period_end': '2018-12',
                'impact': 'Trung bình',
                'color': '#B0B0B0',  # xám trung
                'description': 'Tháng 8/2018: Giá gạo tăng'
            },
            {
                'event': 'Đại dịch COVID-19',
                'month': '2020-01',
                'period_start': '2020-01',
                'period_end': '2021-12',
                'impact': 'Lớn',
                'color': '#808080',  # xám đậm
                'description': 'Tháng 1/2020: Đại dịch COVID-19'
            },
            {
                'event': 'Xung đột Nga-Ukraine',
                'month': '2022-03',
                'period_start': '2022-03',
                'period_end': '2022-12',
                'impact': 'Trung bình',
                'color': '#B0B0B0',  # xám trung
                'description': 'Tháng 3/2022: Xung đột Nga-Ukraine'
            }
        ]
        
        # Thêm vùng màu xám cho các giai đoạn lịch sử
        for event in historical_events:
            if event['period_start'] in df['Time'].values and event['period_end'] in df['Time'].values:
                fig.add_vrect(
                    x0=event['period_start'],
                    x1=event['period_end'],
                    fillcolor=event['color'],
                    opacity=0.3,
                    layer="below",
                    line_width=0
                )
        
        # Tính toán vị trí Y cho các nhãn để tránh chồng lên nhau
        y_positions = {}
        base_y_positions = [1.15, 1.20, 1.25, 1.30]  # Các vị trí y cơ bản cho nhãn
        
        for i, event in enumerate(historical_events):
            if event['month'] in df['Time'].values:
                # Tính toán chỉ số tháng để xác định vị trí Y
                month_index = list(df['Time'].values).index(event['month'])
                position_idx = month_index % len(base_y_positions)
                y_positions[event['month']] = base_y_positions[position_idx]
                
                # Tìm giá trị Y thực tế cho vị trí nhãn
                data_y = None
                for indicator in indicators:
                    if indicator in df.columns:
                        data_y = df.loc[df['Time'] == event['month'], indicator].values[0]
                        break
                
                # Thêm nhãn văn bản cho sự kiện tại tháng cụ thể
                fig.add_annotation(
                    x=event['month'],
                    y=data_y if data_y is not None else 0,
                    yref='y',
                    text=event['description'],
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="#636363",
                    ax=0,
                    ay=-40,
                    font=dict(size=10, color='#333333', family='Arial, sans-serif'),
                    bgcolor='rgba(255, 255, 255, 0.8)',
                    bordercolor='#c7c7c7',
                    borderwidth=1,
                    borderpad=4,
                    standoff=2
                )
        
        # Thêm chú thích về màu sắc
        fig.add_annotation(
            x=1,
            y=-0.15,
            xref='paper',
            yref='paper',
            text='<b>Mức độ ảnh hưởng:</b> ' + 
                 '<span style="background-color:#E0E0E0;padding:2px 5px;margin:0 3px;">Nhẹ</span> ' +
                 '<span style="background-color:#B0B0B0;padding:2px 5px;margin:0 3px;">Trung bình</span> ' +
                 '<span style="background-color:#808080;color:white;padding:2px 5px;margin:0 3px;">Lớn</span>',
            showarrow=False,
            font=dict(size=10, color='#333333'),
            align='right',
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='#c7c7c7',
            borderwidth=1,
            borderpad=4
        )
        
        # Áp dụng theme chung
        fig = self.apply_theme_to_figure(fig)
        
        return fig

    def create_correlation_heatmap(self, indicators):
        """Create correlation heatmap for selected indicators"""
        if len(indicators) < 2:
            return None

        corr_matrix = self.data_handler.create_correlation_data(indicators)
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            x=[self.indicator_names.get(i, i) for i in indicators],
            y=[self.indicator_names.get(i, i) for i in indicators],
            colorscale='RdBu',
            zmin=-1, zmax=1,
            hoverongaps=False,
            hovertemplate='Correlation: %{z:.2f}<extra></extra>'
        ))

        fig.update_layout(
            title="Ma trận tương quan giữa các chỉ số",
            template="plotly_white"
        )
        return fig

    def create_seasonal_chart(self, indicator):
        """Create seasonal chart with enhanced hover information"""
        if not indicator:
            return None
        
        # Sử dụng filter_data thay vì get_indicator_data
        df = self.data_handler.filter_data(indicators=[indicator])
        
        # Tạo cột tháng để nhóm
        monthly_avg = df.groupby(df['Month'])[indicator].mean()
        monthly_std = df.groupby(df['Month'])[indicator].std()
        
        # Lấy thông tin giải thích
        explanation = self.get_indicator_explanation(indicator)
        
        hover_texts = [
            f"<b>Tháng {month}</b><br>" +
            f"Giá trị trung bình: {avg:.2f}<br>" +
            f"Độ lệch chuẩn: {std:.2f}<br>" +
            f"<b>Nhận định:</b> " + (
                "Cao điểm theo mùa" if avg > monthly_avg.mean() + monthly_std.mean() else
                "Thấp điểm theo mùa" if avg < monthly_avg.mean() - monthly_std.mean() else
                "Bình thường theo mùa"
            ) + f"<br><br><i>{explanation.get('interpretation', '')}</i>"
            for month, avg, std in zip(range(1, 13), monthly_avg, monthly_std)
        ]
        
        fig = go.Figure()
        
        # Thêm đường cho giá trị trung bình
        fig.add_trace(go.Scatter(
            x=list(range(1, 13)),
            y=monthly_avg,
            mode='lines+markers',
            line=dict(
                width=3,
                color=self.color_scheme.get(indicator, '#3b82f6')
            ),
            marker=dict(
                size=10,
                color=self.color_scheme.get(indicator, '#3b82f6'),
                line=dict(width=2, color='white')
            ),
            name=f"{self.indicator_names.get(indicator, indicator)} (trung bình)",
            hovertemplate="%{customdata}<extra></extra>",
            customdata=hover_texts
        ))
        
        # Thêm vùng độ lệch chuẩn
        fig.add_trace(go.Scatter(
            x=list(range(1, 13)),
            y=monthly_avg + monthly_std,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=list(range(1, 13)),
            y=monthly_avg - monthly_std,
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(59, 130, 246, 0.2)',
            name='Độ lệch chuẩn',
            hoverinfo='skip'
        ))
        
        # Thêm đánh dấu cho các tháng cao điểm/thấp điểm
        high_months = [month for month in range(1, 13) 
                       if monthly_avg.iloc[month-1] > monthly_avg.mean() + monthly_std.mean()]
        
        low_months = [month for month in range(1, 13) 
                      if monthly_avg.iloc[month-1] < monthly_avg.mean() - monthly_std.mean()]
        
        if high_months:
            fig.add_trace(go.Scatter(
                x=high_months,
                y=[monthly_avg.iloc[month-1] for month in high_months],
                mode='markers',
                marker=dict(
                    symbol='star',
                    size=12,
                    color='#dc2626',
                    line=dict(width=1, color='white')
                ),
                name='Cao điểm theo mùa',
                hoverinfo='skip'
            ))
        
        if low_months:
            fig.add_trace(go.Scatter(
                x=low_months,
                y=[monthly_avg.iloc[month-1] for month in low_months],
                mode='markers',
                marker=dict(
                    symbol='star',
                    size=12,
                    color='#0369a1',
                    line=dict(width=1, color='white')
                ),
                name='Thấp điểm theo mùa',
                hoverinfo='skip'
            ))
        
        # Cập nhật layout
        fig.update_layout(
            title=dict(
                text=f"Biến động theo mùa của {explanation.get('title', indicator)}",
                font=dict(size=20, color='#1e293b'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title="Tháng",
                tickmode='array',
                ticktext=['Th.'+str(i) for i in range(1, 13)],
                tickvals=list(range(1, 13)),
                gridcolor='#e2e8f0',
                zeroline=False,
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title=f"Giá trị trung bình của {explanation.get('title', indicator)}",
                gridcolor='#e2e8f0',
                zeroline=True,
                zerolinecolor='#94a3b8',
                zerolinewidth=1,
                tickfont=dict(size=12)
            ),
            hoverlabel=self.hover_style,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=12)
            ),
            margin=dict(t=80, l=60, r=40, b=60),
            annotations=[
                dict(
                    x=1,
                    y=-0.15,
                    xref='paper',
                    yref='paper',
                    text='*Biểu đồ thể hiện giá trị trung bình theo tháng, vùng xám là độ lệch chuẩn',
                    showarrow=False,
                    font=dict(size=10, color='#64748b'),
                    align='right'
                )
            ]
        )
        
        return fig

    def create_trend_chart(self, indicator):
        """Create trend analysis chart for an indicator"""
        if not indicator:
            return None
        
        # Lấy dữ liệu sử dụng filter_data
        df = self.data_handler.filter_data(indicators=[indicator])
        df['Time'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)
        
        # Tính toán xu hướng dài hạn sử dụng trung bình động 12 tháng
        df[f'{indicator}_MA12'] = df[indicator].rolling(window=12, min_periods=1).mean()
        
        # Tính phần trăm thay đổi để xác định xu hướng
        df[f'{indicator}_pct_change'] = df[indicator].pct_change(periods=12) * 100
        
        # Lấy thông tin giải thích
        explanation = self.get_indicator_explanation(indicator)
        
        fig = go.Figure()
        
        # Thêm đường cho giá trị thực tế
        fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df[indicator],
            mode='lines',
            name=f"{explanation.get('title', indicator)} (Thực tế)",
            line=dict(color=self.color_scheme.get(indicator, '#3b82f6'), width=2)
        ))
        
        # Thêm đường cho xu hướng dài hạn (trung bình động)
        fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df[f'{indicator}_MA12'],
            mode='lines',
            name='Xu hướng dài hạn (MA-12)',
            line=dict(color='#ef4444', width=2, dash='dash')
        ))
        
        # Thêm vùng màu cho xu hướng tăng/giảm
        for i in range(1, len(df) - 1):
            if df[f'{indicator}_pct_change'].iloc[i] > 0:
                fig.add_vrect(
                    x0=df['Time'].iloc[i],
                    x1=df['Time'].iloc[i+1],
                    fillcolor='rgba(74, 222, 128, 0.2)',
                    layer='below',
                    line_width=0
                )
            elif df[f'{indicator}_pct_change'].iloc[i] < 0:
                fig.add_vrect(
                    x0=df['Time'].iloc[i],
                    x1=df['Time'].iloc[i+1],
                    fillcolor='rgba(248, 113, 113, 0.2)',
                    layer='below',
                    line_width=0
                )
        
        # Cập nhật layout
        fig.update_layout(
            title=dict(
                text=f"Phân tích xu hướng dài hạn của {explanation.get('title', indicator)}",
                font=dict(size=20, color='#1e293b'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title='Thời gian',
                gridcolor='#e2e8f0',
                tickangle=-45,
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title=f"Giá trị của {explanation.get('title', indicator)}",
                gridcolor='#e2e8f0',
                zeroline=True,
                zerolinecolor='#94a3b8',
                zerolinewidth=1,
                tickfont=dict(size=12)
            ),
            hoverlabel=self.hover_style,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=12)
            ),
            margin=dict(t=80, l=60, r=40, b=60),
            annotations=[
                dict(
                    x=1, 
                    y=-0.15,
                    xref='paper',
                    yref='paper',
                    text='*Vùng màu xanh: xu hướng tăng | Vùng màu đỏ: xu hướng giảm',
                    showarrow=False,
                    font=dict(size=10, color='#64748b'),
                    align='right'
                )
            ]
        )
        
        return fig

    def get_indicator_explanation(self, indicator):
        """Get detailed explanation for an indicator"""
        explanations = {
            'Core_Inflation': {
                'title': 'Lạm phát cơ bản',
                'description': 'Chỉ số giá tiêu dùng không bao gồm giá thực phẩm và năng lượng, phản ánh xu hướng lạm phát dài hạn.',
                'impact': 'Ảnh hưởng trực tiếp đến chính sách tiền tệ và lãi suất của ngân hàng trung ương.',
                'interpretation': 'Giá trị dương cho thấy áp lực lạm phát tăng, giá trị âm thể hiện xu hướng giảm phát.',
                'threshold': {
                    'high': '> 2%: Cần theo dõi chặt chẽ',
                    'medium': '1-2%: Mức ổn định',
                    'low': '< 1%: Áp lực lạm phát thấp'
                }
            },
            'Core_Inlation': {
                'title': 'Lạm phát cơ bản',
                'description': 'Chỉ số giá tiêu dùng không bao gồm giá thực phẩm và năng lượng, phản ánh xu hướng lạm phát dài hạn.',
                'impact': 'Ảnh hưởng trực tiếp đến chính sách tiền tệ và lãi suất của ngân hàng trung ương.',
                'interpretation': 'Giá trị dương cho thấy áp lực lạm phát tăng, giá trị âm thể hiện xu hướng giảm phát.',
                'threshold': {
                    'high': '> 2%: Cần theo dõi chặt chẽ',
                    'medium': '1-2%: Mức ổn định',
                    'low': '< 1%: Áp lực lạm phát thấp'
                }
            },
            'Food_Inflation': {
                'title': 'Lạm phát thực phẩm',
                'description': 'Biến động giá các mặt hàng thực phẩm, chiếm tỷ trọng lớn trong chi tiêu của người dân.',
                'impact': 'Ảnh hưởng trực tiếp đến đời sống người dân và chỉ số giá tiêu dùng tổng thể.',
                'interpretation': 'Thường có tính chu kỳ theo mùa vụ và chịu ảnh hưởng từ thời tiết, thiên tai.',
                'threshold': {
                    'high': '> 3%: Giá thực phẩm tăng mạnh',
                    'medium': '1-3%: Biến động bình thường',
                    'low': '< 1%: Giá thực phẩm ổn định'
                }
            },
            'USD_VND': {
                'title': 'Tỷ giá USD/VND',
                'description': 'Tỷ giá hối đoái giữa đồng Việt Nam và đô la Mỹ, phản ánh sức mạnh tương đối giữa hai đồng tiền.',
                'impact': 'Ảnh hưởng đến hoạt động xuất nhập khẩu, đầu tư nước ngoài và giá cả hàng hóa.',
                'interpretation': 'Tăng thể hiện VND mất giá, giảm thể hiện VND tăng giá so với USD.',
                'threshold': {
                    'high': '> 2% tháng: VND mất giá mạnh',
                    'medium': '0.5-2%: Biến động bình thường',
                    'low': '< 0.5%: Tỷ giá ổn định'
                }
            },
            'Brent': {
                'title': 'Giá dầu Brent',
                'description': 'Giá dầu thô Brent - một trong những chỉ số tham chiếu quan trọng của thị trường dầu mỏ thế giới.',
                'impact': 'Ảnh hưởng đến chi phí sản xuất, vận tải và giá nhiên liệu trong nước.',
                'interpretation': 'Biến động mạnh thường do căng thẳng địa chính trị hoặc thay đổi cung cầu toàn cầu.',
                'threshold': {
                    'high': '> 80 USD/thùng: Giá cao',
                    'medium': '50-80 USD/thùng: Mức cân bằng',
                    'low': '< 50 USD/thùng: Giá thấp'
                }
            },
            'Export': {
                'title': 'Kim ngạch xuất khẩu',
                'description': 'Tổng giá trị hàng hóa và dịch vụ xuất khẩu của Việt Nam.',
                'impact': 'Phản ánh năng lực cạnh tranh và khả năng tham gia chuỗi giá trị toàn cầu.',
                'interpretation': 'Tăng trưởng dương thể hiện cải thiện năng lực xuất khẩu.',
                'threshold': {
                    'high': '> 10% năm: Tăng trưởng mạnh',
                    'medium': '5-10%: Tăng trưởng ổn định',
                    'low': '< 5%: Tăng trưởng chậm'
                }
            },
            'Import': {
                'title': 'Kim ngạch nhập khẩu',
                'description': 'Tổng giá trị hàng hóa và dịch vụ nhập khẩu vào Việt Nam.',
                'impact': 'Phản ánh nhu cầu tiêu dùng và đầu tư trong nước.',
                'interpretation': 'Tăng có thể do đầu tư mở rộng sản xuất hoặc tiêu dùng tăng.',
                'threshold': {
                    'high': '> 12% năm: Nhu cầu cao',
                    'medium': '6-12%: Nhu cầu bình thường',
                    'low': '< 6%: Nhu cầu thấp'
                }
            },
            'VN_Trade_Balance': {
                'title': 'Cán cân thương mại',
                'description': 'Chênh lệch giữa giá trị xuất khẩu và nhập khẩu.',
                'impact': 'Ảnh hưởng đến tỷ giá hối đoái và dự trữ ngoại hối.',
                'interpretation': 'Dương là thặng dư, âm là thâm hụt thương mại.',
                'threshold': {
                    'high': '> 1 tỷ USD: Thặng dư lớn',
                    'medium': '-1 đến 1 tỷ USD: Cân bằng',
                    'low': '< -1 tỷ USD: Thâm hụt lớn'
                }
            },
            'Gold': {
                'title': 'Giá vàng',
                'description': 'Giá vàng thế giới được giao dịch trên thị trường quốc tế, thường tính bằng USD/ounce.',
                'impact': 'Là tài sản trú ẩn an toàn, ảnh hưởng đến thị trường tài chính và lạm phát kỳ vọng.',
                'interpretation': 'Tăng khi có bất ổn kinh tế/chính trị, giảm khi kinh tế phát triển ổn định.',
                'threshold': {
                    'high': '> 1800 USD/ounce: Giá cao',
                    'medium': '1500-1800 USD/ounce: Mức bình thường',
                    'low': '< 1500 USD/ounce: Giá thấp'
                }
            },
            'VN_Gasoline_Prices': {
                'title': 'Giá xăng dầu Việt Nam',
                'description': 'Giá bán lẻ xăng dầu trong nước, phản ánh biến động giá năng lượng toàn cầu và chính sách quản lý giá.',
                'impact': 'Ảnh hưởng trực tiếp đến chi phí sản xuất, vận tải và lạm phát.',
                'interpretation': 'Biến động theo giá dầu thế giới nhưng có độ trễ và mức độ thay đổi khác nhau do quỹ bình ổn giá.',
                'threshold': {
                    'high': '> 25.000 VND/lít: Giá cao',
                    'medium': '20.000-25.000 VND/lít: Mức bình thường',
                    'low': '< 20.000 VND/lít: Giá thấp'
                }
            },
            'VN_rice_price': {
                'title': 'Giá gạo Việt Nam',
                'description': 'Giá gạo xuất khẩu của Việt Nam, thường tính bằng USD/tấn.',
                'impact': 'Ảnh hưởng đến thu nhập nông dân, an ninh lương thực và cán cân thương mại.',
                'interpretation': 'Biến động theo mùa vụ, chính sách xuất khẩu và nhu cầu thị trường quốc tế.',
                'threshold': {
                    'high': '> 500 USD/tấn: Giá cao',
                    'medium': '400-500 USD/tấn: Mức bình thường',
                    'low': '< 400 USD/tấn: Giá thấp'
                }
            },
            'VN_coffee,tea,mate,spices': {
                'title': 'Xuất khẩu cà phê, chè và gia vị',
                'description': 'Giá trị xuất khẩu các mặt hàng cà phê, chè, mate và gia vị của Việt Nam.',
                'impact': 'Đóng góp vào kim ngạch xuất khẩu và thu nhập của nông dân vùng sản xuất.',
                'interpretation': 'Biến động theo mùa vụ và nhu cầu thị trường quốc tế.',
                'threshold': {
                    'high': '> 15% tăng trưởng năm: Rất tốt',
                    'medium': '5-15% tăng trưởng năm: Bình thường',
                    'low': '< 5% tăng trưởng năm: Thấp'
                }
            },
            'MonthlyCPI': {
                'title': 'Chỉ số giá tiêu dùng hàng tháng',
                'description': 'Chỉ số đo lường sự thay đổi về giá của một rổ hàng hóa và dịch vụ tiêu dùng phổ biến theo tháng.',
                'impact': 'Là chỉ số chính để đánh giá lạm phát và điều chỉnh chính sách tiền tệ.',
                'interpretation': 'Tăng liên tục cho thấy áp lực lạm phát, giảm có thể báo hiệu suy thoái.',
                'threshold': {
                    'high': '> 0.5% tháng: Lạm phát cao',
                    'medium': '0.2-0.5% tháng: Lạm phát vừa phải',
                    'low': '< 0.2% tháng: Lạm phát thấp'
                }
            },
            'China_CPI': {
                'title': 'Chỉ số giá tiêu dùng Trung Quốc',
                'description': 'Chỉ số giá tiêu dùng của Trung Quốc, đo lường mức độ lạm phát tại thị trường lớn nhất khu vực.',
                'impact': 'Ảnh hưởng đến giá hàng hóa xuất nhập khẩu và chuỗi cung ứng toàn cầu.',
                'interpretation': 'Biến động giá tại Trung Quốc thường có tác động lan tỏa đến Việt Nam.',
                'threshold': {
                    'high': '> 3% năm: Lạm phát cao',
                    'medium': '1-3% năm: Lạm phát vừa phải',
                    'low': '< 1% năm: Lạm phát thấp'
                }
            },
            'Industrial_products': {
                'title': 'Sản xuất công nghiệp',
                'description': 'Chỉ số sản xuất công nghiệp, phản ánh tăng trưởng trong lĩnh vực sản xuất và chế tạo.',
                'impact': 'Ảnh hưởng trực tiếp đến tăng trưởng GDP và việc làm trong ngành công nghiệp.',
                'interpretation': 'Tăng thể hiện hoạt động sản xuất mạnh mẽ, giảm báo hiệu suy giảm kinh tế.',
                'threshold': {
                    'high': '> 8% năm: Tăng trưởng mạnh',
                    'medium': '4-8% năm: Tăng trưởng ổn định',
                    'low': '< 4% năm: Tăng trưởng yếu'
                }
            },
            'Agriculture, Forestry and Fishing': {
                'title': 'Nông, lâm nghiệp và thủy sản',
                'description': 'Chỉ số tăng trưởng của ngành nông, lâm nghiệp và thủy sản, phản ánh sản lượng trong lĩnh vực này.',
                'impact': 'Ảnh hưởng đến an ninh lương thực, đời sống nông dân và xuất khẩu nông sản.',
                'interpretation': 'Có tính chu kỳ theo mùa vụ và chịu ảnh hưởng lớn từ điều kiện thời tiết.',
                'threshold': {
                    'high': '> 4% năm: Tăng trưởng tốt',
                    'medium': '2-4% năm: Tăng trưởng ổn định',
                    'low': '< 2% năm: Tăng trưởng thấp'
                }
            },
            'Unemployment Rate': {
                'title': 'Tỷ lệ thất nghiệp',
                'description': 'Phần trăm lực lượng lao động không có việc làm nhưng đang tích cực tìm kiếm việc làm.',
                'impact': 'Phản ánh sức khỏe của thị trường lao động và tình hình kinh tế.',
                'interpretation': 'Tăng trong thời gian dài báo hiệu suy thoái kinh tế, giảm thể hiện phục hồi.',
                'threshold': {
                    'high': '> 3% (Việt Nam): Thất nghiệp cao',
                    'medium': '2-3%: Mức bình thường',
                    'low': '< 2%: Thất nghiệp thấp'
                }
            },
            'VN_fiscal_deficit': {
                'title': 'Thâm hụt ngân sách',
                'description': 'Chênh lệch giữa chi tiêu công và thu ngân sách của chính phủ.',
                'impact': 'Ảnh hưởng đến nợ công, áp lực lạm phát và tỷ giá hối đoái.',
                'interpretation': 'Thâm hụt cao có thể kích thích tăng trưởng ngắn hạn nhưng gây áp lực dài hạn.',
                'threshold': {
                    'high': '> 5% GDP: Thâm hụt cao',
                    'medium': '3-5% GDP: Mức bình thường',
                    'low': '< 3% GDP: Thâm hụt thấp'
                }
            },
            'VN_Interest_Rate': {
                'title': 'Lãi suất chính sách',
                'description': 'Lãi suất cơ bản do Ngân hàng Nhà nước Việt Nam điều hành.',
                'impact': 'Ảnh hưởng đến chi phí vay vốn, đầu tư và tiết kiệm trong nền kinh tế.',
                'interpretation': 'Tăng thường nhằm kiểm soát lạm phát, giảm để kích thích tăng trưởng.',
                'threshold': {
                    'high': '> 6%: Lãi suất cao',
                    'medium': '4-6%: Mức bình thường',
                    'low': '< 4%: Lãi suất thấp'
                }
            },
            'VN_money_supply': {
                'title': 'Cung tiền M2',
                'description': 'Tổng lượng tiền trong lưu thông và tiền gửi không kỳ hạn, tiền gửi có kỳ hạn ngắn.',
                'impact': 'Ảnh hưởng đến lạm phát, tăng trưởng tín dụng và hoạt động kinh tế.',
                'interpretation': 'Tăng nhanh có thể gây lạm phát, tăng chậm có thể hạn chế tăng trưởng.',
                'threshold': {
                    'high': '> 15% năm: Tăng trưởng nhanh',
                    'medium': '10-15% năm: Mức bình thường',
                    'low': '< 10% năm: Tăng trưởng chậm'
                }
            },
            'PC1': {
                'title': 'Thành phần chính 1',
                'description': 'Thành phần chính đầu tiên từ phân tích PCA, tổng hợp biến động của nhiều chỉ số kinh tế.',
                'impact': 'Cung cấp cái nhìn tổng quan về xu hướng chung của nền kinh tế.',
                'interpretation': 'Giá trị dương thường thể hiện sự mở rộng, giá trị âm báo hiệu thu hẹp kinh tế.',
                'threshold': {
                    'high': '> 1: Tăng trưởng mạnh',
                    'medium': '-1 đến 1: Mức bình thường',
                    'low': '< -1: Suy giảm'
                }
            }
        }
        
        return explanations.get(indicator, {
            'title': self.indicator_names.get(indicator, indicator),
            'description': 'Chỉ số kinh tế quan trọng cần theo dõi.',
            'impact': 'Có ảnh hưởng đến các quyết định chính sách và hoạt động kinh tế.',
            'interpretation': 'Cần phân tích trong bối cảnh tổng thể của nền kinh tế.',
            'threshold': {
                'high': 'Giá trị cao hơn bình thường',
                'medium': 'Giá trị trong khoảng bình thường',
                'low': 'Giá trị thấp hơn bình thường'
            }
        })

    def get_correlation_explanation(self, indicator1, indicator2, correlation):
        """Get explanation for correlation between two indicators"""
        if correlation > 0.7:
            strength = "mạnh tích cực"
            interpretation = "có xu hướng tăng/giảm cùng chiều"
        elif correlation > 0.3:
            strength = "trung bình tích cực"
            interpretation = "thường tăng/giảm cùng chiều"
        elif correlation > -0.3:
            strength = "yếu"
            interpretation = "không có mối liên hệ rõ ràng"
        elif correlation > -0.7:
            strength = "trung bình tiêu cực"
            interpretation = "thường tăng/giảm ngược chiều"
        else:
            strength = "mạnh tiêu cực"
            interpretation = "có xu hướng tăng/giảm ngược chiều"

        return {
            'strength': strength,
            'interpretation': interpretation,
            'description': f"Mối tương quan {strength} ({correlation:.2f}) giữa {self.indicator_names.get(indicator1)} và {self.indicator_names.get(indicator2)} cho thấy hai chỉ số này {interpretation}."
        }

    def create_bar_chart(self, indicators):
        """Create bar chart for selected indicators"""
        if not indicators:
            return None

        df = self.data_handler.filter_data(indicators=indicators)
        df['Time'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)
        
        fig = go.Figure()
        
        # Xác định số lượng điểm dữ liệu để tự động điều chỉnh độ rộng của cột
        num_data_points = len(df)
        # Nếu có nhiều điểm dữ liệu, làm cho cột rộng hơn để dễ nhìn
        base_width = min(0.8, 20 / num_data_points) if num_data_points > 0 else 0.8
        bar_width = base_width / len(indicators) if len(indicators) > 0 else base_width
        
        # Màu sắc sống động và đối lập hơn
        vibrant_colors = ['#FF5733', '#33A8FF', '#33FF57', '#FF33A8', '#A833FF', '#FFCE33', '#33FFE0', '#E033FF']
        
        for i, indicator in enumerate(indicators):
            color_idx = i % len(vibrant_colors)
            fig.add_trace(go.Bar(
                x=df['Time'],
                y=df[indicator],
                name=self.indicator_names.get(indicator, indicator),
                marker=dict(
                    color=vibrant_colors[color_idx],
                    line=dict(color='black', width=1)  # Thêm đường viền đen để dễ nhìn trên nền
                ),
                width=bar_width,
                offset=bar_width * (i - len(indicators)/2 + 0.5),
                hovertemplate=f"<b>{self.indicator_names.get(indicator, indicator)}</b>: %{{y:.2f}}<br>Thời gian: %{{x}}<extra></extra>",
                opacity=0.9  # Độ mờ nhẹ để màu không quá chói
            ))

        # Tính toán chiều cao khung biểu đồ dựa trên số lượng chỉ số
        chart_height = max(600, 400 + 50 * len(indicators))
        
        # Giới hạn số lượng điểm trên trục x nếu có quá nhiều
        tickvals = df['Time'].iloc[::max(1, len(df) // 12)] if len(df) > 12 else df['Time']

        fig.update_layout(
            title=dict(
                text=f"So sánh giá trị {', '.join([self.indicator_names.get(ind, ind) for ind in indicators])} theo thời gian",
                font=dict(size=20, color='#1e293b'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title="Thời gian",
                tickangle=-45,
                tickmode='array',
                tickvals=tickvals,
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                title="Giá trị",
                gridcolor='rgba(230, 230, 230, 0.8)'  # Lưới nhạt hơn để cột nổi bật
            ),
            barmode='group',
            template="plotly_white",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            plot_bgcolor='white',  # Nền trắng thay vì xám
            height=chart_height,
            margin=dict(l=80, r=80, t=100, b=100)
        )
        
        # Thêm đường lưới ngang để dễ đọc giá trị
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200, 200, 200, 0.3)')
        
        return fig

    def create_scatter_plot(self, indicators):
        """Create scatter plot with enhanced visualization"""
        if len(indicators) != 2:
            return None
        
        indicator1, indicator2 = indicators
        df = self.data_handler.filter_data(indicators=indicators)
        df['Time'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)
        
        # Lấy thông tin giải thích
        explanation1 = self.get_indicator_explanation(indicator1)
        explanation2 = self.get_indicator_explanation(indicator2)
        
        # Tạo layout chung
        layout = self.create_common_layout(
            title=f"Mối quan hệ giữa {explanation1.get('title', indicator1)} và {explanation2.get('title', indicator2)}",
            xaxis_title=explanation1.get('title', indicator1),
            yaxis_title=explanation2.get('title', indicator2)
        )
        
        # Khởi tạo figure với layout
        fig = go.Figure(layout=layout)
        
        # Tính hệ số tương quan
        correlation = df[indicator1].corr(df[indicator2])
        correlation_text = f"Hệ số tương quan: {correlation:.2f}"
        
        # Màu sắc theo thời gian
        color_scale = px.colors.sequential.Viridis
        
        hover_texts = []
        for i, row in df.iterrows():
            hover_text = (
                f"<b>Thời điểm:</b> {row['Time']}<br>" +
                f"<b>{explanation1.get('title', indicator1)}:</b> {row[indicator1]:.2f}<br>" +
                f"<b>{explanation2.get('title', indicator2)}:</b> {row[indicator2]:.2f}<br>" +
                f"<b>Mối quan hệ:</b> Khi {explanation1.get('title', indicator1)} tăng, {explanation2.get('title', indicator2)} {'cũng tăng' if correlation > 0 else 'giảm'}"
            )
            hover_texts.append(hover_text)
        
        # Thêm scatter plot
        fig.add_trace(go.Scatter(
            x=df[indicator1],
            y=df[indicator2],
            mode='markers',
            marker=dict(
                size=10,
                color=df['Year'],
                colorscale=color_scale,
                opacity=0.8,
                line=dict(width=1, color='white'),
                showscale=True,
                colorbar=dict(title="Năm")
            ),
            text=df['Time'],
            hovertemplate="%{customdata}<extra></extra>",
            customdata=hover_texts,
            name='Dữ liệu'
        ))
        
        # Thêm đường xu hướng nếu có tương quan đáng kể
        if abs(correlation) > 0.3:
            z = np.polyfit(df[indicator1], df[indicator2], 1)
            x_range = np.linspace(df[indicator1].min(), df[indicator1].max(), 100)
            y_range = z[0] * x_range + z[1]
            
            fig.add_trace(go.Scatter(
                x=x_range,
                y=y_range,
                mode='lines',
                line=dict(
                    color='rgba(255, 0, 0, 0.5)' if correlation < 0 else 'rgba(0, 128, 0, 0.5)',
                    width=2,
                    dash='dash'
                ),
                name=f'Xu hướng ({correlation:.2f})',
                hoverinfo='skip'
            ))
        
        # Áp dụng theme chung
        fig = self.apply_theme_to_figure(fig)
        
        return fig

    def create_calendar_heatmap(self, indicator):
        """Create calendar heatmap with enhanced annotations"""
        if not indicator:
            return None
        
        # Get data using filter_data
        df = self.data_handler.filter_data(indicators=[indicator])
        df['Time'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)
        
        # Get unique years and limit to last 10 years if too many
        years = sorted(df['Year'].unique())
        if len(years) > 10:
            years = years[-10:]  # Take only the last 10 years
        
        # Calculate vertical spacing based on number of years
        vertical_spacing = min(0.03, 1.0 / (len(years) + 1))
        
        # Create subplots
        fig = make_subplots(
            rows=len(years),
            cols=1,
            subplot_titles=[f'Năm {year}' for year in years],
            vertical_spacing=vertical_spacing
        )
        
        # Calculate overall min and max for consistent color scale
        vmin, vmax = df[indicator].min(), df[indicator].max()
        
        # Get indicator explanation
        explanation = self.get_indicator_explanation(indicator)
        
        for i, year in enumerate(years, 1):
            year_data = df[df['Year'] == year]
            
            # Create month labels and values
            months = list(range(1, 13))
            values = []
            hover_texts = []
            
            for month in months:
                month_data = year_data[year_data['Month'] == month]
                if not month_data.empty:
                    value = month_data[indicator].iloc[0]
                    values.append(value)
                    
                    # Create detailed hover text
                    date_key = f'{year}-{month:02d}'
                    hover_text = self.get_hover_template(date_key, indicator, value)
                    
                    # Add historical context if available
                    annotation = self.historical_annotations.get(date_key, {})
                    if annotation:
                        hover_text += f"<br><br><b>Sự kiện:</b> {annotation['event']}"
                        hover_text += f"<br><b>Tác động:</b> {annotation['impact']}"
                        hover_text += f"<br><b>Bối cảnh:</b> {annotation['context']}"
                    
                    hover_texts.append(hover_text)
                else:
                    values.append(None)
                    hover_texts.append("Không có dữ liệu")
            
            # Add heatmap trace
            fig.add_trace(
                go.Heatmap(
                    x=months,
                    y=[year],
                    z=[values],
                    colorscale='RdBu_r',
                    zmin=vmin,
                    zmax=vmax,
                    showscale=True if i == 1 else False,
                    hoverongaps=False,
                    text=[hover_texts],
                    hovertemplate="%{text}<extra></extra>"
                ),
                row=i,
                col=1
            )
            
            # Add markers for significant events
            for month in months:
                date_key = f'{year}-{month:02d}'
                if date_key in self.historical_annotations:
                    fig.add_trace(
                        go.Scatter(
                            x=[month],
                            y=[year],
                            mode='markers',
                            marker=dict(
                                symbol='star',
                                size=8,
                                color='black',
                                line=dict(width=1, color='white')
                            ),
                            showlegend=False,
                            hoverinfo='skip'
                        ),
                        row=i,
                        col=1
                    )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=f"Biến động theo tháng và năm của {explanation['title']}",
                font=dict(size=20, color='#1e293b'),
                x=0.5,
                xanchor='center'
            ),
            height=100 * len(years) + 150,
            showlegend=False,
            hoverlabel=self.hover_style
        )
        
        # Update all xaxes
        for i in range(len(years)):
            fig.update_xaxes(
                ticktext=['Th.' + str(i) for i in range(1, 13)],
                tickvals=list(range(1, 13)),
                gridcolor='#e2e8f0',
                row=i+1,
                col=1
            )
        
        # Add year labels
        for i in range(len(years)):
            fig.update_yaxes(
                ticktext=[str(years[i])],
                tickvals=[years[i]],
                gridcolor='#e2e8f0',
                row=i+1,
                col=1
            )
        
        # Add colorbar title
        fig.update_layout(
            coloraxis_colorbar=dict(
                title=dict(
                    text="Giá trị",
                    side="right"
                )
            )
        )
        
        return fig

    def create_sankey_chart(self, indicators, time_points=None):
        """Create Sankey diagram showing flow between time points"""
        if len(indicators) < 1:
            return None
            
        df = self.data_handler.filter_data(indicators=indicators)
        if time_points is None:
            # Select 4 evenly spaced time points
            time_points = list(range(0, len(df), len(df)//3))[:4]
        
        # Prepare nodes and links
        nodes = []
        links = []
        node_index = 0
        
        # Ensure all indicators have colors
        indicator_colors = {}
        for idx, indicator in enumerate(indicators):
            indicator_colors[indicator] = self.color_scheme.get(indicator, self.fallback_colors[idx % len(self.fallback_colors)])
        
        for t in range(len(time_points)-1):
            start_idx = time_points[t]
            end_idx = time_points[t+1]
            
            # Add nodes for current time point
            for indicator in indicators:
                nodes.append(dict(
                    name=f"{self.indicator_names.get(indicator)}\n{df.iloc[start_idx]['Year']}-{df.iloc[start_idx]['Month']}",
                    color=indicator_colors[indicator]
                ))
                
                if t == len(time_points)-2:  # Add end nodes for last time point
                    nodes.append(dict(
                        name=f"{self.indicator_names.get(indicator)}\n{df.iloc[end_idx]['Year']}-{df.iloc[end_idx]['Month']}",
                        color=indicator_colors[indicator]
                    ))
                
                # Add links with valid colors
                if t < len(time_points)-2:
                    start_val = df.iloc[start_idx][indicator]
                    end_val = df.iloc[end_idx][indicator]
                    links.append(dict(
                        source=node_index,
                        target=node_index + len(indicators),
                        value=max(0.1, abs(end_val - start_val)),  # Ensure positive value
                        color=indicator_colors[indicator]
                    ))
                
                node_index += 1
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=[n['name'] for n in nodes],
                color=[n['color'] for n in nodes]
            ),
            link=dict(
                source=[l['source'] for l in links],
                target=[l['target'] for l in links],
                value=[l['value'] for l in links],
                color=[l['color'] for l in links]
            )
        )])

        fig.update_layout(
            title=dict(
                text="Dòng chảy giá trị theo thời gian",
                font=dict(size=20, color='#1e293b')
            ),
            font=dict(size=10),
            hoverlabel=self.hover_style,
            template="plotly_white",
            height=600,
            margin=dict(t=60, l=40, r=40, b=40)
        )
        
        return fig

    def create_pie_chart(self, indicators, time_point=None):
        """Create pie chart showing distribution at a specific time point"""
        if len(indicators) < 2:
            return None
            
        df = self.data_handler.filter_data(indicators=indicators)
        
        if time_point is None:
            # Use the latest time point by default
            time_point = len(df) - 1
            
        # Get data for the specified time point
        data = df.iloc[time_point]
        values = [data[ind] for ind in indicators]
        labels = [self.indicator_names.get(ind) for ind in indicators]
        colors = [self.color_scheme.get(ind) for ind in indicators]
        
        # Calculate percentiles for interpretation
        percentiles = {}
        for indicator in indicators:
            indicator_values = df[indicator]
            percentiles[indicator] = stats.percentileofscore(indicator_values, data[indicator])/100
            
        hover_text = [
            f"<b>{label}</b><br>" +
            f"<b>Giá trị:</b> {value:.2f}<br>" +
            f"<b>Tỷ trọng:</b> {value/sum(values)*100:.1f}%<br>" +
            f"<b>💡 Nhận định:</b> {self.get_value_interpretation(indicator, percentiles[indicator])}"
            for label, value, indicator in zip(labels, values, indicators)
        ]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=colors),
            textinfo='percent',
            hovertext=hover_text,
            hoverinfo='text'
        )])

        fig.update_layout(
            title=dict(
                text=f"Phân bố các chỉ số ({data['Year']}-{data['Month']})",
                font=dict(size=20, color='#1e293b')
            ),
            hoverlabel=self.hover_style,
            template="plotly_white",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=12)
            ),
            margin=dict(t=60, l=40, r=40, b=40)
        )
        
        return fig

    def get_chart_explanation(self, chart_type):
        """Get explanation for chart type"""
        explanations = {
            'Biểu đồ xu hướng': {
                'title': 'Biểu đồ xu hướng theo thời gian',
                'description': 'Hiển thị sự biến động của các chỉ số theo thời gian, giúp nhận diện xu hướng và chu kỳ.',
                'usage': 'Phù hợp để theo dõi xu hướng dài hạn và so sánh biến động giữa các chỉ số.',
                'reading_guide': [
                    'Độ dốc của đường biểu thị tốc độ thay đổi (càng dốc = thay đổi càng nhanh)',
                    'Điểm đỉnh và đáy giúp xác định các giai đoạn biến động mạnh',
                    'Đường càng dao động = độ biến động cao, đường ít dao động = ổn định',
                    'Dấu sao (★) đánh dấu những điểm biến động mạnh > 5% so với kỳ trước',
                    'Vùng nền màu thể hiện các giai đoạn lịch sử quan trọng ảnh hưởng đến chỉ số'
                ]
            },
            'Biểu đồ phân tán': {
                'title': 'Biểu đồ tương quan',
                'description': 'Thể hiện mối quan hệ giữa hai chỉ số, với màu sắc thể hiện thời gian.',
                'usage': 'Dùng để phân tích mối quan hệ và phát hiện các điểm bất thường.',
                'reading_guide': [
                    'Các điểm nằm dọc theo đường chéo từ dưới-trái lên trên-phải: tương quan dương (cùng tăng/giảm)',
                    'Các điểm nằm dọc theo đường chéo từ trên-trái xuống dưới-phải: tương quan âm (một tăng, một giảm)',
                    'Điểm nằm xa xu hướng chung: điểm bất thường, cần chú ý',
                    'Màu sắc cho biết thời gian, giúp theo dõi sự thay đổi của mối quan hệ theo thời gian',
                    'Sự phân tán của điểm cho biết độ mạnh của mối tương quan (càng gần = tương quan càng mạnh)'
                ]
            },
            'Bản đồ nhiệt thời gian': {
                'title': 'Bản đồ nhiệt theo tháng và năm',
                'description': 'Hiển thị cường độ của chỉ số theo màu sắc, phân chia theo tháng và năm.',
                'usage': 'Phù hợp để phân tích mẫu hình theo mùa và xu hướng dài hạn.',
                'reading_guide': [
                    'Màu đỏ thể hiện giá trị cao, màu xanh thể hiện giá trị thấp',
                    'Nhìn theo hàng ngang (mỗi năm): xác định chu kỳ theo mùa',
                    'Nhìn theo cột dọc (cùng tháng qua các năm): xác định xu hướng dài hạn',
                    'Dấu sao (★) đánh dấu các sự kiện lịch sử đặc biệt ảnh hưởng đến chỉ số',
                    'So sánh các ô cùng màu để tìm mẫu hình lặp lại theo mùa hoặc chu kỳ kinh tế'
                ]
            },
            'Biểu đồ mùa vụ': {
                'title': 'Biểu đồ biến động theo mùa',
                'description': 'Phân tích sự biến động của chỉ số theo từng tháng trong năm.',
                'usage': 'Xác định mẫu hình mùa vụ, tháng cao điểm và thấp điểm.',
                'reading_guide': [
                    'Đường chính thể hiện giá trị trung bình của chỉ số theo từng tháng',
                    'Vùng màu xám thể hiện độ biến thiên (độ lệch chuẩn) của giá trị',
                    'Dấu sao màu đỏ (★) đánh dấu tháng có giá trị cao bất thường (cao điểm theo mùa)',
                    'Dấu sao màu xanh (★) đánh dấu tháng có giá trị thấp bất thường (thấp điểm theo mùa)',
                    'Vùng có độ biến thiên rộng: chỉ số có độ dao động lớn trong tháng đó qua các năm'
                ]
            },
            'Ma trận tương quan': {
                'title': 'Ma trận tương quan giữa các chỉ số',
                'description': 'Hiển thị mức độ tương quan giữa tất cả các chỉ số được chọn.',
                'usage': 'Phù hợp để xác định nhanh mối liên hệ giữa nhiều chỉ số cùng lúc.',
                'reading_guide': [
                    'Màu xanh thể hiện tương quan dương (cùng tăng/giảm), màu đỏ thể hiện tương quan âm (một tăng, một giảm)',
                    'Độ đậm của màu thể hiện độ mạnh của tương quan (càng đậm = liên hệ càng mạnh)',
                    'Các ô theo đường chéo chính luôn có giá trị 1 (tương quan hoàn hảo với chính nó)',
                    'Hệ số gần 0 (màu nhạt): hai chỉ số ít hoặc không liên quan đến nhau',
                    'Hệ số gần 1 hoặc -1 (màu đậm): hai chỉ số có mối liên hệ chặt chẽ'
                ]
            },
            'Biểu đồ xu hướng chi tiết': {
                'title': 'Phân tích xu hướng của chỉ số',
                'description': 'Phân tích chi tiết xu hướng của chỉ số với đường trung bình di động.',
                'usage': 'Loại bỏ nhiễu ngắn hạn để xem xu hướng dài hạn rõ ràng hơn.',
                'reading_guide': [
                    'Đường màu chính thể hiện giá trị thực của chỉ số',
                    'Đường đứt khúc là đường trung bình di động (MA), làm mịn dao động ngắn hạn',
                    'Khi đường giá trị cắt lên trên đường MA: tín hiệu xu hướng tăng',
                    'Khi đường giá trị cắt xuống dưới đường MA: tín hiệu xu hướng giảm',
                    'Dấu chấm xanh/đỏ thể hiện điểm bắt đầu của xu hướng tăng/giảm'
                ]
            },
            'Biểu đồ cột': {
                'title': 'Biểu đồ cột so sánh các chỉ số',
                'description': 'So sánh giá trị của các chỉ số theo thời gian hoặc nhóm.',
                'usage': 'Phù hợp để so sánh giá trị rời rạc giữa các biến số khác nhau.',
                'reading_guide': [
                    'Chiều cao của cột thể hiện giá trị của chỉ số tại thời điểm đó',
                    'So sánh các cột cùng màu để thấy biến động của một chỉ số theo thời gian',
                    'So sánh các cột khác màu tại cùng thời điểm để so sánh các chỉ số với nhau',
                    'Những cột cao bất thường cho thấy các giai đoạn tăng trưởng mạnh hoặc suy giảm',
                    'Khoảng cách đều đặn giữa các cột liên tiếp thể hiện chu kỳ ổn định'
                ]
            },
            'Biểu đồ hộp': {
                'title': 'Biểu đồ hộp phân tích phân phối',
                'description': 'Hiển thị phân phối thống kê của các chỉ số kinh tế.',
                'usage': 'Phù hợp để phân tích độ biến động và phát hiện giá trị bất thường.',
                'reading_guide': [
                    'Đường ngang giữa hộp: giá trị trung vị (50% số quan sát)',
                    'Viền dưới và trên của hộp: tứ phân vị thứ nhất (25%) và thứ ba (75%)',
                    'Các "râu" kéo dài: phạm vi bình thường của dữ liệu (1.5 x khoảng tứ phân vị)',
                    'Điểm nằm ngoài "râu": giá trị bất thường (outliers), cần chú ý đặc biệt',
                    'Hộp càng cao: độ phân tán dữ liệu càng lớn, hộp thấp: dữ liệu tập trung'
                ]
            },
            'Biểu đồ histogram': {
                'title': 'Biểu đồ phân phối tần suất',
                'description': 'Hiển thị tần suất xuất hiện của các khoảng giá trị trong chỉ số.',
                'usage': 'Phù hợp để hiểu phân phối và mô hình thống kê của dữ liệu.',
                'reading_guide': [
                    'Trục X: các khoảng giá trị của chỉ số, trục Y: tần suất xuất hiện',
                    'Đỉnh của histogram: giá trị phổ biến nhất của chỉ số',
                    'Đường cong đỏ (KDE): ước tính phân phối xác suất liên tục của dữ liệu',
                    'Histogram lệch phải: nhiều giá trị cao bất thường, lệch trái: nhiều giá trị thấp bất thường',
                    'Histogram có nhiều đỉnh: dữ liệu có thể thuộc về nhiều chu kỳ hoặc thời kỳ khác nhau'
                ]
            },
            'Biểu đồ vùng': {
                'title': 'Biểu đồ vùng tích lũy',
                'description': 'Hiển thị xu hướng của các chỉ số theo thời gian với diện tích tô màu.',
                'usage': 'Phù hợp để theo dõi xu hướng và đóng góp tương đối của các thành phần.',
                'reading_guide': [
                    'Trục X: thời gian, trục Y: giá trị tích lũy của các chỉ số',
                    'Diện tích màu thể hiện giá trị hoặc tỷ trọng đóng góp của từng chỉ số',
                    'Vùng trên cùng thể hiện tổng giá trị của tất cả các chỉ số theo thời gian',
                    'Mở rộng vùng theo chiều dọc: đóng góp của chỉ số tăng lên',
                    'Thu hẹp vùng theo chiều dọc: đóng góp của chỉ số giảm xuống'
                ]
            },
            'Biểu đồ radar': {
                'title': 'Biểu đồ radar so sánh nhiều chỉ số',
                'description': 'Hiển thị giá trị chuẩn hóa của nhiều chỉ số trên các trục tỏa ra từ tâm.',
                'usage': 'Phù hợp để so sánh toàn diện nhiều chỉ số cùng lúc.',
                'reading_guide': [
                    'Mỗi trục tỏa ra từ tâm thể hiện một chỉ số riêng biệt',
                    'Giá trị gần tâm: thấp hơn, giá trị xa tâm: cao hơn (đã chuẩn hóa)',
                    'Diện tích của đa giác thể hiện mức độ tổng thể của tất cả các chỉ số',
                    'Biểu đồ cân đối (gần hình tròn): các chỉ số tương đối đồng đều',
                    'Biểu đồ không cân đối: một số chỉ số nổi trội hơn các chỉ số khác'
                ]
            },
            'Biểu đồ bong bóng': {
                'title': 'Biểu đồ bong bóng so sánh ba chiều',
                'description': 'Hiển thị mối quan hệ giữa ba chỉ số: X, Y và kích thước bong bóng.',
                'usage': 'Phù hợp để phân tích mối quan hệ phức tạp giữa ba biến.',
                'reading_guide': [
                    'Trục X và Y: hai chỉ số chính cần so sánh',
                    'Kích thước bong bóng: chỉ số thứ ba, càng lớn = giá trị càng cao',
                    'Màu sắc thể hiện thời gian, giúp theo dõi sự thay đổi theo thời gian',
                    'Đường chấm đỏ thể hiện xu hướng tương quan giữa hai chỉ số trên trục X và Y',
                    'Bong bóng di chuyển theo đường chéo: hai chỉ số X và Y có tương quan mạnh'
                ]
            },
            'Biểu đồ dòng chảy': {
                'title': 'Biểu đồ dòng chảy Sankey',
                'description': 'Hiển thị dòng chảy và mối quan hệ giữa các nhóm chỉ số.',
                'usage': 'Phù hợp để phân tích sự phân bổ và dòng chảy giữa các thành phần.',
                'reading_guide': [
                    'Độ rộng của mỗi dòng thể hiện lượng hoặc giá trị dòng chảy',
                    'Các nút thể hiện các nhóm hoặc thành phần chính',
                    'Màu sắc theo nút nguồn hoặc nút đích, giúp phân biệt các dòng chảy',
                    'Dòng càng rộng: đóng góp hoặc mối liên hệ càng mạnh',
                    'Di chuột qua mỗi dòng để xem chi tiết giá trị và mối liên hệ'
                ]
            },
            'Biểu đồ bánh': {
                'title': 'Biểu đồ tròn thể hiện tỷ lệ',
                'description': 'Hiển thị tỷ lệ đóng góp của từng chỉ số vào tổng thể.',
                'usage': 'Phù hợp để so sánh tỷ trọng của các thành phần trong một tổng thể.',
                'reading_guide': [
                    'Mỗi phần của bánh thể hiện tỷ lệ phần trăm của một chỉ số',
                    'Tổng của tất cả các phần luôn bằng 100%',
                    'Phần lớn nhất thể hiện chỉ số đóng góp nhiều nhất',
                    'Tránh sử dụng biểu đồ này khi có quá nhiều chỉ số (gây khó đọc)',
                    'Di chuột qua mỗi phần để xem chi tiết giá trị và phần trăm'
                ]
            }
        }
        
        return explanations.get(chart_type, None)

    def create_box_plot(self, indicators):
        """Create a box plot for the selected indicators

        Args:
            indicators (list): List of indicator names to visualize

        Returns:
            plotly.graph_objects.Figure: A box plot showing the distribution of each indicator
        """
        if not indicators or len(indicators) == 0:
            return None
        
        # Get data from data handler
        data = self.data_handler.data.copy()
        
        # Create figure
        fig = go.Figure()
        
        for indicator in indicators:
            # Skip if indicator not in data
            if indicator not in data.columns:
                continue
            
            # Get the visible name for the indicator
            indicator_name = self.indicator_names.get(indicator, indicator)
            
            # Add box plot for this indicator
            fig.add_trace(go.Box(
                y=data[indicator],
                name=indicator_name,
                marker_color=self.color_scheme.get(indicator, self.fallback_colors[0]),
                boxmean=True,  # Show mean and standard deviation
                boxpoints='suspectedoutliers'  # Only show outlier points
            ))
        
        # Update layout
        fig.update_layout(
            title="Phân phối của các chỉ số kinh tế",
            height=600,
            template="plotly_white",
            hoverlabel=self.hover_style,
            xaxis_title="Chỉ số",
            yaxis_title="Giá trị (chuẩn hóa)",
            legend_title="Chỉ số kinh tế",
            font=dict(family="Roboto, sans-serif", size=12),
            margin=dict(l=40, r=40, t=60, b=40),
        )
        
        return fig

    def create_histogram(self, indicator):
        """Create a histogram for the selected indicator
        
        Args:
            indicator (str): Indicator name to visualize
            
        Returns:
            plotly.graph_objects.Figure: A histogram showing the distribution of the indicator
        """
        if not indicator:
            return None
        
        # Get data from data handler
        data = self.data_handler.data.copy()
        
        # Skip if indicator not in data
        if indicator not in data.columns:
            return None
        
        # Get the visible name for the indicator
        indicator_name = self.indicator_names.get(indicator, indicator)
        
        # Create figure with histogram
        fig = go.Figure(data=[go.Histogram(
            x=data[indicator],
            marker_color=self.color_scheme.get(indicator, self.fallback_colors[0]),
            nbinsx=30,
            opacity=0.75,
            name=indicator_name,
            histnorm='probability'
        )])
        
        # Add KDE curve
        if len(data[indicator]) > 5:  # Need enough data points for KDE
            kde_x = np.linspace(data[indicator].min(), data[indicator].max(), 1000)
            kde = stats.gaussian_kde(data[indicator].dropna())
            kde_y = kde(kde_x)
            
            fig.add_trace(go.Scatter(
                x=kde_x,
                y=kde_y,
                mode='lines',
                name='Đường KDE',
                line=dict(color='red', width=2)
            ))
        
        # Update layout
        fig.update_layout(
            title=f"Phân phối của {indicator_name}",
            height=500,
            template="plotly_white",
            hoverlabel=self.hover_style,
            xaxis_title=indicator_name,
            yaxis_title="Tần suất",
            bargap=0.05,
            font=dict(family="Roboto, sans-serif", size=12),
            margin=dict(l=40, r=40, t=60, b=40),
        )
        
        return fig

    def create_area_chart(self, indicators):
        """Create an area chart for the selected indicators
        
        Args:
            indicators (list): List of indicator names to visualize
            
        Returns:
            plotly.graph_objects.Figure: An area chart showing the trend of each indicator
        """
        if not indicators or len(indicators) == 0:
            return None
        
        # Get data from data handler
        data = self.data_handler.data.copy()
        
        # Create date column for better x-axis display
        data['Date'] = data.apply(lambda row: f"{int(row['Year'])}-{int(row['Month']):02d}", axis=1)
        
        # Create figure
        fig = go.Figure()
        
        for i, indicator in enumerate(indicators):
            # Skip if indicator not in data
            if indicator not in data.columns:
                continue
            
            # Get the visible name for the indicator
            indicator_name = self.indicator_names.get(indicator, indicator)
            
            # Add area trace for this indicator
            fillcolor = self.color_scheme.get(indicator, self.fallback_colors[i % len(self.fallback_colors)])
            # Convert hex to RGB and add transparency
            r, g, b = tuple(int(fillcolor.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            fillcolor_rgba = f'rgba({r},{g},{b},0.5)'  # 50% transparency
            
            fig.add_trace(go.Scatter(
                x=data['Date'],
                y=data[indicator],
                mode='lines',
                name=indicator_name,
                fill='tozeroy' if i == 0 else 'tonexty',
                line=dict(width=0.5, color=fillcolor),
                fillcolor=fillcolor_rgba,  # Use rgba for transparency
                stackgroup='one'  # For stacked area chart
            ))
        
        # Update layout
        fig.update_layout(
            title="Biểu đồ vùng của các chỉ số kinh tế",
            height=600,
            template="plotly_white",
            hoverlabel=self.hover_style,
            xaxis_title="Thời gian",
            yaxis_title="Giá trị (chuẩn hóa)",
            legend_title="Chỉ số kinh tế",
            font=dict(family="Roboto, sans-serif", size=12),
            margin=dict(l=40, r=40, t=60, b=40),
        )
        
        # Add important historical events as annotations
        for date, event_info in self.historical_annotations.items():
            year, month = map(int, date.split('-'))
            date_str = f"{year}-{month:02d}"
            
            if date_str in data['Date'].values:
                fig.add_annotation(
                    x=date_str,
                    y=1,
                    text=event_info['event'],
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    ax=0,
                    ay=-40,
                    bgcolor="rgba(255, 255, 255, 0.8)",
                    bordercolor="#c7c7c7",
                    font=dict(size=10)
                )
        
        return fig

    def create_radar_chart(self, indicators):
        """Create a radar chart for the selected indicators
        
        Args:
            indicators (list): List of indicator names to visualize
            
        Returns:
            plotly.graph_objects.Figure: A radar chart comparing indicators
        """
        if not indicators or len(indicators) < 3:
            return None
        
        # Get data from data handler
        data = self.data_handler.data.copy()
        
        # Get most recent data
        latest_data = data.iloc[-1]
        
        # Get min and max values for normalization
        min_values = data[indicators].min()
        max_values = data[indicators].max()
        
        # Normalize data to 0-1 scale
        normalized_values = [(latest_data[indicator] - min_values[indicator]) / 
                             (max_values[indicator] - min_values[indicator]) 
                             for indicator in indicators]
        
        # Get indicator names for display
        indicator_names = [self.indicator_names.get(indicator, indicator) for indicator in indicators]
        
        # Add first value again to close the polygon
        indicator_names.append(indicator_names[0])
        normalized_values.append(normalized_values[0])
        
        # Create figure
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=normalized_values,
            theta=indicator_names,
            fill='toself',
            name='Giá trị hiện tại',
            line_color='rgba(59, 130, 246, 0.8)',
            fillcolor='rgba(59, 130, 246, 0.2)'
        ))
        
        # Update layout
        fig.update_layout(
            title="Biểu đồ radar của các chỉ số kinh tế hiện tại",
            height=600,
            template="plotly_white",
            hoverlabel=self.hover_style,
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=False,
            font=dict(family="Roboto, sans-serif", size=12),
            margin=dict(l=40, r=40, t=60, b=40),
        )
        
        return fig

    def create_bubble_chart(self, indicators):
        """Create a bubble chart for the selected indicators
        
        Args:
            indicators (list): List of 3 indicator names to visualize (x, y, and size)
            
        Returns:
            plotly.graph_objects.Figure: A bubble chart comparing three indicators
        """
        if not indicators or len(indicators) != 3:
            return None
        
        # Get data from data handler
        data = self.data_handler.data.copy()
        
        # Create date column for better display
        data['Date'] = data.apply(lambda row: f"{int(row['Year'])}-{int(row['Month']):02d}", axis=1)
        
        # Assign indicators
        x_indicator = indicators[0]
        y_indicator = indicators[1]
        size_indicator = indicators[2]
        
        # Skip if any indicator not in data
        if not all(indicator in data.columns for indicator in indicators):
            return None
        
        # Get indicator names for display
        x_name = self.indicator_names.get(x_indicator, x_indicator)
        y_name = self.indicator_names.get(y_indicator, y_indicator)
        size_name = self.indicator_names.get(size_indicator, size_indicator)
        
        # Normalize size indicator for better visualization
        size_values = data[size_indicator]
        size_min, size_max = size_values.min(), size_values.max()
        normalized_size = ((size_values - size_min) / (size_max - size_min) * 30) + 5  # Scale to 5-35
        
        # Create figure
        fig = go.Figure()
        
        # Create colormap based on time
        color_scale = px.colors.sequential.Plasma
        
        fig.add_trace(go.Scatter(
            x=data[x_indicator],
            y=data[y_indicator],
            mode='markers',
            marker=dict(
                size=normalized_size,
                color=list(range(len(data))),  # Color by time (index)
                colorscale=color_scale,
                colorbar=dict(title="Thời gian"),
                showscale=True,
                line=dict(width=1, color='white')
            ),
            text=data['Date'],
            hovertemplate=
            f'<b>%{{text}}</b><br>' +
            f'{x_name}: %{{x:.2f}}<br>' +
            f'{y_name}: %{{y:.2f}}<br>' +
            f'{size_name}: %{{marker.size:.2f}}<extra></extra>',
        ))
        
        # Update layout
        fig.update_layout(
            title=f"Biểu đồ bong bóng: {x_name} vs {y_name} (kích thước: {size_name})",
            height=600,
            template="plotly_white",
            hoverlabel=self.hover_style,
            xaxis_title=x_name,
            yaxis_title=y_name,
            font=dict(family="Roboto, sans-serif", size=12),
            margin=dict(l=40, r=40, t=60, b=40),
        )
        
        # Add a trend line
        if len(data) > 3:
            try:
                x_values = data[x_indicator]
                y_values = data[y_indicator]
                
                # Calculate trend line
                z = np.polyfit(x_values, y_values, 1)
                p = np.poly1d(z)
                
                # Add trend line to the plot
                x_range = np.linspace(x_values.min(), x_values.max(), 100)
                fig.add_trace(go.Scatter(
                    x=x_range,
                    y=p(x_range),
                    mode='lines',
                    name=f'Xu hướng: y = {z[0]:.2f}x + {z[1]:.2f}',
                    line=dict(color='rgba(255, 0, 0, 0.7)', width=2, dash='dash')
                ))
            except:
                # Skip trend line if there's an error
                pass
        
        return fig

# Initialize global visualization handler
viz_handler = VisualizationHandler() 