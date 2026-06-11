"""
Generate static HTML dashboard for GitHub Pages deployment
"""

import yaml
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime


def load_network_assets():
    """Load all YAML files from network-assets/production directory"""
    base_path = Path.cwd() / "network-assets" / "production"
    tenant_devices = defaultdict(list)
    stats = {"total_files": 0, "total_devices": 0, "tenants": {}}

    # Iterate through all tenant directories
    for tenant_dir in sorted(base_path.iterdir()):
        if tenant_dir.is_dir():
            tenant_name = tenant_dir.name
            stats["tenants"][tenant_name] = {"files": 0, "devices": 0}

            # Find all YAML files in the tenant directory
            for yaml_file in tenant_dir.glob("*.yml"):
                try:
                    with open(yaml_file, "r") as f:
                        data = yaml.safe_load(f)

                    # Extract devices from the YAML file
                    if data and "devices" in data:
                        stats["total_files"] += 1
                        stats["tenants"][tenant_name]["files"] += 1

                        for device in data["devices"]:
                            device_info = {
                                "tenant": tenant_name,
                                "name": device.get("name", "N/A"),
                                "description": device.get("description", "N/A"),
                                "role": device.get("role", {}).get("slug", "N/A"),
                                "site": device.get("site", {}).get("slug", "N/A"),
                                "status": device.get("status", "N/A"),
                                "device_type": device.get("device_type", {}).get(
                                    "slug", "N/A"
                                ),
                                "platform": device.get("platform", {}).get(
                                    "slug", "N/A"
                                ),
                                "source_file": yaml_file.name,
                                "environment": device.get("custom_fields", {}).get(
                                    "environment", "N/A"
                                ),
                            }
                            tenant_devices[tenant_name].append(device_info)
                            stats["total_devices"] += 1
                            stats["tenants"][tenant_name]["devices"] += 1

                except Exception as e:
                    print(f"Error loading {yaml_file}: {str(e)}")

    return dict(tenant_devices), stats


