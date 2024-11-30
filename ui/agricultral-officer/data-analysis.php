<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GreenGrid</title>
    <link rel="icon" type="image/png" href="../../../Images/GREENGRID Logo 1.png">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/admin-lte@3.1/dist/css/adminlte.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.bundle.min.js"></script>
    <link rel="stylesheet" href="../../../styles/style.css">
</head>

<body class="sidebar-mini"></body>
<div class="wrapper">

    <!-- Navbar -->
    <nav class="main-header navbar navbar-expand navbar-white navbar-light">
        <!-- Left navbar links -->
        <ul class="navbar-nav">
            <li class="nav-item">
                <a class="nav-link" data-widget="pushmenu" href="#" role="button"><i class="fas fa-bars"></i></a>
            </li>
            <li class="nav-item d-none d-sm-inline-block">
                <a href="#" class="nav-link">Contact</a>
            </li>
        </ul>

        <!-- Right navbar links -->
        <ul class="navbar-nav ml-auto">
            <!-- Messages -->
            <li class="nav-item dropdown">
                <a class="nav-link" data-toggle="dropdown" href="#">
                    <i class="far fa-envelope"></i>
                    <span class="badge badge-success navbar-badge">4</span>
                </a>
                <div class="dropdown-menu dropdown-menu-lg dropdown-menu-right">
                    <span class="dropdown-item dropdown-header">4 New Messages</span>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item">
                        <i class="fas fa-envelope mr-2"></i> Order #1234 Request
                        <span class="float-right text-muted text-sm">3 mins</span>
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item">
                        <i class="fas fa-envelope mr-2"></i> Stock Update Required
                        <span class="float-right text-muted text-sm">12 mins</span>
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item">
                        <i class="fas fa-envelope mr-2"></i> Delivery Confirmation
                        <span class="float-right text-muted text-sm">2 hrs</span>
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item">
                        <i class="fas fa-envelope mr-2"></i> New Supplier Message
                        <span class="float-right text-muted text-sm">4 hrs</span>
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item dropdown-footer">See All Messages</a>
                </div>
            </li>

            <!-- Notifications -->
            <li class="nav-item dropdown">
                <a class="nav-link" data-toggle="dropdown" href="#">
                    <i class="far fa-bell"></i>
                    <span class="badge badge-warning navbar-badge">8</span>
                </a>
                <div class="dropdown-menu dropdown-menu-lg dropdown-menu-right">
                    <span class="dropdown-header">8 Notifications</span>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item">
                        <i class="fas fa-shopping-cart mr-2"></i> 4 new orders
                        <span class="float-right text-muted text-sm">5 mins</span>
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item">
                        <i class="fas fa-users mr-2"></i> 3 new registrations
                        <span class="float-right text-muted text-sm">2 hrs</span>
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item">
                        <i class="fas fa-chart-line mr-2"></i> Weekly report ready
                        <span class="float-right text-muted text-sm">1 day</span>
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item dropdown-footer">See All Notifications</a>
                </div>
            </li>

            <!-- Alerts -->
            <li class="nav-item dropdown">
                <a class="nav-link" data-toggle="dropdown" href="#">
                    <i class="fas fa-exclamation-circle"></i>
                    <span class="badge badge-danger navbar-badge">5</span>
                </a>
                <div class="dropdown-menu dropdown-menu-lg dropdown-menu-right">
                    <span class="dropdown-header">5 Alerts</span>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item">
                        <i class="fas fa-exclamation-triangle text-warning mr-2"></i> Low stock: Rice
                        <span class="float-right text-muted text-sm">Now</span>
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item">
                        <i class="fas fa-temperature-high text-danger mr-2"></i> Temperature Alert: W3
                        <span class="float-right text-muted text-sm">10 mins</span>
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item">
                        <i class="fas fa-exclamation-circle text-warning mr-2"></i> Maintenance Due
                        <span class="float-right text-muted text-sm">2 hrs</span>
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item">
                        <i class="fas fa-truck text-danger mr-2"></i> Delayed Shipment
                        <span class="float-right text-muted text-sm">4 hrs</span>
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item">
                        <i class="fas fa-exclamation-triangle text-warning mr-2"></i> Quality Check Required
                        <span class="float-right text-muted text-sm">6 hrs</span>
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="dropdown-item dropdown-footer">See All Alerts</a>
                </div>
            </li>

            <!-- Fullscreen Button -->
            <li class="nav-item">
                <a class="nav-link" data-widget="fullscreen" href="#" role="button">
                    <i class="fas fa-expand-arrows-alt"></i>
                </a>
            </li>
        </ul>
    </nav>
    <!-- /.navbar -->

    <!-- Main Sidebar Container -->
    <aside class="main-sidebar sidebar-dark-custom elevation-4">
        <!-- Brand Logo -->
        <a href="index3.html" class="brand-link">
            <img src="../../../Images/GREENGRID Logo 1.png" alt="GreenGrid Logo"
                class="brand-image img-circle elevation-3" style="opacity: .8">
            <span class="brand-text font-weight-light"><b>GreenGrid</b></span>
        </a>

        <!-- Sidebar -->
        <div class="sidebar">
            <!-- Sidebar user panel (optional) -->
            <div class="user-panel mt-3 pb-3 mb-3 d-flex">
                <div class="image">
                    <i class="fa-solid fa-user-tie fa-2x" style="color: #fff; margin: 0 10px;"></i>
                </div>
                <div class="info">
                    <a href="#" class="d-block">Agricultural Officer</a>
                </div>
            </div>

            <!-- SidebarSearch Form -->
            <div class="form-inline">
                <div class="input-group" data-widget="sidebar-search">
                    <input class="form-control form-control-sidebar" type="search" placeholder="Search"
                        aria-label="Search">
                    <div class="input-group-append">
                        <button class="btn btn-sidebar">
                            <i class="fas fa-search fa-fw"></i>
                        </button>
                    </div>
                </div>
                <div class="sidebar-search-results">
                    <div class="list-group">
                        <a href="#" class="list-group-item">
                            <div class="search-title text-light">No element found!</div>
                            <div class="search-path"></div>
                        </a>
                    </div>
                </div>
            </div>

            <!-- Simplified sidebar menu -->
            <nav class="mt-2">
                <ul class="nav nav-pills nav-sidebar flex-column" data-widget="treeview" role="menu"
                    data-accordion="false">
                    <li class="nav-item">
                        <a href="officer-dashboard.html" class="nav-link">
                            <i class="nav-icon fas fa-tachometer-alt"></i>
                            <p>Dashboard</p>
                        </a>
                    </li>

                    <!-- Product Insight -->
                    <li class="nav-item">
                        <a href="production-monitoring.html" class="nav-link">
                            <i class="nav-icon fas fa-box"></i>
                            <p>Production Monitoring</p>
                        </a>
                    </li>

                    <!-- Order Processing System -->
                    <li class="nav-item">
                        <a href="order-processing.html" class="nav-link">
                            <i class="nav-icon fas fa-shopping-cart"></i>
                            <p>Order Processing</p>
                        </a>
                    </li>

                    <!-- Data Analysis -->
                    <li class="nav-item">
                        <a href="data-analysis.html" class="nav-link">
                            <i class="nav-icon fas fa-chart-line"></i>
                            <p>Data Analysis</p>
                        </a>
                    </li>

                    <!-- Subsidy Management -->
                    <li class="nav-item">
                        <a href="subsidy-management.html" class="nav-link">
                            <i class="nav-icon fas fa-hand-holding-usd"></i>
                            <p>Subsidy Management</p>
                        </a>
                    </li>

                    <!-- Settings and Logout -->
                    <li class="nav-item">
                        <a href="settings.html" class="nav-link">
                            <i class="nav-icon fas fa-cog"></i>
                            <p>Settings</p>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="login.html" class="nav-link">
                            <i class="nav-icon fas fa-sign-out-alt"></i>
                            <p>Logout</p>
                        </a>
                    </li>
                </ul>
            </nav>
            <!-- /.sidebar-menu -->
        </div>
        <!-- /.sidebar -->
    </aside>

    <!-- Content Wrapper -->
    <div class="content-wrapper">
        <!-- Content Header -->
        <div class="content-header">
            <div class="container-fluid">
                <div class="row mb-2">
                    <div class="col-sm-6">
                        <h1 class="m-0">Data Analysis</h1>
                    </div>
                </div>
            </div>
        </div>

        <!-- Main content -->
        <section class="content">
            <div class="container-fluid">
                <!-- Analysis Filters -->
                <div class="card mb-4">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-3">
                                <div class="form-group">
                                    <label>Date Range</label>
                                    <select class="form-control">
                                        <option>Last 30 Days</option>
                                        <option>Last Quarter</option>
                                        <option>Last 6 Months</option>
                                        <option>Last Year</option>
                                        <option>Custom Range</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="form-group">
                                    <label>Division</label>
                                    <select class="form-control">
                                        <option>All Divisions</option>
                                        <option>Dhaka</option>
                                        <option>Chittagong</option>
                                        <option>Rajshahi</option>
                                        <option>Khulna</option>
                                        <option>Barisal</option>
                                        <option>Sylhet</option>
                                        <option>Rangpur</option>
                                        <option>Mymensingh</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="form-group">
                                    <label>Crop Type</label>
                                    <select class="form-control">
                                        <option>All Crops</option>
                                        <option>Rice (Boro)</option>
                                        <option>Rice (Aman)</option>
                                        <option>Rice (Aus)</option>
                                        <option>Wheat</option>
                                        <option>Jute</option>
                                        <option>Vegetables</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="form-group">
                                    <label>Analysis Type</label>
                                    <select class="form-control">
                                        <option>Production Trends</option>
                                        <option>Yield Analysis</option>
                                        <option>Price Analysis</option>
                                        <option>Weather Impact</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Charts Row 1 -->
                <div class="row">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">
                                <h3 class="card-title">Crop Production Trends</h3>
                            </div>
                            <div class="card-body">
                                <canvas id="productionTrendsChart" height="300"></canvas>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">
                                <h3 class="card-title">Regional Distribution</h3>
                            </div>
                            <div class="card-body">
                                <canvas id="regionalDistributionChart" height="300"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Charts Row 2 -->
                <div class="row mt-4">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">
                                <h3 class="card-title">Yield Comparison</h3>
                            </div>
                            <div class="card-body">
                                <canvas id="yieldComparisonChart" height="300"></canvas>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">
                                <h3 class="card-title">Price Fluctuation</h3>
                            </div>
                            <div class="card-body">
                                <canvas id="priceFluctuationChart" height="300"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Summary Statistics -->
                <div class="card mt-4">
                    <div class="card-header">
                        <h3 class="card-title">Key Metrics</h3>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-3">
                                <div class="info-box bg-info">
                                    <span class="info-box-icon"><i class="fas fa-seedling"></i></span>
                                    <div class="info-box-content">
                                        <span class="info-box-text">Total Production</span>
                                        <span class="info-box-number">127,500 Tons</span>
                                        <span class="progress-description">
                                            15% increase from last year
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="info-box bg-success">
                                    <span class="info-box-icon"><i class="fas fa-chart-line"></i></span>
                                    <div class="info-box-content">
                                        <span class="info-box-text">Average Yield</span>
                                        <span class="info-box-number">4.2 Tons/Hectare</span>
                                        <span class="progress-description">
                                            8% increase from last year
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="info-box bg-warning">
                                    <span class="info-box-icon"><i class="fas fa-coins"></i></span>
                                    <div class="info-box-content">
                                        <span class="info-box-text">Average Price</span>
                                        <span class="info-box-number">৳35/kg</span>
                                        <span class="progress-description">
                                            5% decrease from last month
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="info-box bg-danger">
                                    <span class="info-box-icon"><i class="fas fa-water"></i></span>
                                    <div class="info-box-content">
                                        <span class="info-box-text">Water Usage</span>
                                        <span class="info-box-number">2,100 L/kg</span>
                                        <span class="progress-description">
                                            10% reduction achieved
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Seasonal Analysis Section -->
                <div class="card mt-4">
                    <div class="card-header">
                        <h3 class="card-title">Seasonal Analysis</h3>
                    </div>
                    <div class="card-body">
                        <!-- Seasonal Data Table -->
                        <div class="table-responsive mt-4">
                            <table class="table table-bordered">
                                <thead>
                                    <tr>
                                        <th>Season</th>
                                        <th>Production</th>
                                        <th>YoY Change</th>
                                        <th>Major Crops</th>
                                        <th>Weather Impact</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>Summer</td>
                                        <td>25,000 MT</td>
                                        <td>
                                            <span class="text-success">
                                                <i class="fas fa-arrow-up"></i> +15%
                                            </span>
                                        </td>
                                        <td>Aus Rice, Jute</td>
                                        <td>
                                            <span class="text-danger">
                                                <i class="fas fa-thermometer-high"></i> Heat Stress
                                            </span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>Rainy</td>
                                        <td>35,000 MT</td>
                                        <td>
                                            <span class="text-success">
                                                <i class="fas fa-arrow-up"></i> +20%
                                            </span>
                                        </td>
                                        <td>Aman Rice, Jute</td>
                                        <td>
                                            <span class="text-warning">
                                                <i class="fas fa-cloud-rain"></i> Flood Risk
                                            </span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>Autumn</td>
                                        <td>28,000 MT</td>
                                        <td>
                                            <span class="text-danger">
                                                <i class="fas fa-arrow-down"></i> -5%
                                            </span>
                                        </td>
                                        <td>Late Aman, Early Vegetables</td>
                                        <td>
                                            <span class="text-success">
                                                <i class="fas fa-check"></i> Favorable
                                            </span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>Late Autumn</td>
                                        <td>32,000 MT</td>
                                        <td>
                                            <span class="text-success">
                                                <i class="fas fa-arrow-up"></i> +10%
                                            </span>
                                        </td>
                                        <td>Boro Rice, Potato</td>
                                        <td>
                                            <span class="text-warning">
                                                <i class="fas fa-smog"></i> Morning Fog
                                            </span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>Winter</td>
                                        <td>30,000 MT</td>
                                        <td>
                                            <span class="text-success">
                                                <i class="fas fa-arrow-up"></i> +8%
                                            </span>
                                        </td>
                                        <td>Wheat, Winter Vegetables</td>
                                        <td>
                                            <span class="text-danger">
                                                <i class="fas fa-temperature-low"></i> Cold Stress
                                            </span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>Spring</td>
                                        <td>22,000 MT</td>
                                        <td>
                                            <span class="text-danger">
                                                <i class="fas fa-arrow-down"></i> -3%
                                            </span>
                                        </td>
                                        <td>Maize, Pulses</td>
                                        <td>
                                            <span class="text-success">
                                                <i class="fas fa-check"></i> Favorable
                                            </span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- Add necessary scripts -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Production Trends Chart
            new Chart(document.getElementById('productionTrendsChart'), {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    datasets: [{
                        label: 'Rice Production (Tons)',
                        data: [12000, 15000, 18000, 16000, 14000, 13000, 15000, 17000, 19000, 20000, 18000, 16000],
                        borderColor: '#28a745',
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // Regional Distribution Chart
            new Chart(document.getElementById('regionalDistributionChart'), {
                type: 'pie',
                data: {
                    labels: ['Dhaka', 'Chittagong', 'Rajshahi', 'Khulna', 'Barisal', 'Sylhet', 'Rangpur', 'Mymensingh'],
                    datasets: [{
                        data: [25, 18, 22, 15, 12, 13.5, 12, 10],
                        backgroundColor: ['#28a745', '#17a2b8', '#ffc107', '#dc3545', '#6c757d', '#20c997', '#e83e8c', '#6610f2']
                    }]
                }
            });

            // Yield Comparison Chart
            new Chart(document.getElementById('yieldComparisonChart'), {
                type: 'bar',
                data: {
                    labels: ['Boro Rice', 'Aman Rice', 'Aus Rice', 'Wheat', 'Maize', 'Potato'],
                    datasets: [
                        {
                            label: '2023 Yield (Tons/Hectare)',
                            data: [4.5, 3.8, 2.9, 3.2, 8.5, 22.0],
                            backgroundColor: '#28a745'
                        },
                        {
                            label: '2024 Yield (Tons/Hectare)',
                            data: [4.8, 4.0, 3.1, 3.5, 9.0, 23.5],
                            backgroundColor: '#17a2b8'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Yield (Tons/Hectare)'
                            }
                        }
                    }
                }
            });

            // Price Fluctuation Chart
            new Chart(document.getElementById('priceFluctuationChart'), {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    datasets: [
                        {
                            label: 'Rice (৳/kg)',
                            data: [45, 48, 50, 47, 45, 42, 40, 42, 45, 48, 50, 52],
                            borderColor: '#28a745',
                            fill: false
                        },
                        {
                            label: 'Wheat (৳/kg)',
                            data: [35, 38, 40, 42, 40, 38, 35, 36, 38, 40, 42, 44],
                            borderColor: '#ffc107',
                            fill: false
                        },
                        {
                            label: 'Potato (৳/kg)',
                            data: [25, 22, 20, 18, 15, 18, 20, 22, 25, 28, 30, 28],
                            borderColor: '#dc3545',
                            fill: false
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Price (৳/kg)'
                            }
                        }
                    }
                }
            });

            // Seasonal Analysis Charts
            new Chart(document.getElementById('seasonalCropChart'), {
                type: 'radar',
                data: {
                    labels: ['Summer', 'Rainy', 'Autumn', 'Late Autumn', 'Winter', 'Spring'],
                    datasets: [{
                        label: 'Crop Diversity Index',
                        data: [8, 7, 6, 9, 8, 5],
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgb(54, 162, 235)',
                        pointBackgroundColor: 'rgb(54, 162, 235)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgb(54, 162, 235)'
                    }]
                },
                options: {
                    scales: {
                        r: {
                            beginAtZero: true,
                            max: 10
                        }
                    }
                }
            });

            // Seasonal Production Chart
            new Chart(document.getElementById('seasonalProductionChart'), {
                type: 'bar',
                data: {
                    labels: ['Summer', 'Rainy', 'Autumn', 'Late Autumn', 'Winter', 'Spring'],
                    datasets: [{
                        label: 'Production Volume (MT)',
                        data: [25000, 35000, 28000, 32000, 30000, 22000],
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgb(75, 192, 192)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Production Volume (MT)'
                            }
                        }
                    }
                }
            });
        });
    </script>
    </body>

</html>

</html>