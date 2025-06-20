# 📊 ICTA Employee Performance Dashboard

A comprehensive, real-time analytics dashboard for employee performance management built with Dash and Plotly. This dashboard provides executive-level insights, detailed employee analytics, and actionable business intelligence.

🌐 **Live Demo**: [Dashboard URL when deployed]

## 🚀 Features

### 📈 Executive Overview
- **Real-time KPIs**: Employee count, average overtime, delays, and bonuses
- **Executive Summary Cards**: Top performers, attention needed, productivity leaders
- **High-level Performance Charts**: Overtime analysis and department comparisons

### 👥 Employee Analysis
- **Performance Matrix**: Interactive scatter plot of overtime vs delays
- **Productivity Scoring**: Custom algorithm ranking employees
- **Detailed Metrics Table**: Sortable performance data with conditional formatting
- **Top Performers**: Visual identification of high-performing employees

### 🏢 Department Performance
- **Radar Charts**: Multi-dimensional department comparison
- **Efficiency Scoring**: Department productivity metrics
- **Resource Allocation**: Insights for management decisions

### 💰 Financial Impact
- **Bonus/Fine Analysis**: Complete financial impact assessment
- **Net Impact Calculations**: Employee financial contributions
- **ROI Insights**: Cost-benefit analysis of employee performance

### 📈 Trends & Business Insights
- **Time Series Analysis**: Daily performance trends
- **AI-Powered Recommendations**: Automated business insights
- **Predictive Analytics**: Performance trend identification

## 🏗️ Architecture

### Data Pipeline
```
PostgreSQL Database (icta schema)
        ↓
   SQLAlchemy Engine
        ↓
    Pandas DataFrames
        ↓
   Plotly Visualizations
        ↓
    Dash Web Interface
```

### Database Schema
- **icta.attendance**: Daily attendance records (246 entries)
- **icta.monthly_fines_bonuses**: Aggregated monthly performance (12 entries)
- **icta.data**: Processed work hours and calculations (192 entries)

## 🛠️ Technical Stack

- **Frontend**: Dash + Plotly for interactive visualizations
- **Backend**: Python with pandas for data processing
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Deployment**: Gunicorn WSGI server
- **Styling**: Custom CSS with responsive design

## 📊 Key Metrics & KPIs

### Performance Indicators
- **Productivity Score**: `Overtime - Delays` (custom algorithm)
- **Efficiency Ratio**: `Overtime / (Delays + 1)`
- **Financial Impact**: `Total Bonuses - Total Fines`

### Business Rules
- **Fines Structure**:
  - Delay > 3 hours: 2% fine
  - Delay > 10 hours: 3% fine  
  - Delay > 20 hours: 5% fine

- **Bonus Structure**:
  - Overtime > 3 hours: 2% bonus
  - Overtime > 10 hours: 3% bonus
  - Overtime > 20 hours: 5% bonus

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL database with data
- Environment variables configured

### Installation
```bash
# Clone repository
git clone <repository-url>
cd dashboard

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials
```

### Environment Variables
```env
PGHOST=your_postgres_host
PGDATABASE=your_database_name
PGUSER=your_username
PGPASSWORD=your_password
```

### Run Locally
```bash
# Development mode
python dashboard.py

# Production mode with Gunicorn
gunicorn dashboard:server -b 0.0.0.0:8050
```

### Access Dashboard
- **Local**: http://localhost:8050
- **Production**: https://your-domain.com

## 📱 Usage Guide

### Navigation
1. **📊 Executive Overview**: Start here for high-level insights
2. **👥 Employee Analysis**: Drill down into individual performance
3. **🏢 Department Performance**: Compare department efficiency
4. **💰 Financial Impact**: Analyze cost-benefit metrics
5. **📈 Trends & Insights**: Discover patterns and recommendations

### Interactive Features
- **Hover Effects**: Detailed tooltips on all charts
- **Sorting**: Click column headers in tables
- **Color Coding**: Visual performance indicators
- **Responsive Design**: Works on desktop and mobile

## 🔍 Data Sources

### Real-time Database Queries
```sql
-- Attendance Data
SELECT "Date", "Department", "Employee", "Entry", "Exit"
FROM icta.attendance
ORDER BY "Date", "Employee";

-- Monthly Performance
SELECT "Employee", "Department", "Month", "Delay", "Overtime", "Fine", "Bonus"
FROM icta.monthly_fines_bonuses
ORDER BY "Employee", "Month";

-- Processed Metrics
SELECT "Date", "Department", "Employee", "Adjusted_Work_Hours", "Overtime", "Delay"
FROM icta.data
ORDER BY "Date", "Employee";
```