def generate_html(tenant_data, stats):
    """Generate static HTML dashboard"""

    # Convert data to JSON for JavaScript
    data_json = json.dumps(tenant_data, indent=2)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Network Assets Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-card h3 {{
            font-size: 2em;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-card p {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .controls {{
            padding: 20px 30px;
            background: white;
            border-bottom: 1px solid #e0e0e0;
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            align-items: center;
        }}
        
        .search-box {{
            flex: 1;
            min-width: 250px;
        }}
        
        .search-box input {{
            width: 100%;
            padding: 12px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }}
        
        .search-box input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        select {{
            padding: 12px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            background: white;
            cursor: pointer;
            transition: border-color 0.3s;
        }}
        
        select:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .tenant-section {{
            margin-bottom: 30px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .tenant-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.3s;
        }}
        
        .tenant-header:hover {{
            opacity: 0.9;
        }}
        
        .tenant-header h2 {{
            font-size: 1.5em;
            text-transform: uppercase;
        }}
        
        .tenant-badge {{
            background: rgba(255,255,255,0.3);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        
        .tenant-devices {{
            padding: 20px;
            background: #f8f9fa;
        }}
        
        .device-table {{
            width: 100%;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .device-table table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .device-table th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
        }}
        
        .device-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .device-table tr:hover {{
            background: #f8f9fa;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        
        .badge-active {{
            background: #d4edda;
            color: #155724;
        }}
        
        .badge-inactive {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .badge-role {{
            background: #e7f3ff;
            color: #004085;
        }}
        
        .no-results {{
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }}
        
        .no-results h3 {{
            font-size: 1.5em;
            margin-bottom: 10px;
        }}
        
        .charts-section {{
            padding: 30px;
            background: #f8f9fa;
            border-top: 1px solid #e0e0e0;
        }}
        
        .charts-section h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        
        .charts-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-top: 20px;
        }}
        
        .chart-box {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .chart-box h3 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        
        .chart-canvas {{
            max-height: 400px;
        }}
        
        footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}
        
        .hidden {{
            display: none;
        }}
        
        @media (max-width: 768px) {{
            .device-table {{
                overflow-x: auto;
            }}
            
            header h1 {{
                font-size: 1.8em;
            }}
            
            .controls {{
                flex-direction: column;
            }}
            
            .search-box {{
                width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🌐 Network Assets Ingestion Dashboard</h1>
            <p>Production Network Devices Backup Overview</p>
            <p style="margin-top: 10px; font-size: 0.9em; opacity: 0.8;">Last Updated: {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <h3>{len(tenant_data)}</h3>
                <p>Total Tenants</p>
            </div>
            <div class="stat-card">
                <h3>{stats['total_devices']}</h3>
                <p>Total Devices</p>
            </div>
            <div class="stat-card">
                <h3>{stats['total_devices'] // len(tenant_data) if len(tenant_data) > 0 else 0}</h3>
                <p>Avg Devices/Tenant</p>
            </div>
        </div>
        
        <div class="charts-section">
            <h2>📊 Analytics & Insights</h2>
            <div class="charts-container">
                <div class="chart-box">
                    <h3>Devices by Tenant</h3>
                    <canvas id="tenantChart" class="chart-canvas"></canvas>
                </div>
                <div class="chart-box">
                    <h3>Device Roles Distribution</h3>
                    <canvas id="roleChart" class="chart-canvas"></canvas>
                </div>
            </div>
        </div>
        
        <div class="controls">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="🔍 Search by device name or description...">
            </div>
            <select id="tenantFilter">
                <option value="">All Tenants</option>
            </select>
            <select id="roleFilter">
                <option value="">All Roles</option>
            </select>
            <select id="statusFilter">
                <option value="">All Statuses</option>
            </select>
        </div>
        
        <div class="content" id="content">
            <!-- Tenant sections will be dynamically generated here -->
        </div>
        
        <footer>
            <p>Built by FIRE team</p>
            <p style="margin-top: 5px; opacity: 0.8;">Generated from <a href='https://github.com/CBA-General/network-automation-radar-tenants/tree/main/network-assets/production'>Network Assets</a></p>
        </footer>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script>
        // Data from Python
        const tenantData = {data_json};
        
        // Global state
        let filters = {{
            search: '',
            tenant: '',
            role: '',
            status: ''
        }};
        
        // Initialize dashboard
        function init() {{
            populateFilters();
            renderContent();
            setupEventListeners();
        }}
        
        // Populate filter dropdowns
        function populateFilters() {{
            const tenants = Object.keys(tenantData).sort();
            const roles = new Set();
            const statuses = new Set();
            
            // Collect unique roles and statuses
            Object.values(tenantData).forEach(devices => {{
                devices.forEach(device => {{
                    roles.add(device.role);
                    statuses.add(device.status);
                }});
            }});
            
            // Populate tenant filter
            const tenantFilter = document.getElementById('tenantFilter');
            tenants.forEach(tenant => {{
                const option = document.createElement('option');
                option.value = tenant;
                option.textContent = tenant.toUpperCase();
                tenantFilter.appendChild(option);
            }});
            
            // Populate role filter
            const roleFilter = document.getElementById('roleFilter');
            Array.from(roles).sort().forEach(role => {{
                const option = document.createElement('option');
                option.value = role;
                option.textContent = role;
                roleFilter.appendChild(option);
            }});
            
            // Populate status filter
            const statusFilter = document.getElementById('statusFilter');
            Array.from(statuses).sort().forEach(status => {{
                const option = document.createElement('option');
                option.value = status;
                option.textContent = status;
                statusFilter.appendChild(option);
            }});
        }}
        
        // Filter devices based on current filters
        function filterDevices(devices) {{
            return devices.filter(device => {{
                // Search filter
                if (filters.search) {{
                    const searchLower = filters.search.toLowerCase();
                    const matchName = device.name.toLowerCase().includes(searchLower);
                    const matchDesc = device.description.toLowerCase().includes(searchLower);
                    if (!matchName && !matchDesc) return false;
                }}
                
                // Role filter
                if (filters.role && device.role !== filters.role) return false;
                
                // Status filter
                if (filters.status && device.status !== filters.status) return false;
                
                return true;
            }});
        }}
        
        // Render content
        function renderContent() {{
            const content = document.getElementById('content');
            content.innerHTML = '';
            
            let hasResults = false;
            const tenants = Object.keys(tenantData).sort();
            
            tenants.forEach(tenant => {{
                // Skip if tenant filter is active and doesn't match
                if (filters.tenant && tenant !== filters.tenant) return;
                
                const devices = filterDevices(tenantData[tenant]);
                
                if (devices.length === 0) return;
                
                hasResults = true;
                
                // Create tenant section
                const section = document.createElement('div');
                section.className = 'tenant-section';
                
                const header = document.createElement('div');
                header.className = 'tenant-header';
                header.innerHTML = `
                    <h2>${{tenant.toUpperCase()}}</h2>
                    <span class="tenant-badge">${{devices.length}} devices</span>
                `;
                
                const deviceContainer = document.createElement('div');
                deviceContainer.className = 'tenant-devices';
                
                const table = document.createElement('div');
                table.className = 'device-table';
                table.innerHTML = `
                    <table>
                        <thead>
                            <tr>
                                <th>Device Name</th>
                                <th>Description</th>
                                <th>Role</th>
                                <th>Site</th>
                                <th>Status</th>
                                <th>Type</th>
                                <th>Platform</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${{devices.map(device => `
                                <tr>
                                    <td><strong>${{device.name}}</strong></td>
                                    <td>${{device.description}}</td>
                                    <td><span class="badge badge-role">${{device.role}}</span></td>
                                    <td>${{device.site}}</td>
                                    <td><span class="badge badge-${{device.status === 'active' ? 'active' : 'inactive'}}">${{device.status}}</span></td>
                                    <td>${{device.device_type}}</td>
                                    <td>${{device.platform}}</td>
                                </tr>
                            `).join('')}}
                        </tbody>
                    </table>
                `;
                
                deviceContainer.appendChild(table);
                section.appendChild(header);
                section.appendChild(deviceContainer);
                content.appendChild(section);
            }});
            
            if (!hasResults) {{
                content.innerHTML = `
                    <div class="no-results">
                        <h3>No devices found</h3>
                        <p>Try adjusting your filters or search terms</p>
                    </div>
                `;
            }}
        }}
        
        // Setup event listeners
        function setupEventListeners() {{
            document.getElementById('searchInput').addEventListener('input', (e) => {{
                filters.search = e.target.value;
                renderContent();
            }});
            
            document.getElementById('tenantFilter').addEventListener('change', (e) => {{
                filters.tenant = e.target.value;
                renderContent();
            }});
            
            document.getElementById('roleFilter').addEventListener('change', (e) => {{
                filters.role = e.target.value;
                renderContent();
            }});
            
            document.getElementById('statusFilter').addEventListener('change', (e) => {{
                filters.status = e.target.value;
                renderContent();
            }});
        }}
        
        // Create charts
        function createCharts() {{
            // Prepare data for tenant chart
            const tenants = Object.keys(tenantData).sort();
            const tenantCounts = tenants.map(tenant => tenantData[tenant].length);
            
            // Create gradient colors for tenant chart
            const ctx1 = document.getElementById('tenantChart').getContext('2d');
            const gradient1 = ctx1.createLinearGradient(0, 0, 0, 400);
            gradient1.addColorStop(0, '#667eea');
            gradient1.addColorStop(1, '#764ba2');
            
            // Tenant Chart
            new Chart(ctx1, {{
                type: 'bar',
                data: {{
                    labels: tenants.map(t => t.toUpperCase()),
                    datasets: [{{
                        label: 'Number of Devices',
                        data: tenantCounts,
                        backgroundColor: gradient1,
                        borderColor: '#667eea',
                        borderWidth: 2,
                        borderRadius: 8,
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {{
                        legend: {{
                            display: false
                        }},
                        tooltip: {{
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            padding: 12,
                            cornerRadius: 8,
                            callbacks: {{
                                label: function(context) {{
                                    return 'Devices: ' + context.parsed.y;
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            grid: {{
                                color: 'rgba(0, 0, 0, 0.05)'
                            }},
                            ticks: {{
                                font: {{
                                    size: 12
                                }}
                            }}
                        }},
                        x: {{
                            grid: {{
                                display: false
                            }},
                            ticks: {{
                                font: {{
                                    size: 10
                                }},
                                maxRotation: 45,
                                minRotation: 45
                            }}
                        }}
                    }}
                }}
            }});
            
            // Prepare data for role chart
            const roleCounts = {{}};
            Object.values(tenantData).forEach(devices => {{
                devices.forEach(device => {{
                    roleCounts[device.role] = (roleCounts[device.role] || 0) + 1;
                }});
            }});
            
            const roles = Object.keys(roleCounts).sort();
            const counts = roles.map(role => roleCounts[role]);
            
            // Create role chart
            const ctx2 = document.getElementById('roleChart').getContext('2d');
            
            // Generate colors for pie chart
            const colors = [
                '#667eea', '#764ba2', '#f093fb', '#4facfe',
                '#43e97b', '#fa709a', '#fee140', '#30cfd0',
                '#a8edea', '#fed6e3', '#c471f5', '#12c2e9'
            ];
            
            new Chart(ctx2, {{
                type: 'doughnut',
                data: {{
                    labels: roles,
                    datasets: [{{
                        data: counts,
                        backgroundColor: colors,
                        borderWidth: 2,
                        borderColor: '#fff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {{
                        legend: {{
                            position: 'right',
                            labels: {{
                                padding: 15,
                                font: {{
                                    size: 12
                                }},
                                generateLabels: function(chart) {{
                                    const data = chart.data;
                                    return data.labels.map((label, i) => ({{
                                        text: `${{label}} (${{data.datasets[0].data[i]}})`,
                                        fillStyle: data.datasets[0].backgroundColor[i],
                                        hidden: false,
                                        index: i
                                    }}));
                                }}
                            }}
                        }},
                        tooltip: {{
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            padding: 12,
                            cornerRadius: 8,
                            callbacks: {{
                                label: function(context) {{
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((context.parsed / total) * 100).toFixed(1);
                                    return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', () => {{
            init();
            createCharts();
        }});
    </script>
</body>
</html>"""

    return html_content


def main():
    print("Loading network assets...")
    tenant_data, stats = load_network_assets()

    print(f"Found {len(tenant_data)} tenants with {stats['total_devices']} devices")

    print("Generating static HTML dashboard...")
    html_content = generate_html(tenant_data, stats)

    # Create output directory
    output_dir = Path("/tmp")
    output_dir.mkdir(exist_ok=True)

    # Write dashboard.html
    output_file = output_dir / "dashboard.html"
    with open(output_file, "w") as f:
        f.write(html_content)

    print(f"✅ Dashboard generated successfully at: {output_file}")


if __name__ == "__main__":
    main()
