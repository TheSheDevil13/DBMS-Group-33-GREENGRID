-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 28, 2024 at 10:55 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `greengrid`
--

-- --------------------------------------------------------

--
-- Table structure for table `agriculturalanalyst`
--

CREATE TABLE `agriculturalanalyst` (
  `AEmployeeID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `agriculturalanalyst`
--

INSERT INTO `agriculturalanalyst` (`AEmployeeID`) VALUES
(21),
(23),
(25);

-- --------------------------------------------------------

--
-- Table structure for table `agriculturaloffice`
--

CREATE TABLE `agriculturaloffice` (
  `AgriOfficeID` int(11) NOT NULL,
  `AgriOfficeName` varchar(50) NOT NULL,
  `Number` varchar(11) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Street` text NOT NULL,
  `City` text NOT NULL,
  `PostalCode` varchar(6) NOT NULL,
  `LocalGovtID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `agriculturaloffice`
--

INSERT INTO `agriculturaloffice` (`AgriOfficeID`, `AgriOfficeName`, `Number`, `Email`, `Street`, `City`, `PostalCode`, `LocalGovtID`) VALUES
(12, 'Bangladesh Agricultural Research Institute', '01700000001', 'bari@bangladesh.gov.bd', 'Farmgate, Dhaka', 'Dhaka', '1000', 1),
(13, 'Department of Agriculture', '01700000002', 'doa@bangladesh.gov.bd', 'Agricultural Zone, Mymensingh', 'Mymensingh', '2200', 2),
(14, 'Palli Karma-Sahayak Foundation', '01700000003', 'pksp@bangladesh.gov.bd', 'Agricultural Office Road, Chittagong', 'Chittagong', '4000', 3),
(15, 'Bangladesh Rural Development Board', '01700000004', 'brdb@bangladesh.gov.bd', 'Rajshahi Agro Center, Rajshahi', 'Rajshahi', '6000', 4),
(16, 'Agricultural Marketing Directorate', '01700000005', 'amd@bangladesh.gov.bd', 'Agro Road, Khulna', 'Khulna', '9000', 5),
(44, 'Bangladesh Agriculture Research Center', '01700000006', 'barc@bangladesh.gov.bd', 'Farmgate, Dhaka', 'Dhaka', '1205', 1),
(45, 'Department of Crop Science', '01700000007', 'crop@bangladesh.gov.bd', 'Khamarbari, Dhaka', 'Dhaka', '1216', 1),
(46, 'Farmers Development Agency', '01700000008', 'fda@bangladesh.gov.bd', 'Shyamoli, Dhaka', 'Dhaka', '1207', 1);

-- --------------------------------------------------------

--
-- Table structure for table `AgriculturalOfficer`
--

CREATE TABLE `AgriculturalOfficer` (
  `OEmployeeID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `AgriculturalOfficer`
--

INSERT INTO `AgriculturalOfficer` (`OEmployeeID`) VALUES
(22),
(24);

-- --------------------------------------------------------

--
-- Table structure for table `Demand`
--

CREATE TABLE `Demand` (
  `ShopID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL,
  `RequestedQuantity` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Demand`
--

INSERT INTO `Demand` (`ShopID`, `ProductID`, `RequestedQuantity`) VALUES
(1, 5, 150.00),
(2, 1, 200.00),
(3, 4, 250.00),
(4, 3, 300.00),
(5, 2, 350.00);

-- --------------------------------------------------------

--
-- Table structure for table `Dispatch`
--

CREATE TABLE `Dispatch` (
  `WarehouseID` int(11) NOT NULL,
  `StockID` int(11) NOT NULL,
  `ShopID` int(11) NOT NULL,
  `DispatchQuantity` decimal(10,2) DEFAULT NULL,
  `DispatchDate` date DEFAULT NULL,
  `DispatchStatus` enum('Pending','In Transit','Delivered','Cancelled','Ready for Pickup') DEFAULT NULL,
  `DeliveryStatus` enum('Pending','In Transit','Delivered') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Dispatch`
--

INSERT INTO `Dispatch` (`WarehouseID`, `StockID`, `ShopID`, `DispatchQuantity`, `DispatchDate`, `DispatchStatus`, `DeliveryStatus`) VALUES
(6, 1, 1, 150.00, '2024-11-29', 'Delivered', 'Delivered'),
(7, 2, 2, 200.00, '2024-11-28', 'Pending', 'In Transit'),
(8, 5, 3, 300.00, '2024-11-26', 'Ready for Pickup', 'Pending'),
(9, 3, 4, 250.00, '2024-11-27', 'Delivered', 'Delivered'),
(10, 4, 5, 100.00, '2024-11-30', 'In Transit', 'Pending');

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `EmployeeID` int(11) NOT NULL,
  `EmployeeName` varchar(50) NOT NULL,
  `Number` varchar(11) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `AgriOfficeID` int(11) DEFAULT NULL,
  `Street` text DEFAULT NULL,
  `City` text DEFAULT NULL,
  `PostalCode` varchar(6) DEFAULT NULL,
  `EmployeeType` enum('O','A','W') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`EmployeeID`, `EmployeeName`, `Number`, `Email`, `AgriOfficeID`, `Street`, `City`, `PostalCode`, `EmployeeType`) VALUES
(21, 'Mohammad Shakil', '01711223344', 'shakil@bangladesh.gov.bd', 12, 'Farmgate, Dhaka', 'Dhaka', '1000', 'O'),
(22, 'Sultana Begum', '01722334455', 'sultana@bangladesh.gov.bd', 13, 'Agricultural Zone, Mymensingh', 'Mymensingh', '2200', 'A'),
(23, 'Rafiqul Islam', '01733445566', 'rafiqul@bangladesh.gov.bd', 14, 'Agricultural Office Road, Chittagong', 'Chittagong', '4000', 'W'),
(24, 'Sajeda Khatun', '01744556677', 'sajeda@bangladesh.gov.bd', 15, 'Rajshahi Agro Center, Rajshahi', 'Rajshahi', '6000', 'A'),
(25, 'Tariq Anwar', '01755667788', 'tariq@bangladesh.gov.bd', 16, 'Agro Road, Khulna', 'Khulna', '9000', 'W'),
(41, 'Rahim Uddin', '01766778899', 'rahim@bangladesh.gov.bd', 44, 'Farmgate, Dhaka', 'Dhaka', '1205', 'O'),
(42, 'Hasina Parvin', '01777889900', 'hasina@bangladesh.gov.bd', 45, 'Khamarbari, Dhaka', 'Dhaka', '1216', 'A'),
(43, 'Mohammad Ali', '01788990011', 'mohammadali@bangladesh.gov.bd', 46, 'Shyamoli, Dhaka', 'Dhaka', '1207', 'W');

-- --------------------------------------------------------

--
-- Table structure for table `farmer`
--

CREATE TABLE `farmer` (
  `FarmerID` int(11) NOT NULL,
  `FarmerName` varchar(50) NOT NULL,
  `Number` varchar(11) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Street` text DEFAULT NULL,
  `City` text DEFAULT NULL,
  `PostalCode` varchar(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `farmer`
--

INSERT INTO `farmer` (`FarmerID`, `FarmerName`, `Number`, `Email`, `Street`, `City`, `PostalCode`) VALUES
(1, 'Abdul Karim', '01711223345', 'karim@farmer.com', 'Dhanmondi, Dhaka', 'Dhaka', '1209'),
(2, 'Fatema Akter', '01722334456', 'fatema@farmer.com', 'Madhupur, Tangail', 'Tangail', '1900'),
(3, 'Hasan Ali', '01733445567', 'hasan@farmer.com', 'Narsingdi, Dhaka', 'Narsingdi', '1600'),
(4, 'Shamim Hossain', '01744556678', 'shamim@farmer.com', 'Feni, Chittagong', 'Feni', '3900'),
(5, 'Salma Begum', '01755667789', 'salma@farmer.com', 'Chandpur, Chittagong', 'Chandpur', '4200');

-- --------------------------------------------------------

--
-- Table structure for table `farmer_deliver`
--

CREATE TABLE `farmer_deliver` (
  `FarmerID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL,
  `WarehouseID` int(11) NOT NULL,
  `ProductQuantity` decimal(10,2) NOT NULL,
  `PricePerUnit` decimal(10,2) NOT NULL,
  `DeliveryStatus` enum('Pending','In Transit','Delivered') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `farmer_deliver`
--

INSERT INTO `farmer_deliver` (`FarmerID`, `ProductID`, `WarehouseID`, `ProductQuantity`, `PricePerUnit`, `DeliveryStatus`) VALUES
(1, 5, 10, 50.00, 120.00, 'Delivered'),
(2, 4, 8, 75.00, 130.00, 'In Transit'),
(3, 3, 7, 100.00, 125.00, 'Pending'),
(4, 2, 6, 150.00, 110.00, 'In Transit'),
(5, 1, 9, 200.00, 115.00, 'Delivered');

-- --------------------------------------------------------

--
-- Table structure for table `farmer_subsidery`
--

CREATE TABLE `farmer_subsidery` (
  `FarmerID` int(11) NOT NULL,
  `OEmployeeID` int(11) NOT NULL,
  `SubsideryQuantity` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `farmer_subsidery`
--

INSERT INTO `farmer_subsidery` (`FarmerID`, `OEmployeeID`, `SubsideryQuantity`) VALUES
(1, 22, '500 kg'),
(2, 24, '1000 kg'),
(3, 22, '1500 kg'),
(4, 24, '2000 kg'),
(5, 22, '2500 kg');

-- --------------------------------------------------------

--
-- Table structure for table `farmer_subsidery_type`
--

CREATE TABLE `farmer_subsidery_type` (
  `FarmerID` int(11) NOT NULL,
  `OEmployeeID` int(11) NOT NULL,
  `SubsideryType` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `farmer_subsidery_type`
--

INSERT INTO `farmer_subsidery_type` (`FarmerID`, `OEmployeeID`, `SubsideryType`) VALUES
(1, 22, 'Seed Subsidy'),
(2, 24, 'Fertilizer Subsidy'),
(3, 22, 'Pesticide Subsidy'),
(4, 24, 'Equipment Subsidy'),
(5, 22, 'Seed Subsidy');

-- --------------------------------------------------------

--
-- Table structure for table `localgovernment`
--

CREATE TABLE `localgovernment` (
  `LocalGovtID` int(11) NOT NULL,
  `LocalGovtName` varchar(50) NOT NULL,
  `Number` varchar(11) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Street` text DEFAULT NULL,
  `City` text DEFAULT NULL,
  `PostalCode` varchar(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `localgovernment`
--

INSERT INTO `localgovernment` (`LocalGovtID`, `LocalGovtName`, `Number`, `Email`, `Street`, `City`, `PostalCode`) VALUES
(1, 'Dhaka City Corporation', '01721234567', 'dhakacc@bangladesh.gov.bd', 'Purana Paltan, Dhaka', 'Dhaka', '1000'),
(2, 'Mymensingh City Corporation', '01731234567', 'mymensinghcc@bangladesh.gov.bd', 'Mymensingh Sadar, Mymensingh', 'Mymensingh', '2200'),
(3, 'Chittagong City Corporation', '01741234567', 'ctgcc@bangladesh.gov.bd', 'Karnaphuli, Chittagong', 'Chittagong', '4000'),
(4, 'Rajshahi City Corporation', '01751234567', 'rajshahicc@bangladesh.gov.bd', 'Rajshahi Sadar, Rajshahi', 'Rajshahi', '6000'),
(5, 'Khulna City Corporation', '01761234567', 'khulnacc@bangladesh.gov.bd', 'Khulna Sadar, Khulna', 'Khulna', '9000');

-- --------------------------------------------------------

--
-- Table structure for table `order`
--

CREATE TABLE `order` (
  `OrderID` int(11) NOT NULL,
  `OrderDate` date NOT NULL,
  `OrderStatus` enum('Pending','Processing','Shipped','Delivered','Cancelled','Returned') NOT NULL,
  `ShopID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order`
--

INSERT INTO `order` (`OrderID`, `OrderDate`, `OrderStatus`, `ShopID`) VALUES
(1, '2024-11-01', 'Pending', 1),
(2, '2024-11-02', 'Processing', 2),
(3, '2024-11-03', 'Shipped', 3),
(4, '2024-11-04', 'Delivered', 4),
(5, '2024-11-05', 'Cancelled', 5);

-- --------------------------------------------------------

--
-- Table structure for table `order_details`
--

CREATE TABLE `order_details` (
  `OrderID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL,
  `OrderQuantity` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_details`
--

INSERT INTO `order_details` (`OrderID`, `ProductID`, `OrderQuantity`) VALUES
(1, 5, 100.00),
(2, 4, 150.00),
(3, 3, 200.00),
(4, 2, 50.00),
(5, 1, 75.00);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `ProductID` int(11) NOT NULL,
  `OEmployeeID` int(11) NOT NULL,
  `ProductName` varchar(100) NOT NULL,
  `Category` varchar(100) NOT NULL,
  `PricePerUnit` decimal(10,2) NOT NULL,
  `Seasonality` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`ProductID`, `OEmployeeID`, `ProductName`, `Category`, `PricePerUnit`, `Seasonality`) VALUES
(1, 22, 'BRRI Dhan 28', 'Rice', 40.00, 'Boro'),
(2, 24, 'Fertilizer Package A', 'Fertilizer', 350.00, 'Year-Round'),
(3, 22, 'Hybrid Maize', 'Grain', 45.00, 'Kharif'),
(4, 24, 'Mixed Seeds Package', 'Seeds', 200.00, 'Seasonal'),
(5, 22, 'Chili Powder', 'Spices', 300.00, 'Rabi');

-- --------------------------------------------------------

--
-- Table structure for table `productiondata`
--

CREATE TABLE `productiondata` (
  `ProductionID` int(11) NOT NULL,
  `HarvestDate` date NOT NULL,
  `ProductionCost` decimal(10,2) NOT NULL,
  `ShelfLife` varchar(50) DEFAULT NULL,
  `Acreage` decimal(10,2) DEFAULT NULL,
  `YieldRate` decimal(10,2) DEFAULT NULL,
  `AEmployeeID` int(11) NOT NULL,
  `FarmerID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `productiondata`
--

INSERT INTO `productiondata` (`ProductionID`, `HarvestDate`, `ProductionCost`, `ShelfLife`, `Acreage`, `YieldRate`, `AEmployeeID`, `FarmerID`, `ProductID`) VALUES
(1, '2024-04-15', 15000.00, '6 months', 2.50, 8.00, 21, 1, 1),
(2, '2024-04-20', 18000.00, '3 months', 3.00, 7.50, 21, 2, 2),
(3, '2024-05-10', 12000.00, '4 months', 4.00, 6.00, 23, 3, 3),
(4, '2024-06-01', 10000.00, '5 months', 1.50, 9.00, 23, 4, 4),
(5, '2024-07-15', 5000.00, '2 months', 1.00, 10.00, 25, 5, 5);

-- --------------------------------------------------------

--
-- Table structure for table `retailshop`
--

CREATE TABLE `retailshop` (
  `ShopID` int(11) NOT NULL,
  `ShopName` varchar(50) NOT NULL,
  `Number` varchar(11) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Street` text DEFAULT NULL,
  `City` text DEFAULT NULL,
  `PostalCode` varchar(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `retailshop`
--

INSERT INTO `retailshop` (`ShopID`, `ShopName`, `Number`, `Email`, `Street`, `City`, `PostalCode`) VALUES
(1, 'Shwapno', '01800123456', 'shwapno@example.com', 'Road 17, Sector 4', 'Dhaka', '1207'),
(2, 'Unimart', '01800987654', 'unimart@example.com', 'House 12, Street 5', 'Chittagong', '4203'),
(3, 'Meena Bazar', '01800223344', 'meena@example.com', 'Block A, Shyamoli', 'Rajshahi', '6201'),
(4, 'Gulshan Market', '01800334455', 'gulshan@example.com', 'House 5, Road 3', 'Dhaka', '1212'),
(5, 'Agora', '01800445566', 'agora@example.com', 'Plot 3, Main Road', 'Sylhet', '3100');

-- --------------------------------------------------------

--
-- Table structure for table `Stock`
--

CREATE TABLE `Stock` (
  `StockID` int(11) NOT NULL,
  `StockQuantity` decimal(10,2) DEFAULT NULL,
  `LastUpdateDate` date DEFAULT NULL,
  `StockAvailability` enum('In Stock','Out of Stock') DEFAULT NULL,
  `WarehouseID` int(11) DEFAULT NULL,
  `ProductID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Stock`
--

INSERT INTO `Stock` (`StockID`, `StockQuantity`, `LastUpdateDate`, `StockAvailability`, `WarehouseID`, `ProductID`) VALUES
(1, 2000.00, '2024-11-05', 'In Stock', 6, 1),
(2, 1500.00, '2024-11-04', 'In Stock', 7, 2),
(3, 1800.00, '2024-11-03', 'Out of Stock', 8, 3),
(4, 1200.00, '2024-11-02', 'In Stock', 10, 4),
(5, 1600.00, '2024-11-01', 'In Stock', 9, 5);

-- --------------------------------------------------------

--
-- Table structure for table `warehouse`
--

CREATE TABLE `warehouse` (
  `WarehouseID` int(11) NOT NULL,
  `Street` text NOT NULL,
  `City` text NOT NULL,
  `PostalCode` varchar(6) NOT NULL,
  `Temperature` decimal(5,2) NOT NULL,
  `Humidity` decimal(5,2) NOT NULL,
  `LightExposure` decimal(6,2) NOT NULL,
  `WEmployeeID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `warehouse`
--

INSERT INTO `warehouse` (`WarehouseID`, `Street`, `City`, `PostalCode`, `Temperature`, `Humidity`, `LightExposure`, `WEmployeeID`) VALUES
(6, 'Gulshan, Dhaka', 'Dhaka', '1207', 25.00, 60.00, 300.00, 41),
(7, 'Chittagong Port', 'Chittagong', '4203', 27.00, 70.00, 250.00, 42),
(8, 'Rajshahi Warehouse', 'Rajshahi', '6201', 22.00, 65.00, 200.00, 41),
(9, 'Sylhet Warehouse', 'Sylhet', '3100', 23.00, 62.00, 220.00, 43),
(10, 'Barisal Depot', 'Barisal', '8200', 24.00, 68.00, 230.00, 42);

-- --------------------------------------------------------

--
-- Table structure for table `warehousemanager`
--

CREATE TABLE `warehousemanager` (
  `WEmployeeID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `warehousemanager`
--

INSERT INTO `warehousemanager` (`WEmployeeID`) VALUES
(41),
(42),
(43);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `agriculturalanalyst`
--
ALTER TABLE `agriculturalanalyst`
  ADD PRIMARY KEY (`AEmployeeID`);

--
-- Indexes for table `agriculturaloffice`
--
ALTER TABLE `agriculturaloffice`
  ADD PRIMARY KEY (`AgriOfficeID`),
  ADD UNIQUE KEY `number` (`Number`),
  ADD UNIQUE KEY `email` (`Email`),
  ADD KEY `FK_AgriOffice_LocalGov` (`LocalGovtID`);

--
-- Indexes for table `AgriculturalOfficer`
--
ALTER TABLE `AgriculturalOfficer`
  ADD PRIMARY KEY (`OEmployeeID`);

--
-- Indexes for table `Demand`
--
ALTER TABLE `Demand`
  ADD PRIMARY KEY (`ShopID`,`ProductID`),
  ADD KEY `demand_ibfk_2` (`ProductID`);

--
-- Indexes for table `Dispatch`
--
ALTER TABLE `Dispatch`
  ADD PRIMARY KEY (`WarehouseID`,`StockID`,`ShopID`),
  ADD KEY `dispatch_ibfk_2` (`StockID`),
  ADD KEY `dispatch_ibfk_3` (`ShopID`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`EmployeeID`),
  ADD UNIQUE KEY `Number` (`Number`),
  ADD UNIQUE KEY `Email` (`Email`),
  ADD KEY `FK_Employee_Government` (`AgriOfficeID`);

--
-- Indexes for table `farmer`
--
ALTER TABLE `farmer`
  ADD PRIMARY KEY (`FarmerID`),
  ADD UNIQUE KEY `Number` (`Number`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Indexes for table `farmer_deliver`
--
ALTER TABLE `farmer_deliver`
  ADD PRIMARY KEY (`FarmerID`,`ProductID`,`WarehouseID`),
  ADD KEY `ProductID` (`ProductID`),
  ADD KEY `WarehouseID` (`WarehouseID`);

--
-- Indexes for table `farmer_subsidery`
--
ALTER TABLE `farmer_subsidery`
  ADD PRIMARY KEY (`FarmerID`,`OEmployeeID`),
  ADD KEY `FK2_farmer_subsidery` (`OEmployeeID`);

--
-- Indexes for table `farmer_subsidery_type`
--
ALTER TABLE `farmer_subsidery_type`
  ADD PRIMARY KEY (`FarmerID`,`OEmployeeID`,`SubsideryType`);

--
-- Indexes for table `localgovernment`
--
ALTER TABLE `localgovernment`
  ADD PRIMARY KEY (`LocalGovtID`),
  ADD UNIQUE KEY `Number` (`Number`),
  ADD UNIQUE KEY `Email` (`Email`),
  ADD UNIQUE KEY `unique_Number` (`Number`),
  ADD UNIQUE KEY `unique_Email` (`Email`);

--
-- Indexes for table `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`OrderID`),
  ADD KEY `ShopID` (`ShopID`);

--
-- Indexes for table `order_details`
--
ALTER TABLE `order_details`
  ADD PRIMARY KEY (`OrderID`,`ProductID`),
  ADD KEY `ProductID` (`ProductID`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`ProductID`),
  ADD KEY `FK_Product_AgriOfficer` (`OEmployeeID`);

--
-- Indexes for table `productiondata`
--
ALTER TABLE `productiondata`
  ADD PRIMARY KEY (`ProductionID`),
  ADD KEY `AEmployeeID` (`AEmployeeID`),
  ADD KEY `FarmerID` (`FarmerID`),
  ADD KEY `ProductID` (`ProductID`);

--
-- Indexes for table `retailshop`
--
ALTER TABLE `retailshop`
  ADD PRIMARY KEY (`ShopID`),
  ADD UNIQUE KEY `Number` (`Number`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Indexes for table `Stock`
--
ALTER TABLE `Stock`
  ADD PRIMARY KEY (`StockID`),
  ADD KEY `stock_ibfk_1` (`WarehouseID`),
  ADD KEY `stock_ibfk_2` (`ProductID`);

--
-- Indexes for table `warehouse`
--
ALTER TABLE `warehouse`
  ADD PRIMARY KEY (`WarehouseID`),
  ADD KEY `WEmployeeID` (`WEmployeeID`);

--
-- Indexes for table `warehousemanager`
--
ALTER TABLE `warehousemanager`
  ADD PRIMARY KEY (`WEmployeeID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `agriculturaloffice`
--
ALTER TABLE `agriculturaloffice`
  MODIFY `AgriOfficeID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `EmployeeID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `farmer`
--
ALTER TABLE `farmer`
  MODIFY `FarmerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `localgovernment`
--
ALTER TABLE `localgovernment`
  MODIFY `LocalGovtID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `order`
--
ALTER TABLE `order`
  MODIFY `OrderID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `ProductID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `productiondata`
--
ALTER TABLE `productiondata`
  MODIFY `ProductionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `retailshop`
--
ALTER TABLE `retailshop`
  MODIFY `ShopID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `Stock`
--
ALTER TABLE `Stock`
  MODIFY `StockID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `warehouse`
--
ALTER TABLE `warehouse`
  MODIFY `WarehouseID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `agriculturalanalyst`
--
ALTER TABLE `agriculturalanalyst`
  ADD CONSTRAINT `FK_AgriculturalAnalyst_Employee` FOREIGN KEY (`AEmployeeID`) REFERENCES `employee` (`EmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `agriculturaloffice`
--
ALTER TABLE `agriculturaloffice`
  ADD CONSTRAINT `FK_AgriOffice_LocalGov` FOREIGN KEY (`LocalGovtID`) REFERENCES `localgovernment` (`LocalGovtID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `AgriculturalOfficer`
--
ALTER TABLE `AgriculturalOfficer`
  ADD CONSTRAINT `FK_OEmployeeID_Employee` FOREIGN KEY (`OEmployeeID`) REFERENCES `Employee` (`EmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Demand`
--
ALTER TABLE `Demand`
  ADD CONSTRAINT `demand_ibfk_1` FOREIGN KEY (`ShopID`) REFERENCES `RetailShop` (`ShopID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `demand_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `Product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Dispatch`
--
ALTER TABLE `Dispatch`
  ADD CONSTRAINT `dispatch_ibfk_1` FOREIGN KEY (`WarehouseID`) REFERENCES `Warehouse` (`WarehouseID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `dispatch_ibfk_2` FOREIGN KEY (`StockID`) REFERENCES `Stock` (`StockID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `dispatch_ibfk_3` FOREIGN KEY (`ShopID`) REFERENCES `RetailShop` (`ShopID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `employee`
--
ALTER TABLE `employee`
  ADD CONSTRAINT `FK_Employee_AgriOffice` FOREIGN KEY (`AgriOfficeID`) REFERENCES `agriculturaloffice` (`AgriOfficeID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `farmer_deliver`
--
ALTER TABLE `farmer_deliver`
  ADD CONSTRAINT `farmer_deliver_ibfk_1` FOREIGN KEY (`FarmerID`) REFERENCES `farmer` (`FarmerID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `farmer_deliver_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `farmer_deliver_ibfk_3` FOREIGN KEY (`WarehouseID`) REFERENCES `warehouse` (`WarehouseID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `farmer_subsidery`
--
ALTER TABLE `farmer_subsidery`
  ADD CONSTRAINT `FK1_farmer_subsidery` FOREIGN KEY (`FarmerID`) REFERENCES `farmer` (`FarmerID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK2_farmer_subsidery` FOREIGN KEY (`OEmployeeID`) REFERENCES `agriculturalofficer` (`OEmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `farmer_subsidery_type`
--
ALTER TABLE `farmer_subsidery_type`
  ADD CONSTRAINT `farmer_subsidery_type_ibfk_1` FOREIGN KEY (`FarmerID`,`OEmployeeID`) REFERENCES `farmer_subsidery` (`FarmerID`, `OEmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `order`
--
ALTER TABLE `order`
  ADD CONSTRAINT `order_ibfk_1` FOREIGN KEY (`ShopID`) REFERENCES `retailshop` (`ShopID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `order_details`
--
ALTER TABLE `order_details`
  ADD CONSTRAINT `order_details_ibfk_1` FOREIGN KEY (`OrderID`) REFERENCES `order` (`OrderID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `order_details_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `product`
--
ALTER TABLE `product`
  ADD CONSTRAINT `FK_Product_AgriOfficer` FOREIGN KEY (`OEmployeeID`) REFERENCES `AgriculturalOfficer` (`OEmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `productiondata`
--
ALTER TABLE `productiondata`
  ADD CONSTRAINT `productiondata_ibfk_1` FOREIGN KEY (`AEmployeeID`) REFERENCES `agriculturalanalyst` (`AEmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `productiondata_ibfk_2` FOREIGN KEY (`FarmerID`) REFERENCES `farmer` (`FarmerID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `productiondata_ibfk_3` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Stock`
--
ALTER TABLE `Stock`
  ADD CONSTRAINT `stock_ibfk_1` FOREIGN KEY (`WarehouseID`) REFERENCES `Warehouse` (`WarehouseID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `stock_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `Product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `warehouse`
--
ALTER TABLE `warehouse`
  ADD CONSTRAINT `warehouse_ibfk_1` FOREIGN KEY (`WEmployeeID`) REFERENCES `warehousemanager` (`WEmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `warehousemanager`
--
ALTER TABLE `warehousemanager`
  ADD CONSTRAINT `FK_WarehouseManager_Employee` FOREIGN KEY (`WEmployeeID`) REFERENCES `employee` (`EmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
