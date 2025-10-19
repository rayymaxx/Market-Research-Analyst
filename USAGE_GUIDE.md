# Market Research AI - Usage Guide

## Getting Started

### 1. First Launch
1. Start the backend: `cd marketresearch/api && python run.py`
2. Start the frontend: `cd frontend && npm run dev`
3. Open your browser to `http://localhost:3000`

### 2. Landing Page
- Click **"Start Research"** to begin your first analysis
- Or click **"Try Sample Research"** for a demo

## Core Features

### 🔬 Research Workflow

#### Starting New Research
1. Navigate to **"New Research"** from the sidebar
2. Enter your **research topic** (e.g., "Electric vehicle charging infrastructure")
3. Describe your **research request** in detail
4. Use **Quick Start Templates** for common research types
5. Click **"Start AI Research"**

#### Monitoring Progress
- Watch **real-time progress** as AI agents work
- See which **agent is active** (Data Gatherer → Insights Specialist → Communications Expert)
- Track **tools being used** (web search, SWOT analysis, etc.)
- Monitor **completion percentage**

#### Viewing Results
- Results appear automatically when research completes
- **Download reports** in Markdown format
- **Share results** with team members
- **Preview sections** before downloading

### 📚 Knowledge Management

#### Uploading Documents
1. Go to **"Knowledge Base"** page
2. Use the **drag & drop** upload area
3. Supported formats: PDF, DOCX, TXT, MD, JSON, CSV
4. Files are automatically processed and indexed

#### Managing Knowledge
- View **document statistics** by category
- **Reindex** knowledge base after uploads
- Monitor **total documents** and categories
- Files enhance AI research with contextual insights

### 📊 Analytics & Insights

#### Dashboard Overview
- View **total research** conducted
- Check **success rates** and completion stats
- See **recent activity** and research history
- Monitor **knowledge base** growth

#### Analytics Page
- Track **research performance** over time
- View **success rate trends**
- Analyze **knowledge utilization**
- Monitor **system health**

#### History Management
- Browse **all past research** sessions
- **Search** by topic or filter by status
- **View details** of completed research
- **Delete** unwanted sessions

### 📄 Reports & Export

#### Generating Reports
- All completed research automatically generates reports
- Reports include:
  - Executive summary
  - Market analysis
  - Competitive landscape
  - SWOT analysis
  - Strategic recommendations

#### Export Options
- **Download** as Markdown files
- **Share** via browser sharing API
- **Preview** report contents
- Track **download statistics**

## Advanced Usage

### ⚙️ Settings Configuration

#### API Settings
- Configure **backend URL** (default: localhost:8000)
- Enable/disable **auto-refresh** for progress
- Adjust **polling intervals**

#### User Profile
- Set **username** and **email**
- Customize **notification preferences**
- Manage **research history**

#### Data Management
- **Clear research history** when needed
- **Reset settings** to defaults
- **Export/import** configurations

### 🎯 Best Practices

#### Research Topics
- Be **specific** with your research requests
- Include **industry context** and **target markets**
- Mention **geographic scope** if relevant
- Specify **time frames** for analysis

#### Knowledge Base
- Upload **relevant industry reports**
- Add **competitor profiles** and **market data**
- Keep documents **up-to-date**
- Organize by **categories** (company profiles, industry reports, etc.)

#### Research Quality
- Use **detailed research requests** for better results
- Upload **supporting documents** before research
- Review **progress indicators** during execution
- **Download reports** immediately after completion

## Troubleshooting

### Common Issues

#### Research Fails to Start
- Check **backend connection** (localhost:8000)
- Verify **Gemini API key** is configured
- Ensure **research topic** is not empty
- Try **refreshing** the page

#### Slow Performance
- Check **internet connection**
- Reduce **concurrent research** sessions
- Clear **browser cache**
- Restart **backend service**

#### Upload Issues
- Verify **file format** is supported
- Check **file size** (max 10MB)
- Ensure **stable connection**
- Try **different file types**

### Getting Help

#### Error Messages
- **Rate limit errors**: Wait and retry
- **Connection errors**: Check backend status
- **Upload errors**: Verify file format
- **Authentication errors**: Check API configuration

#### Support Resources
- Check **API documentation** at `/docs`
- Review **browser console** for errors
- Verify **network connectivity**
- Restart **both services** if needed

## Tips for Success

### Research Efficiency
1. **Prepare topics** in advance
2. **Upload relevant documents** first
3. **Use templates** for common research types
4. **Monitor progress** actively
5. **Download results** immediately

### Knowledge Management
1. **Organize documents** by category
2. **Update regularly** with new information
3. **Remove outdated** content
4. **Reindex** after major uploads
5. **Monitor statistics** for insights

### System Optimization
1. **Close unused tabs** for better performance
2. **Clear history** periodically
3. **Use latest browser** versions
4. **Enable notifications** for completion alerts
5. **Backup important** research results

## Mobile Usage

### Responsive Design
- **Full functionality** on all devices
- **Touch-friendly** interface
- **Mobile sidebar** with hamburger menu
- **Optimized layouts** for small screens

### Mobile Tips
- Use **landscape mode** for better viewing
- **Tap and hold** for context menus
- **Swipe navigation** where available
- **Zoom** for detailed content review

---

For technical support or feature requests, please refer to the project documentation or open an issue on GitHub.