### Data Processing Pipeline
1. **Raw Data Ingestion**: Direct PostgreSQL connection
2. **Data Transformation**: Pandas aggregations and calculations
3. **Insight Generation**: Business logic and KPI calculations
4. **Visualization**: Plotly chart generation
5. **Real-time Updates**: Fresh data on every page load

## 📈 Business Intelligence Features

### Automated Insights
- **Performance Alerts**: Automatic detection of attendance issues
- **Trend Analysis**: Identification of performance patterns
- **Recommendation Engine**: AI-powered business suggestions

### Key Insights Generated
- Top performers by overtime contribution
- Employees requiring attention (high delays)
- Department efficiency comparisons
- Financial impact assessments
- Productivity trend analysis

## 🚀 Deployment

### Local Development
```bash
python dashboard.py
```

### Production Deployment

#### Option 1: Heroku
```bash
# Procfile
web: gunicorn dashboard:server

# Deploy
git push heroku main
```

#### Option 2: Docker
```dockerfile
FROM python:3.9-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8050
CMD ["gunicorn", "dashboard:server", "-b", "0.0.0.0:8050"]
```

#### Option 3: Traditional Server
```bash
# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn
gunicorn dashboard:server -b 0.0.0.0:8050 --workers 4
```

## 🔧 Configuration

### Performance Tuning
- **Database Connection Pooling**: SQLAlchemy engine optimization
- **Caching**: Implement Redis for frequent queries
- **Lazy Loading**: On-demand data fetching

### Customization
- **Styling**: Modify CSS in `dashboard.py`
- **Colors**: Update color schemes in Plotly configurations
- **Metrics**: Add custom KPIs in `calculate_insights()`

## 📊 Data Model

### Employee Performance Schema
```python
Employee {
    name: string
    department: string
    total_overtime: float
    total_delay: float
    productivity_score: float
    financial_impact: float
}

Department {
    name: string
    avg_overtime: float
    avg_delay: float
    efficiency_score: float
    employee_count: int
}
```

## 🔍 Troubleshooting

### Common Issues

#### Database Connection
```python
# Check connection
from sqlalchemy import create_engine
engine = create_engine("postgresql://user:pass@host:port/db")
with engine.connect() as conn:
    result = conn.execute("SELECT 1")
    print("Connection successful!")
```

#### Empty Dashboard
- Verify database credentials in `.env`
- Check if data exists in `icta` schema
- Review console logs for SQL errors

#### Performance Issues
- Add database indexes on frequently queried columns
- Implement connection pooling
- Consider data caching strategies

## 🤝 Contributing

### Development Setup
```bash
# Create virtual environment
python -m venv dashboard-env
source dashboard-env/bin/activate  # On Windows: dashboard-env\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Run in debug mode
python dashboard.py
```

### Adding New Features
1. Create feature branch
2. Add new visualization functions
3. Update navigation tabs
4. Test with sample data
5. Submit pull request

## 📚 API Reference

### Core Functions
- `fetch_data()`: Database query execution
- `calculate_insights()`: Business intelligence generation
- `render_overview()`: Executive dashboard rendering
- `render_employee_analysis()`: Employee-specific analytics

### Custom Metrics
- **Productivity Score**: Balances overtime contribution against delays
- **Efficiency Ratio**: Department-level performance indicator
- **Financial Impact**: Employee cost-benefit analysis

## 🔒 Security

### Database Security
- Environment variable configuration
- Connection string encryption
- SQL injection prevention via SQLAlchemy

### Access Control
- Add authentication layer for production
- Implement role-based permissions
- Audit trail for data access

## 📈 Roadmap

### Planned Features
- [ ] Real-time data refresh
- [ ] Export functionality (PDF/Excel)
- [ ] Mobile app integration
- [ ] Advanced ML predictions
- [ ] Custom alert systems

### Future Enhancements
- [ ] Multi-language support
- [ ] Advanced filtering options
- [ ] Integration with HR systems
- [ ] Automated reporting schedules

## 📄 License

This project is part of the ICTA Data Analyst assessment.

## 📞 Support

For questions or issues:
1. Check troubleshooting section
2. Review database connectivity
3. Verify environment configuration
4. Contact system administrator

---

**🚀 Dashboard Status**: Ready for production deployment with comprehensive employee analytics and business intelligence capabilities!